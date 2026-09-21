some weird ass auth token sent with set_cmd requests sometimes, so fucking cool I finally figured this out

```
rd0 = wa_inner_version (from get_cmd)
rd1 = cr_version (from get_cmd)

rd0 = MC888B_Nordic1_B14
rd1 = ""

o = sha256(rd0+rd1)
_ = RD
_ = "ADB702A684070366F5C99F3D80E2A1AD885D902AE7AD7B5B26F1EAF56F062F9A"
a = sha256(o + _)
a = "3CB03DAF07D19425800B0D317112F853BF69A2A69F486AF4D7170D9EF3860870"
AD=a
```