import pytest

from pyproxmox_ve import ProxmoxVEAPI
from pyproxmox_ve.exceptions import ProxmoxAPIResponseError


@pytest.mark.asyncio
@pytest.mark.order(
    after="test_access_users.py::TestAccessUsers::test_create_user",
)
class TestAccessTFA:
    async def test_get_tfa_all_not_exist(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.access.tfa.get_tfa_all()
        assert response is None

    async def test_get_tfa_user_not_exist(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.access.tfa.get_tfa_user(
            user_id="pyproxmox-ve-pytest@pam"
        )
        assert response is None

    async def test_create_tfa_user(self, proxmox: ProxmoxVEAPI):
        if proxmox.api_token:
            pytest.skip("API Auth can not be used to create TFA entries")

        response = await proxmox.access.tfa.create_tfa_user(
            user_id="pyproxmox-ve-pytest@pam",
            type="recovery",
        )

        assert response.id
        assert response.recovery
        assert len(response.recovery) > 0

    async def test_get_tfa_user(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.access.tfa.get_tfa_user(
            user_id="pyproxmox-ve-pytest@pam"
        )

        if proxmox.api_token:
            assert response is None
            return

        assert response
        assert len(response) > 0

    async def test_get_tfa_user_entry(self, proxmox: ProxmoxVEAPI):
        if proxmox.api_token:
            with pytest.raises(ProxmoxAPIResponseError) as exc_info:
                await proxmox.access.tfa.get_tfa_user_entry(
                    user_id="pyproxmox-ve-pytest@pam", tfa_id="recovery"
                )

            error = exc_info.value
            assert error.status == 404
            return

        response = await proxmox.access.tfa.get_tfa_user_entry(
            user_id="pyproxmox-ve-pytest@pam", tfa_id="recovery"
        )
        assert response
        assert response.id == "recovery"
        assert response.type == "recovery"

    async def test_update_tfa_user_entry(self, proxmox: ProxmoxVEAPI):
        pytest.skip("TFA still needs to be worked on")
        await proxmox.access.tfa.update_tfa_user_entry(
            user_id="pyproxmox-ve-pytest@pam",
            tfa_id="recovery",
            description="pytest-tfa-description",
        )

        await proxmox.access.tfa.get_tfa_user_entry(
            user_id="pyproxmox-ve-pytest@pam", tfa_id="recovery"
        )

    async def test_delete_tfa_user_entry(self, proxmox: ProxmoxVEAPI):
        if proxmox.api_token:
            pytest.skip("API Auth can not be used to delete TFA entries")

        await proxmox.access.tfa.delete_tfa_user_entry(
            user_id="pyproxmox-ve-pytest@pam", tfa_id="recovery"
        )

        with pytest.raises(ProxmoxAPIResponseError) as exc_info:
            await proxmox.access.tfa.get_tfa_user_entry(
                user_id="pyproxmox-ve-pytest@pam", tfa_id="recovery"
            )

        error = exc_info.value
        assert error.status == 404
        assert "no such tfa entry" in error.reason.lower()
