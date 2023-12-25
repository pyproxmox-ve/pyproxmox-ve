# API General Design

This page documents the general API design for pyproxmox-ve. Here you should grasp a quick understanding on how to access any Class method implemented in the module to create, read, update or delete a resource on the Proxmox VE API.

## ProxmoxVEAPI

The [ProxmoxVEAPI](pyproxmoxveapi.md) class is where you will spend most of your time. Each group of API resources are typically implemented in their own separate file/class unless there are only a few API operations then they may be housed into a common file.

Let's take the `/access/users/*` path as an example. Here are all the API endpoints as of Proxmox v8.1 under this API path:

|  Endpoint | Method | Purpose |
| --------- | ------ | ------- |
| /access/users | GET | Get all API Users |
| /access/users | POST | Create a new API User |
| /access/users/{userid} | GET | Get a specific API User |
| /access/users/{userid} | PUT | Update a specific API User |
| /access/users/{userid} | DELETE | Delete a specific API User |
| /access/users/{userid}/tfa | GET | Get 2FA details for a specific API User |
| /access/users/{userid}/unlock-tfa | PUT | Unlock 2FA for a specific API User |
| /access/users/{userid}/token | GET | Get a specific API User's Tokens |
| /access/users/{userid}/token/{tokenid} | GET | Get a specific API User's Token |
| /access/users/{userid}/token/{tokenid} | POST | Create a new API token for an existing API User |
| /access/users/{userid}/token/{tokenid} | PUT | Update a specific API User's Token |
| /access/users/{userid}/token/{tokenid} | DELETE | Delete a specific API User's Token |

Majority of each endpoint pattern is modelled as an API until it becomes to cumbersome. Therefore we model firstly the `/access` pattern as an API object called `AccessAPI` and then `/access/users` pattern as `AccessUsersAPI`.

``` py hl_lines="4"
class AccessAPI:
    def __init__(self, api: "ProxmoxVEAPI") -> None:
        self.api = api
        self.users = AccessUsersAPI(api)
```

We could go further and implement a `AccessUsersTokenAPI` object under our `AccessUsersAPI` but since there are a handful of endpoints, it is modelled somewhat like this:

``` py hl_lines="2 12"
class AccessUsersAPI(BaseResourceAPI):
    async def get_users(
        self, enabled: bool = None, full: bool = False
    ) -> list[User]:
        """Gathers all Users.

        Args:
            enabled:        Optional filter for enable property.
            full:           Include group and token information.
        """
        ...
    async def get_user_token(
        self, user_id: str, token_id: str
    ) -> UserToken | dict:
        """Get a specific users API token.

        Args:
            user_id:        User ID in the format of <username>@<realm>
            token_id:       Token ID
        """
        ...
```

Ok, but where is the `AccessAPI`?

## APIs attached to the ProxmoxVEAPI Class

The [ProxmoxVEAPI](pyproxmoxveapi.md) would implement a simple variable like this:

``` py hl_lines="10"
class ProxmoxVEAPI:
    ...
    def __init__(
        self,
        ...
    ) -> None:
        ...

        # APIs
        self.access = AccessAPI(self)
        self.version = VersionAPI(self)
```

So if we want to get the users or a specific user token in the implementation shown previously, we do this:

``` py hl_lines="3 4"
api = ProxmoxVEAPI(...)

users = await api.access.users.get_users()
user_token = await api.acess.users.get_user_token(...)
```

## aiohttp specific implementation

Typically you won't need to change this behaviour but [ProxmoxVEAPI](pyproxmoxveapi.md) allows you to pass in a seperate:

- SSLContext
- BaseConnector (you should only ever use TCPConnector)
- ClientSession

If you do not know what these do, don't touch them and leave them be!

## API Version and API Types

There are no plans to implement any older API versions or different API types, the current supported are version `api2` and type `json`.

## To Pydantic or not to Pydantic

Pydantic is an optional installation in this module, however it is a requirement for anyone looking to contribute due to the tests and compatibility. To avoid forcing this module to be a requirement, there has been some slight hacks put in place to make type hints work properly in editors, and to ensure those who do not install pydantic don't run into import errors.

There are 3 key parts I would like to stress to the reader and they are as follows:

1. `use_pydantic` is important when initializing [ProxmoxVEAPI](pyproxmoxveapi.md), because this will determine if the logic is used to load data into Pydantic models, so if you don't set this to `True` then you may run into AttributeErrors and other errors.

2. `TYPE_CHECKING` is a must to avoid import errors for users not using Pydantic, however return type hints will break if you do not import `from __future__ import annotations` at the top of the file in this module.

3. Finally and the big one, since we can not import Pydantic models directly in the API implementation files, we can't pass it into the `query()`, `create()` or `update()` functions. So to dynamically load these models we need a way to tell which model (and where it is located) so that we can attempt to dynamically import the model and validate the data. This is currently done using a `tuple(str, str)` like this: `("pyproxmox_ve.models.user", "UserCreate")`, this method is currently being reviewed and could change at a later date.

!!! note
    If you would like to understand more about point 3, then this logic is stored inside the [ProxmoxVEAPI](pyproxmoxveapi.md) class, specifically under the function [_normalize_data](pyproxmoxveapi.md#pyproxmox_ve.api.ProxmoxVEAPI._normalize_data) method.
