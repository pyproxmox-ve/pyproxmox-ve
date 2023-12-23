import pytest
from aiohttp import ClientResponseError

from pyproxmox_ve import ProxmoxVEAPI


@pytest.mark.asyncio
async def test_access_users_get_users(proxmox: ProxmoxVEAPI):
    response = await proxmox.access.users.get_users(enabled=True, full=True)
    assert isinstance(response, list)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_access_users_get_user_not_exist(proxmox: ProxmoxVEAPI):
    with pytest.raises(ClientResponseError) as exc_info:
        await proxmox.access.users.get_user(username="pyproxmox-ve-pytest", realm="pam")

    error = exc_info.value
    assert error.status == 500
    assert "no such user" in error.message


@pytest.mark.asyncio
async def test_access_users_create_user(proxmox: ProxmoxVEAPI):
    response = await proxmox.access.users.create_user(
        username="pyproxmox-ve-pytest", realm="pam"
    )
    assert response
    assert response.get("data") is None


@pytest.mark.asyncio
async def test_access_users_create_user_exist(proxmox: ProxmoxVEAPI):
    with pytest.raises(ClientResponseError) as exc_info:
        await proxmox.access.users.create_user(
            username="pyproxmox-ve-pytest", realm="pam"
        )

    error = exc_info.value
    assert error.status == 500
    assert "create user failed" in error.message
