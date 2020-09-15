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

import functools
import time

from .exceptions import SecurityChallengesRequired


INFINITE = 0


class cached_property(object):
    """(C) 2011 Christopher Arndt, MIT License
    Decorator for read-only properties evaluated only once within TTL period.
    It can be used to created a cached property like this::
        import random
        # the class containing the property must be a new-style class
        class MyClass(object):
            # create property whose value is cached for ten minutes
            @cached_property(ttl=600)
            def randint(self):
                # will only be evaluated every 10 min. at maximum.
                return random.randint(0, 100)
    The value is cached  in the '_cache' attribute of the object instance that
    has the property getter method wrapped by this decorator. The '_cache'
    attribute value is a dictionary which has a key for every property of the
    object which is wrapped by this decorator. Each entry in the cache is
    created only when the property is accessed for the first time and is a
    two-element tuple with the last computed property value and the last time
    it was updated in seconds since the epoch.
    The default time-to-live (TTL) is 300 seconds (5 minutes). Set the TTL to
    zero for the cached value to never expire.
    To expire a cached property value manually just do::
        del instance._cache[<property name>]
    """

    def __init__(self, ttl=300):
        self.ttl = ttl

    def __call__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__
        self.__module__ = fget.__module__
        return self

    def __get__(self, inst, owner):
        now = time.time()
        value, last_update = None, None
        if not hasattr(inst, '_cache'):
            inst._cache = {}

        entry = inst._cache.get(self.__name__, None)
        if entry is not None:
            value, last_update = entry
            if now - last_update > self.ttl > 0:
                entry = None

        if entry is None:
            value = self.fget(inst)
            cache = inst._cache
            cache[self.__name__] = (value, now)

        return value


def completed_security_challenges(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.is_fully_authenticated:
            raise SecurityChallengesRequired(SecurityChallengesRequired.__doc__)
        else:
            return func(self, *args, **kwargs)
    return wrapper
