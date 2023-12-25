from typing import Optional

from pyproxmox_ve.models.base import ProxmoxBaseModel
from pyproxmox_ve.models.enums import AccessACLEnum


class ACL(ProxmoxBaseModel):
    path: str
    roleid: str
    type: AccessACLEnum
    ugid: str
    propagate: Optional[bool] = 1


class ACLUpdate(ProxmoxBaseModel):
    path: str
    roles: str
    delete: Optional[bool] = None
    groups: Optional[str] = None
    propagate: Optional[bool] = 1
    tokens: Optional[str] = None
    users: Optional[str] = None


class PasswordUpdate(ProxmoxBaseModel):
    password: str
    userid: str


class AuthenticationTicket(ProxmoxBaseModel):
    username: str
    password: str
    new_format: bool = None
    otp: str = None
    path: str = None
    privs: str = None
    realm: str = None
    tfa_challenge: str = None


class AuthenticationTicketResponse(ProxmoxBaseModel):
    username: str
    CSRFPrevisionToken: Optional[str] = None
    clustername: Optional[str] = None
    ticket: Optional[str] = None
