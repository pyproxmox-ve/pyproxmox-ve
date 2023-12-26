from typing import Optional

from pydantic import Field

from pyproxmox_ve.models.base import ProxmoxBaseModel, ProxmoxBaseModelWithoutAlias
from pyproxmox_ve.models.enums import (
    AccessACLEnum,
    DomainTypeEnum,
    LDAPModeEnum,
    SSLVersionEnum,
    SyncScopeEnum,
    TFAEnum,
)


class ACL(ProxmoxBaseModel):
    path: str
    roleid: str
    type: AccessACLEnum
    ugid: str
    propagate: Optional[int] = 1


class ACLUpdate(ProxmoxBaseModel):
    path: str
    roles: str
    delete: Optional[int] = None
    groups: Optional[str] = None
    propagate: Optional[int] = 1
    tokens: Optional[str] = None
    users: Optional[str] = None


class PasswordUpdate(ProxmoxBaseModel):
    password: str
    userid: str


class AuthenticationTicket(ProxmoxBaseModel):
    username: str
    password: str
    new_format: int = None
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


class DomainBase(ProxmoxBaseModelWithoutAlias):
    realm: Optional[str] = None
    type: Optional[DomainTypeEnum] = None
    acr_values: Optional[str] = Field(None, serialization_alias="acr-values")
    autocreate: Optional[int] = None
    base_dn: Optional[str] = None
    bind_dn: Optional[str] = None
    capath: Optional[str] = "/etc/ssl/certs"
    case_sensitive: Optional[int] = Field(1, serialization_alias="case-sensitive")
    cert: Optional[str] = None
    certkey: Optional[str] = None
    check_connection: Optional[int] = Field(0, serialization_alias="check-connection")
    client_id: Optional[str] = None
    client_key: Optional[str] = None
    comment: Optional[str] = None
    default: Optional[int] = None
    domain: Optional[str] = None
    filter: Optional[str] = None
    group_classes: Optional[str] = None
    group_dn: Optional[str] = None
    group_filter: Optional[str] = None
    group_name_attr: Optional[str] = None
    issuer_url: Optional[str] = None
    mode: Optional[LDAPModeEnum] = LDAPModeEnum.ldap
    password: Optional[str] = None
    port: Optional[int] = None
    prompt: Optional[str] = None
    scopes: Optional[str] = None
    secure: Optional[int] = None
    server1: Optional[str] = None
    server2: Optional[str] = None
    sslversion: Optional[SSLVersionEnum] = None
    sync_defaults_options: Optional[str] = None
    sync_attributes: Optional[str] = None
    tfa: Optional[str] = None
    user_attr: Optional[str] = None
    user_classes: Optional[str] = None
    username_claim: Optional[str] = None
    verify: Optional[int] = 0


class Domain(DomainBase):
    type: str
    comment: Optional[str] = None
    tfa: Optional[TFAEnum] = None


class DomainCreate(DomainBase):
    realm: str
    type: DomainTypeEnum


class DomainUpdate(DomainBase):
    realm: str


class DomainSync(ProxmoxBaseModel):
    realm: str
    dry_run: Optional[int] = 0
    enable_new: Optional[int] = 1
    remove_vanished: Optional[str] = None
    scope: Optional[SyncScopeEnum] = None
