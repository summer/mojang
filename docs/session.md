#
<h2>Accessing Session</h2>

<br>

### Session information
Access the currently authenticated session information through the `session` object:

```py
print(user.session.access_token)
print(user.session.client_token)

print(user.session.user_agent)
print(user.session.minecraft_name)
```

<p>Possible <b><code>session</code></b> attributes include:</p>

<div class="wy-table-responsive"><table class="longtable docutils align-default">
<colgroup>
<col style="width: 10%">
<col style="width: 90%">
</colgroup>
    <tbody>

<tr class="row-odd">
<td><p><code style="color:black;">username</code> (str)</p></td>
<td><p>Username that was used to log into the account</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">password</code> (str)</p></td>
<td><p>Password that was used to log into the account</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">access_token</code> (str)</p></td>
<td><p> Access token used to authenticate with the account</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">client_token</code> (str)</p></td>
<td><p> A random seed that was used to generate the access token</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">profile_name</code> (str)</p></td>
<td><p>Name of the Minecraft profile</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">profile_id</code> (str)</p></td>
<td><p>UUID of Minecraft profile</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">user_agent</code> (str)</p></td>
<td><p>User agent / browser / device associated with the session</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">proxy</code> (str)</p></td>
<td><p>HTTPS proxy that all session requests are routed through</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">maximum_pool_size</code> (int)</p></td>
<td><p>Maximum number of concurrent connections allowed</p></td>
</tr>
</tbody>
</table></div>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>Getting <code>profile_name</code> and <code>profile_id</code> from the session directly instead of through <a href="/en/latest/profile/#profile"><code>Profile</code></a> does not require completing authentication.
<br><br>
So although <code>Profile</code> might return <code>None</code> because you haven't completed security challenges, you can still get some information about the Minecraft profile through these 2 attributes.</p>
</div>

<br>
<br>
### Refreshing session / avoiding re-login

All Mojang sessions expire after a about a day. If a user wishes to stay logged in on the account for days at a time, you are strongly advised to refresh the session every ~12 hours or so. This can be done by calling:
```py
user.session.refresh()
``` 
Refreshing the session invalidates the session's current access token and updates it with a new one, which has a fresh lifespan. The library already refreshes the session once for you after you login and complete authentication, so you don't have to do it for some time.

If a session dies for whatever reason, you will **not** be able to refresh it and will have to complete the authentication process all over again.



<br><br>