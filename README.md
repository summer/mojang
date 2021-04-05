#
[![PyPI version](https://badge.fury.io/py/mojang.svg)](https://badge.fury.io/py/mojang)![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)

<center><a href="https://mojang.readthedocs.io"><img  src="https://readthedocs.org/projects/mojang/badge/?version=latest"  alt="Read the Docs"></a><a href="https://github.com/summer/mojang/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License"></a><a href="https://pypistats.org/packages/mojang"><img src="https://img.shields.io/pypi/dm/mojang.svg" alt="Downloads"></a><h4><a  href="https://mojang.readthedocs.io/en/latest/">Documentation</a></h4>
</center>
  

```Mojang``` is a Python package for accessing Mojang's services. It serves as a simple wrapper around Mojang's [API](https://wiki.vg/Mojang_API).

  

It can be used to get name drop dates, convert UUIDs, and much more.


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
