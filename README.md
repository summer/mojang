**NOTE:** As of December 2020, parts of the API might be obsolete now; e.g., logging into accounts, and some other functions might be broken as well. So use at your own risk. I've taken a break from programming to solely focus on school instead, so if nothing more, you can still use this project as a type of blueprint and incorporate parts of its source code into your own projects.

#
[![PyPI version](https://badge.fury.io/py/mojang.svg)](https://badge.fury.io/py/mojang)![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)

<center><a href="https://mojang.readthedocs.io"><img  src="https://readthedocs.org/projects/mojang/badge/?version=latest"  alt="Read the Docs"></a><a href="https://github.com/summer/mojang/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License"></a><a href="https://pypistats.org/packages/mojang"><img src="https://img.shields.io/pypi/dm/mojang.svg" alt="Downloads"></a><h4><a  href="https://mojang.readthedocs.io/en/latest/">Documentation</a></h4>
</center>
  

```Mojang``` is a Python package for accessing Mojang's services. It serves as a wrapper around Mojang's [API](https://wiki.vg/Mojang_API), [authentication API](https://wiki.vg/Authentication), and some parts of the [Minecraft.net](https://www.minecraft.net/) website.

  

It can be used to get name drop dates, convert UUIDs, change a Minecraft profile's skin, code name snipers, and much more.


## Installation
**Python 3.6 or higher is required.**

To install the library, you can just run the following console command:
```
python -m pip install mojang
```



## MojangAPI Quickstart

```py
import time
from mojang import MojangAPI

uuid = MojangAPI.get_uuid("Notch")

if not uuid:
    print("Notch does not exist.")
else:
    print("Notch's UUID is", uuid)
    profile = MojangAPI.get_profile(uuid)
    print("Notch's skin URL is", profile.skin_url)
 
servers = MojangAPI.get_blocked_servers()
print(f"There are {len(servers)} blocked servers on Minecraft.")

drop_timestamp = MojangAPI.get_drop_timestamp("Notch")

if not drop_timestamp:
    print("Notch is not dropping")
else:
    seconds = drop_timestamp - time.time()
    print(f"Notch drops in {seconds} seconds")
```

For a complete list of functions, see the [MojangAPI reference](https://mojang.readthedocs.io/en/latest/reference/#mojangapi).

## MojangUser Quickstart
To log into a Mojang account,  you can import ```MojangUser```  and create a user object.

```py
from mojang import MojangUser

user = MojangUser("YOUR_LOGIN_USERNAME", "YOUR_PASSWORD")

# example attributes include
print(user.id) # account's user ID
print(user.dob) # account's date of birth
print(user.email)

# access current session information
print(user.session.access_token)
print(user.session.client_token)
```
### Completing security challenges
If the account has security questions and you're logging in from a new IP address, you **must** answer them to complete authentication and unlock access to all of Mojang's services. Otherwise, you will not be able to modify account data or access the Minecraft profile.

```py
from mojang import MojangUser
from mojang.exceptions import SecurityAnswerError

user = MojangUser("YOUR_USERNAME", "YOUR_PASSWORD")

if not user.is_fully_authenticated: 
    # print the security challenges if you need them
    print(user.security_challenges)
    
    # make a list of the 3 answers to send
    # make sure they are in the same order as the challenges
    # they are not case-sensitive
    answers = ["oreos", "blue", "phoenix"]
	
    # completes authentication
    # throws SecurityAnswerError if a question is incorrect
    try:
        user.answer_security_challenges(answers)
    except SecurityAnswerError:
        print("A security answer was answered incorrectly.")

```

If security challenges do **not** have to be answered, ```is_fully_authenticated``` will be set to ```True``` after logging in.

### Logging in with a proxy

Simply pass a HTTPS proxy when creating a user object, and all of the session's requests will be routed through it:
```py
user = MojangUser("YOUR_USERNAME", "YOUR_PASSWORD", proxy="8.8.8.8")
```
**NOTE:** For proxies that require authentication (i.e., have a username and password), make sure they're in the following format: ```username:password@proxy:port```


**Example:**
```py
from mojang import MojangUser

proxy = "proxy_username:proxy_password@8.8.8.8.8:443"

user = MojangUser("YOUR_USERNAME", "YOUR_PASSWORD", proxy=proxy)
```




### Interacting with the account's Minecraft profile

Access the Minecraft profile through the ```profile``` object.


```py
print(user.profile.id)
print(user.profile.name)

if not user.profile.is_name_change_allowed:
    print("Account does not have an available name change")
    print(f"It was last changed on {user.profile.name_changed_at}")

# also
user.profile.created_at
user.profile.is_migrated
user.profile.is_suspended
user.profile.has_legacy_profile
# and many more!
```

### Skins
```py
# check if the profile has a skin first
if user.profile.skin:
    # some skin attributes include
    user.profile.skin.url
    user.profile.skin.texture_id
    user.profile.skin.model

# upload a skin from an image file and set it to slim or classic
file_path = "C:\\Users\\Summer\\Desktop\\skin.png"
user.profile.skin_upload("slim", file_path)

# delete the profile's skin and set the default one
user.profile.skin_reset()

# or even copy another player's skin!
uuid = MojangAPI.get_uuid("Notch")
user.profile.skin_copy(uuid) # now your account will have Notch's skin

# get a dictionary object of all the skin's information
print(user.profile.skin.to_dict())
```
### Capes

```py
if user.profile.capes:
    print(f"Found {len(user.profile.capes} capes on the profile")

# access them by index
user.profile.capes[0].name
user.profile.capes[0].type
user.profile.capes[0].url

# or just loop through
for cape in user.profile.capes:
    print(cape.name)
    print(cape.url)
    print(cape.version)
```


### Changing profile name
```py
if not user.profile.change_name("Notch")
    print("Failed to change name to Notch")
```


