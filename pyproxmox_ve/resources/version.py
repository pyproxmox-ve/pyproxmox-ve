from __future__ import annotations

from typing import TYPE_CHECKING

from pyproxmox_ve.resources.base import BaseResourceAPI

if TYPE_CHECKING:
    from pyproxmox_ve.models.version import Version


class VersionAPI(BaseResourceAPI):
    async def get_version(self) -> Version | dict:
        return await self.api.query(
            module_model=("pyproxmox_ve.models.version", "Version"),
            method="GET",
            endpoint="/version",
            data_key="data",
        )
