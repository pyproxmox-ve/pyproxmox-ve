from typing import Optional

from pydantic import Field

from pyproxmox_ve.models.base import ProxmoxBaseModel
from pyproxmox_ve.models.enums import (
    AccessACLEnum,
    DomainTypeEnum,
    LDAPModeEnum,
    SSLVersionEnum,
    TFAEnum,
)


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
    csrf_token: Optional[str] = Field(None, alias="CSRFPreventionToken")
    clustername: Optional[str] = None
    ticket: Optional[str] = None


class Domain(ProxmoxBaseModel):
    realm: str
    type: str
    comment: Optional[str] = None
    tfa: Optional[TFAEnum] = None


class DomainCreate(ProxmoxBaseModel):
    realm: str
    type: DomainTypeEnum
    acr_values: Optional[str] = None
    autocreate: Optional[bool] = False
    base_dn: Optional[str] = None
    bind_dn: Optional[str] = None
    capath: Optional[str] = "/etc/ssl/certs"
    case_sensitive: Optional[bool] = True
    cert: Optional[str] = None
    certkey: Optional[str] = None
    check_connection: Optional[bool] = False
    client_id: Optional[str] = None
    client_key: Optional[str] = None
    comment: Optional[str] = None
    default: Optional[bool] = None
    domain: Optional[str] = None
    filter: Optional[str] = None
    group_classes: Optional[str] = "groupOfNames, group, univent..."
    group_dn: Optional[str] = None
    group_filter: Optional[str] = None
    group_name_attr: Optional[str] = None
    issuer_url: Optional[str] = None
    mode: Optional[LDAPModeEnum] = LDAPModeEnum.ldap
    password: Optional[str] = None
    port: Optional[int] = None
    prompt: Optional[str] = None
    scopes: Optional[str] = "email profile"
    secure: Optional[bool] = None
    server1: Optional[str] = None
    server2: Optional[str] = None
    sslversion: Optional[SSLVersionEnum] = None
    sync_defaults_options: Optional[str] = None
    sync_attributes: Optional[str] = None
    tfa: Optional[str] = None
    user_attr: Optional[str] = None
    user_classes: Optional[str] = None
    username_claim: Optional[str] = None
    verify: Optional[bool] = False
