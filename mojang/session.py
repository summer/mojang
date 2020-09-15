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

import logging
from typing import Optional, Any

import requests
from requests.adapters import HTTPAdapter

from .exceptions import MojangError, AuthenticationError, ProxyError, Ratelimited, ServerOverloaded, LoginError


log = logging.getLogger(__name__)


class MojangSession:
    def __init__(self,
                 username: str,
                 password: str,
                 proxy: Optional[str] = None,
                 user_agent: Optional[str] = None,
                 maximum_pool_size: Optional[int] = None):

        log.debug("Initializing Mojang Session object...")

        self.username = username
        self.password = password    
        self.proxy = proxy
        self.user_agent = user_agent
        self.maximum_pool_size = maximum_pool_size

        self.access_token = None
        self.client_token = None
        self.profile_name = None
        self.profile_id = None
        self._user_id = None

        self._session = requests.Session()

        if user_agent:
            self._session.headers.update({"User-Agent": user_agent}) 

        if proxy:
            self._session.proxies.update({"https": f"https://{proxy}", "http": f"http://{proxy}"})
            self._validate_proxy()

        if maximum_pool_size:
            adapter = HTTPAdapter(pool_connections=maximum_pool_size, pool_maxsize=maximum_pool_size)  
            self._session.mount("https://", adapter)

        self._do_authenticate()

    def _validate_proxy(self) -> None:
        """Makes sure proxy works by fetching Mojang API

        Raises:
            ProxyError: if proxy is dead or in an invalid format
        """
        log.debug("Checking if proxy is valid...")
        try:
            self._session.get("https://api.mojang.com/", timeout=10)
        except requests.exceptions.ProxyError:
            raise ProxyError

    def _request(self, method: str, url: str, **kwargs) -> Any:
        """Internal request handler

        Returns:
            `requests.Response` object

        Raises:
            AuthenticationError: if HTTP code 401
            Ratelimited: if HTTP code 429
            ServerOverloaded: if HTTP code 529
        """
        resp = self._session.request(method, url, **kwargs)

        if resp.ok:
            return resp

        code = resp.status_code

        if code == 401:
            raise AuthenticationError
        elif code == 429:
            raise Ratelimited
        elif code == 529:
            raise ServerOverloaded

        return resp

    def _do_authenticate(self) -> None:
        payload = {
            "agent": {
                "name": "Minecraft",
                "version": 1
            },
            "username": self.username,
            "password": self.password,
            "requestUser": True
        }
        data = self._request("post", "https://authserver.mojang.com/authenticate", json=payload).json()

        if data.get("errorMessage"):
            message = data["errorMessage"]
            if message == "Invalid credentials.":
                raise Ratelimited
            elif "use email as username in message":
                raise LoginError(message)
            elif "Invalid username or password." in message:
                raise LoginError
            else:
                raise MojangError(data)

        self.access_token = data["accessToken"]
        self.client_token = data["clientToken"]
        self._user_id = data["user"]["id"]
        if data["availableProfiles"]:
            self.profile_name = data["availableProfiles"][0]["name"]
            self.profile_id = data["availableProfiles"][0]["id"]
        self._session.headers.update({"Authorization": "Bearer " + self.access_token})

    def refresh(self) -> None:
        """Refresh the session's access token to increase the session's lifespan
        Call this every 12 hours when you want the account to stay logged in
        """
        payload = {
            "accessToken": self.access_token,
            "clientToken": self.client_token
        }
        data = self._request("post", "https://authserver.mojang.com/refresh", json=payload).json()
        self.access_token = data['accessToken']
        self.client_token = data['clientToken']

    def to_dict(self) -> dict:
        """Returns a dictionary of all Session attributes"""
        session_dict = self.__dict__.copy()
        del session_dict["_session"]
        return session_dict
