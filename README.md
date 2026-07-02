# ZTE-Wrapper

Super simple API wrapper for modern ZTE routers using a more advanced authentication method.

Currentl the only available method is `get_sms()`, which returns the SMS messages on the router.

## How to add more methods
`src/zte_wrapper/authwrapper.py` handles authentication and some other things for you. Simply add your implementation of new endpoints to `src/zte_wrapper/wrapper.py` to use them.