# Contributing

When contributing to this repository, please first discuss the change you wish to make via discussions or via an informal method such as Discord.

Please note we have a code of conduct and it's simply 1 rule, don't be a dickhead.

Any feedback for the contributing workflows whether it be the branch structure, coding style, tests or general feedback of the implementation is welcome and should be brought up either as a discussion/issue or informally over a chat like Discord. Do not use emails.

# Branch Structure

Keeping it simple, no one is allowed to push directly into the main branch unless you are an administrator and its a last resort, however its strongly advised never to push directly to main to perform a hotfix due to the workflow of creating a release from the main branch to kick off the PyPI package upload.

The "staging" branch is simply called `dev`. This branch should incorprate all feature branches and run CI/CD to perform all relevant tests before a merge request is created into `main`.

Typically, you should raise an issue (or create an issue from a project task) and assign a branch to the relevant issue, issues are used to track progress and then will be used to merge into the `dev` branch. Always ensure before you create a merge request into `dev`, that your feature branch is up to date with the latest dev branch to avoid merge conflicts.

# Coding Style

- Minimum version of Python to use during development and testing must be 3.10.12
- Always use [f-strings](https://docs.python.org/3/tutorial/inputoutput.html) when possible as they are far more superior than `%` and `.format()` in most cases.
- Always write tests for any new functions/API calls implemented or changed (if the logic has changed)
- All functions should follow the typical API documentation format, more on this can be found here `to-do`
- List comprehensions should always be used where possible unless the code is too ugly and readable, that is for you and the reviewer to agree with :-)

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

Remember, every class and method is documented with a docstring and should always have type annotations/hints to improve the developer experience.
![Alt text]()

# Test Infrastructure
to-do

# Pull Request Process
to-do