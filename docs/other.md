#
<h2>Other</h2>
<br>
### Error Handling

<p><b>On top of their respective exceptions, all library calls can also raise the following exceptions:</b></p>
- `MojangError` - Base class for all errors. Typically occurs due to an undocumented error. 
Please report the issue on GitHub so that it can be fixed.
<br><br>
- `AuthenticationError` - If the session dies and re-authentication is required. You have to login all over again.
<br><br>
- `Ratelimited` - If the account or IP address is being ratelimited. Wait a few minutes for it to go away.
<br><br>
- `ServerOverloaded` - If Mojang's servers are being overloaded and cannot process your request. Happens quite often during "rare name" drops.


<br><br>
### Updating cached data
To avoid getting ratelimited, the library caches all account and profile data until a change is detected from a library call (then the cache is updated). So if for any reason you wish to get the latest information about the account, perhaps after tampering with account data externally outside of the API, you can do this by calling ```update_cache()```

**Example:**
```py
# updates account data cache (email, dob, email verification status, etc.)
user.update_cache()

# updates profile data cache (profile name, skin, capes, etc.)
user.profile.update_cache()
```

<br><br>
### Name snipers

Some multi-threaded programs, such as name snipers, tend to spam hundreds of requests concurrently. If you try to spam claim a name through a single ```MojangUser``` object using multi-threading, it might flood the session's connection pool and not all of the requests will go through.

To fix this, you can increase the connection pool size when <a href="/en/latest/authentication/#other-login-parameters">logging in</a>.


<div class="admonition danger">
<p class="admonition-title">Ratelimits (as of August 2020)</p>
<p>
Due to Mojang's strict ratelimiting, there is no need to flood Mojang's servers with more requests than necessary.
<br><br>
The ratelimit for <b><i>changing</i></b> a Minecraft name through <code>change_name</code> is 18 requests per account and 90 requests per IP address every 30 seconds. Therefore, you can use 5 accounts to send 18 requests each before the IP address gets ratelimited.
<br><br>
The ratelimit for <b><i>blocking</i></b> a Minecraft name through <code>block_name</code> is 3 requests per account and 30 requests per IP address every 30 seconds. So you can use 10 accounts to send 3 requests each before the IP address gets ratelimited.

</p>
</div>
<br><br>