import pytest_asyncio
from pytest import FixtureRequest

from pyproxmox_ve import ProxmoxVEAPI


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        dest="url",
        type=str,
        help="URL for ProxmoxVE API",
        default="http://127.0.0.1:8006",
    )
    parser.addoption(
        "--username",
        action="store",
        dest="username",
        type=str,
        help="API Username for ProxmoxVE API",
        default="root@pam",
    )
    parser.addoption(
        "--password",
        action="store",
        dest="password",
        type=str,
        help="Password for ProxmoxVE API when using Cookie Auth",
        default="proxmox123!",
    )
    parser.addoption(
        "--api-token-id",
        action="store",
        dest="api_token_id",
        type=str,
        help="API Token ID for ProxmoxVE API",
        default="test_token",
    )
    parser.addoption(
        "--api-token",
        action="store",
        dest="api_token",
        type=str,
        help="API Token for ProxmoxVE API",
        default="0d06e68c-930c-4d5f-bad5-9c18de0d85bf",
    )
    parser.addoption(
        "--use-cookie-auth",
        action="store_true",
        dest="use_cookie_auth",
        help="Uses Cookie auth instead of API key",
        default=False,
    )


@pytest_asyncio.fixture
async def proxmox(request: FixtureRequest) -> ProxmoxVEAPI:
    """Creates a base ProxmoxVEAPI object to be used during every test."""
    url = request.config.getoption("url")
    username = request.config.getoption("username")
    password = request.config.getoption("password")
    api_token_id = request.config.getoption("api_token_id")
    api_token = request.config.getoption("api_token")
    use_cookie_auth = request.config.getoption("use_cookie_auth")

    api = ProxmoxVEAPI(
        url=url,
        username=username,
        password=password,
        api_token_id=api_token_id,
        api_token=api_token if not use_cookie_auth else None,
        use_pydantic=True,
        raise_exceptions=True,  # Always explicitly raise custom exceptions during pytest
    )

    if use_cookie_auth:
        await api.get_ticket()

    yield api

    await api.close()
