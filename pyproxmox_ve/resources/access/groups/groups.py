from __future__ import annotations

from typing import TYPE_CHECKING

from pyproxmox_ve.resources.base import BaseResourceAPI

if TYPE_CHECKING:
    from pyproxmox_ve.models.groups import Group


class AccessGroupsAPI(BaseResourceAPI):
    async def get_groups(self) -> list[Group | dict]:
        """Get all groups."""
        return await self.api.query(
            endpoint="/access/groups",
            method="GET",
            module_model=("pyproxmox_ve.models.groups", "Group"),
        )

    async def get_group(self, group_id: str) -> Group | dict:
        """Get a specific Group.

        Args:
            group_id:       Name of the Group
        """
        return await self.api.query(
            endpoint=f"/access/groups/{group_id}",
            method="GET",
            module_model=("pyproxmox_ve.models.groups", "Group"),
        )

    async def create_group(self, group_id: str, **kwargs) -> None:
        """Create a group.

        Args:
            group_id:       Name of the group
        """
        kwargs.update({"groupid": group_id})
        return await self.api.create(
            endpoint="/access/groups",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.groups", "GroupCreate"),
        )

    async def update_group(self, group_id: str, **kwargs) -> None:
        """Update an existing group.

        Args:
            group_id:       Name of the group
        """
        kwargs.update({"groupid": group_id})
        return await self.api.update(
            endpoint=f"/access/groups/{group_id}",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.groups", "GroupUpdate"),
        )

    async def delete_group(self, group_id: str) -> None:
        """Delete a group.

        Args:
            group_id:       Name of the group
        """
        return await self.api.delete(endpoint=f"/access/groups/{group_id}")
