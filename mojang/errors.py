"""
The MIT License (MIT)

Copyright (c) 2020-present https://github.com/summer

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

from typing import Optional

import requests


class MojangError(Exception):
    """Base error class for all library-related exceptions in this file
    Essentially, this could be caught to handle any exceptions thrown from this library.
    """

    def __init__(
        self,
        message: Optional[str] = None,
        response: Optional[requests.Response] = None,
    ):

        if response:

            try:
                data = response.json()
                message = f"[HTTP {response.status_code}] - [{data['errorMessage']}]"
            except (KeyError, requests.JSONDecodeError):
                message = f"[HTTP {response.status_code}] - {response.url}\n\n"
        else:
            if message:
                message = f"{self.__class__.__doc__}\n{message}"
            else:
                message = self.__class__.__doc__

        super().__init__(message)


class BadRequest(MojangError):
    """HTTP 400. The server could not process our request, likely due to an error of ours."""


class Unauthorized(MojangError):
    """HTTP 401. We are not authorized to access the requested resource.
    This can occur due to an invalid or expired Bearer token.
    """


class Forbidden(MojangError):
    """HTTP 403. We do not have permission to access the requested resource."""


class NotFound(MojangError):
    """HTTP 404. This resource does not exist."""


class TooManyRequests(MojangError):
    """HTTP 429. The server is ratelimiting us. Please wait for a bit before trying again."""


class ServerError(MojangError):
    """HTTP 5xx. The server encountered an unexpected condition that prevented it from fulfilling the request."""


class LoginFailure(MojangError):
    """The login process failed for some reason. This can occur due to an incorrect email or password."""


class MissingMinecraftLicense(MojangError):
    """The Microsoft account is valid, but it is missing a Minecraft license."""


class MissingMinecraftProfile(MojangError):
    """The account has a Minecraft license, but it hasn't created a profile yet."""
