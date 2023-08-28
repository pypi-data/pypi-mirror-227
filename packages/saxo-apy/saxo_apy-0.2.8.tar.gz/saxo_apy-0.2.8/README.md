```text
   _____         __   __  ____                   _____  __     __
  / ____|   /\   \ \ / / / __ \            /\   |  __ \ \ \   / /
 | (___    /  \   \ V / | |  | |  ____    /  \  | |__) | \ \_/ / 
  \___ \  / /\ \   ) (  | |  | | |____|  / /\ \ |  ___/   \   /  
  ____) |/ ____ \ / _ \ | |__| |        / ____ \| |        | |   
 |_____//_/    \//_/ \_\ \____/        /_/    \/|_|        |_|  
 ```

[![python](https://img.shields.io/badge/python-3.7%2B-blue)](https://github.com/gidven/saxo-openapi-client-python)
[![pypi](https://img.shields.io/pypi/v/saxo-apy?style=flat-square)](https://pypi.org/project/saxo-apy)
[![license](https://img.shields.io/github/license/gidven/saxo-openapi-client-python?style=flat-square)](https://github.com/gidven/saxo-openapi-client-python/blob/main/LICENSE)

# Saxo-APY: Python Client for Saxo Bank OpenAPI

*A lightweight Python client for hassle-free tinkering with Saxo OpenAPI.*

> NOTE: This Python package was created by an enthusiast as a learning project. None of the contents in this repository are maintained by Saxo Bank, and Saxo Bank does not guarantee correctness of the provided implementation.

## At First Glance

> For more inspiration see [the samples](./samples/)!

```python
from saxo_apy import SaxoOpenAPIClient

client = SaxoOpenAPIClient("app_config.json")
client.login()

me = client.get("port/v1/users/me")
eurusd_price = client.get("/trade/v1/infoprices?Uic=21&AssetType=FxSpot")
portfolio_orders = client.get("/port/v1/orders/me")

print(f"Welcome {me['UserId']}!")
print(f"EURUSD is trading at: {eurusd_price['Quote']['Bid']} / {eurusd_price['Quote']['Ask']}")
print(f"You have: {portfolio_orders['__count']} orders in your portfolio")
```

Output:

```text
🌐 opening login page in browser - waiting for user to authenticate... 🔑
📞 received callback from Saxo SSO
✅ authorization succeeded - connected to SIM environment with WRITE / TRADE permissions (session ID ceb2be9095f64eaf9e5caeb21d6fc799)

Welcome 16371609!
EURUSD is trading at: 1.08229 / 1.08249 (Bid/Ask)
You have: 15 orders in your portfolio
```

## Features

- [x] Authentication and session management with Saxo SSO
  - Supports OAuth 2.0 `Code` grant type
  - Works seamlessly in both `SIM` and `LIVE` environments
  - Automated handling of callback from SSO (optional)
  - Headless authentication for deployed applications (optional)
  - Keep sessions and active websockets connections alive by refreshing access tokens via asyncio
- [x] Read operations (`GET` requests)
- [x] Write operations (`POST`, `PUT`, `PATCH`, `DELETE` requests)
- [x] Supports async requests, streaming, and decoding of streaming messages
- [x] Error handling with comprehensive exception messages

## Installation

This python package is available on PyPI. Install the client by running the below `pip` command in your terminal:

`pip install saxo-apy`

## Requirements

- Python 3.7+
- An OpenAPI application registered [on Saxo Bank's Developer Portal](https://www.developer.saxo/openapi/appmanagement)
  - [Create a free developer account](https://www.developer.saxo/accounts/sim/signup) if you don't have one already.
  - Ensure the application is set up with `Grant Type: Code` as authentication flow.
  - At least 1 localhost redirect needs to be defined such as `http://localhost:12321/redirect` (for development/testing purposes)
  - (Optional) enable trading permissions for the app if you want to 'write' to your account (and place orders)

## Dependencies

This package requires 5 dependencies:

- `pydantic`, for parsing config and JSON responses 
- `Flask`, to run a local server and catch the callback from Saxo SSO
- `httpx`, for sending requests to OpenAPI and managing the client session
- `websockets`, for setting up a websocket connection to Saxo's streaming service
- `loguru`, to handle logging

## Notes

The client supports OAuth Code flow and will automatically spin up a server to listen for the redirect from Saxo SSO. At least 1 `localhost` redirect needs to be defined in application config for this purpose.

By default, the client will use the *first available localhost redirect* to run the server on (typically only 1 exists in the config).

The client validates redirect urls in application config automatically. OAuth 2.0 code flow requires a fixed port to be specified on the redirect url. In case this is incorrectly configured, an error message will guide you to ensure app config is correct with OpenAPI:

```text
one or more redirect urls have no port configured, which is required for grant type 'Code' - ensure a port is configured in the app config object for each url (example: http://localhost:23432/redirect)
```
