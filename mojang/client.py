import ast
import base64
import logging
from typing import Any, Dict, List, Optional, Tuple
import re

import requests

from mojang._http_client import _HTTPClient
from mojang._types import Profile, Skin, Cape, NameInformation
from mojang.errors import (
    MojangError,
    BadRequest,
    LoginFailure,
    MissingMinecraftLicense,
    MissingMinecraftProfile,
)

from mojang._utils import _assert_valid_username


_log = logging.getLogger(__name__)


_BASE_API_URL = "https://api.minecraftservices.com"


class MojangAuth(_HTTPClient):
    # Potential Xbox Live login failure errors
    _XERRORS = {
        2148916233: "The account doesn't have an Xbox account.",
        2148916235: "The account is from a country where Xbox Live is not available/banned.",
        2148916236: "The account needs adult verification on Xbox page. (South Korea)",
        2148916237: "The account needs adult verification on Xbox page. (South Korea)",
        2148916238: "The account is a child (under 18) and cannot proceed unless the account is added to a Family by an adult.",
    }

    def __init__(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        bearer_token: Optional[str] = None,
        session: Optional[requests.Session] = None,
        retry_on_ratelimit: Optional[bool] = False,
        ratelimit_sleep_time: Optional[int] = 60,
        debug_mode: Optional[bool] = False,
    ):
        super().__init__(session, retry_on_ratelimit, ratelimit_sleep_time, debug_mode)

        self.email = email
        self.password = password
        self.bearer_token = bearer_token

        if bearer_token:
            self._set_authorization_header(bearer_token)
        elif email is None and password is None:
            raise TypeError(
                "Either an email/password or bearer token must be supplied."
            )
        else:
            self._login()

        self._validate_session()

    def _set_authorization_header(self, bearer_token: str) -> None:
        if not bearer_token.startswith("Bearer"):
            _log.debug("Appended Bearer string onto the token as it was missing")
            bearer_token = f"Bearer {bearer_token}"

        _log.debug(f"Setting authorization header to {bearer_token}")
        self.session.headers.update({"Authorization": f"{bearer_token}"})

    def _has_minecraft_profile(self) -> bool:
        # This check still needs to be verified
        resp = self.request("get", f"{_BASE_API_URL}/minecraft/profile")
        return bool(resp.ok)

    def _validate_session(self) -> None:
        resp = self.request(
            "get", f"{_BASE_API_URL}/entitlements/mcstore", ignore_codes=[401]
        )

        # The response content is empty if the authorization token isn't set or valid
        if not resp.text:
            raise LoginFailure("The bearer token is invalid.")

        if resp.status_code == 401:
            raise MissingMinecraftLicense

        data = resp.json()

        if not bool(data["items"]):
            raise MissingMinecraftLicense

        if not self._has_minecraft_profile():
            raise MissingMinecraftProfile

    def _get_oauth2_token_and_url(self) -> Tuple[str, str]:
        """Begins the Microsoft OAuth2 Flow"""
        params = {
            "client_id": "000000004C12AE6F",
            "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
            "scope": "service::user.auth.xboxlive.com::MBI_SSL",
            "display": "touch",
            "response_type": "token",
            "locale": "en",
        }

        resp = self.request(
            "get", "https://login.live.com/oauth20_authorize.srf", params=params
        )

        # Parses the values via regex since the HTML can't be parsed
        value = re.search(r'value="(.+?)"', resp.text)[0].replace('value="', "")[:-1]
        url = re.search(r"urlPost:'(.+?)'", resp.text)[0].replace("urlPost:'", "")[:-1]

        return value, url

    def _authenticate_with_microsoft(self, token: str, url: str) -> Tuple[str, str]:
        """Authenticates with Microsoft"""
        payload = {
            "login": self.email,
            "loginfmt": self.email,
            "passwd": self.password,
            "PPFT": token,
        }

        resp = self.request("post", url, data=payload)
        if "access_token" not in resp.url:
            raise LoginFailure

        raw_login_data = resp.url.split("#")[1]
        data = dict(item.split("=") for item in raw_login_data.split("&"))

        access_token = requests.utils.unquote(data["access_token"])
        refresh_token = requests.utils.unquote(data["refresh_token"])

        return access_token, refresh_token

    def _authenticate_with_xboxlive(self, access_token: str) -> Tuple[str, str]:
        """Authenticates with XBL"""
        json_data = {
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": access_token,
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
        }

        resp = self.request(
            "post", "https://user.auth.xboxlive.com/user/authenticate", json=json_data
        )

        xbl_token = resp.json()["Token"]
        user_hash = resp.json()["DisplayClaims"]["xui"][0]["uhs"]

        return xbl_token, user_hash

    def _get_xsts_token(self, xbl_token: str) -> str:
        """Gets the XSTS token which is required to authenticate with Minecraft services"""
        json_data = {
            "Properties": {"SandboxId": "RETAIL", "UserTokens": [xbl_token]},
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT",
        }

        resp = self.request(
            "post",
            "https://xsts.auth.xboxlive.com/xsts/authorize",
            ignore_codes=[401],
            json=json_data,
        )

        if resp.status_code == 401:
            data = resp.json()
            if data.get("XErr"):
                if data["XErr"] in self._XERRORS:
                    raise LoginFailure(data["XErr"])
            raise MojangError(response=resp)

        return resp.json()["Token"]

    def _authenticate_with_minecraft(self, user_hash, xsts_token):
        json_payload = {
            "identityToken": f"XBL3.0 x={user_hash};{xsts_token}",
            "ensureLegacyEnabled": True,
        }

        resp = self.request(
            "post",
            f"{_BASE_API_URL}/authentication/login_with_xbox",
            json=json_payload,
        )

        return resp.json()

    def _login(self):
        token, url = self._get_oauth2_token_and_url()
        access_token, refresh_token = self._authenticate_with_microsoft(token, url)
        xbl_token, user_hash = self._authenticate_with_xboxlive(access_token)
        xsts_token = self._get_xsts_token(xbl_token)
        data = self._authenticate_with_minecraft(user_hash, xsts_token)

        self.bearer_token = data["access_token"]

        self._set_authorization_header(self.bearer_token)


