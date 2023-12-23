from pyproxmox_ve import ProxmoxVEAPI
import pytest


@pytest.mark.asyncio
async def test_version_endpoint(proxmox: ProxmoxVEAPI):
    response = await proxmox.version.get_version()
    print(response)
