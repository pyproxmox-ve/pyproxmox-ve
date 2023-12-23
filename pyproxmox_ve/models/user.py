from typing import Optional
from typing_extensions import Annotated
from pydantic import Field
from pyproxmox_ve.models.base import ProxmoxBaseModel


class UserToken(ProxmoxBaseModel):
    comment: Optional[str] = None
    expire: Optional[int] = 0
    privsep: Optional[bool] = True
    tokenid: Optional[Annotated[str, Field(pattern="(^:[A-Za-z][A-Za-z0-9\\.\\-_]+)")]]


class UserBase(ProxmoxBaseModel):
    userid: str
    comment: Optional[str] = None
    email: Optional[str] = None
    enable: Optional[bool] = None
    expire: Optional[int] = 0
    firstname: Optional[str] = None
    groups: Optional[str] = None
    keys: Optional[list[str]] = []
    lastname: Optional[str] = None


class UserCreate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    realm_type: Optional[str] = None
    tfa_locked_until: Optional[int] = None
    tokens: Optional[list[dict]] = []
    totp_locked: Optional[bool] = None
