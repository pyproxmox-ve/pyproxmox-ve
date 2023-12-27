from typing import Optional

from pydantic import Field

from pyproxmox_ve.models.base import ProxmoxBaseModel


class LogEntry(ProxmoxBaseModel):
    time: int
    pid: Optional[int] = None
    tag: Optional[str] = None
    node: str
    message: str = Field(alias="msg")
    user: Optional[str] = None
    id: Optional[str] = None
    uid: Optional[str] = None
    pri: Optional[int] = None
