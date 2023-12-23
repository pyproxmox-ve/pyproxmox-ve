from typing_extensions import TYPE_CHECKING
from pyproxmox_ve.models.version import Version

if TYPE_CHECKING:
    from pyproxmox_ve.api import ProxmoxVEAPI


class VersionAPI:
    def __init__(self, api: "ProxmoxVEAPI") -> None:
        self.api = api

    async def get_version(self) -> Version:
        return await self.api.query_with_model(
            model=Version, method="GET", endpoint=f"/version", data_key="data"
        )
