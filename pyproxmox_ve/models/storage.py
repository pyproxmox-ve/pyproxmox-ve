from typing import Optional

from pydantic import Field

from pyproxmox_ve.models.base import BoolInt, ProxmoxBaseModel
from pyproxmox_ve.models.enums import (
    StoragePreallocationEnum,
    StorageSMBEnum,
    StorageTransportEnum,
    StorageTypeEnum,
)


class StorageBase(ProxmoxBaseModel):
    bwlimit: Optional[str] = None
    cornstar_hg: Optional[str] = None
    cornstar_tg: Optional[str] = None
    content: Optional[str] = None
    content_dirs: Optional[str] = None
    create_base_path: Optional[BoolInt] = None
    create_subdirs: Optional[BoolInt] = None
    data_pool: Optional[str] = None
    disable: Optional[BoolInt] = None
    domain: Optional[str] = None
    encryption_key: Optional[str] = None
    fingerprint: Optional[str] = None
    format: Optional[str] = None
    fs_name: Optional[str] = None
    fuse: Optional[BoolInt] = None
    is_mountpoint: Optional[str] = Field(None, serialization_alias="is_mountpoint")
    keyring: Optional[str] = None
    lrbd: Optional[BoolInt] = None
    lio_tpg: Optional[str] = Field(None, serialization_alias="lio_tpg")
    master_pubkey: Optional[str] = None
    max_protected_backups: Optional[int] = None
    maxfiles: Optional[int] = None
    mkdir: Optional[BoolInt] = None
    monhost: Optional[str] = None
    mountpoint: Optional[str] = None
    namespace: Optional[str] = None
    nocow: Optional[BoolInt] = None
    nodes: Optional[str] = None
    nowritecache: Optional[BoolInt] = None
    options: Optional[str] = None
    path: Optional[str] = None
    password: Optional[str] = None
    pool: Optional[str] = None
    port: Optional[int] = None
    preallocation: Optional[StoragePreallocationEnum] = None
    prune_backups: Optional[str] = None
    saferemove: Optional[BoolInt] = None
    saferemove_throughput: Optional[str] = None
    server: Optional[str] = None
    server2: Optional[str] = None
    shared: Optional[BoolInt] = None
    smbversion: Optional[StorageSMBEnum] = None
    sparse: Optional[BoolInt] = None
    storage: Optional[str] = None
    subdir: Optional[str] = None
    tagged_only: Optional[BoolInt] = Field(None, serialization_alias="tagged_only")
    transport: Optional[StorageTransportEnum] = None
    username: Optional[str] = None


class Storage(StorageBase):
    pass


class StorageCreate(StorageBase):
    storage: str
    type: StorageTypeEnum
    authsupported: Optional[str] = None
    base: Optional[str] = None
    blocksize: Optional[str] = None
    datastore: Optional[str] = None
    export: Optional[str] = None
    iscsiprovider: Optional[str] = None
    portal: Optional[str] = None
    share: Optional[str] = None
    target: Optional[str] = None
    thinpool: Optional[str] = None
    vgname: Optional[str] = None
    volume: Optional[str] = None


class StorageUpdate(StorageBase):
    storage: str


class StorageResponseBase(StorageBase):
    storage: str
    type: StorageTypeEnum
    config: Optional[dict] = None


class StorageCreateResponse(StorageResponseBase):
    pass


class StorageUpdateResponse(StorageResponseBase):
    pass
