#
<h2>Authentication</h2>

<br>

### Logging in
To log into a Mojang account, you can import `MojangUser`  and create a user object.


```py
from mojang import MojangUser

user = MojangUser("YOUR_LOGIN_USERNAME", "YOUR_PASSWORD")
```

<p><b>Raises:</b></p>
- `LoginError` - If the login username or password is incorrect **OR** if you are being ratelimited. Unfortunately,
there is no way to distinguish between both because Mojang returns the same response message.


<br>
### Completing security challenges
<div class="admonition important">
<p class="admonition-title">Important</p>
<p>If the account has security questions and you're logging in from a new IP address, you **must** answer them to complete authentication and unlock access to all of Mojang's services. Otherwise, you will not be able to modify account data or access the Minecraft profile.</p>
</div>

```py
from mojang import MojangUser
from mojang.exceptions import SecurityAnswerError

user = MojangUser("YOUR_USERNAME", "YOUR_PASSWORD")

if user.is_fully_authenticated:
	print("Authenticated, security challenges are not required.")
else:
	# print the security challenges if you need them
    print(user.security_challenges) 
    
    # make a list of the 3 answers to send
    # make sure they are in the same order as the challenges
    # they are not case-sensitive
    answers = ["oreos", "blue", "phoenix"]

	# throws SecurityAnswerError if a question is incorrect
	try:
	    user.answer_security_challenges(answers)
	except SecurityAnswerError:
		print("A security answer was answered incorrectly.")
```


If security challenges do **not** have to be answered, `is_fully_authenticated` will be set to `True` already after logging in.

<br>
### Logging in with a proxy

Simply pass a HTTPS proxy when creating a user object, and all of the session's requests will be routed through it:
```py
user = MojangUser("YOUR_USERNAME", "YOUR_PASSWORD", proxy="8.8.8.8:5000")
```


Proxies that require authentication (i.e., have a username and password) should be in the following format: `username:password@proxy:port`


**Example:**
```py
# do not put https:// in front of the proxy
proxy = "proxy_username:proxy_password@8.8.8.8.8:443"

user = MojangUser("YOUR_USERNAME", "YOUR_PASSWORD", proxy=proxy)
```

<p><b>Raises:</b></p>
- `ProxyError` - If the proxy appears to be dead or in an invalid format.

<br>

### Other login parameters
Give the session a custom user agent:
```py
user = MojangUser("YOUR_USERNAME", "YOUR_PASSWORD", user_agent="Mozilla/5.0")
```

Increase the maximum pool size:
```
user = MojangUser("YOUR_USERNAME", "YOUR_PASSWORD", maximum_pool_size=20)
```
This paramater may be useful if you are coding multi-threaded programs and end up flooding the session's connection pool from too many concurrent requests.

So if you plan to send 25 requests concurrently at the same exact time through one
```MojangUser``` object (such as 25 ```change_name``` requests), set ```maximum_pool_size``` size to 25.
<br><br>
