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


class StorageTypeEnum(str, Enum):
    btrfs = "btrfs"
    cephfs = "cephfs"
    cifs = "cifs"
    dir = "dir"
    glusterfs = "glusterfs"
    iscsi = "iscsi"
    iscsidirect = "iscsidirect"
    lvm = "lvm"
    lvmthin = "lvmthin"
    nfs = "nfs"
    pbs = "pbs"
    rbd = "rbd"
    zfs = "zfs"
    zfspool = "zfspool"


class StoragePreallocationEnum(str, Enum):
    off = "off"
    metadata = "metadata"
    falloc = "falloc"
    full = "full"


class StorageSMBEnum(str, Enum):
    default = "default"
    v2_0 = "2.0"
    v2_1 = "2.1"
    v3 = "3"
    v3_0 = "3.0"
    v3_11 = "3.11"


class StorageTransportEnum(str, Enum):
    tcp = "tcp"
    rdma = "rdma"
    unix = "unix"


class ClusterFenceEnum(str, Enum):
    watchdog = "watchdog"
    hardware = "hardware"
    both = "both"


class KeyboardEnum(str, Enum):
    de = "de"
    de_ch = "de-ch"
    da = "da"
    en_gb = "en-gb"
    en_us = "en-us"
    es = "es"
    fi = "fi"
    fr = "fr"
    fr_be = "fr-be"
    fr_ca = "fr-ca"
    fr_ch = "fr-ch"
    hu = "hu"
    k_is = "is"
    it = "it"
    ja = "ja"
    lt = "lt"
    mk = "mk"
    nl = "nl"
    no = "no"
    pl = "pl"
    pt = "pt"
    pt_br = "pt-br"
    sv = "sv"
    sl = "sl"
    tr = "tr"


class LanguageEnum(str, Enum):
    ar = "ar"
    ca = "ca"
    da = "da"
    de = "de"
    en = "en"
    es = "es"
    eu = "eu"
    fa = "fa"
    fr = "fr"
    hr = "hr"
    he = "he"
    it = "it"
    ja = "ja"
    ka = "ka"
    kr = "kr"
    nb = "nb"
    nl = "nl"
    nn = "nn"
    pl = "pl"
    pt_BR = "pt_BR"
    ru = "ru"
    sl = "sl"
    sv = "sv"
    tr = "tr"
    ukr = "ukr"
    zh_CN = "zh_CN"
    zh_TW = "zh_TW"


class ResourceTypeEnum(str, Enum):
    node = "node"
    storage = "storage"
    pool = "pool"
    qemu = "qemu"
    lxc = "lxc"
    openvz = "openvz"
    sdn = "sdn"


class ClusterStatusEnum(str, Enum):
    cluster = "cluster"
    node = "node"


class LogEnum(str, Enum):
    emerg = "emerg"
    alert = "alert"
    crit = "crit"
    err = "err"
    warning = "warning"
    notice = "notice"
    info = "info"
    debug = "debug"
    nolog = "nolog"


class RuleTypeEnum(str, Enum):
    inbound = "in"
    outbound = "out"
    both = "both"


class PolicyEnum(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    DROP = "DROP"


class ReferenceTypeEnum(str, Enum):
    alias = "alias"
    ipset = "ipset"
