# ZTE-Wrapper

Super simple API wrapper for modern ZTE routers using a more advanced authentication method.

Available functions:
- Get SMS messages `get_sms()`
- Get network throughput, ISP name, etc `get_network_details()`
- Get network signal strength `get_signal_strength()`

## How to add more methods
`src/zte_wrapper/authwrapper.py` handles authentication and some other things for you. Simply add your implementation of new endpoints to `src/zte_wrapper/wrapper.py` to use them.

## Notes
- When referring to "megabytes" or "bytes", they are in base 2 format (e.g. 1Gib = 1024Mib)
- Authenticating logs off other clients from the web panel. This shouldn't happen that often, as the authentication is only run when required

## Confirmed working devices
- ZTE MC888