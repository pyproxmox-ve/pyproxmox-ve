from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyproxmox_ve.api import ProxmoxVEAPI
    from pyproxmox_ve.models.cluster import Options, Resource, Status
    from pyproxmox_ve.models.logs import LogEntry

from pyproxmox_ve.resources.cluster.firewall.firewall import ClusterFirewallAPI


class ClusterAPI:
    def __init__(self, api: ProxmoxVEAPI) -> None:
        self.api = api

        self.firewall = ClusterFirewallAPI(api)

    async def get_logs(self, max_logs: int = None) -> list[LogEntry | dict]:
        """Get all logs.

        Args:
            max_logs:   Maximum number of log entries
        """
        return await self.api.query(
            endpoint="/cluster/log",
            method="GET",
            params={"max": max_logs},
            module_model=("pyproxmox_ve.models.logs", "LogEntry"),
        )

    async def get_next_vm_id(self, vmid: int = None) -> int:
        """Gets the next available VM id.

        Args:
            vmid:   Explicit check to see if this ID is available
        """
        vm_id = await self.api.query(
            endpoint="/cluster/nextid", method="GET", params={"vmid": vmid}
        )
        return int(vm_id)

    async def get_options(self) -> Options | dict:
        """Gets the cluster options."""
        return await self.api.query(
            endpoint="/cluster/options",
            method="GET",
            module_model=("pyproxmox_ve.models.cluster", "Options"),
        )

    async def update_options(self, **kwargs) -> None:
        """Updates the cluster options."""
        return await self.api.update(
            endpoint="/cluster/options",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.cluster", "OptionsUpdate"),
        )

    async def get_resources(self, resource_type: str = None) -> list[Resource | dict]:
        """Get resources.

        Args:
            resource_type:   Resource type (eg. node, storage, pool qemu, lxc, openvz, sdn)
        """
        return await self.api.query(
            endpoint="/cluster/resources",
            method="GET",
            module_model=("pyproxmox_ve.models.cluster", "Resource"),
            params={"type": resource_type},
        )

    async def get_status(self) -> list[Status | dict]:
        """Get Cluster status."""
        return await self.api.query(
            endpoint="/cluster/status",
            method="GET",
            module_model=("pyproxmox_ve.models.cluster", "Status"),
        )

    async def get_tasks(self) -> list[dict]:
        """Get recent tasks."""
        return await self.api.query(endpoint="/cluster/tasks", method="GET")
