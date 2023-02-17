## **Setting up the Client**
### **Logging in with a Microsoft email and password**
```py
from mojang import Client

client = Client("YOUR_MICROSOFT_EMAIL", "YOUR_PASSWORD")
```

Always make sure that you are using your Microsoft credentials to login. The Mojang account must already be migrated to Microsoft, as the `Mojang` package does not support migration features.

If your login credentials are incorrect, a `LoginFailure` exception will occur.


### **Logging in with a Bearer token**

```py
from mojang import Client

client = Client(bearer_token="BEARER_TOKEN_HERE")
```

Logging in with a Bearer token is faster and more efficient, as the entire Microsoft authentication flow is skipped and the session headers are set directly. If you're logging in a lot, it would be good practice to save the Bearer token for future use after logging in once with your Microsoft credentials.

The Bearer token can always be obtained by accessing the `bearer_token` attribute after logging in:
```py
# login normally using your Microsoft account first
client = Client("YOUR_MICROSOFT_EMAIL", "YOUR_PASSWORD")

# print / save the bearer token
print(client.bearer_token)
```


### **Using a custom `requests` session**


```py
import requests
from mojang import Client

session = requests.Session()

# Simply pass the session to Client when logging in
client = Client("YOUR_MICROSOFT_EMAIL", "YOUR_PASSWORD", session=session)

# Access the session, which is now already authenticated to Mojang
resp = client.session.get("https://api.minecraftservices.com/minecraft/profile")

print(resp.json())

# Alternatively, use the client's custom request handler
# This way, ratelimiting and errors are handled for you
client.request("get", "https://api.minecraftservices.com/minecraft/profile")
```

By using a custom `requests` session, you can optionally use proxies, custom headers, and more, while the authentication process and everything else is taken care of for you.

Keep in mind, you can also pass a custom session object to Mojang's Public API, so much of the same applies.

```py
import requests
from mojang import API

session = requests.Session()

api = API(session=session)

api.get_username("Notch")
```


### **Enabling rate limit handling**

By default, the API will throw a `TooManyRequests` exception whenever it is being rate limited. To enable rate limit handling, just set `retry_on_ratelimit` to `True` when creating a new Client instance or API instance. The library will then sleep for a specified amount of time before attempting the request again. 

**Client instance:**
```py
client = Client("YOUR_MICROSOFT_EMAIL", "YOUR_PASSWORD", 
                retry_on_ratelimit=True,
                ratelimit_sleep_time=60)

```

**API instance:**
```py
api = API(retry_on_ratelimit=True, ratelimit_sleep_duration=60)
```


### **Enabling debug mode**
Setting `debug_mode` to `True` will set the logging level to `DEBUG` and all library and network requests will be printed to the console. 
```py
client = Client("YOUR_MICROSOFT_EMAIL", "YOUR_PASSWORD", 
                debug_mode=True)
```
```py
api = API(debug_mode=True)
```

## **Once authenticated...**

### **Accessing your Minecraft profile's information**
```py
profile = client.get_profile()

print(f"Profile ID: {profile.id} | Profile Name: {profile.name}")

print(f"This profile has {len(profile.capes)} capes")

# Print the profile's skins
for skin in profile.skins:
    print(skin.id)
    print(skin.enabled)
    print(skin.url)
    print(skin.variant)

# Print the profile's capes
for cape in profile.capes:
    print(cape.id)
    print(cape.enabled)
    print(cape.url)
    print(cape.alias)
```

### **Accessing the profile's name change information and creation date**
```py
name_info = client.get_name_change_info()

delta = datetime.today() - name_info.created_at.replace(tzinfo=None)

print(f"This account was created {delta.days} days ago.")
print(f"The name was last changed on {name_info.changed_at}")

if name_info.name_change_allowed:
    print("A name change is allowed")

```


### **Changing your Minecraft username**

Before changing your Minecraft username, you should always make sure that your account has an available name change, as shown in the above example. You can only change your username once every 30 days.

You should also make sure that the username you want is available:

```py
username = "Notch"

if client.is_username_available(username):
    client.change_username(username)
else:
    print(f"{username} is not free")
```

If you're checking usernames in bulk, you may get ratelimited pretty quickly using the `client.is_username_available()` method. In these scenarios, it may be best to use the Public API instead, which has a limit of 600 requests every 10 minutes.

```py
from mojang import API

api = API(retry_on_ratelimit=True, ratelimit_sleep_time=600)

usernames = ["Notch", "Bob", "Alice"]

for username in usernames:
    if api.get_username(username):
        print(f"{username} is taken.")
    else:
        print(f"{username} is not taken.")
```


### **Changing your Minecraft skin or skin variant**
```py
# Change your skin via URL
skin_url = "http://textures.minecraft.net/texture/2ff6d970b1b6243fe5a44c5ac540c320506987a5c55ba99a90f758b00d3e05a1"
client.change_skin(variant="slim", url=skin_url)

# Change your skin via file path / image name
client.change_skin(variant="classic", image_path="skin.png")

# Or just copy another player's skin
client.copy_skin("Notch")

# Keep your current skin, but change the variant to slim
client.change_skin_variant("slim")
```
