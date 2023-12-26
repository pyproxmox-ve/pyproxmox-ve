from typing import Optional

from pydantic import Field

from pyproxmox_ve.models.base import ProxmoxBaseModel


class Group(ProxmoxBaseModel):
    groupid: Optional[str] = None
    comment: Optional[str] = None
    users: Optional[str | list[str]] = Field(None, alias="members")


class GroupCreate(Group):
    groupid: str


class GroupUpdate(Group):
    groupid: str
