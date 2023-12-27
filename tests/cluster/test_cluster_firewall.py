import pytest

from pyproxmox_ve import ProxmoxVEAPI
from pyproxmox_ve.exceptions import ProxmoxAPIResponseError


@pytest.mark.asyncio
class TestClusterFirewall:
    async def test_get_aliases(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.firewall.get_aliases()
        assert response is None

    async def test_create_alias(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.create_alias(
            cidr="192.0.2.0/24", name="pytest-alias"
        )

    async def test_get_alias(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.firewall.get_alias(name="pytest-alias")
        assert response
        assert response.cidr == "192.0.2.0/24"
        assert response.ip_version == 4

    async def test_update_alias(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.update_alias(
            cidr="192.0.2.0/24",
            name="pytest-alias",
            comment="pytest-alias-comment-updated",
        )

        response = await proxmox.cluster.firewall.get_alias(name="pytest-alias")
        assert response
        assert response.comment == "pytest-alias-comment-updated"

    async def test_delete_alias(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.delete_alias(name="pytest-alias")

    async def test_get_alias_not_exist(self, proxmox: ProxmoxVEAPI):
        with pytest.raises(ProxmoxAPIResponseError) as exc_info:
            await proxmox.cluster.firewall.get_alias(name="pytest-alias")

        error = exc_info.value
        assert error.status == 400
        assert "no such alias" in str(error.errors)

    async def test_create_security_group(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.create_security_group(group_name="pytest-sg")

    async def test_get_security_groups(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.firewall.get_security_groups()
        assert response

    async def test_get_security_group_rules_not_exist(self, proxmox: ProxmoxVEAPI):
        with pytest.raises(ProxmoxAPIResponseError) as exc_info:
            await proxmox.cluster.firewall.get_security_group_rules(
                group_name="pytest-sg-bad"
            )

        error = exc_info.value
        assert error.status == 500
        assert "no such security group" in error.reason

    async def test_create_security_group_rule(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.create_security_group_rule(
            group_name="pytest-sg",
            action="ACCEPT",
            rule_type="in",
            enable=1,
            proto="tcp",
            destination_port="8006",
        )

    async def test_get_security_group_rules(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.firewall.get_security_group_rules(
            group_name="pytest-sg"
        )
        assert response

    async def test_get_security_group_rule(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.firewall.get_security_group_rule(
            group_name="pytest-sg", position=0
        )
        assert response
        assert response.protocol == "tcp"
        assert response.destination_port == "8006"
        assert response.position == 0

    async def test_update_security_group_rule(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.update_security_group_rule(
            group_name="pytest-sg", position=0, comment="pytest-sg-rule-updated"
        )

        response = await proxmox.cluster.firewall.get_security_group_rule(
            group_name="pytest-sg", position=0
        )
        assert response
        assert response.comment == "pytest-sg-rule-updated"

    async def test_delete_security_group_rule(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.delete_security_group_rule(
            group_name="pytest-sg", position=0
        )

    async def test_delete_security_group(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.delete_security_group(group_name="pytest-sg")

    async def test_create_ipset(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.create_ipset(name="pytest-ipset")

    async def test_get_ipsets(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.firewall.get_ipsets()
        assert response

    async def test_create_ipset_entry(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.create_ipset_entry(
            name="pytest-ipset", cidr="192.0.2.0/24"
        )

    async def test_get_ipset_entries(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.firewall.get_ipset_entries(name="pytest-ipset")
        assert response

    async def test_get_ipset_entry_network(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.firewall.get_ipset_entry_network(
            name="pytest-ipset", cidr="192.0.2.0/24"
        )
        assert response
        assert response.cidr == "192.0.2.0/24"

    async def test_update_ipset_entry_by_cidr(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.update_ipset_entry_network(
            name="pytest-ipset",
            cidr="192.0.2.0/24",
            comment="pytest-ipset-entry-comment",
        )

        response = await proxmox.cluster.firewall.get_ipset_entry_network(
            name="pytest-ipset", cidr="192.0.2.0/24"
        )
        assert response
        assert response.comment == "pytest-ipset-entry-comment"

    async def test_delete_ipset_entry_network(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.delete_ipset_entry_network(
            name="pytest-ipset", cidr="192.0.2.0/24"
        )

        response = await proxmox.cluster.firewall.get_ipset_entries(name="pytest-ipset")
        assert response is None

    async def test_delete_ipset(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.delete_ipset(name="pytest-ipset")

        response = await proxmox.cluster.firewall.get_ipsets()
        assert response is None

    async def test_create_rule(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.create_rule(
            action="ACCEPT",
            rule_type="in",
            enable=False,
            protocol="tcp",
            source="192.0.2.0/24",
        )

    async def test_get_rules(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.firewall.get_rules()
        assert response

    async def test_get_rule(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.firewall.get_rule(position=0)
        assert response
        assert response.action == "ACCEPT"
        assert response.source == "192.0.2.0/24"

    async def test_update_rule(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.update_rule(
            position=0, comment="pytest-rule-updated"
        )

        response = await proxmox.cluster.firewall.get_rule(position=0)
        assert response
        assert response.comment == "pytest-rule-updated"

    async def test_delete_rule(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.delete_rule(position=0)

        response = await proxmox.cluster.firewall.get_rules()
        assert response is None

    async def test_get_macros(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.firewall.get_macros()
        assert response
        assert len(response) > 1  # Proxmox comes with a lot of in-built macros

    async def test_get_options(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.firewall.get_options()
        assert response

    async def test_update_options(self, proxmox: ProxmoxVEAPI):
        await proxmox.cluster.firewall.update_options(policy_in="ACCEPT")

        response = await proxmox.cluster.firewall.get_options()
        assert response.policy_in == "ACCEPT"

    @pytest.mark.order(
        before="test_delete_alias",
    )
    async def test_get_references(self, proxmox: ProxmoxVEAPI):
        response = await proxmox.cluster.firewall.get_references()
        assert response
