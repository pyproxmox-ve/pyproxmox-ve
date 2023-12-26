from enum import Enum


class ConsoleEnum(str, Enum):
    applet = "applet"
    vv = "vv"
    html5 = "html5"
    xtermjs = "xtermhjs"


class AccessACLEnum(str, Enum):
    user = "user"
    group = "group"
    token = "token"


class TFAEnum(str, Enum):
    totp = "totp"
    u2f = "u2f"
    yubico = "yubico"
    oauth = "oauth"
    webauthn = "webauthn"
    recovery = "recovery"
    incompatible = "incompatible"


class DomainTypeEnum(str, Enum):
    ad = "ad"
    ldap = "ldap"
    openid = "openid"
    pam = "pam"
    pve = "pve"


class LDAPModeEnum(str, Enum):
    ldap = "ldap"
    ldaps = "ldaps"
    ldap_starttls = "ldap+starttls"


class SSLVersionEnum(str, Enum):
    tlsv1 = "tlsv1"
    tlsv1_1 = "tlsv1_1"
    tlsv1_2 = "tlsv1_2"
    tlsv1_3 = "tlsv1_3"


class SyncScopeEnum(str, Enum):
    users = "users"
    groups = "groups"
    both = "both"
