from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyproxmox_ve.api import ProxmoxVEAPI
    from pyproxmox_ve.models.pools import Pool


class PoolsAPI:
    def __init__(self, api: ProxmoxVEAPI) -> None:
        self.api = api

    async def get_pools(
        self, pool_id: str = None, type: str = None, **kwargs
    ) -> list[Pool | dict]:
        """Get all or a single pool.

        Args:
            pool_id:    Get a specific pool if present
            type:       qemu, lxc or storage
        """
        kwargs.update({"poolid": pool_id, "type": type})
        return await self.api.query(
            endpoint="/pools",
            method="GET",
            module_model=("pyproxmox_ve.models.pools", "Pool"),
            params=kwargs,
        )

    async def create_pool(self, pool_id: str, **kwargs) -> None:
        """Create a new resource pool.

        Args:
            pool_id:    Name of the pool
        """
        kwargs.update({"poolid": pool_id})
        return await self.api.create(
            endpoint="/pools",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.pools", "PoolCreate"),
        )

    async def update_pool(self, pool_id: str, **kwargs) -> None:
        """Update an existing resource pool.

        Args:
            pool_id:    Name of the pool
        """
        kwargs.update({"poolid": pool_id})
        return await self.api.update(
            endpoint="/pools",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.pools", "PoolUpdate"),
        )

    async def delete_pool(self, pool_id: str) -> None:
        """Delete an existing pool.

        Args:
            pool_id:    Name of the pool
        """
        return await self.api.delete(endpoint="/pools", params={"poolid": pool_id})
