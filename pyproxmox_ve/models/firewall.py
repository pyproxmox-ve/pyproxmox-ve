from typing import Optional

from pydantic import Field

from pyproxmox_ve.models.base import BoolInt, ProxmoxBaseModel
from pyproxmox_ve.models.enums import (
    LogEnum,
    PolicyEnum,
    ReferenceTypeEnum,
    RuleTypeEnum,
)


class AliasBase(ProxmoxBaseModel):
    name: str
    cidr: str
    comment: Optional[str] = None


class Alias(AliasBase):
    digest: Optional[str] = None
    ip_version: int = Field(..., alias="ipversion")


class AliasCreate(AliasBase):
    pass


class AliasUpdate(AliasBase):
    pass


class SecurityGroupSummary(ProxmoxBaseModel):
    group: str
    digest: str
    comment: Optional[str] = None


class SecurityGroupCreate(ProxmoxBaseModel):
    group: str
    comment: Optional[str] = None
    digest: Optional[str] = None
    rename: Optional[str] = None


class RuleBase(ProxmoxBaseModel):
    action: Optional[str] = None
    comment: Optional[str] = None
    destination: Optional[str] = Field(None, alias="dest")
    destination_port: Optional[str] = Field(None, alias="dport")
    enable: Optional[BoolInt] = None
    icmp_type: Optional[str] = Field(None, alias="icmp-type")
    interface: Optional[str] = Field(None, alias="iface")
    log: Optional[LogEnum] = None
    macro: Optional[str] = None
    position: Optional[int] = Field(None, alias="pos")
    protocol: Optional[str] = Field(None, alias="proto")
    source: Optional[str] = None
    source_port: Optional[str] = Field(None, alias="sport")
    type: Optional[RuleTypeEnum] = None


class SecurityGroupRuleBase(RuleBase):
    pass


class SecurityGroupRule(SecurityGroupRuleBase):
    digest: Optional[str] = None
    ip_version: Optional[int] = Field(None, alias="ipversion")


class SecurityGroupRuleCreate(SecurityGroupRuleBase):
    action: str
    group: str
    type: RuleTypeEnum


class SecurityGroupRuleUpdate(SecurityGroupRuleBase):
    group: str


class IPSetBase(ProxmoxBaseModel):
    name: str
    digest: Optional[str] = None
    comment: Optional[str] = None


class IPSet(IPSetBase):
    pass


class IPSetCreate(IPSetBase):
    rename: Optional[str] = None


class IPSetUpdate(IPSetBase):
    pass


class IPSetEntryBase(ProxmoxBaseModel):
    cidr: str
    comment: Optional[str] = None
    nomatch: Optional[str] = None


class IPSetEntry(IPSetEntryBase):
    pass


class IPSetEntryCreate(IPSetEntryBase):
    name: str


class IPSetEntryUpdate(IPSetEntryBase):
    name: str
    digest: Optional[str] = None


class Rule(RuleBase):
    digest: Optional[str] = None
    ip_version: Optional[int] = Field(None, alias="ipversion")


class RuleCreate(RuleBase):
    pass


class RuleUpdate(RuleBase):
    pass


class Macro(ProxmoxBaseModel):
    description: str = Field(alias="descr")
    name: str = Field(alias="macro")


class OptionsBase(ProxmoxBaseModel):
    entables: Optional[bool] = True
    enable: Optional[int] = None
    log_ratelimit: Optional[str] = Field(None, serialization_alias="log_ratelimit")
    policy_in: Optional[PolicyEnum] = Field(None, serialization_alias="policy_in")
    policy_out: Optional[PolicyEnum] = Field(None, serialization_alias="policy_out")


class Options(OptionsBase):
    pass


class OptionsUpdate(OptionsBase):
    delete: Optional[str] = None


class Reference(ProxmoxBaseModel):
    name: str
    ref: str
    scope: str
    type: ReferenceTypeEnum
    comment: Optional[str] = None
