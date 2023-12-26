from typing import Any, Dict, Optional

from pyproxmox_ve.models.base import ProxmoxBaseModel
from pyproxmox_ve.models.enums import TFAEnum


class UserTokenBase(ProxmoxBaseModel):
    expire: Optional[int] = 0
    privsep: Optional[int] = 1


class UserToken(UserTokenBase):
    comment: Optional[str] = None
    tokenid: Optional[str] = None


class UserTokenResponse(ProxmoxBaseModel):
    full_tokenid: str
    info: dict
    value: str


class UserBase(ProxmoxBaseModel):
    userid: Optional[str] = None
    comment: Optional[str] = None
    email: Optional[str] = None
    enable: Optional[int] = None
    expire: Optional[int] = 0
    firstname: Optional[str] = None
    groups: Optional[list[str] | str] = None
    keys: Optional[list[str] | str] = None
    lastname: Optional[str] = None


class UserCreate(UserBase):
    userid: str
    password: Optional[str] = None


class UserUpdate(UserBase):
    append: Optional[int] = None


class UserUniqueToken(UserTokenBase):
    pass


class User(UserBase):
    realm_type: Optional[str] = None
    tfa_locked_until: Optional[int] = None
    tokens: Optional[list[UserToken]] = []
    totp_locked: Optional[int] = None


class UserWithTokenDict(UserBase):
    tokens: Optional[Dict[str, UserUniqueToken]] = None


class UserTFAType(ProxmoxBaseModel):
    realm: Optional[TFAEnum] = None
    types: Optional[list[Any]] = None
    user: TFAEnum
