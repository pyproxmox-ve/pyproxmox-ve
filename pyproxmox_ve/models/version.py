from pyproxmox_ve.models.base import ProxmoxBaseModel
from pyproxmox_ve.models.enums import ConsoleEnum


class Version(ProxmoxBaseModel):
    version: str
    repoid: str
    release: str
    console: ConsoleEnum | None = None
