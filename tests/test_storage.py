import pytest

from pyproxmox_ve import ProxmoxVEAPI
from pyproxmox_ve.exceptions import ProxmoxAPIResponseError


@pytest.mark.asyncio
class TestStorage:
    async def test_get_storages(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.storage.get_storages()
        assert response
        assert len(response) > 0

    async def test_get_storage(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.storage.get_storage(storage="local")
        assert response
        assert response.path == "/var/lib/vz"

    async def test_create_storage(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.storage.create_storage(
            storage="pytest-storage", type="lvm", vgname="pve"
        )

        assert response
        assert response.storage == "pytest-storage"
        assert response.type == "lvm"

    async def test_update_storage(self, proxmox: ProxmoxVEAPI):
        await proxmox.storage.update_storage(storage="pytest-storage", content="images")

        response = await proxmox.storage.get_storage(storage="pytest-storage")
        assert response
        assert response.storage == "pytest-storage"
        assert response.content == "images"

    async def test_delete_storage(self, proxmox: ProxmoxVEAPI):
        await proxmox.storage.delete_storage(storage="pytest-storage")

        with pytest.raises(ProxmoxAPIResponseError) as exc_info:
            await proxmox.storage.get_storage(storage="pytest-storage")

        error = exc_info.value
        assert error.status == 500
        assert "does not exist" in error.reason
