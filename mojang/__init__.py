from mojang.api import API
from mojang.client import Client

from mojang.errors import (
    MojangError,
    LoginFailure,
    BadRequest,
    Forbidden,
    NotFound,
    TooManyRequests,
    ServerError,
    Unauthorized,
    MissingMinecraftLicense,
    MissingMinecraftProfile,
)
