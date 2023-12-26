import pytest

from pyproxmox_ve import ProxmoxVEAPI


@pytest.mark.asyncio
@pytest.mark.order(
    before="test_users.py::TestAccessUsers::test_delete_user",
    after="test_users_token.py::TestAccessUsersToken::test_create_user_token",
)
class TestAccessDomains:
    async def test_get_domains(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.access.domains.get_domains()
        assert response
        assert len(response) > 0

    """
    async def test_create_domain(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.access.domains.create_domain(
            realm="pytest-ldap",
            realm_type="ldap",
            server="192.0.2.100",
            base_domain_name="pytest",
            user_attr="uid",
            mode="ldap",
        )
        print(response)
    """
