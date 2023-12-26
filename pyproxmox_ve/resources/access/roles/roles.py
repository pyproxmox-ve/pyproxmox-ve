from __future__ import annotations

from typing import TYPE_CHECKING

from pyproxmox_ve.resources.base import BaseResourceAPI

if TYPE_CHECKING:
    from pyproxmox_ve.models.roles import Permissions, Role


class AccessRolesAPI(BaseResourceAPI):
    async def get_roles(self) -> list[Role | dict]:
        """Get all roles."""
        return await self.api.query(
            endpoint="/access/roles",
            method="GET",
            module_model=("pyproxmox_ve.models.roles", "Role"),
        )

    async def get_role(self, role_id: str) -> Permissions | dict:
        """Get a specific role.

        Args:
            role_id:    Name of the role
        """
        return await self.api.query(
            endpoint=f"/access/roles/{role_id}",
            method="GET",
            module_model=("pyproxmox_ve.models.roles", "Permissions"),
        )

    async def create_role(self, role_id: str, **kwargs) -> None:
        """Create a new role.

        Args:
            role_id:    Name of the role
        """
        kwargs.update({"roleid": role_id})
        return await self.api.create(
            endpoint="/access/roles",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.roles", "RoleCreate"),
        )

    async def update_role(self, role_id: str, **kwargs) -> None:
        """Update an existing role.

        Args:
            role_id:    Name of the role
        """
        kwargs.update({"roleid": role_id})
        return await self.api.update(
            endpoint=f"/access/roles/{role_id}",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.roles", "RoleUpdate"),
        )

    async def delete_role(self, role_id: str) -> None:
        """Delete an existing role.

        Args:
            role_id:    Name of the role
        """
        return await self.api.delete(endpoint=f"/access/roles/{role_id}")
