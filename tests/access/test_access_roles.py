import pytest

from pyproxmox_ve import ProxmoxVEAPI
from pyproxmox_ve.exceptions import ProxmoxAPIResponseError


@pytest.mark.asyncio
class TestAccessRoles:
    async def test_get_roles(self, proxmox: ProxmoxVEAPI):
        roles = await proxmox.access.roles.get_roles()
        assert roles
        assert len(roles) > 0

    async def test_get_role_not_exist(self, proxmox: ProxmoxVEAPI):
        with pytest.raises(ProxmoxAPIResponseError) as exc_info:
            await proxmox.access.roles.get_role(role_id="pytest-role")

        error = exc_info.value
        assert error.status == 500
        assert "does not exist" in error.reason

    async def test_get_role(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.access.roles.get_role(role_id="Administrator")
        assert response
        assert response.datastore_allocate
        assert response.vm_clone
        assert response.vm_config_cpu
        assert response.mapping_use
        assert response.pool_allocate

    async def test_create_role(self, proxmox: ProxmoxVEAPI):
        await proxmox.access.roles.create_role(
            role_id="pytest-role", privs="Datastore.Allocate"
        )

    async def test_update_role(self, proxmox: ProxmoxVEAPI):
        await proxmox.access.roles.update_role(
            role_id="pytest-role", append=True, privs="VM.Allocate"
        )

        existing_role = await proxmox.access.roles.get_role(role_id="pytest-role")
        assert existing_role.datastore_allocate
        assert existing_role.vm_allocate

    async def test_delete_role(self, proxmox: ProxmoxVEAPI):
        await proxmox.access.roles.delete_role(role_id="pytest-role")
