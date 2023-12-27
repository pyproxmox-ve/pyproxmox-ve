from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyproxmox_ve.api import ProxmoxVEAPI
    from pyproxmox_ve.models.firewall import (
        Alias,
        IPSet,
        IPSetEntry,
        Macro,
        Options,
        Reference,
        Rule,
        SecurityGroupRule,
        SecurityGroupSummary,
    )


class ClusterFirewallAPI:
    def __init__(self, api: ProxmoxVEAPI) -> None:
        self.api = api

    async def get_aliases(self) -> list[Alias | dict]:
        """Get the Firewall directory."""
        return await self.api.query(
            endpoint="/cluster/firewall/aliases",
            method="GET",
            module_model=("pyproxmox_ve.models.firewall", "Alias"),
        )

    async def create_alias(self, cidr: str, name: str, **kwargs) -> None:
        """Create IP or Network alias.

        Args:
            cidr:   Network/IP CIDR notation
            name:   Alias name
        """
        kwargs.update({"cidr": cidr, "name": name})
        return await self.api.create(
            endpoint="/cluster/firewall/aliases",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.firewall", "AliasCreate"),
        )

    async def get_alias(self, name: str) -> Alias | dict:
        """Get a specific alias.

        Args:
            name:   Name of the alias
        """
        return await self.api.query(
            endpoint=f"/cluster/firewall/aliases/{name}",
            method="GET",
            module_model=("pyproxmox_ve.models.firewall", "Alias"),
        )

    async def update_alias(self, cidr: str, name: str, **kwargs) -> None:
        """Update a specific alias.

        Args:
            cidr:   Network/IP CIDR notation
            name:   Alias name
        """
        kwargs.update({"cidr": cidr, "name": name})
        return await self.api.update(
            endpoint=f"/cluster/firewall/aliases/{name}",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.firewall", "AliasUpdate"),
        )

    async def delete_alias(self, name: str, digest: str = None) -> None:
        """Delete a specific alias.

        Args:
            name:   Alias name
            digest: Prevent changes if current configuration file has different digest
        """
        return await self.api.delete(
            endpoint=f"/cluster/firewall/aliases/{name}", params={"digest": digest}
        )

    async def get_security_groups(self) -> list[SecurityGroupSummary | dict]:
        """Get all security groups."""
        return await self.api.query(
            endpoint="/cluster/firewall/groups",
            method="GET",
            module_model=("pyproxmox_ve.models.firewall", "SecurityGroupSummary"),
        )

    async def create_security_group(
        self, group_name: str, rename: str = None, **kwargs
    ) -> None:
        """Creates or updates a security group.

        Args:
            group_name:     Name of the group
            rename:         If set to same as group_name, you can update the comment
        """
        kwargs.update({"group": group_name, "rename": rename})
        return await self.api.create(
            endpoint="/cluster/firewall/groups",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.firewall", "SecurityGroupCreate"),
        )

    async def get_security_group_rules(
        self, group_name: str
    ) -> list[SecurityGroupRule | dict]:
        """Get a specific security group and their rules."""
        return await self.api.query(
            endpoint=f"/cluster/firewall/groups/{group_name}",
            method="GET",
            module_model=("pyproxmox_ve.models.firewall", "SecurityGroupRule"),
        )

    async def create_security_group_rule(
        self, group_name: str, action: str, rule_type: str, **kwargs
    ) -> None:
        """Create a new rule for an existing security group.

        Args:
            group_name:     Name of the group
            action:         Rule action
            rule_type:      Type of rule (eg. in, out or group)
        """
        kwargs.update({"group": group_name, "action": action, "type": rule_type})
        return await self.api.create(
            endpoint=f"/cluster/firewall/groups/{group_name}",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.firewall", "SecurityGroupRuleCreate"),
        )

    async def delete_security_group(self, group_name: str) -> None:
        """Delete an existing security group.

        Args:
            group_name:     Name of the group
        """
        return await self.api.delete(endpoint=f"/cluster/firewall/groups/{group_name}")

    async def get_security_group_rule(
        self, group_name: str, position: int
    ) -> SecurityGroupRule | dict:
        """Get a specific rule in a security group.

        Args:
            group_name:     Name of the group
            position:       Position of the rule
        """
        return await self.api.query(
            endpoint=f"/cluster/firewall/groups/{group_name}/{position}",
            method="GET",
            module_model=("pyproxmox_ve.models.firewall", "SecurityGroupRule"),
        )

    async def update_security_group_rule(
        self, group_name: str, position: int, **kwargs
    ) -> None:
        """Update a specific rule in a security group.

        Args:
            group_name:     Name of the group
            position:       Position of the rule
        """
        kwargs.update({"group": group_name, "pos": position})
        return await self.api.update(
            endpoint=f"/cluster/firewall/groups/{group_name}/{position}",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.firewall", "SecurityGroupRuleUpdate"),
        )

    async def delete_security_group_rule(self, group_name: str, position: int) -> None:
        """Delete a specific rule in a security group.

        Args:
            group_name:     Name of the group
            position:       Position of the rule to delete
        """
        return await self.api.delete(
            endpoint=f"/cluster/firewall/groups/{group_name}/{position}"
        )

    async def get_ipsets(self) -> list[IPSet | dict]:
        """Get all IP Sets."""
        return await self.api.query(endpoint="/cluster/firewall/ipset", method="GET")

    async def create_ipset(self, name: str, **kwargs) -> None:
        """Create a new IPSet.

        Args:
            name:   Name of the IPSet
        """
        kwargs.update({"name": name})
        return await self.api.create(
            endpoint="/cluster/firewall/ipset",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.firewall", "IPSetCreate"),
        )

    async def get_ipset_entries(self, name: str) -> list[IPSetEntry | dict]:
        """Get all entries of an existing IPSet.

        Args:
            name:       Name of the IPSet
        """
        return await self.api.query(
            endpoint=f"/cluster/firewall/ipset/{name}",
            method="GET",
            module_model=("pyproxmox_ve.models.firewall", "IPSetEntry"),
        )

    async def create_ipset_entry(self, name: str, cidr: str, **kwargs) -> None:
        """Create a new entry in an IPSet.

        Args:
            name:   Name of the IPSet
            cidr:   CIDR info (IP / Network)
        """
        kwargs.update({"name": name, "cidr": cidr})
        return await self.api.create(
            endpoint=f"/cluster/firewall/ipset/{name}",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.firewall", "IPSetEntryCreate"),
        )

    async def delete_ipset(self, name: str) -> None:
        """Delete an IPSet.

        Args:
            name:   Name of the IPSet
        """
        return await self.api.delete(endpoint=f"/cluster/firewall/ipset/{name}")

    async def get_ipset_entry_network(self, name: str, cidr: str) -> IPSetEntry | dict:
        """Get a specific IPSet entry based on the CIDR.

        Args:
            name:   Name of the IPSet
            cidr:   CIDR info (IP / Network)
        """
        return await self.api.query(
            endpoint=f"/cluster/firewall/ipset/{name}/{cidr}",
            method="GET",
            module_model=("pyproxmox_ve.models.firewall", "IPSetEntry"),
        )

    async def update_ipset_entry_network(self, name: str, cidr: str, **kwargs) -> None:
        """Update a specific IPSet entry based on the CIDR.

        Args:
            name:   Name of the IPSet
            cidr:   CIDR info (IP / Network)
        """
        kwargs.update({"name": name, "cidr": cidr})
        return await self.api.update(
            endpoint=f"/cluster/firewall/ipset/{name}/{cidr}",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.firewall", "IPSetEntryUpdate"),
        )

    async def delete_ipset_entry_network(self, name: str, cidr: str) -> None:
        """Delete a specific IPSet entry based on the CIDR.

        Args:
            name:   Name of the IPSet
            cidr:   CIDR info (IP / Network)
        """
        return await self.api.delete(endpoint=f"/cluster/firewall/ipset/{name}/{cidr}")

    async def get_rules(self) -> list[Rule | dict]:
        """Get all rules."""
        return await self.api.query(
            endpoint="/cluster/firewall/rules",
            method="GET",
            module_model=("pyproxmox_ve.models.firewall", "Rule"),
        )

    async def create_rule(self, action: str, rule_type: str, **kwargs) -> None:
        """Create a new rule.

        Args:
            action:     Rule action (eg, ACCEPT, DROP, REJECT)
            rule_type:  Rule Type (eg. in, out or group)
        """
        kwargs.update({"action": action, "type": rule_type})
        return await self.api.create(
            endpoint="/cluster/firewall/rules",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.firewall", "RuleCreate"),
        )

    async def get_rule(self, position: int) -> Rule | dict:
        """Get a specific rule.

        Args:
            position:   Position of the rule
        """
        return await self.api.query(
            endpoint=f"/cluster/firewall/rules/{position}",
            method="GET",
            module_model=("pyproxmox_ve.models.firewall", "Rule"),
        )

    async def update_rule(self, position: int, **kwargs) -> None:
        """Update an existing rule.

        Args:
            position:   Position of the rule
        """
        return await self.api.update(
            endpoint=f"/cluster/firewall/rules/{position}",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.firewall", "RuleUpdate"),
        )

    async def delete_rule(self, position: int) -> None:
        """Delete a specific rule.

        Args:
            position:   Position of the rule
        """
        return await self.api.delete(endpoint=f"/cluster/firewall/rules/{position}")

    async def get_macros(self) -> list[Macro | dict]:
        """Get all available Macros."""
        return await self.api.query(
            endpoint="/cluster/firewall/macros",
            method="GET",
            module_model=("pyproxmox_ve.models.firewall", "Macro"),
        )

    async def get_options(self) -> Options | dict:
        """Get firewall options."""
        return await self.api.query(
            endpoint="/cluster/firewall/options",
            method="GET",
            module_model=("pyproxmox_ve.models.firewall", "Options"),
        )

    async def update_options(self, **kwargs) -> None:
        """Update firewall options."""
        return await self.api.update(
            endpoint="/cluster/firewall/options",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.firewall", "OptionsUpdate"),
        )

    async def get_references(self, reference_type: str = None) -> Reference | dict:
        """Get all IPSet/Alias references.

        Args:
            reference_type:   alias or ipset
        """
        return await self.api.query(
            endpoint="/cluster/firewall/refs",
            method="GET",
            params={"type": reference_type},
        )
