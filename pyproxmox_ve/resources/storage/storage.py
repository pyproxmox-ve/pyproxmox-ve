from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyproxmox_ve.api import ProxmoxVEAPI
    from pyproxmox_ve.models.storage import (
        Storage,
        StorageCreateResponse,
        StorageUpdateResponse,
    )


class StorageAPI:
    def __init__(self, api: ProxmoxVEAPI) -> None:
        self.api = api

    async def get_storages(self, **kwargs) -> list[dict]:
        """Get all storages."""
        return await self.api.query(
            endpoint="/storage",
            method="GET",
            params=kwargs,
        )

    async def create_storage(
        self, storage: str, type: str, **kwargs
    ) -> StorageCreateResponse | dict:
        """Create a new storage.

        Args:
            storage:    Storage identifier
            type:       Storage Type (eg. cephfs, dir, flusterfs, iscsi, lvm, nfs, etc..)
        """
        kwargs.update({"storage": storage, "type": type})
        return await self.api.create(
            endpoint="/storage",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.storage", "StorageCreate"),
            data_key="data",
            validate_response=True,
            response_model=("pyproxmox_ve.models.storage", "StorageCreateResponse"),
        )

    async def get_storage(self, storage: str) -> Storage | dict:
        """Get a specific storage.

        Args:
            storage:    Name of the storage
        """
        return await self.api.query(
            endpoint=f"/storage/{storage}",
            method="GET",
            module_model=("pyproxmox_ve.models.storage", "Storage"),
        )

    async def update_storage(
        self, storage: str, **kwargs
    ) -> StorageUpdateResponse | dict:
        """Update a specific storage.

        Note that this API endpoint does return the original object and not the
        updated object, therefore its recommended to run `get_storage` again if you
        need the updated information.

        Args:
            storage:    Name of the storage
        """
        kwargs.update({"storage": storage})
        return await self.api.update(
            endpoint=f"/storage/{storage}",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.storage", "StorageUpdate"),
            data_key="data",
            validate_response=True,
            response_model=("pyproxmox_ve.models.storage", "StorageUpdateResponse"),
        )

    async def delete_storage(self, storage: str) -> None:
        """Delete a specific storage.

        Args:
            storage:    Name of the storage
        """
        return await self.api.delete(endpoint=f"/storage/{storage}")
