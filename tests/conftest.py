from pyproxmox_ve import ProxmoxVEAPI
from pytest import FixtureRequest
import pytest
import asyncio


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
        default="root",
    )
    parser.addoption(
        "--realm",
        action="store",
        dest="realm",
        type=str,
        help="API Realm for ProxmoxVE API",
        default="pam",
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


@pytest.fixture
def event_loop(request: FixtureRequest):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def proxmox(event_loop, request: FixtureRequest) -> ProxmoxVEAPI:
    """Creates a base ProxmoxVEAPI object to be used during every test"""
    url = request.config.getoption("url")
    username = request.config.getoption("username")
    realm = request.config.getoption("realm")
    api_token_id = request.config.getoption("api_token_id")
    api_token = request.config.getoption("api_token")

    async def _make_api_obj():
        return ProxmoxVEAPI(
            url=url,
            username=username,
            realm=realm,
            api_token_id=api_token_id,
            api_token=api_token,
        )

    api = event_loop.run_until_complete(_make_api_obj())
    yield api

    async def _finalize():
        await api.close()

    event_loop.run_until_complete(_finalize())
