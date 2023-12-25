# Tests

[pytest](https://docs.pytest.org/en/7.4.x/) is the testing framework of choice in this project. If you are not very familiar with the basics of pytest, I would recommend reading the documentation or having a look at the tests in this project to see the structure and provided functionality.

Each API endpoint or class/function that interacts with a resource which changes potential production data must implement a test and pass before a merge request is accepted.

## Test Structure

All tests belong in the `tests` directory of the project. The structure of this folder may change from time to time but the basis is that for every API endpoint, you try to group them cleanly into their respective files according to the API endpoint path, prefixed with `test_`. Here are some examples:

`/access/users*` endpoints are resources related to web UI users, we can create users, delete users, update fields, create API tokens, etc... A `GET` to `/access/users` will return a list of users, so to access these resources in Python, we would do:

```python
from pyproxmox_ve import ProxmoxVEAPI

api = ProxmoxVEAPI()
api.access.users        # This is the AccessUsersAPI object stored in `pyproxmox_ve/resources/access/users/users.py`
```

Methods should be self documenting in a way that I can figure out the purpose of it, so to get all users, I can use:
```python

users = api.access.users.get_users()
```

There is also another endpoint where I can edit a users specific API token using a `PUT` to the `/access/users/{userid}/token/{tokenid}` endpoint. Since there are not many resources under the user path, we've opted to fit them all in the single file instead of creating more files, for example instead of doing this:

```python

api.access.users.tokens.get_user_token(user_id="root@pam", token_id="test_token")

# I can do this instead
api.access.users.get_user_token(user_id="root@pam", token_id="test_token")
```

!!! note
    Remember, every class and method must be documented with a docstring and should always have type annotations/hints to improve the developer experience.

# Test Infrastructure