class Client(MojangAuth):
    def get_profile(self) -> Profile:
        """Get information about the current profile.

        Returns:
            A `Profile` object that contains information about a Minecraft profile
        """
        data = self.request("get", f"{_BASE_API_URL}/minecraft/profile").json()

        capes = []
        skins = []

        if data.get("capes"):
            for cape_data in data["capes"]:
                cape = Cape(
                    id=cape_data["id"],
                    enabled=(cape_data["state"] == "ACTIVE"),
                    url=cape_data["url"],
                    alias=cape_data["alias"],
                )
                capes.append(cape)

        if data.get("skins"):
            for skin_data in data["skins"]:
                skin = Skin(
                    id=skin_data["id"],
                    enabled=(skin_data["state"] == "ACTIVE"),
                    url=skin_data["url"],
                    variant=skin_data["variant"],
                    alias=skin_data.get("alias"),
                )
                skins.append(skin)

        return Profile(
            id=data["id"],
            name=data["name"],
            capes=capes,
            skins=skins,
        )

    def get_name_change_info(self) -> Dict[str, Any]:
        """Check if the account's username can be changed.

        Returns:
            A dictionary object that contains information about the account's username. \
                Possible keys are `changed_at`, `created_at`, \
                and `name_change_allowed`.
        """
        data = self.request(
            "get", f"{_BASE_API_URL}/minecraft/profile/namechange"
        ).json()

        return NameInformation(
            changed_at=data.get("changedAt"),
            created_at=data.get("createdAt"),
            name_change_allowed=data.get("nameChangeAllowed"),
        )

    def get_billing_info(self) -> List[Dict[str, Any]]:
        """Get general billing info and credit card information stored on the account."""
        return self.request("get", f"{_BASE_API_URL}/creditcards").json()

    def _get_username_status(self, username: str):
        """Check a username's status

        Args:
            username: The Minecraft username to check.

        Note:
            Possible return values include AVAILABLE, TAKEN, DUPLICATE, and NOT_ALLOWED
            TAKEN - For every 1 and 2-character username, any username with invalid characters,
            or any name with more than 16 characters.
            DUPLICATE - The username is taken or pseudo-hard-deleted.
        """

        _assert_valid_username(username)

        resp = self.request(
            "get", f"{_BASE_API_URL}/minecraft/profile/name/{username}/available"
        )

        return resp.json()["status"]

    def is_username_available(self, username: str) -> bool:
        """Check if a username is available.

        Warning: Limitations
            A username must be between 3 and 16 characters and cannot contain invalid characters.
            If any of these constraints are broken, or if a username has already been taken by someone else,
            this function will return `False`.

        Args:
            username: The Minecraft username to check.

        Returns:
            `True` if the username is available; `False` if the username is invalid or already taken
        """
        return self._get_username_status(username) == "AVAILABLE"

    def is_username_blocked(self, username: str) -> bool:
        """
        Check if a username is blocked by Mojang's username filter.

        Note:
            This function allows for the checking of usernames that have potentially been blocked.
            Blocking can happen either one of two ways - a username sniper has blocked the name for 24 hours on
            an empty Mojang account, or the username has been blocked by Mojang's inappropriate name filter for
            whatever reason. The reasons names are blocked aren't public, but this endpoint is the best way to
            check if a name is blocked.

        Args:
            username: The Minecraft username to check.

        Returns:
            `True` if the username is blocked; `False` if the username is not blocked
        """
        return self._get_username_status(username) == "NOT_ALLOWED"

    def change_username(self, username: str) -> Dict[str, Any]:
        """Change the profile's Minecraft username.

        Warning: Limitations
            You can only change your username once every 30 days. A username must be
            between 3 and 16 characters and cannot contain invalid characters.

        Args:
            username:  The username you want to change to.

        Returns:
            A dictionary object that contains information about whether the username was claimed. \
                Possible keys are `success` (which contains `True` or `False`) and `error` with an error message \
                (only if the function fails).
        """
        _assert_valid_username(username)

        resp = self.request(
            "put",
            f"{_BASE_API_URL}/minecraft/profile/name/{username}",
            ignore_codes=[400, 403],
        )

        if resp.ok:
            return dict(success=True)

        if resp.status_code == 400:
            try:
                error = resp.json()["errorMessage"].replace(
                    "changeProfileName.profileName:", ""
                )
            except (requests.JSONDecodeError, KeyError) as exc:
                raise BadRequest(response=resp) from exc

            return dict(success=False, error=error)

        if resp.status_code == 403:
            return dict(
                success=False,
                error="Either the current account does not have an available name change, or the name you supplied"
                "has already been taken or is still on cooldown.",
            )

        raise MojangError(response=resp)

    def change_skin(
        self,
        variant: Optional[str] = "classic",
        url: Optional[str] = None,
        image_path: Optional[str] = None,
    ) -> None:
        """Set a new skin for your profile.

        Skin Requirements:
            Image dimensions have to be **64x32**. The max allowed image size is 24576 bytes (24.576 KB). This function
            will raise a `MojangError` if the skin variant, or the provided image path or URL is invalid for some reason.

        Args:
            variant: Set "slim" for the slim model, or "classic" for the default.
            url: A direct image URL to the skin you want to change to.
            image_path: The file name or full file path to the skin image file.

        Raises:
            MojangError: If the skin could not be changed for some reason.
        """
        variant = variant.strip().lower()

        if variant != "slim" and variant != "classic":
            raise ValueError("Skin variant must be set to either slim or classic.")

        if image_path is None and url is None:
            raise TypeError(
                "Missing required parameters. Please supply a skin URL or a skin image path."
            )

        if url:
            json_payload = {"url": url, "variant": variant}
            self.request(
                "post", f"{_BASE_API_URL}/minecraft/profile/skins", json=json_payload
            )
        else:
            files = {
                "file": open(f"{image_path}", "rb"),
                "variant": (None, variant),
            }
            self.request(
                "post", f"{_BASE_API_URL}/minecraft/profile/skins", files=files
            )

    def copy_skin(
        self,
        username: Optional[str] = None,
        uuid: Optional[str] = None,
    ) -> None:
        """Copy another player's Minecraft skin and skin variant. This will set their skin on your account.

        Pass either the player's username or their UUID - not both.

        Args:
            username: The username of the player whose skin you want to copy.
            uuid: The UUID of the player whose skin you want to copy.

        Raises:
            ValueError: If an invalid username or UUID is supplied.
        """
        if username is None and uuid is None:
            raise TypeError("Either a username or a UUID must be supplied")
        if username:
            _assert_valid_username(username)
            resp = self.request(
                "get", f"https://api.mojang.com/users/profiles/minecraft/{username}"
            )
            try:
                uuid = resp.json()["id"]
            except requests.JSONDecodeError as exc:
                raise ValueError("Username does not exist") from exc

        resp = self.request(
            "get",
            f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}",
            ignore_codes=[400],
        )

        try:
            value = resp.json()["properties"][0]["value"]
        except (KeyError, requests.JSONDecodeError) as exc:
            raise MojangError("Invalid UUID supplied") from exc
        data = ast.literal_eval(base64.b64decode(value).decode())

        skin_url = None
        skin_variant = "classic"
        if data["textures"].get("SKIN"):
            skin_url = data["textures"]["SKIN"]["url"]
            if data["textures"]["SKIN"].get("metadata"):
                skin_variant = "slim"

        # If the user doesn't have a skin, also reset the player's skin back to the default
        if skin_url is None:
            self.reset_skin()
        else:
            self.change_skin(
                url=skin_url,
                variant=skin_variant,
            )

    def change_skin_variant(self, variant: str) -> None:
        """Change the skin variant for your current Minecraft skin.

        Args:
            variant: Set "slim" for the slim model, or "classic" for the default.
        """
        profile = self.get_profile()
        self.change_skin(url=profile.skins[0].url, variant=variant)

    def reset_skin(self) -> None:
        """Reset the profile's Minecraft skin to the default one"""
        self.request("delete", f"{_BASE_API_URL}/minecraft/profile/skins/active")

    def disable_cape(self) -> None:
        """Disable the profile's cape so it is no longer shown"""
        self.request("delete", f"{_BASE_API_URL}/minecraft/profile/capes/active")
