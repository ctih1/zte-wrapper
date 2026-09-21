ZTE's thing seems to work with a few tokens. I have no idea what they are abbrevations of, but here's what they're used for

1. LD token
Seems to be some hashing thing that's used for logging in. This makes a password hash with `sha256(sha256(plaintxt_pass)+ld_token)`

2. STOK
The main authentication token which is sent as a cookie. Can be obtained with the help of the LD token

3. RD0 and RD1
RD0 seems to be the device firmware version (well, it shows up as `MC888B_Nordic1_B14`) for me.
RD1 is empty for me, but I'd assume it's some sort of software / hardware version number? 
Regardless, both are used to combine into a 2nd token, which is used for obtaining the AD token

4. RD
Some token similar to LD that's used as a part of a hash for the `AD` token used with `goform_set_cmd_process`.

5. AD
An auth thing used for `goform_set_cmd_process`, which is constructed like this:

```python
ad_token = sha256(sha256(rd0+rd1) + rd_token)
```