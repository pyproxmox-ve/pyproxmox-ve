from __future__ import annotations
from typing_extensions import TYPE_CHECKING

from pyproxmox_ve.resources.base import BaseResourceAPI

if TYPE_CHECKING:
    from pyproxmox_ve.models.user import User


class AccessUsersAPI(BaseResourceAPI):
    async def get_users(
        self, enabled: bool = None, full: bool = False
    ) -> list[dict | User]:
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

    async def get_user(self, username: str, realm: str) -> User | None:
        """Gets a User.

        Args:
            username:       Username of the User
            realm:          Authentication Realm of the User
        """
        userid = f"{username}@{realm}"
        user = await self.api.query(
            module_model=("pyproxmox_ve.models.user", "User"),
            method="GET",
            endpoint=f"/access/users/{userid}",
        )

        return user

    async def create_user(self, username: str, realm: str, **kwargs) -> None:
        """Creates a User.

        Args:
            user_id:    User ID in the format of <username>@<realm>
        """
        kwargs.update({"userid": f"{username}@{realm}"})
        return await self.api.create(
            module_model=("pyproxmox_ve.models.user", "UserCreate"),
            endpoint="/access/users",
            obj_in=kwargs,
        )
