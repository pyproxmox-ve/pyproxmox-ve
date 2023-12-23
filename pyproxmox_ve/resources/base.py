from typing_extensions import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from pyproxmox_ve.api import ProxmoxVEAPI


class BaseResourceAPI:
    def __init__(self, api: "ProxmoxVEAPI", model: Any = None) -> None:
        self.api = api
        self.model = model