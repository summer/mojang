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
from typing import Optional


class MojangError(Exception):
    """Base error class for all library-related exceptions in this file
    Essentially, this could be caught to handle any exceptions thrown from this library.
    """
    def __init__(self, message: Optional[str] = None):
        self.message = message if message else self.__class__.__doc__
        super().__init__(self.message)


class AuthenticationError(MojangError):
    """Occurs when the session has died and requires logging in again.
    A session can die from spamming too many requests in a short period of time.
    """


class LoginError(MojangError):
    """Incorrect username or password. This Exception can also occur when you are being ratelimited
    and/or logging in too frequently. If you are certain the credentials are correct, try again in 10 minutes.
    """


class ProxyError(MojangError):
    """Occurs due to a dead or invalid proxy"""


class SecurityAnswerError(MojangError):
    """A security question was answered incorrectly"""


class SecurityChallengesRequired(MojangError):
    """Must complete security challenges to unlock access to function"""


class ForbiddenNameChange(MojangError):
    """Name change is not allowed. Name was already changed once in the past 30 days. 
    Wait until 30 days pass before attempting to change your name again.
    """


class Ratelimited(MojangError):
    """Occurs when client is being ratelimited"""


class ServerOverloaded(MojangError):
    """Occurs when Mojang server is being overloaded and cannot process the request"""
