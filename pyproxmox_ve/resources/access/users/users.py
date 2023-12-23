from typing_extensions import TYPE_CHECKING
from pyproxmox_ve.models.user import User

if TYPE_CHECKING:
    from pyproxmox_ve.api import ProxmoxVEAPI


class AccessUsersAPI:
    def __init__(self, api: "ProxmoxVEAPI") -> None:
        self.api = api

    async def get_users(self, enabled: bool = None, full: bool = False) -> list[User]:
        """Gathers all Users.

        Args:
            enabled:        Optional filter for enable property.
            full:           Include group and token information.
        """
        return await self.api.query_with_model(
            model=User,
            method="GET",
            endpoint="/access/users",
            params=self.api._build_params(enabled=enabled, full=full),
        )
