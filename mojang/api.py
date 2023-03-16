import ast
import base64
import logging
import json
from typing import Any, List, Dict, Optional

from mojang._types import UserProfile
from mojang._http_client import _HTTPClient
from mojang.errors import MojangError


_log = logging.getLogger(__name__)


_API_BASE_URL = "https://api.mojang.com"
_SESSIONSERVER_BASE_URL = "https://sessionserver.mojang.com"
_AUTHSERVER_BASE_URL = "https://authserver.mojang.com"


class API(_HTTPClient):
    def get_uuid(
        self,
        username: str,
        timestamp: Optional[int] = None,
    ) -> Optional[str]:
        """Convert a Minecraft name to a UUID.

        Warning: Limited Functionality
            As of November 2020, Mojang stopped supporting the timestamp parameter, which allowed
            users to get UUID of the name at the timestamp provided. If a timestamp is provided,
            it is silently ignored and the current UUID is returned. Please remind them to fix this here:
            [WEB-3367](https://bugs.mojang.com/browse/WEB-3367).

        Args:
            username:  The Minecraft username to be converted.
            timestamp (optional): Get the username's UUID at a specified UNIX timestamp.
                You can also get the username's first UUID by passing `0` to this parameter.
                However, this only works if the name was changed at least once, or if the account is legacy.

        Returns:
            The UUID (`str`) or `None` if the username does not exist.
        """
        if timestamp:
            url = f"{_API_BASE_URL}/users/profiles/minecraft/{username}?at={timestamp}"
        else:
            url = f"{_API_BASE_URL}/users/profiles/minecraft/{username}"

        resp = self.request("get", url, ignore_codes=[400])

        try:
            return resp.json()["id"]
        except (KeyError, json.decoder.JSONDecodeError):
            return None

    def get_uuids(self, names: List[str]) -> Dict[str, str]:
        """Convert up to 10 usernames to UUIDs in a single network request.

        Args:
            names: The Minecraft username(s) to be converted.
                If more than 10 are included, only the first 10 will be parsed.

        Returns:
            A dictionary object that contains the converted usernames. Names are also case-corrected.
            If a username does not exist, it will not be included in the returned dictionary.
        """
        if not isinstance(names, list):
            raise TypeError(
                "Invalid data type passed. Make sure that you are passing a list of UUIDs instead of a string or dictionary."
            )

        if len(names) > 10:
            names = names[:10]

        resp = self.request(
            "post",
            f"{_API_BASE_URL}/profiles/minecraft",
            ignore_codes=[400],
            json=names,
        )

        data = resp.json()

        if not isinstance(data, list):
            raise MojangError(response=resp)

        return {name_data["name"]: name_data["id"] for name_data in data}

    def get_username(self, uuid: str) -> Optional[str]:
        """Convert a UUID to a username.

        Args:
            uuid: The Minecraft UUID to be converted to a username.

        Returns:
            The username. `None` otherwise.
        """
        resp = self.request(
            "get",
            f"{_SESSIONSERVER_BASE_URL}/session/minecraft/profile/{uuid}",
            ignore_codes=[400],
        )

        if resp.status_code == 400:
            return None

        try:
            return resp.json()["name"]
        except json.decoder.JSONDecodeError:
            return None

    def get_profile(self, uuid: str) -> Optional[UserProfile]:
        """Get more information about a user from their UUID

        Args:
            uuid: The Minecraft UUID

        Returns:
            `UserProfile` object. Otherwise, `None` if the profile does not exist.
        """
        resp = self.request(
            "get",
            f"{_SESSIONSERVER_BASE_URL}/session/minecraft/profile/{uuid}",
            ignore_codes=[400],
        )

        try:
            value = resp.json()["properties"][0]["value"]
        except (KeyError, json.decoder.JSONDecodeError):
            return None
        data = ast.literal_eval(base64.b64decode(value).decode())

        cape_url = None
        skin_url = None
        skin_variant = "classic"

        textures = data["textures"]
        if textures.get("CAPE"):
            cape_url = textures["CAPE"]["url"]

        if textures.get("SKIN"):
            skin_url = textures["SKIN"]["url"]

            if textures["SKIN"].get("metadata"):
                skin_variant = "slim"

        return UserProfile(
            id=data["profileId"],
            timestamp=data["timestamp"],
            name=data["profileName"],
            is_legacy_profile=bool(data.get("legacy")),
            cape_url=cape_url,
            skin_url=skin_url,
            skin_variant=skin_variant,
        )

    def get_blocked_servers(self) -> List[str]:
        """Get a list of SHA1 hashes of blacklisted Minecraft servers that do not follow EULA.
        These servers have to abide by the EULA or they will be shut down forever. The hashes are not cracked.

        Returns:
            Blacklisted server hashes
        """
        resp = self.request("get", f"{_SESSIONSERVER_BASE_URL}/blockedservers")
        return resp.text.splitlines()

    def refresh_access_token(
        self, access_token: str, client_token: str
    ) -> Dict[str, Any]:
        """Refreshes access token

        Args:
            access_token: The access token to refresh.
            client_token: The client token that was used to obtain the access token.

        Returns:
            A dictionary object that contains the new access token and other account and profile information
        """
        payload = {
            "accessToken": access_token,
            "clientToken": client_token,
            "requestUser": True,
        }

        account = {}
        data = self.request(
            "post", f"{_AUTHSERVER_BASE_URL}/refresh", json=payload
        ).json()

        account["username"] = data["user"]["username"]
        account["uuid"] = data["user"]["id"]
        account["access_token"] = data["accessToken"]
        account["client_token"] = data["clientToken"]
        if data.get("selectedProfile"):
            account["profile_id"] = data["selectedProfile"]["id"]
            account["profile_name"] = data["selectedProfile"]["name"]
        else:
            account["profile_id"] = None
            account["profile_name"] = None
        return account
