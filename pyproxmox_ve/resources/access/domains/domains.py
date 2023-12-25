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
