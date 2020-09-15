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
import datetime
import logging
import time
from typing import Optional, Union

from .session import MojangSession
from .profile import Profile
from .utils import cached_property, completed_security_challenges, INFINITE
from .exceptions import SecurityAnswerError, MojangError


log = logging.getLogger(__name__)


class MojangUser:
    def __init__(self,
                 username: str,
                 password: str,
                 proxy: Optional[str] = None,
                 user_agent: Optional[str] = None,
                 maximum_pool_size: Optional[int] = None):
        """Log into a Mojang acccount

        Args:
            username: Username used to log into the account
            password: Password of the account.
            proxy: HTTPS proxy all session requests will be routed through.
            user_agent: User agent that will be associated with the session. 
              Defaults to a generic Chrome user agent otherwise.
            maximum_pool_size: Maximum number of concurrent requests you plan to send using this session.

        Raises:
            LoginError: if username or password is incorrect
            Ratelimited: if account or IP address is ratelimited
            ProxyError: if proxy is invalid or dead
        """
        self.session = MojangSession(username=username, password=password, proxy=proxy, 
                                     user_agent=user_agent, maximum_pool_size=maximum_pool_size)

        self.has_minecraft = True if self.session.profile_name else False
        self.id = self.session._user_id

        self._security_challenges = self._get_security_challenges()

        self.email = None
        self.dob = None
        self.is_secured = None
        self.is_legacy_user = None
        self.is_email_verified = None
        self.is_verified_by_parent = None

        self.profile = None

        if self.is_fully_authenticated:
            log.info("Completed authentication. Security challenges are not required.")
            self.session.refresh()
            self._populate_members()
        else:
            log.info("Answering security challenges is required to complete authentication.")

    @property
    def is_fully_authenticated(self) -> bool:
        resp = self.session._request("get", "https://api.mojang.com/user/security/location")
        return True if resp.ok else False

    def _get_security_challenges(self) -> None:
        return self.session._request("get", "https://api.mojang.com/user/security/challenges").json()

    @completed_security_challenges
    def _populate_members(self):
        """Populates account and profile fields and extends session lifetime"""
        self.update_cache()
        if self.has_minecraft:
            self.profile = Profile(self.session)

    @cached_property(ttl=INFINITE)
    def security_challenges(self) -> Union[dict, None]:
        """Get the account's security challenges"""
        if self._security_challenges:
            challenges_formatted = dict()
            for i, challenge in enumerate(self._security_challenges):
                challenges_formatted[i] = challenge["question"]["question"]
            return challenges_formatted
        return None

    def answer_security_challenges(self, answers: list) -> None:
        """Answer security challenges to complete authentication

        Args:
            answers: list of answers in the same order as the questions

        Raises:
            SecurityAnswerError: If a security challenge was answered incorrectly
        """
        answers_formatted = []
        for i, challenge in enumerate(self._security_challenges):  # type: ignore
            answer_id = challenge["answer"]["id"]
            answers_formatted.append({"id": answer_id, "answer": answers[i]})

        resp = self.session._request("post", "https://api.mojang.com/user/security/location", json=answers_formatted)
        if resp.ok:
            self.session.refresh()
            self._populate_members()
        else:
            raise SecurityAnswerError(resp.json()["errorMessage"])

    @completed_security_challenges
    def update_cache(self):
        """Updates the account data. Call this method if you want the account's latest information."""
        data = self.session._request("get", "https://api.mojang.com/user").json()
        self.email = data["email"]
        self.dob = datetime.datetime.fromtimestamp(data["dateOfBirth"] / 1000)
        self.is_secured = data["secured"]
        self.is_legacy_user = data["legacyUser"]
        self.is_email_verified = data["emailVerified"]
        self.is_verified_by_parent = data["verifiedByParent"]

    @completed_security_challenges
    def block_username(self, username: str) -> bool:
        """Block a Minecraft username. Only Mojang accounts that do not own Minecraft should call this function.

        Args:
            username: username to block.

        Returns:
            bool: True if the username was successfully blocked. False otherwise.
        """
        if self.profile:
            raise MojangError("Cannot block a username on an account that owns Minecraft")

        # NOTE: Sometimes, the server returns 204 even when the name was not successfully blocked
        # during big name drops. It seems to be an incorrect response from the server from being overloaded.
        resp = self.session._request("put", f"https://api.mojang.com/user/profile/agent/minecraft/name/{username}")
        return True if resp.ok else False

    @completed_security_challenges
    def redeem_code(self, code: str) -> None:
        """Redeem a digital Minecraft code.

        Args:
            code: Minecraft code to redeem.

        Raises:
            ValueError: If the code could not be redeemed for some reason.
        """
        payload = {
            "code": code,
            "languageCode": "en-us",
            "productType": "GAME"
        }
        response_code = self.session._request("post", "https://api.mojang.com/token/redeem", json=payload).json()["responseCode"]

        response_codes = {
            "SUCCESS": "The digital code has been successfully redeemed",
            "REDEEMED": "The digital code has already been redeemed",
            "INVALID_CODE": "The digital code is invalid and cannot be redeemed",
            "ALREADY_OWN": "Failed to redeem the digital code because the account has a Minecraft license"
        }

        if not response_code == "SUCCESS":
            if response_code not in response_codes:
                raise ValueError(response_code)
            else:
                raise ValueError(response_codes[response_code])
        
        time.sleep(3.5)
        self.profile = Profile(self.session)

    def to_dict(self):
        account_dict = self.__dict__.copy()
        del account_dict["_security_challenges"]
        return account_dict

    def __repr__(self):
        return "%s(username=%s, password=%s, proxy=%s, user_agent=%s, maximum_pool_size=%s)" % (
            self.__class__.__name__,
            repr(self.session.username),
            repr(self.session.password),
            repr(self.session.proxy) if self.session.proxy else None,
            repr(self.session.user_agent) if self.session.user_agent else None,
            repr(self.session.maximum_pool_size) if self.session.maximum_pool_size else None
        )
