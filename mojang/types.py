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

from datetime import datetime
from typing import List, Optional

from pydantic.dataclasses import dataclass


@dataclass
class UserProfile:
    id: str
    timestamp: int
    name: str
    is_legacy_profile: bool
    skin_variant: str
    cape_url: Optional[str] = None
    skin_url: Optional[str] = None


@dataclass
class Skin:
    id: str
    enabled: bool
    url: str
    variant: str
    alias: Optional[str] = None


@dataclass
class Cape:
    id: str
    enabled: bool
    url: str
    alias: str


@dataclass
class Profile:
    id: str
    name: str
    capes: List[Cape]
    skins: List[Skin]


@dataclass
class NameInformation:
    name_change_allowed: bool
    created_at: Optional[datetime] = None
    changed_at: Optional[datetime] = None
