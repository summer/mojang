#
<br>
## get_uuid
<dl class="py method">
<dt id="MojangAPI.get_uuid()">
<span class="sig-prename descclassname">MojangAPI.</span><span class="sig-name descname">get_uuid</span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="/en/latest/api/#get_uuid" title="Permalink to this definition">¶</a></dt>
<dd><p>Convert a username to a UUID</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>username</strong> (<code><span class="pre">str</span></code>) – The Minecraft username to be converted.</p></li>
<li><p><strong>timestamp</strong> (<code><span class="pre">int</span></code>, <i>optional</i>) – Get the username's UUID at a specified UNIX timestamp. You can also get the username's first UUID by passing <code>0</code>. However, this only works if the name was changed at least once, or if the account is legacy.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><code>str</code> | <code>None</code> – The UUID</em>. Otherwise, None if the username does not exist.</p>
</dd>
</dl>
</dl>
<p class="rubric">Example</p>
```py
uuid = MojangAPI.get_uuid("Notch")

if not uuid:
    print("The username Notch is not taken")
else:
    print(f"Notch's UUID is {uuid}")
```

<p class="rubric">Example #2</p>
```py
timestamp = 1598678824

uuid = MojangAPI.get_uuid("Notch", timestamp)
printf(f"Notch's UUID on {timestamp} was {uuid}")
```

---
<br>
## get_uuids
<dl class="py method">
<dt id="MojangAPI.get_uuids()">
<span class="sig-prename descclassname">MojangAPI.</span><span class="sig-name descname">get_uuids</span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="/en/latest/api/#get_uuids" title="Permalink to this definition">¶</a></dt>
<dd><p>Convert up to 10 usernames to UUIDs in a single network request.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>names</strong> (<code><span class="pre">list</span></code>) – The Minecraft username(s) to be converted. If more than 10 are included, only the first 10 will be parsed.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><code>dict</code> – username:uuid pairs of the converted usernames.</em> Names are also case-corrected. If a username does not exist, it will not be included in the returned dictionary.
</dl>
</dl>
<p class="rubric">Example</p>
```py
usernames = ["Notch", "Herobrine", "Dream"]

players = MojangAPI.get_uuids(usernames)

for name, uuid in players.items():
    print(name, uuid)
```

---
<br>
## get_username
<dl class="py method">
<dt id="MojangAPI.get_username()">
<span class="sig-prename descclassname">MojangAPI.</span><span class="sig-name descname">get_username</span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="/en/latest/api/#get_username" title="Permalink to this definition">¶</a></dt>
<dd><p>Convert a UUID to a username</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>uuid</strong> (<code><span class="pre">str</span></code>) – The Minecraft UUID to be converted to a username.
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><code>str</code> | <code>None</code> – The username</em>. Otherwise, <code>None</code> if the UUID does not exist.</p>
</dl>
</dl>
<p class="rubric">Example</p>
```py
username = MojangAPI.get_username("e149b689-d25c-4ace-a9ea-4be1e8407f85")

if not username:
    print("UUID does not appear to be valid.")
```
---
<br>

## get_drop_timestamp
<dl class="py method">
<dt id="MojangAPI.get_drop_timestamp()">
<span class="sig-prename descclassname">MojangAPI.</span><span class="sig-name descname">get_drop_timestamp</span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="/en/latest/api/#get_drop_timestamp" title="Permalink to this definition">¶</a></dt>
<dd><p>Get the timestamp of when a username drops</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd">
<ul class="simple">
<li><p><strong>username</strong> (<code><span class="pre">str</span></code>) – The Minecraft username.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><code>int</code> | <code>None</code> – The drop timestamp</em>. Otherwise, <code>None</code> if the username is not being released/dropped.</p>
</dd>
<dt class="field-even">Raises</dt>
<dd class="field-even"><p><code>ValuerError</code> – In case the username does not exist or is invalid. Technically, this occurs when the library fails to convert the username to a UUID for internal use.
</dl>
</dl>
<p class="rubric">Example</p>
```py
drop_timestamp = MojangAPI.get_drop_timestamp("Notch")

if not drop_timestamp:
    print("Notch is not dropping")
else:
    seconds = drop_timestamp - time.time()
    print(f"Notch drops in {seconds} seconds")
```
---
<br>

