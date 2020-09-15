"""
The MIT License (MIT)

Copyright (c) 2020 https://github.com/summer

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import ast
import base64
import logging
import json
import time
from typing import Union, Optional
import requests

from .models import UserProfile
from .exceptions import MojangError


log = logging.getLogger(__name__)


class MojangAPI:
    
    # NOTE: Names are held for exactly 37 days after being released. 
    # Update this value (by converting days to seconds) if the duration is ever changed.
    _NAME_HOLD_DURATION = 3196800000

    @classmethod
    def get_uuid(cls, username: str, timestamp: Optional[int] = None) -> Union[str, None]:
        """Convert a Minecraft name to a UUID.

        Args:
            username:  The Minecraft username to be converted.
            timestamp (optional): Get the username's UUID at a specified UNIX timestamp. 
                You can also get the username's first UUID by passing 0. 
                However, this only works if the name was changed at least once, or if the account is legacy.

        Returns:
            str: The UUID. Otherwise, None if the username does not exist.
        """

        if timestamp is None:
            timestamp_now = int(time.time() * 1000.0)
            timestamp = int((timestamp_now - cls._NAME_HOLD_DURATION) / 1000)

        resp = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}?at={timestamp}")
        if resp.ok:
            try:
                return resp.json()["id"]
            except json.decoder.JSONDecodeError:
                return None
        return None


    @staticmethod
    def get_uuids(names: list) -> dict:
        """Convert up to 10 usernames to UUIDs in a single network request.
        
        Args:
            names: The Minecraft username(s) to be converted. 
                If more than 10 are included, only the first 10 will be parsed.

        Returns:
            dict: username:uuid pairs of the converted usernames. Names are also case-corrected.
                If a username does not exist, it will not be included in the returned dictionary.
        """
        if len(names) > 10:
            names = names[:10]
        data = requests.post("https://api.mojang.com/profiles/minecraft", json=names).json()

        if not isinstance(data, list):
            if data.get("error"):
                raise ValueError(data["errorMessage"])
            else:
                raise MojangError(data)

        sorted_names = dict()
        for name_data in data:
            sorted_names[name_data["name"]] = name_data["id"]
    
        return sorted_names


    @staticmethod
    def get_username(uuid: str) -> Union[str, None]:
        """Convert a UUID to a username.

        Args:
            uuid: The Minecraft UUID to be converted to a username.

        Returns:
            str: UUID if username exists. None otherwise. 
        """
        resp = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
        if resp.ok:
            return resp.json()["name"]
        return None


    @classmethod
    def get_drop_timestamp(cls, username: str) -> Union[int, None]:
        """Get the timestamp of when a username drops
        
        Args:
            username: Minecraft name to get drop date of

        Returns:
            int: The drop timestamp. Otherwise, None if the username is not being released/dropped.
        """
        uuid = cls.get_uuid(username)
        if not uuid:
            raise ValueError("Username is invalid. Failed to convert username to UUID")
        resp = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names")
        name_changes = [name_change for name_change in reversed(resp.json())]
        for i, name_info in enumerate(name_changes):
            if name_info["name"].lower() == username.lower():
                try:
                    name_changed_timestamp = name_changes[i - 1]["changedToAt"]
                    drop_timestamp = (name_changed_timestamp + cls._NAME_HOLD_DURATION) / 1000
                    return int(drop_timestamp)
                except KeyError:
                    return None


    @staticmethod
    def get_profile(uuid: str) -> Union[UserProfile, None]:
        """Returns a `UserProfile` object

        `UserProfile` Attributes:
            id (str): UUID of the profile
            name (str): Name of the profile
            cape_url (str or None): URL to the profile's cape
            skin_url (str or None): URL to the profile's skin
            skin_model (str): Skin model of the profile
            is_legacy_profile (bool): Check if the profile is legacy
            timestamp (int): Timestamp of when the profile was retrieved
        """
        resp = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")

        try:
            value = resp.json()["properties"][0]["value"]
        except KeyError:
            return None
        user_profile = ast.literal_eval(base64.b64decode(value).decode())
        return UserProfile(user_profile)


    @staticmethod
    def get_name_history(uuid: str) -> list:
        """Get a user's name history

        Args:
            uuid: The user's UUID.

        Returns:
            list: A list of dictionaries, each of which contains a name:changed_to_at pair. 
                If changed_to_at is set to 0, it is because it is the profile's first name.
        """
        name_history = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()

        name_data = list()
        for data in name_history:
            name_data_dict = dict()
            name_data_dict["name"] = data["name"]
            if data.get("changedToAt"):
                name_data_dict["changed_to_at"] = data["changedToAt"]
            else:
                name_data_dict["changed_to_at"] = 0
            name_data.append(name_data_dict)
        return name_data


    @staticmethod
    def get_api_status() -> dict:
        """Get the API / network status of various Mojang services

        Returns:
            dict: Returns dictionary with status of various Mojang services. 
                Possible values are green (no issues), yellow (some issues), red (service unavailable).
        """
        data = requests.get("https://status.mojang.com/check").json()
        servers = dict()
        for server_data in data:
            for k, v in server_data.items():
                servers[k] = v
        return servers


    @staticmethod
    def get_blocked_servers() -> list:
        """Returns a list of SHA1 hashes of current blacklisted servers that do not follow EULA.
        These servers have to abide by the EULA or be shut down forever. The hashes are not cracked.
        """
        return requests.get("https://sessionserver.mojang.com/blockedservers").text.splitlines()


    @staticmethod
    def get_sale_statistics(item_sold_minecraft: bool = True,
                            prepaid_card_redeemed_minecraft: bool = True,
                            item_sold_cobalt: bool = False,
                            item_sold_scrolls: bool = False,
                            prepaid_card_redeemed_cobalt: bool = False,
                            item_sold_dungeons: bool = False
                            ):
        """Get statistics on the sales of Minecraft.
        You will receive a single object corresponding to the sum of sales of the requested type(s)
        At least one type of sale must be set to True.

        Returns:
            dict: the sales metrics. Possible keys include `total`, `last24h` and `sale_velocity_per_seconds`
        """
        options = [k for k, v in locals().items() if v]

        if not options:
            raise MojangError("Invalid parameters supplied. Include at least one metric key.")

        data = requests.post("https://api.mojang.com/orders/statistics", json={"metricKeys": options}).json()
        metrics = dict()
        metrics["total"] = data["total"]
        metrics["last24h"] = data["last24h"]
        metrics["sale_velocity_per_seconds"] = data["saleVelocityPerSeconds"]
        return metrics


    @staticmethod
    def refresh_access_token(access_token: str, client_token: str) -> dict:
        """Refreshes access token

        Args:
            access_token: access token to refresh
            client_token: same client token that was used to obtain the access_token 

        Returns:
            dict: new access token and other account information
        """
        payload = {
            "accessToken": access_token,
            "clientToken": client_token,
            "requestUser": True
        }

        account = dict()
        data = requests.post("https://authserver.mojang.com/refresh", json=payload).json()

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
