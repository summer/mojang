#
<h2>Accessing Minecraft Profile</h2>



<br>
### Profile
Access the account's Minecraft profile through the `profile` object:

```py
print(user.profile.id)
print(user.profile.name)

if not user.profile.is_name_change_allowed:
    print("Account does not have an available name change")
    print(f"It was last changed on {user.profile.name_changed_at}")

if not user.profile.is_migrated:
    print("Account is not migrated")

# get a dictionary object of all the profile's information
print(user.profile.to_dict())
```

<p>Possible <b><code>profile</code></b> attributes include:</p>
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
<td><p>Minecraft / profile name</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">is_paid</code> (bool)</p></td>
<td><p>Check if the profile is paid</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">is_migrated</code> (bool)</p></td>
<td><p>Check if the profile is migrated</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">is_suspended</code> (bool)</p></td>
<td><p>Check if the profile is suspended</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">is_legacy_profile</code> (bool)</p></td>
<td><p>Check if the profile is legacy</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">is_name_change_allowed</code> (bool)</p></td>
<td><p>Check if a name change is allowed</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">created_at</code> (int)</p></td>
<td><p>Timestamp of when the profile was created</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">name_changed_at</code> (int)</p></td>
<td><p>Timestamp of when the name was last changed</p></td>
</tr>
</tbody>
</table></div>

If the account does not have a profile or the account has not completed authentication
by answering required security challenges, `profile` will be set to `None`

<br>
<br>
### Skin information

Access the profile's skin through the `skin` object:

```py
# check if the profile has a skin first
if user.profile.skin:
    print(user.profile.skin.url)
    print(user.profile.skin.texture_id)

# get a dictionary object of all the skin's information
print(user.profile.skin.to_dict())
```


<p>Possible <b><code>skin</code></b> attributes include:</p>
<div class="wy-table-responsive"><table class="longtable docutils align-default">
<colgroup>
<col style="width: 40%">
<col style="width: 90%">
</colgroup>
    <tbody>

<tr class="row-odd">
<td><p><code style="color:black;">type</code> (str)</p></td>
<td><p>Type of skin</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">url</code> (str)</p></td>
<td><p>URL to the skin's image</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">texture_id</code> (str)</p></td>
<td><p>Texture ID of the skin</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">is_visible</code> (bool)</p></td>
<td><p>Check if the skin is visible</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">is_selected</code> (bool)</p></td>
<td><p>Check if the skin is selected</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">is_deleted</code> (bool)</p></td>
<td><p>Check if the skin is deleted</p></td>
</tr>

</tbody>
</table></div>

If the account does not have a skin, `skin` will be set to `None`


<br>
<br>
### Capes
```py
if user.profile.capes:
    print(f"Found {len(user.profile.capes} capes on the profile")

# access them by index
user.profile.capes[0].name
user.profile.capes[0].url

# or just loop through
for cape in user.profile.capes:
    print(cape.name)
    print(cape.url)

    # get a dictionary object of all the cape's information
    print(cape.to_dict())
```

<p>Possible <b><code>cape</code></b> attributes include:</p>
<div class="wy-table-responsive"><table class="longtable docutils align-default">
<colgroup>
<col style="width: 40%">
<col style="width: 90%">
</colgroup>
    <tbody>

<tr class="row-odd">
<td><p><code style="color:black;">name</code> (str)</p></td>
<td><p>Name of the cape</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">type</code> (str)</p></td>
<td><p>Type of cape</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">url</code> (str)</p></td>
<td><p>URL to the cape's texture</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">version</code> (str)</p></td>
<td><p>The cape's version</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">is_visible</code> (bool)</p></td>
<td><p>Check if the cape is visible</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">is_selected</code> (bool)</p></td>
<td><p>Check if the cape is selected</p></td>
</tr>

<tr class="row-odd">
<td><p><code style="color:black;">is_deleted</code> (bool)</p></td>
<td><p>Check if the cape is deleted</p></td>
</tr>

</tbody>
</table></div>


