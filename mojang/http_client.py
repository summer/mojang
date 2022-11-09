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

import time
from typing import Any, List, Optional
import logging

import requests

from http.client import HTTPConnection


from .errors import (
    MojangError,
    BadRequest,
    Forbidden,
    NotFound,
    TooManyRequests,
    ServerError,
    Unauthorized,
)

log = logging.getLogger(__name__)


class HTTPClient:
    def __init__(
        self,
        session: Optional[requests.Session] = None,
        retry_on_rate_limit: Optional[bool] = False,
        ratelimit_sleep_time: Optional[int] = 60,
        debug_mode: Optional[bool] = False,
    ):
        self.ratelimit_sleep_time = ratelimit_sleep_time
        self.retry_on_rate_limit = retry_on_rate_limit

        if session:
            self.session = session
        else:
            self.session = requests.Session()

            self.session.headers.update(
                {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    "(KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
                }
            )

        if debug_mode:
            HTTPConnection.debuglevel = 1
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

    def request(
        self,
        method: str,
        url: str,
        ignore_codes: Optional[List[int]] = None,
        **kwargs: Any,
    ) -> Any:
        """Internal request handler"""

        resp = self.session.request(method, url, **kwargs)

        log.debug(f"Making API request: {method} {url}\n")

        if resp.ok:
            return resp

        if ignore_codes:
            if resp.status_code in ignore_codes:
                return resp

        if resp.status_code == 400:
            raise BadRequest

        if resp.status_code == 401:
            raise Unauthorized

        if resp.status_code == 403:
            raise Forbidden

        if resp.status_code == 404:
            raise NotFound

        if resp.status_code == 429:
            if self.retry_on_rate_limit:
                log.warning(
                    f"We are being ratelimited. Sleeping for {self.ratelimit_sleep_time} seconds."
                )
                time.sleep(self.ratelimit_sleep_time)
                return self.request(method, url, ignore_codes, **kwargs)
            else:
                raise TooManyRequests

        if resp.status_code >= 500:
            raise ServerError

        raise MojangError(response=resp)
