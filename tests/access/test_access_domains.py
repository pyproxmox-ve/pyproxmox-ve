import pytest

from pyproxmox_ve import ProxmoxVEAPI
from pyproxmox_ve.exceptions import ProxmoxAPIResponseError


@pytest.mark.asyncio
@pytest.mark.order(
    before="test_access_users.py::TestAccessUsers::test_delete_user",
)
class TestAccessDomains:
    async def test_get_domains(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.access.domains.get_domains()
        assert response
        assert len(response) > 0

    async def test_create_domain(self, proxmox: ProxmoxVEAPI):
        await proxmox.access.domains.create_domain(
            realm="pytest-ldap",
            realm_type="ldap",
            server="192.0.2.100",
            base_domain_name="pytest",
            mode="ldap",
            server1="192.0.2.100",
            user_attr="uid",
            base_dn="CN=pyproxmox_ve,DC=pyproxmox_ve,DC=github,DC=io",
        )

    async def test_get_domain(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.access.domains.get_domain(realm="pytest-ldap")
        assert response
        assert response.type == "ldap"
        assert response.base_dn == "CN=pyproxmox_ve,DC=pyproxmox_ve,DC=github,DC=io"
        assert response.server1 == "192.0.2.100"
        assert response.user_attr == "uid"

    async def test_update_domain(self, proxmox: ProxmoxVEAPI):
        await proxmox.access.domains.update_domain(
            realm="pytest-ldap",
            user_attr="guid",
            group_filter="Test",
        )

        updated_domain = await proxmox.access.domains.get_domain(realm="pytest-ldap")
        assert updated_domain.user_attr == "guid"
        assert updated_domain.group_filter == "Test"

    async def test_sync_domain(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.access.domains.sync(
            realm="pytest-ldap", dry_run=True, scope="both"
        )
        assert response
        assert isinstance(response, str)

    async def test_delete_domain(self, proxmox: ProxmoxVEAPI):
        await proxmox.access.domains.delete_domain(realm="pytest-ldap")

        with pytest.raises(ProxmoxAPIResponseError) as exc_info:
            await proxmox.access.domains.get_domain(realm="pytest-ldap")

            error = exc_info.value
            assert error.status == 500
            assert "does not exist" in error.reason