If the account does not have a cape, `cape` will be set to `None` rather than an empty list.

<br>
<br>
## Methods

### change_name
<dl class="py method">
<dt id="MojangAPI.change_name()">
<span class="sig-prename descclassname">MojangUser.profile.</span><span class="sig-name descname">change_name</span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="/en/latest/profile/#change_name" title="Permalink to this definition">¶</a></dt>
<dd><p>Change the profile's Minecraft username</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>name</strong> (<code><span class="pre">str</span></code>) – New name to change to</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><code>bool</code> – True if successfully changed. False otherwise.
<dt class="field-even">Raises</dt>
<dd class="field-even"><p><code>ForbiddenNameChange</code> – If the name was already changed once less than 30 days ago.
</dl>
</dl>
<p class="rubric">Example</p>
```py
if not user.profile.change_name("Notch")
    print("Failed to change name")
```
---
<br>

### skin_upload
<dl class="py method">
<dt id="MojangAPI.skin_upload()">
<span class="sig-prename descclassname">MojangUser.profile.</span><span class="sig-name descname">skin_upload</span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="/en/latest/profile/#skin_upload" title="Permalink to this definition">¶</a></dt>
<dd><p>Change the profile's Minecraft skin by uploading an image file or image bytes of a skin. Must be one or the other.</p>
<p>This also sets the skin and deletes the old one.</p>
<b>Skin upload requirements:</b>
<ul>
<li>Max allowed image size is 24.576 KB</li>
<li>Image dimensions have to be 64x32 px.</li>
<li>Mojang prefers that the image is a .png file, but this does not seem to be set in stone.</li>
</ul>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>model</strong> (<code><span class="pre">str</span></code>) – slim or classic</p></li>
<li><p><strong>image_file_path</strong> (<code><span class="pre">str</span></code>, <i>optional</i>) – file path to the skin's image</p></li>
<li><p><strong>image_bytes</strong> (<code><span class="pre">bytes</span></code>, <i>optional</i>) – image bytes of the skin</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><code>None</code>
<dt class="field-even">Raises</dt>
<dd class="field-even"><p><code>ValueError </code> – If the uploaded skin image is invalid. Includes a message with the reason.
</dl>
</dl>


<p class="rubric">Example</p>
```py
# Upload an image file of a skin
skin_path = "C:\\Users\\Administrator\\Desktop\\skin.png"
user.profile.skin_upload("slim", skin_path)


# Uploading a skin directly from image bytes
resp = requests.get("https://example.com/skin.jpg")
user.profile.skin_upload("slim", image_bytes=resp.content)
```

---
<br>

### skin_copy
<dl class="py method">
<dt id="MojangAPI.skin_copy()">
<span class="sig-prename descclassname">MojangUser.profile.</span><span class="sig-name descname">skin_copy</span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="/en/latest/profile/#skin_copy" title="Permalink to this definition">¶</a></dt>
<dd><p>Change the profile's Minecraft skin by copying another player's skin. Also copies the skin model (slim/classic).</p>
<p>If the player has the default skin, this will reset the profile's skin to default.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>uuid</strong> (<code><span class="pre">str</span></code>) – UUID of the player whose skin you want to copy</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><code>None</code>
</dl>
</dl>
<p class="rubric">Example</p>
```py
# with help from the MojangAPI
uuid = MojangAPI.get_uuid("Notch")

# now your account will have Notch's skin
user.profile.skin_copy(uuid)
```

---
<br>

### skin_reset
<dl class="py method">
<dt id="MojangAPI.skin_reset()">
<span class="sig-prename descclassname">MojangUser.profile.</span><span class="sig-name descname">skin_reset</span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="/en/latest/profile/#skin_reset" title="Permalink to this definition">¶</a></dt>
<dd><p>Reset the profile's Minecraft back to the default skin.</p>
<dl class="field-list simple">
<dd class="field-odd"><ul class="simple">
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><code>None</code>
</dl>
</dl>
<p class="rubric">Example</p>
```py
user.profile.skin_reset()
```
---
<br>
