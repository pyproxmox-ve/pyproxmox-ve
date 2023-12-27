from typing import Optional

from pydantic import Field

from pyproxmox_ve.models.base import ProxmoxBaseModel


class PoolBase(ProxmoxBaseModel):
    pool_id: str = Field(alias="poolid")
    comment: Optional[str] = None


class Pool(PoolBase):
    members: Optional[list[dict]] = None


class PoolCreate(PoolBase):
    pass


class PoolUpdate(PoolBase):
    allow_move: Optional[int] = Field(0, serialization_alias="allow-move")
    delete: Optional[int] = 0
    storage: Optional[str] = None
    vms: Optional[str] = None
