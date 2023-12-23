from typing_extensions import TYPE_CHECKING
from pyproxmox_ve.resources.access.users.users import AccessUsersAPI

if TYPE_CHECKING:
    from pyproxmox_ve.api import ProxmoxVEAPI


class AccessAPI:
    def __init__(self, api: "ProxmoxVEAPI") -> None:
        self.api = api
        self.users = AccessUsersAPI(api)
