from uuid import uuid4

import pytest

from pyproxmox_ve import ProxmoxVEAPI
from pyproxmox_ve.exceptions import ProxmoxAPIResponseError


@pytest.mark.asyncio
class TestAccessUsers:
    async def test_get_users(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.access.users.get_users(enabled=True, full=True)
        assert isinstance(response, list)
        assert len(response) > 0

    async def test_get_user_not_exist(self, proxmox: ProxmoxVEAPI):
        with pytest.raises(ProxmoxAPIResponseError) as exc_info:
            await proxmox.access.users.get_user(user_id="pyproxmox-ve-pytest@pam")

        error = exc_info.value
        assert error.status == 500
        assert "no such user" in error.reason

    async def test_create_user(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.access.users.create_user(
            user_id="pyproxmox-ve-pytest@pam",
            comment="comment",
            firstname="firstname",
            lastname="lastname",
        )
        assert response
        assert response.get("data") is None

    async def test_get_user(self, proxmox: ProxmoxVEAPI):
        user = await proxmox.access.users.get_user(user_id="pyproxmox-ve-pytest@pam")
        assert user.enable == 1
        assert user.expire == 0
        assert user.comment == "comment"
        assert user.firstname == "firstname"
        assert user.lastname == "lastname"

    async def test_create_user_exist(self, proxmox: ProxmoxVEAPI):
        with pytest.raises(ProxmoxAPIResponseError) as exc_info:
            await proxmox.access.users.create_user(user_id="pyproxmox-ve-pytest@pam")

        error = exc_info.value
        assert error.status == 500
        assert "create user failed" in error.reason

    async def test_update_user(self, proxmox: ProxmoxVEAPI):
        uuid = str(uuid4())
        await proxmox.access.users.update_user(
            user_id="pyproxmox-ve-pytest@pam", comment=uuid
        )

        user = await proxmox.access.users.get_user(user_id="pyproxmox-ve-pytest@pam")
        assert user
        assert user.comment == uuid

    async def test_delete_user_not_exist(self, proxmox: ProxmoxVEAPI):
        if proxmox.api_token:
            with pytest.raises(ProxmoxAPIResponseError) as exc_info:
                await proxmox.access.users.delete_user(
                    user_id="pyproxmox-ve-pytest-wrong@pam"
                )

            error = exc_info.value
            assert error.status == 500
            assert "no such user" in error.reason
        else:
            await proxmox.access.users.delete_user(
                user_id="pyproxmox-ve-pytest-wrong@pam"
            )

            # Cookie auth returns 200 for some odd reason...

    async def test_get_user_tfa_types(self, proxmox: ProxmoxVEAPI):
        tfa_types = await proxmox.access.users.get_user_tfa_types(
            user_id="pyproxmox-ve-pytest@pam"
        )
        assert (
            tfa_types is None
        )  # Enabling TFA type per user may be done via different API endpoint??

    async def test_unlock_user_tfa(self, proxmox: ProxmoxVEAPI):
        with pytest.raises(ProxmoxAPIResponseError) as exc_info:
            await proxmox.access.users.unlock_user_tfa(
                user_id="pyproxmox-ve-pytest-wrong@pam"
            )

        error = exc_info.value
        assert error.status == 500
        assert (
            "no such user" in error.reason
        )  # May need to enable TFA first via a different endpoint for user to be recognized??

    async def test_delete_user(self, proxmox: ProxmoxVEAPI):
        await proxmox.access.users.delete_user(user_id="pyproxmox-ve-pytest@pam")

        # Check user no longer exist
        with pytest.raises(ProxmoxAPIResponseError) as exc_info:
            await proxmox.access.users.get_user(user_id="pyproxmox-ve-pytest@pam")

        error = exc_info.value
        assert error.status == 500
        assert "no such user" in error.reason
