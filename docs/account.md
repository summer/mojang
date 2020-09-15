#
<h2>Accessing Mojang Account</h2>


<br>
### User
Access the Mojang account directly through the `user` attribute:

```py
print(user.id) # account's user ID
print(user.dob) # account's date of birth
print(user.email)
```


<p>Possible <b><code>user</code></b> attributes include:</p>
<div class="wy-table-responsive"><table class="longtable docutils align-default">
<colgroup>
<col style="width: 43%">
<col style="width: 90%">
</colgroup>
    <tbody>

<tr class="row-odd">
<td><p><code style="color:black;">id</code> (str)</p></td>
<td><p>User ID of the account</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">email</code> (str)</p></td>
<td><p>E-mail address of the account</p></td>
</tr>


<tr class="row-odd">
<td><p><code style="color:black;">dob</code> (datetime.datetime)</p></td>
<td><p>Date of birth of the account</p></td>
</tr>


<tr class="row-odd">
<td><p><code style="color:black;">security_challenges</code> (dict)</p></td>
<td><p>Security challenges of the account</p></td>
</tr>

<tr class="row-odd">
<td><p><a href="/en/latest/profile/#profile"><code>profile</code></a> (Profile)</p></td>
<td><p>Minecraft profile object</p></td>
</tr>


<tr class="row-odd">
<td><p><a href="/en/latest/session/#session-information"><code>session</code></a> (MojangSession)</p></td>
<td><p>Session object</p></td>
</tr>


<tr class="row-odd">
<td><p><code style="color:black;">has_minecraft</code> (bool)</p></td>
<td><p>Check if the account has a Minecraft profile or not</p></td>
</tr>



<tr class="row-odd">
<td><p><code style="color:black;">is_secured</code> (bool)</p></td>
<td><p>Check if the account is secured</p></td>
</tr>


<tr class="row-odd">
<td><p><code style="color:black;">is_legacy_user</code> (bool)</p></td>
<td><p>Check if the account is legacy</p></td>
</tr>


<tr class="row-odd">
<td><p><code style="color:black;">is_email_verified</code> (bool)</p></td>
<td><p>Check if the account has a verified e-mail address</p></td>
</tr>


<tr class="row-odd">
<td><p><code style="color:black;">is_verified_by_parent</code> (bool)</p></td>
<td><p>Check if the account was verified by a parent</p></td>
</tr>


<tr class="row-odd">
<td><p><code style="color:black;">is_fully_authenticated</code> (bool)</p></td>
<td><p>Check if the account is fully authenticated</p></td>
</tr>



</tbody>
</table></div>


<br><br>
## Methods

### block_username
<dl class="py method">
<dt id="MojangUser.block_username()">
<span class="sig-prename descclassname">MojangUser.</span><span class="sig-name descname">block_username</span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="/en/latest/account/#block_username" title="Permalink to this definition">¶</a></dt>
<dd><p>An empty Mojang account that does **not** own a Minecraft license can reserve (aka "block") a Minecraft name, which prevents other users from taking the name for up to 24 hours.</p>
<p>You can redeem a Minecraft license afterwards to secure the name for good.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>name</strong> (<code><span class="pre">str</span></code>) – Name to block / reserve</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><code>bool</code> – True if successfully blocked. False otherwise.
</dl>
</dl>
<p class="rubric">Example</p>
```py
if user.block_username("Notch"):
	print("Blocked the username Notch")
```
<div class="admonition danger">
<p class="admonition-title">False positives</p>
<p>During big name drops, there is a chance that Mojang will not update their database in time in order for the library to see if it's successfully blocked a name or not. Sometimes, Mojang's servers may return an <code>OK</code> response even when the library actually fails to block a name.<br><br>

So just because this function returns <code>True</code> does not mean the name was actually blocked!<br>It means you should double check.<br>
<br>
This is no surprise if thousands of users are flooding their service with requests at the same time, all of which are trying to block and claim the same exact name, so anomalies can and do happen sometimes (such as 2 users successfully claiming one name, thereby duplicating it which is not unheard of).<br><br>

To make sure that the function actually succeeded, you can block a second time after sleeping for at least 30 seconds.</p>
</div>

**Example #2**
```py
if user.block_username("Notch"):
	print("Blocked the username Notch")
    
    time.sleep(35)
    if user.block_username("Notch"):
        print("Success!")
    else:
        print("Aww, we didn't actually get it.)
```


---
<br>
### redeem_code
<dl class="py method">
<dt id="MojangUser.redeem_code()">
<span class="sig-prename descclassname">MojangUser.</span><span class="sig-name descname">redeem_code</span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="/en/latest/account/#redeem_code" title="Permalink to this definition">¶</a></dt>
<dd><p>Redeem a digital Minecraft license code. The account must not already own Minecraft.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>code</strong> (<code><span class="pre">str</span></code>) – License code to redeem </p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><code>None</code>
<dt class="field-even">Raises</dt>
<dd class="field-even"><p><code>ValueError</code> – If the license code could not be redeemed. Includes a message with the reason.
</dl>
</dl>
<p class="rubric">Example</p>
```py
try:
    user.redeem_code("ZPBK4-FJP8F-8Y4Y6-HQZKJ-T7X40"):
except ValueError as e:
    print(e.message)
```
---
<br>
<br>
