from typing import Optional

from pydantic import Field

from pyproxmox_ve.models.base import ProxmoxBaseModel
from pyproxmox_ve.models.enums import TFAEnum


class TFA(ProxmoxBaseModel):
    entries: list[dict]
    userid: str
    tfa_locked_until: Optional[int] = Field(None, alias="tfa-locked-until")
    totp_locked: Optional[int] = Field(None, alias="totp-locked")


class TFAEntry(ProxmoxBaseModel):
    created: int
    description: Optional[str] = None
    id: str
    type: TFAEnum
    enable: Optional[bool] = 1


class TFAUserCreate(ProxmoxBaseModel):
    userid: str
    type: TFAEnum
    challenge: Optional[str] = None
    description: Optional[str] = None
    password: Optional[str] = None
    totp: Optional[str] = None
    value: Optional[str] = None


class TFAUserResponse(ProxmoxBaseModel):
    id: str
    challenge: Optional[str] = None
    recovery: Optional[list[str]] = None


class TFAUserEntryUpdate(ProxmoxBaseModel):
    id: str
    userid: str
    description: Optional[str] = None
    enable: Optional[int] = None
    password: Optional[str] = None
