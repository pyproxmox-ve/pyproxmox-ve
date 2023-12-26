from typing import Optional

from pydantic import Field

from pyproxmox_ve.models.base import ProxmoxBaseModel


class Role(ProxmoxBaseModel):
    roleid: Optional[str] = None
    privs: Optional[str] = None
    special: Optional[int] = 0


class RoleCreate(ProxmoxBaseModel):
    roleid: str
    privs: Optional[str] = None


class RoleUpdate(ProxmoxBaseModel):
    roleid: str
    append: Optional[int] = None
    privs: Optional[str] = None


class Permissions(ProxmoxBaseModel):
    datastore_allocate: Optional[int] = Field(None, alias="Datastore.Allocate")
    datastore_allocated_space: Optional[int] = Field(
        None, alias="Datastore.AllocateSpace"
    )
    datastore_allocate_template: Optional[int] = Field(
        None, alias="Datastore.AllocateTemplate"
    )
    datastore_audit: Optional[int] = Field(None, alias="Datastore.Audit")
    group_allocate: Optional[int] = Field(None, alias="Group.Allocate")
    mapping_audit: Optional[int] = Field(None, alias="Mapping.Audit")
    mapping_modify: Optional[int] = Field(None, alias="Mapping.Modify")
    mapping_use: Optional[int] = Field(None, alias="Mapping.Use")
    permissions_modify: Optional[int] = Field(None, alias="Permissions.Modify")
    pool_allocate: Optional[int] = Field(None, alias="Pool.Allocate")
    pool_audit: Optional[int] = Field(None, alias="Pool.Audit")
    realm_allocate: Optional[int] = Field(None, alias="Realm.Allocate")
    realm_allocate_user: Optional[int] = Field(None, alias="Realm.AllocateUser")
    sdn_allocate: Optional[int] = Field(None, alias="SDN.Allocate")
    sdn_audit: Optional[int] = Field(None, alias="SDN.Audit")
    sdn_use: Optional[int] = Field(None, alias="SDN.Use")
    sys_audit: Optional[int] = Field(None, alias="Sys.Audit")
    sys_console: Optional[int] = Field(None, alias="Sys.Console")
    sys_incoming: Optional[int] = Field(None, alias="Sys.Incoming")
    sys_modify: Optional[int] = Field(None, alias="Sys.Modify")
    sys_powermgmt: Optional[int] = Field(None, alias="Sys.PowerMgmt")
    sys_syslog: Optional[int] = Field(None, alias="Sys.Syslog")
    user_modify: Optional[int] = Field(None, alias="User.Modify")
    vm_allocate: Optional[int] = Field(None, alias="VM.Allocate")
    vm_audit: Optional[int] = Field(None, alias="VM.Audit")
    vm_backup: Optional[int] = Field(None, alias="VM.Backup")
    vm_clone: Optional[int] = Field(None, alias="VM.Clone")
    vm_config_cdrom: Optional[int] = Field(None, alias="VM.Config.CDROM")
    vm_config_cpu: Optional[int] = Field(None, alias="VM.Config.CPU")
    vm_config_cloudinit: Optional[int] = Field(None, alias="VM.Config.Cloudinit")
    vm_config_disk: Optional[int] = Field(None, alias="VM.Config.Disk")
    vm_config_hwtype: Optional[int] = Field(None, alias="VM.Config.HWType")
    vm_config_memory: Optional[int] = Field(None, alias="VM.Config.Memory")
    vm_config_network: Optional[int] = Field(None, alias="VM.Config.Network")
    vm_config_options: Optional[int] = Field(None, alias="VM.Config.Options")
    vm_console: Optional[int] = Field(None, alias="VM.Console")
    vm_migrate: Optional[int] = Field(None, alias="VM.Migrate")
    vm_monitor: Optional[int] = Field(None, alias="VM.Monitor")
    vm_powermgmt: Optional[int] = Field(None, alias="VM.PowerMgmt")
    vm_snapshot: Optional[int] = Field(None, alias="VM.Snapshot")
    vm_snapshot_rollback: Optional[int] = Field(None, alias="VM.Snapshot.Rollback")
