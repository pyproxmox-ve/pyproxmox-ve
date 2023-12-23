from typing import Optional, Any
from typing_extensions import Annotated
from pydantic import Field
from pyproxmox_ve.models.base import ProxmoxBaseModel
from pyproxmox_ve.models.enums import ConsoleEnum


class UserToken(ProxmoxBaseModel):
    comment: Optional[str] = None
    expire: Optional[int] = 0
    privsep: Optional[bool] = True
    tokenid: Optional[Annotated[str, Field(pattern="(^:[A-Za-z][A-Za-z0-9\\.\\-_]+)")]]


class User(ProxmoxBaseModel):
    userid: str
    comment: Optional[str] = None
    email: Optional[str] = None
    enable: Optional[bool] = None
    expire: Optional[int] = 0
    firstname: Optional[str] = None
    groups: Optional[str] = None
    keys: Optional[list[str]] = []
    lastname: Optional[str] = None
    realm_type: Optional[str] = None
    tfa_locked_until: Optional[int] = None
    tokens: Optional[list[dict]] = []
    totp_locked: Optional[bool] = None
