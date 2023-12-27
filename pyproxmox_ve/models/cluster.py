from typing import Optional

from pydantic import Field

from pyproxmox_ve.models.base import BoolInt, ProxmoxBaseModel
from pyproxmox_ve.models.enums import (
    ClusterFenceEnum,
    ClusterStatusEnum,
    ConsoleEnum,
    KeyboardEnum,
    LanguageEnum,
    ResourceTypeEnum,
)


class OptionsBase(ProxmoxBaseModel):
    bwlimit: Optional[str] = None
    console: Optional[ConsoleEnum] = None
    crs: Optional[str] = None
    delete: Optional[str] = None
    description: Optional[str] = None
    email_from: Optional[str] = Field(None, serialization_alias="email_from")
    fencing: Optional[ClusterFenceEnum] = ClusterFenceEnum.watchdog
    ha: Optional[str] = None
    http_proxy: Optional[str] = None
    keyboard: Optional[KeyboardEnum] = None
    language: Optional[LanguageEnum] = None
    mac_prefix: Optional[str] = "BC:24:11"
    max_workers: Optional[int] = None
    migration: Optional[str] = None
    migration_unsecure: Optional[BoolInt] = None
    next_id: Optional[dict[str, str]] = Field(None, serialization_alias="next_id")
    notify: Optional[str] = None
    registered_tags: Optional[str] = None
    tag_style: Optional[str] = None
    u2f: Optional[str] = None
    user_tag_access: Optional[str] = None
    webauthn: Optional[str] = None


class Options(OptionsBase):
    pass


class OptionsUpdate(OptionsBase):
    next_id: Optional[str] = Field(None, serialization_alias="next_id")


class Resource(ProxmoxBaseModel):
    id: str
    type: ResourceTypeEnum
    cgroup_mode: Optional[int] = None
    content: Optional[str] = None
    cpu: Optional[float] = None
    disk: Optional[int] = None
    hastate: Optional[str] = None
    level: Optional[str] = None
    maxcpu: Optional[float] = None
    maxmem: Optional[int] = None
    maxdisk: Optional[int] = None
    mem: Optional[int] = None
    name: Optional[str] = None
    node: Optional[str] = None
    plugintype: Optional[str] = None
    pool: Optional[str] = None
    status: Optional[str] = None
    storage: Optional[str] = None
    uptime: Optional[int] = None
    vmid: Optional[int] = None


class Status(ProxmoxBaseModel):
    id: str
    name: str
    type: ClusterStatusEnum
    ip: Optional[str] = None
    level: Optional[str] = None
    local: Optional[bool] = None
    nodeid: Optional[int] = None
    nodes: Optional[int] = None
    online: Optional[bool] = None
    quorate: Optional[bool] = None
    version: Optional[int] = None
