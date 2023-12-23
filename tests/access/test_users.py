from pyproxmox_ve import ProxmoxVEAPI
import pytest


@pytest.mark.asyncio
async def test_access_users_all_endpoint(proxmox: ProxmoxVEAPI):
    response = await proxmox.access.users.get_users(enabled=True, full=True)
    print(response)