## get_profile
<dl class="py method">
<dt id="MojangAPI.get_profile()">
<span class="sig-prename descclassname">MojangAPI.</span><span class="sig-name descname">get_profile</span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="/en/latest/api/#get_profile" title="Permalink to this definition">¶</a></dt>
<dd><p>Get more information about a user from their UUID</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd">
<ul class="simple">
<li><p><strong>uuid</strong> (<code><span class="pre">str</span></code>) – The user's UUID.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><code>UserProfile</code> | <code>None</code> – An object containing multiple information about the profile</em>. Otherwise, None if the profile does not exist.
<p>Possible **UserProfile** object attributes include:</p>

<div class="wy-table-responsive"><table class="longtable docutils align-default">
<colgroup>
<col style="width: 40%">
<col style="width: 90%">
</colgroup>
    <tbody>

<tr class="row-odd">
<td><p><code style="color:black;">id</code> (str)</p></td>
<td><p>UUID of the profile</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">name</code> (str)</p></td>
<td><p>Name of the profile</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">cape_url</code> (str or None)</p></td>
<td><p>URL to the profile's cape</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">skin_url</code> (str or None)</p></td>
<td><p>URL to the profile's skin</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">skin_model</code> (str)</p></td>
<td><p>Skin model of the profile</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">is_legacy_profile</code> (bool)</p></td>
<td><p>Check if the profile is legacy</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">timestamp</code> (int)</p></td>
<td><p>Timestamp of when the profile was retrieved</p></td>
</tr>
</tbody>
</table></div>
</dd>
</dl>
</dl>
<p class="rubric">Example</p>
```py
uuid = MojangAPI.get_uuid("Notch")

if uuid:
    profile = MojangAPI.get_profile(uuid)

    print(profile.name)
    print(profile.skin_url)
    # and so on...
```
---
<br>

## get_name_history
<dl class="py method">
<dt id="MojangAPI.get_name_history()">
<span class="sig-prename descclassname">MojangAPI.</span><span class="sig-name descname">get_name_history</span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="/en/latest/api/#get_name_history" title="Permalink to this definition">¶</a></dt>
<dd><p>Get a user's name history</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd">
<ul class="simple">
<li><p><strong>uuid</strong> (<code><span class="pre">str</span></code>) – The user's UUID.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><code>list</code> – A list of dictionaries, each of which contains a name:changed_to_at pair. If changed_to_at is set to 0, it is because it is the profile's first name.
</dd>
</dl>
</dl>
<p class="rubric">Example</p>
```py
uuid = MojangAPI.get_uuid("Dream")

name_history = MojangAPI.get_name_history(uuid)

for data in name_history:
    if data['changed_to_at'] == 0:
        print(f"{data['name']} was the user's first name")
    else:
        print(f"{uuid} had the name {data['name']} on {data['changed_to_at']}")
```
---
<br>


## get_api_status
<dl class="py method">
<dt id="MojangAPI.get_api_status()">
<span class="sig-prename descclassname">MojangAPI.</span><span class="sig-name descname">get_api_status</span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="/en/latest/api/#get_api_status" title="Permalink to this definition">¶</a></dt>
<dd><p>Get the API / network status of various Mojang services</p>
<dl class="field-list simple">
<dd class="field-odd">
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><code>dict</code> – Contains server:status pairs. Possible statuses are `green` (no issues), `yellow` (some issues), and `red` (service unavailable).

</dd>
</dl>
</dl>
<p class="rubric">Example</p>
```py
data = MojangAPI.get_api_status()

for server, status in data.items():
    if status == "red" or status == "yellow":
        print(f"{server} is experiencing connection issues.")
    else:
        print(f"{server} is alive and healthy!")
```

