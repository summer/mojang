"""
The MIT License (MIT)

Copyright (c) 2021 https://github.com/summer

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


class MojangObject:
    def to_dict(self) -> dict:
        """Returns a dictionary of all instance attributes"""
        return self.__dict__.copy()

    def __repr__(self):
        return "%s(%s)" % (
            self.__class__.__name__,
            self.__dict__
        )


class UserProfile(MojangObject):
    def __init__(self, data: dict):
        self.timestamp = data["timestamp"]
        self.id = data["profileId"]
        self.name = data["profileName"]

        self.is_legacy_profile = data.get("legacy")
        if self.is_legacy_profile is None:
            self.is_legacy_profile = False

        self.cape_url = None
        self.skin_url = None
        self.skin_model = "classic"

        if data["textures"].get("CAPE"):
            self.cape_url = data["textures"]["CAPE"]["url"]

        if data["textures"].get("SKIN"):
            self.skin_url = data["textures"]["SKIN"]["url"]
            if data["textures"]["SKIN"].get("metadata"):
                self.skin_model = "slim"
