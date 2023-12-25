# Basic Usage

After installing the module, `pyproxmox-ve` is now ready to be used.



1. Import the `ProxmoxVEAPI` which is the basis of all API interaction.

    ```python
    from pyproxmox_ve import ProxmoxVEAPI
    ```

2. Initalise the API object with your API credentials

    ```python

    api = ProxmoxVEAPI(
        url="https://192.0.2.100:8006",
        username="root",
        realm="pam",
        api_token_id="mytoken",
        api_token="abcd1234-efgh5678",
        use_pydantic=True # Set to False if you didn't `pip install pyproxmox-ve[pydantic]`
    )
    ```

As a test, we can try to communicate with the API and list the version running:

```python
version = await api.version.get_version()

print(version)
> version='8.1.3' repoid='b46aac3b42da5d15' release='8.1' console=None
```

Currently, all responses that return a status code of 400 or higher will raise an [aiohttp ClientResponseError](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponseError). For example, if my user authentication is wrong in the example above, I receive this error:

```python
# Bad Realm Example
> aiohttp.client_exceptions.ClientResponseError: 401, message="no such user ('root@badrealm')", url=URL('https://192.0.2.100:8006/api2/json/version')

# Bad Token Example
> aiohttp.client_exceptions.ClientResponseError: 401, message='invalid token value!', url=URL('https://192.0.2.100:8006/api2/json/version')
```