---
<br>
## get_blocked_servers
<dl class="py method">
<dt id="MojangAPI.get_blocked_servers()">
<span class="sig-prename descclassname">MojangAPI.</span><span class="sig-name descname">get_blocked_servers</span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="/en/latest/api/#get_blocked_servers" title="Permalink to this definition">¶</a></dt>
<dd><p>Get a list of SHA1 hashes of blacklisted Minecraft servers that do not follow EULA.

These servers have to abide by the EULA or be shut down forever. The hashes are not cracked.</p>
<dl class="field-list simple">
<dd class="field-odd"><ul class="simple">
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><code>list</code> – List of blacklisted server hashes.</em>
</dl>
</dl>
<p class="rubric">Example</p>
```py
servers = MojangAPI.get_blocked_servers()

for hash in servers:
    print(hash)
```

---
<br>

## get_sale_statistics
<dl class="py method">
<dt id="MojangAPI.get_sale_statistics()">
<span class="sig-prename descclassname">MojangAPI.</span><span class="sig-name descname">get_sale_statistics</span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="/en/latest/api/#get_sale_statistics" title="Permalink to this definition">¶</a></dt>
<dd><p>Get statistics on the sales of Minecraft.</p>
<p> You will receive a single object corresponding to the sum of sales of the requested type(s). At least one type of sale must be set to `True`</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd">
<ul class="simple">
<li><p><strong>item_sold_minecraft</strong> (<code><span class="pre">bool</span></code>) – set to True by default
<li><p><strong>prepaid_card_redeemed_minecraft</strong> (<code><span class="pre">bool</span></code>) – set to True by default
<li><p><strong>item_sold_cobalt</strong> (<code><span class="pre">bool</span></code>) – set to False by default
<li><p><strong>item_sold_scrolls</strong> (<code><span class="pre">bool</span></code>) – set to False by default
<li><p><strong>prepaid_card_redeemed_cobalt</strong> (<code><span class="pre">bool</span></code>) – set to False by default
<li><p><strong>item_sold_dungeons</strong> (<code><span class="pre">bool</span></code>) – set to False by default
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><code>dict</code> – A dictionary containing 3 sales metrics containing the sum of the requested type(s)
</dd>
</dl>
</dl>
<p class="rubric">Example</p>
```py
kwargs = dict(item_sold_minecraft=True,
              prepaid_card_redeemed_minecraft=True,
              item_sold_cobalt=False,
              item_sold_scrolls=False,
              prepaid_card_redeemed_cobalt=False,
              item_sold_dungeons=False
              )
                                                                             
metrics = MojangAPI.get_sale_statistics(**kwargs)

print(metrics["total"])
print(metrics["last24h"])
print(metrics["sale_velocity_per_seconds"])
```
---
<br>

## refresh_access_token
<dl class="py method">
<dt id="MojangAPI.refresh_access_token()">
<span class="sig-prename descclassname">MojangAPI.</span><span class="sig-name descname">refresh_access_token</span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="/en/latest/api/#refresh_access_token" title="Permalink to this definition">¶</a></dt>
<dd><p>Refresh an access token and get a new one back, along with other various information.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>access_token</strong> (<code><span class="pre">str</span></code>) – The access token to refresh</p></li>
<li><p><strong>client_token</strong> (<code><span class="pre">str</span></code>) – The client token associated with the access token</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><code>dict</code> – Contains the new access token and other various account information.


</dl>
</dl>
<p class="rubric">Example</p>
```py
access_token = "YOUR_ACCESS_TOKEN"
client_token = "YOUR_CLIENT_TOKEN"

account = MojangAPI.refresh_access_token(access_token, client_token)

print("The new access token is " + account["access_token"])

# main keys include...
print(account["access_token"])
print(account["client_token"])
print(account["username"])
print(account["uuid"])

# if the account has a Minecraft profile. otherwise, these contain None
print(account["profile_id"])
print(account["profile_name"])
```
<br>
<br>
