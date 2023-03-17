import time
from typing import Any, List, Optional
import logging

import requests

from http.client import HTTPConnection


from mojang.errors import (
    MojangError,
    BadRequest,
    Forbidden,
    NotFound,
    TooManyRequests,
    ServerError,
    Unauthorized,
)

_log = logging.getLogger(__name__)


class _HTTPClient:
    def __init__(
        self,
        session: Optional[requests.Session] = None,
        retry_on_ratelimit: Optional[bool] = False,
        ratelimit_sleep_time: Optional[int] = 60,
        debug_mode: Optional[bool] = False,
    ):
        self.ratelimit_sleep_time = ratelimit_sleep_time
        self.retry_on_ratelimit = retry_on_ratelimit

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

        _log.debug(f"Making API request: {method} {url}\n")

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
            if self.retry_on_ratelimit:
                _log.warning(
                    f"We are being ratelimited. Sleeping for {self.ratelimit_sleep_time} seconds."
                )
                time.sleep(self.ratelimit_sleep_time)
                return self.request(method, url, ignore_codes, **kwargs)
            else:
                raise TooManyRequests

        if resp.status_code >= 500:
            raise ServerError

        raise MojangError(response=resp)
