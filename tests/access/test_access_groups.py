import pytest

from pyproxmox_ve import ProxmoxVEAPI
from pyproxmox_ve.exceptions import ProxmoxAPIResponseError


@pytest.mark.asyncio
@pytest.mark.order(
    after="test_access_users.py::TestAccessUsers::test_create_user",
)
class TestAccessGroups:
    async def test_get_groups_not_exist(self, proxmox: ProxmoxVEAPI):
        await proxmox.access.groups.get_groups()

    async def test_get_group_not_exist(self, proxmox: ProxmoxVEAPI):
        with pytest.raises(ProxmoxAPIResponseError) as exc_info:
            await proxmox.access.groups.get_group(group_id="pytest-group")

        error = exc_info.value
        assert error.status == 500
        assert "does not exist" in error.reason

    async def test_create_group(self, proxmox: ProxmoxVEAPI):
        await proxmox.access.groups.create_group(group_id="pytest-group")

        group_exist = await proxmox.access.groups.get_group(group_id="pytest-group")
        assert group_exist

    async def test_create_group_exist(self, proxmox: ProxmoxVEAPI):
        with pytest.raises(ProxmoxAPIResponseError) as exc_info:
            await proxmox.access.groups.create_group(group_id="pytest-group")

        error = exc_info.value
        assert error.status == 500
        assert "already exists" in error.reason

    async def test_update_group(self, proxmox: ProxmoxVEAPI):
        await proxmox.access.groups.update_group(
            group_id="pytest-group", comment="pytest-change-comment"
        )

        group = await proxmox.access.groups.get_group(group_id="pytest-group")
        assert group.comment == "pytest-change-comment"

    @pytest.mark.order(
        after="test_access_users.py::TestAccessUsers::test_delete_user",
    )
    async def test_delete_group(self, proxmox: ProxmoxVEAPI):
        await proxmox.access.groups.delete_group(group_id="pytest-group")
