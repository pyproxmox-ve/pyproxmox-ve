import pytest
from aiohttp import ClientResponseError

from pyproxmox_ve import ProxmoxVEAPI


@pytest.mark.asyncio
@pytest.mark.order(
    before="test_users.py::TestAccessUsers::test_delete_user",
    after="test_users_token.py::TestAccessUsersToken::test_create_user_token",
)
class TestAccess:
    async def test_update_acls(self, proxmox: ProxmoxVEAPI):
        await proxmox.access.update_acl(
            path="/vms", roles="Administrator", tokens="pyproxmox-ve-pytest@pam!pytest"
        )
        acls = await proxmox.access.get_acls()

        acl_found = False
        for acl in acls:
            if (
                acl.path == "/vms"
                and acl.roleid == "Administrator"
                and acl.type == "token"
            ):
                acl_found = True

        assert acl_found

    async def test_get_acls(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.access.get_acls()
        assert response
        assert len(response) > 0

    async def test_update_password(self, proxmox: ProxmoxVEAPI):
        # This endpoint is not available for API tokens.
        with pytest.raises(ClientResponseError) as exc_info:
            await proxmox.access.update_password(
                user_id="pyproxmox-ve-pytest@pam", password="fakepassword123!"
            )

            error = exc_info.value
            assert error.status == 403
            assert "need proper ticket" in error.message

    async def test_get_permissions(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.access.get_permissions(path="/access")
        assert response
        assert response.get("/access")

    async def test_get_ticket(self, proxmox: ProxmoxVEAPI):
        await proxmox.access.get_ticket()

    async def test_create_ticket(self, proxmox: ProxmoxVEAPI):
        # This endpoint is not available for API tokens.
        if proxmox.api_token:
            pytest.skip("API Auth can not be used to create a ticket")

        # TO DO

    async def test_create_ticket_renew(self, proxmox: ProxmoxVEAPI):
        if proxmox.api_token:
            pytest.skip(
                "Ticket renew only works with Cookie authentication, not API token authentication"
            )

        # TO DO
