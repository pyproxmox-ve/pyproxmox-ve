from __future__ import annotations

from typing import TYPE_CHECKING

from pyproxmox_ve.resources.base import BaseResourceAPI

if TYPE_CHECKING:
    from pyproxmox_ve.models.access import Domain


class AccessDomainsAPI(BaseResourceAPI):
    async def get_domains(self) -> list[Domain | dict]:
        """Get all authentication domains."""
        return await self.api.query(
            endpoint="/access/domains",
            method="GET",
            module_model=("pyproxmox_ve.models.access", "Domain"),
        )

    async def create_domain(self, realm: str, realm_type: str, **kwargs) -> None:
        """Create a new authentication domain."""
        kwargs.update({"realm": realm, "type": realm_type})
        return await self.api.create(
            endpoint="/access/domains",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.access", "DomainCreate"),
        )

    async def get_domain(self, realm: str) -> Domain | dict:
        """Get a specific authentication domain.

        Args:
            realm:      Name of the authentication realm
        """
        return await self.api.query(
            endpoint=f"/access/domains/{realm}",
            method="GET",
            module_model=("pyproxmox_ve.models.access", "Domain"),
        )

    async def update_domain(self, realm: str, **kwargs) -> None:
        """Update a specific authentication domain.

        Args:
            realm:      Name of the authentication realm
        """
        kwargs.update({"realm": realm})
        return await self.api.update(
            endpoint=f"/access/domains/{realm}",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.access", "DomainUpdate"),
        )

    async def delete_domain(self, realm: str) -> None:
        """Delete a specific authentication domain."""
        return await self.api.delete(endpoint=f"/access/domains/{realm}")

    async def sync(self, realm: str, **kwargs) -> str:
        """Sync users and/or groups from the configured LDAP server to user.cfg.

        Args:
            realm:              Name of the authentication realm
        """
        kwargs.update({"realm": realm})
        return await self.api.create(
            endpoint=f"/access/domains/{realm}/sync",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.access", "DomainSync"),
            data_key="data",
        )
