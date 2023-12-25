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
    yubico = "yubico"
    oauth = "oauth"


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
