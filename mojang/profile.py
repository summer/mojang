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
import time
from typing import Optional

from .models import Cape, Skin
from .exceptions import ForbiddenNameChange, MojangError


log = logging.getLogger(__name__)


class Profile:
    def __init__(self, session):
        self._session = session

        self.id = None
        self.name = None
        self.skin = None
        self.capes = None

        self.is_paid = None
        self.is_migrated = None
        self.is_suspended = None
        self.is_legacy_profile = None
        self.is_name_change_allowed = None

        self.created_at = None
        self.name_changed_at = None

        self.update_cache()

    def _update_name_data(self) -> None:
        data = self._session._request("get", f"https://api.mojang.com/user/profile/{self.id}/name").json()
        self.name_changed_at = data["changedAt"]
        self.is_name_change_allowed = data["nameChangeAllowed"]

    def _update_profile_data(self) -> None:
        data = self._session._request("get", "https://api.mojang.com/user/profiles/agent/minecraft").json()[0]
        self.name = data["name"]
        self.id = data["id"]
        self.created_at = data["createdAt"]
        self.is_legacy_profile = data["legacyProfile"]
        self.is_suspended = data["suspended"]
        self.is_migrated = data["migrated"]
        self.is_paid = data["paid"]

    def _update_capes(self) -> None:
        capes = self._session._request("get", f"https://api.mojang.com/user/profile/{self.id}/cape").json()
        self.capes = [Cape(cape) for cape in capes] if capes else None

    def _update_skin(self) -> None:
        skins = self._session._request("get", f"https://api.mojang.com/user/profile/{self.id}/skins").json()
        self.skin = Skin(skins[0]) if skins else None

    def update_cache(self) -> None:
        """Updates the profile data.
        Call this method if you want the profile's latest information.
        """
        self._update_profile_data()  # refresh profile data first to populate profile ID
        self._update_name_data()
        self._update_capes()
        self._update_skin()

    def change_name(self, name: str) -> bool:
        """Change the profile's Minecraft username

        Args:
            name: New name to change to

        Returns:
            bool: True if successfully changed. False otherwise.

        Raises:
            ForbiddenNameChange: If the name was already changed once less than 30 days ago.
        """

        payload = {
            "name": name,
            "password": self._session.password
        }

        resp = self._session._request("post", f"https://api.mojang.com/user/profile/{self.id}/name", json=payload)

        if resp.ok:
            time.sleep(2.5)  # give Mojang time to update database before updating cached data
            self._update_profile_data()
            self._update_name_data()

            # double check name was actually claimed
            if self.name.lower() == name.lower() or self.is_name_change_allowed is False:
                return True
            else:
                return False

        message = resp.json()["errorMessage"]
        if "Invalid name change: profileId = " in message:
            return False
        elif "name was set or change less than 30 days ago" in message:
            raise ForbiddenNameChange
        else:
            raise MojangError(f"HTTP {resp.status_code} {resp.text}")

    def skin_reset(self) -> None:
        """Reset the profile's skin back to default"""
        self._session._request("delete", f"https://api.mojang.com/user/profile/{self.id}/skin")
        time.sleep(1.25)  # give Mojang time to update database
        self._update_skin()

    def skin_upload(self, 
                    model: str, 
                    image_file_path: Optional[str] = None, 
                    image_bytes: Optional[bytes] = None) -> None:
        """Uploads a skin to Mojang's servers. It also sets the users skin.

        Args:
            model: "slim" for the slim model. "classic" or empty string for the default.
            image_file_path: image file name and/or file path
            image_bytes (optional): image bytes if raw image content
        """
        
        if not image_bytes:
            with open(image_file_path, "rb") as f:  # type: ignore
                image_bytes = f.read()
    
        resp = self._session._request("put", f"https://api.mojang.com/user/profile/{self.id}/skin", 
                                      files=dict(model=model, file=image_bytes))

        if not resp.ok:
            message = resp.json()["errorMessage"]
            if "Max allowed size is 24576 bytes" in message:
                raise ValueError("Max allowed image size is 24.576 KB")
            elif "Dimensions are not valid" in message:
                raise ValueError("Image dimensions are not valid. Dimensions have to be 64x32 px.")
            elif "Content is not an image" in message:
                raise ValueError("Content is not an image")
            else:
                raise ValueError(message)

        time.sleep(1.25)
        self._update_skin()

    def skin_copy(self, uuid: str) -> None:
        """Copy another player's skin

        Args:
            uuid: UUID of the player whose skin you want to copy
        """
        resp = self._session._request("get", f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
        
        try:
            value = resp.json()["properties"][0]["value"]
        except KeyError:
            raise ValueError("UUID is not valid")

        profile = ast.literal_eval(base64.b64decode(value).decode())
        if profile["textures"].get("SKIN"):
            skin_url = profile["textures"]["SKIN"]["url"]            
            skin_model = "slim" if profile["textures"]["SKIN"].get("metadata") else "classic"
    
            resp = self._session._session.get(skin_url)
            if not resp.ok:
                raise MojangError("Error parsing skin URL")

            self.skin_upload(skin_model, image_bytes=resp.content)
            return

        # reset skin if player has no skin
        self.skin_reset()

    def to_dict(self) -> dict:
        """Returns a dictionary of all Profile attributes"""
        profile_dict = self.__dict__.copy()
        del profile_dict["_session"]
        return profile_dict
