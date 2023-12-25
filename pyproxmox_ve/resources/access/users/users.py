from __future__ import annotations
from typing_extensions import TYPE_CHECKING

from pyproxmox_ve.resources.base import BaseResourceAPI

if TYPE_CHECKING:
    from pyproxmox_ve.models.user import (
        User,
        UserToken,
        UserTokenResponse,
        UserWithTokenDict,
        UserTFAType,
    )


class AccessUsersAPI(BaseResourceAPI):
    async def get_users(
        self, enabled: bool = None, full: bool = False
    ) -> list[User]:
        """Gathers all Users.

        Args:
            enabled:        Optional filter for enable property.
            full:           Include group and token information.
        """
        return await self.api.query(
            module_model=("pyproxmox_ve.models.user", "User"),
            method="GET",
            endpoint="/access/users",
            params=self.api._build_params(enabled=enabled, full=full),
        )

    async def get_user(self, user_id: str) -> UserWithTokenDict | None:
        """Gets a User.

        Args:
            user_id:    User ID in the format of <username>@<realm>
        """
        user = await self.api.query(
            module_model=("pyproxmox_ve.models.user", "UserWithTokenDict"),
            method="GET",
            endpoint=f"/access/users/{user_id}",
        )

        return user

    async def create_user(self, user_id: str, **kwargs) -> None:
        """Creates a User.

        Args:
            user_id:    User ID in the format of <username>@<realm>
        """
        kwargs.update({"userid": user_id})
        return await self.api.create(
            module_model=("pyproxmox_ve.models.user", "UserCreate"),
            endpoint="/access/users",
            obj_in=kwargs,
        )

    async def update_user(self, user_id: str, **kwargs) -> None:
        """Updates a User.

        Args:
            user_id:        User ID in the format of <username>@<realm>
        """
        return await self.api.update(
            module_model=("pyproxmox_ve.models.user", "UserUpdate"),
            endpoint=f"/access/users/{user_id}",
            obj_in=kwargs,
        )

    async def delete_user(self, user_id: str) -> None:
        """Deletes a User.

        Args:
            user_id:        User ID in the format of <username>@<realm>
        """
        return await self.api.delete(endpoint=f"/access/users/{user_id}")

    async def get_user_tokens(self, user_id: str) -> list[UserToken | dict]:
        """Gets all user API tokens.

        Args:
            user_id:        User ID in the format of <username>@<realm>
        """
        return await self.api.query(
            module_model=("pyproxmox_ve.models.user", "UserToken"),
            method="GET",
            endpoint=f"/access/users/{user_id}/token",
        )

    async def get_user_token(
        self, user_id: str, token_id: str
    ) -> UserToken | dict:
        """Get a specific users API token.

        Args:
            user_id:        User ID in the format of <username>@<realm>
            token_id:       Token ID
        """
        return await self.api.query(
            module_model=("pyproxmox_ve.models.user", "UserToken"),
            method="GET",
            endpoint=f"/access/users/{user_id}/token/{token_id}",
        )

    async def create_user_token(
        self, user_id: str, token_id: str, **kwargs
    ) -> UserTokenResponse | dict:
        """Create an API token for a specific user.

        Args:
            user_id:        User ID in the format of <username>@<realm>
            token_id:       Token ID
        """
        return await self.api.create(
            module_model=("pyproxmox_ve.models.user", "UserToken"),
            endpoint=f"/access/users/{user_id}/token/{token_id}",
            obj_in=kwargs,
            data_key="data",
            validate_response=True,
            response_model=("pyproxmox_ve.models.user", "UserTokenResponse"),
        )

    async def update_user_token(
        self, user_id: str, token_id: str, **kwargs
    ) -> UserToken:
        """Get a specific users API token.

        Args:
            user_id:        User ID in the format of <username>@<realm>
            token_id:       Token ID
        """
        return await self.api.update(
            module_model=("pyproxmox_ve.models.user", "UserToken"),
            endpoint=f"/access/users/{user_id}/token/{token_id}",
            obj_in=kwargs,
            validate_response=True,
        )

    async def delete_user_token(self, user_id: str, token_id: str) -> None:
        """Deletes a specific users API token.

        Args:
            user_id:        User ID in the format of <username>@<realm>
            token_id:       Token ID
        """
        return await self.api.delete(
            endpoint=f"/access/users/{user_id}/token/{token_id}"
        )

    async def get_user_tfa_types(self, user_id: str) -> UserTFAType | dict:
        """Get a specific users TFA types.

        Args:
            user_id:        User ID in the format of <username>@<realm>
        """
        return await self.api.query(
            module_model=("pyproxmox_ve.models.user", "UserTFAType"),
            method="GET",
            endpoint=f"/access/users/{user_id}/tfa",
        )

    async def unlock_user_tfa(self, user_id: str) -> bool:
        """Unlock a specific users TFA.

        Args:
            user_id:        User ID in the format of <username>@<realm>
        """
        return await self.api.update(
            endpoint=f"/access/users/{user_id}/unlock-tfa"
        )
