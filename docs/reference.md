#
<h2>Quick Reference</h2>

<br>


## MojangAPI
<h3>Methods</h3>
<div class="wy-table-responsive"><table class="longtable docutils align-default">
<colgroup>
<col style="width: 10%">
<col style="width: 90%">
</colgroup>
    <tbody>

<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/api/#get_uuid" title="get_uuid">
<code class="xref py py-obj "><span class="pre">get_uuid</span></code></a></p></td>
<td><p>Convert username to UUID</p></td>
</tr>



<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/api/#get_uuids" title="get_uuids">
<code class="xref py py-obj "><span class="pre">get_uuids</span></code></a></p></td>
<td><p>Convert up to 10 username to UUIDs</p></td>
</tr>

<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/api/#get_username" title="get_username">
<code class="xref py py-obj "><span class="pre">get_username</span></code></a></p></td>
<td><p>Convert UUID to username</p></td>
</tr>


<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/api/#get_drop_timestamp" title="get_drop_timestamp">
<code class="xref py py-obj "><span class="pre">get_drop_timestamp</span></code></a></p></td>
<td><p>Get a UNIX timestamp of the exact time a name drops</p></td>
</tr>

<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/api/#get_profile" title="get_profile">
<code class="xref py py-obj "><span class="pre">get_profile</span></code></a></p></td>
<td><p>Get multiple information about a Minecraft profile</p></td>
</tr>

<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/api/#get_name_history" title="get_name_history">
<code class="xref py py-obj "><span class="pre">get_name_history</span></code></a></p></td>
<td><p>Get a player's name history from their UUID</p></td>
</tr>

<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/api/#get_api_status" title="get_api_status">
<code class="xref py py-obj "><span class="pre">get_api_status</span></code></a></p></td>
<td><p>Get network status on various Mojang's services</p></td>
</tr>

<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/api/#get_blocked_servers" title="get_blocked_servers">
<code class="xref py py-obj "><span class="pre">get_blocked_servers</span></code></a></p></td>
<td><p>Get a list of blacklisted Minecraft servers</p></td>
</tr>

<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/api/#get_sale_statistics" title="get_sale_statistics">
<code class="xref py py-obj "><span class="pre">get_sale_statistics</span></code></a></p></td>
<td><p>Get statistics on the sales of Minecraft</p></td>
</tr>

<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/api/#refresh_access_token" title="refresh_access_token">
<code class="xref py py-obj "><span class="pre">refresh_access_token</span></code></a></p></td>
<td><p>Refresh an access token and get a new one</p></td>
</tr>


</tbody>
</table></div>

<br>
<br>
## MojangUser

<h3>Account Methods</h3>
<div class="wy-table-responsive"><table class="longtable docutils align-default">
<colgroup>
<col style="width: 10%">
<col style="width: 90%">
</colgroup>
    <tbody>

<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/account/#redeem_code" title="redeem_code">
<code class="xref py py-obj "><span class="pre">redeem_code</span></code></a></p></td>
<td><p>Redeem a Minecraft license code</p></td>
</tr>


<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/account/#block_username" title="block_username">
<code class="xref py py-obj "><span class="pre">block_username</span></code></a></p></td>
<td><p>Reserve aka "block" a Minecraft username</p></td>
</tr>

<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/authentication/#completing-security-challenges" title="answer_security_challenges">
<code class="xref py py-obj "><span class="pre">answer_security_challenges</span></code></a></p></td>
<td><p>Answer security challenges to complete authentication</p></td>
</tr>


<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/other/#updating-cached-data" title="update_cache">
<code class="xref py py-obj "><span class="pre">update_cache</span></code></a></p></td>
<td><p>Update account data cache to get latest information</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">to_dict</code></p></td>
<td><p>Get a dictionary object of all account information</p></td>
</tr>

</tbody>
</table></div>



<h3>Profile Methods</h3>
<div class="wy-table-responsive"><table class="longtable docutils align-default">
<colgroup>
<col style="width: 10%">
<col style="width: 90%">
</colgroup>
    <tbody>

<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/profile/#change_name" title="change_name">
<code class="xref py py-obj "><span class="pre">change_name</span></code></a></p></td>
<td><p>Change Minecraft profile name</p></td>
</tr>


<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/profile/#skin_upload" title="skin_upload">
<code class="xref py py-obj "><span class="pre">skin_upload</span></code></a></p></td>
<td><p>Upload and set a skin from image file or image bytes</p></td>
</tr>

<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/profile/#skin_copy" title="skin_copy">
<code class="xref py py-obj "><span class="pre">skin_copy</span></code></a></p></td>
<td><p>Copy another player's skin by passing their UUID</p></td>
</tr>


<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/profile/#skin_reset" title="skin_reset">
<code class="xref py py-obj "><span class="pre">skin_reset</span></code></a></p></td>
<td><p>Reset skin back to default</p></td>
</tr>

<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/other/#updating-cached-data" title="update_cache">
<code class="xref py py-obj "><span class="pre">update_cache</span></code></a></p></td>
<td><p>Update profile data cache to get latest information</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">to_dict</code></p></td>
<td><p>Get a dictionary object of all profile information</p></td>
</tr>

</tbody>
</table></div>



<h3>Session Methods</h3>
<div class="wy-table-responsive"><table class="longtable docutils align-default">
<colgroup>
<col style="width: 10%">
<col style="width: 90%">
</colgroup>
    <tbody>

<tr class="row-odd"><td><p><a class="reference internal" href="/en/latest/session/#refreshing-session-avoiding-re-login" title="refresh">
<code class="xref py py-obj "><span class="pre">refresh</span></code></a></p></td>
<td><p>Refreshes the session. Call this every 12 hours to avoid logging in again.</p></td>
</tr>
<tr class="row-odd">
<td><p><code style="color:black;">to_dict</code></p></td>
<td><p>Get a dictionary object of all session information</p></td>
</tr>

</tbody>
</table></div>
<br><br>
