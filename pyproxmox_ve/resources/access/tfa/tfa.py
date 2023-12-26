from __future__ import annotations

from typing import TYPE_CHECKING

from pyproxmox_ve.resources.base import BaseResourceAPI

if TYPE_CHECKING:
    from pyproxmox_ve.models.tfa import TFA, TFAEntry, TFAUserResponse


class AccessTFAAPI(BaseResourceAPI):
    async def get_tfa_all(self) -> list[TFA | dict]:
        """Get all TFA configuration."""
        return await self.api.query(
            endpoint="/access/tfa",
            method="GET",
            module_model=("pyproxmox_ve.models.tfa", "TFA"),
        )

    async def get_tfa_user(self, user_id: str) -> TFAEntry | dict:
        """Get a specific TFA configuration for a certain user.

        Args:
            user_id:    Name of the User
        """
        return await self.api.query(
            endpoint=f"/access/tfa/{user_id}",
            method="GET",
            module_model=("pyproxmox_ve.models.tfa", "TFAEntry"),
        )

    async def create_tfa_user(
        self, user_id: str, type: str, **kwargs
    ) -> TFAUserResponse | dict:
        """Create a TFA entry for a specific user.

        Args:
            user_id:    Name of the User
            type:       TFA Type (eg. totp, u2f, webauthn, etc..)
        """
        kwargs.update({"userid": user_id, "type": type})
        return await self.api.create(
            endpoint=f"/access/tfa/{user_id}",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.tfa", "TFAUserCreate"),
            data_key="data",
            validate_response=True,
            response_model=("pyproxmox_ve.models.tfa", "TFAUserResponse"),
        )

    async def get_tfa_user_entry(self, user_id: str, tfa_id: str) -> TFAEntry | dict:
        """Get a specific TFA Entry for a specific user.

        Args:
            user_id:    Name of the user
            tfa_id:     Name of the TFA entry
        """
        return await self.api.query(
            endpoint=f"/access/tfa/{user_id}/{tfa_id}",
            method="GET",
            module_model=("pyproxmox_ve.models.tfa", "TFAEntry"),
        )

    async def update_tfa_user_entry(self, user_id: str, tfa_id: str, **kwargs) -> None:
        """Update a specific TFA entry for a specific user.

        Args:
            user_id:    Name of the user
            tfa_id:     Name of the TFA entry
        """
        kwargs.update({"userid": user_id, "id": tfa_id})
        return await self.api.update(
            endpoint=f"/access/tfa/{user_id}/{tfa_id}",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.tfa", "TFAUserEntryUpdate"),
        )

    async def delete_tfa_user_entry(self, user_id: str, tfa_id: str) -> None:
        """Delete a specific TFA entry for a specific user.

        Args:
            user_id:    Name of the user
            tfa_id:     Name of the TFA entry
        """
        return await self.api.delete(endpoint=f"/access/tfa/{user_id}/{tfa_id}")
