from typing import Optional

import requests


class MojangError(Exception):
    """Base error class for all library-related exceptions in this file.
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
