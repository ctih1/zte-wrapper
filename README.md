# ZTE-Wrapper

Super simple API wrapper for modern ZTE routers using a more advanced authentication method. This has only been tested on an MC888B. If you have any feedback, please share!

## Features
"Support" in this case means that it can be controlled via the library.


| Feature                               | Support |
| ------------------------------------- | ------- |
| Create portforward rules              | ✅      |
| Delete portforward rules              | ✅      |
| List portforward rules                | ✅      |
| Send SMS                              | ✅      |
| Read SMS                              | ✅      |
| List wireless devices                 | ✅      |
| List wired devices                    | ✅      |
| Get signal strength                   | ✅      |
| Band information                      | ✅      |
| Usage statistics                      | ✅      |
| Firewall (e.g. domain/port filtering) | ❌      |
| DHCP Settings                         | ❌      |
| MAC-IP bindings                       | ✅      |
| DDNS settings                         | ✅      |
| VPN settings                          | ❌      |
| Network tools (e.g. traceroute/ping)  | ✅      |
| "Preferred position" tools            | ❌*     |

*: Not planning on implementing

The goal is to get all of the other features working. This **shouldn't** be too hard, since the hard work of authentication and such has been already done.

## Roadmap
~~1. Implement DDNS-settings~~
2. Publish onto PyPI
3. More reliable error handling
4. Implement rest of the features
5. Implement better documentation
6. Write tests

## Notes
- When referring to "megabytes" or "bytes", they are in base 2 format (e.g. 1Gib = 1024Mib)
- Authenticating (aka. running any of the API calls) logs off other clients from the admin web panel.

## Why?
I wanted to harvest statistics from the router to my Prometheus instance. I might actually rewrite the entire admin webpage since it's kind of horrible