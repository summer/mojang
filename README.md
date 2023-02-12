#
[![PyPI version](https://badge.fury.io/py/mojang.svg)](https://badge.fury.io/py/mojang)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mojang?style=flat-square)

[![Read the Docs](https://img.shields.io/readthedocs/mojang?style=flat-square)](https://mojang.readthedocs.io/en/latest/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/summer/mojang/blob/master/LICENSE/)
[![PyPI - Monthly Downloads](https://img.shields.io/pypi/dm/mojang?style=flat-square)](https://pypistats.org/packages/mojang)

[**Documentation**](https://mojang.readthedocs.io/en/latest/)

```Mojang``` is a Python package for accessing Mojang's services. This library can be used to convert UUIDs, get a profile's information, change your Minecraft username or skin, and much more. 

There are 2 components to this package, which are imported in different ways:

- **Public API** - Used to parse information about Minecraft profiles and more. Authentication is not required.
- **Client API** - Used to login to a Mojang account and access it.

At the moment, the Client API only supports authenticating to a Minecraft account via Microsoft's authentication scheme, so your Minecraft account must already be migrated. Alternatively, you may authenticate to a Mojang account directly with a Bearer token.


## Installation
**Python 3.7 or higher is required.**

The easiest way to install the library is using `pip`. Just run the following console command:

```
python -m pip install mojang
```


## **Public API Quickstart**

```py
from mojang import API

# Create a Public API instance
api = API()

uuid = api.get_uuid("Notch")

if not uuid:
    print("Notch is not a taken username.")
else:
    print(f"Notch's UUID is {uuid}")

    profile = api.get_profile(uuid)
    print(f"Notch's skin URL is {profile.skin_url}")
    print(f"Notch's skin variant is {profile.skin_variant}")
    print(f"Notch's cape URL is {profile.cape_url}")
```

- [Full Public API documentation](https://mojang.readthedocs.io/en/latest/api/)


## **Client API Quickstart**
To log into a Mojang account, the account must already be migrated to Microsoft. 
This means that you will be using your Microsoft credentials to login.

```py
from mojang import Client

client = Client("YOUR_MICROSOFT_EMAIL", "YOUR_PASSWORD")

# Get the account's profile information
profile = client.get_profile()

print(profile.id)
print(profile.name)

for skin in profile.skins:
    print(skin.id)
    print(skin.enabled)
    print(skin.url)
    print(skin.variant)
```

Alternatively, supply a Bearer token and skip the Microsoft authentication process.
```py
client = Client(bearer_token="MOJANG_BEARER_TOKEN_HERE")
```
If authentication fails, such as due to an incorrect email or password, a `LoginFailure` exception will occur.

- [Full Client API documentation](https://mojang.readthedocs.io/en/latest/client/)
