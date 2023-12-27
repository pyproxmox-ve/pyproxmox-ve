import pytest

from pyproxmox_ve import ProxmoxVEAPI


@pytest.mark.asyncio
class TestCluster:
    async def test_get_logs(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.get_logs(max_logs=10)
        assert response
        assert len(response) <= 10

    async def test_get_next_vm_id(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.get_next_vm_id()
        assert response
        assert isinstance(response, int)
        assert response >= 100

    async def test_update_options(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.update_options(description="pytest-cluster-description")

    async def test_get_options(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.get_options()
        assert response
        assert response.description == "pytest-cluster-description\n"

    async def test_get_resources(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.get_resources()
        assert response
        assert (
            len(response) > 1
        )  # Default installation should always have local-lvm and local storage

    async def test_get_status(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.get_status()
        assert response

    async def test_get_tasks(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.get_tasks()
        assert response
