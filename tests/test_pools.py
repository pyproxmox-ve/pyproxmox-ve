import pytest

from pyproxmox_ve import ProxmoxVEAPI
from pyproxmox_ve.exceptions import ProxmoxAPIResponseError


@pytest.mark.asyncio
class TestAccessPools:
    async def test_get_pools_not_exist(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.pools.get_pools()
        assert response is None

    async def test_create_pool(self, proxmox: ProxmoxVEAPI):
        await proxmox.pools.create_pool(pool_id="pytest-resource-pool")

    async def test_update_pool(self, proxmox: ProxmoxVEAPI):
        await proxmox.pools.update_pool(
            pool_id="pytest-resource-pool", comment="pytest-pool-comment-update"
        )

        response = await proxmox.pools.get_pools(pool_id="pytest-resource-pool")
        assert response
        assert len(response) == 1
        assert response[0].comment == "pytest-pool-comment-update"

    async def test_delete_pool(self, proxmox: ProxmoxVEAPI):
        await proxmox.pools.delete_pool(pool_id="pytest-resource-pool")

        with pytest.raises(ProxmoxAPIResponseError) as exc_info:
            await proxmox.pools.get_pools(pool_id="pytest-resource-pool")

        error = exc_info.value
        assert error.status == 500
        assert "does not exist" in error.reason
