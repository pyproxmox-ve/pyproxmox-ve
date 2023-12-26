from __future__ import annotations

from typing import TYPE_CHECKING

from pyproxmox_ve.resources.access.domains.domains import AccessDomainsAPI
from pyproxmox_ve.resources.access.users.users import AccessUsersAPI

if TYPE_CHECKING:
    from pyproxmox_ve.api import ProxmoxVEAPI
    from pyproxmox_ve.models.access import ACL, AuthenticationTicketResponse


class AccessAPI:
    def __init__(self, api: ProxmoxVEAPI) -> None:
        self.api = api
        self.users = AccessUsersAPI(api)
        self.domains = AccessDomainsAPI(api)

    async def get_acls(self) -> list[ACL | dict]:
        """Get all ACLs."""
        return await self.api.query(
            module_model=("pyproxmox_ve.models.access", "ACL"),
            method="GET",
            endpoint="/access/acl",
        )

    async def update_acl(self, path: str, roles: str, **kwargs) -> None:
        """Update an existing ACL.

        This method is also used to create new ACLs if they don't exist.

        Args:
            path:   ACL Path
            roles:  List of roles
        """
        kwargs.update({"path": path, "roles": roles})
        return await self.api.update(
            endpoint="/access/acl",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.access", "ACLUpdate"),
        )

    async def update_password(self, user_id: str, password: str) -> None:
        """Update an existing Users password.

        Note that this API endpoint is not available when using API tokens, but is implemented
        for the future when we support ticket/cookie based authentication.

        Args:
            user_id:    User ID in the format of <username>@<realm>
            password:   New Password
        """
        return await self.api.update(
            endpoint="/access/password",
            obj_in={"userid": user_id, "password": password},
            module_model=("pyproxmox_ve.models.access", "PasswordUpdate"),
        )

    async def get_permissions(self, path: str = None, user_id: str = None) -> dict:
        """Get all permissions.

        Args:
            path:       Dump this specific permission path
            user_id:    User ID or Token ID
        """
        return await self.api.query(
            endpoint="/access/permissions",
            method="GET",
            params={"path": path, "userid": user_id},
        )

    async def get_ticket(self) -> None:
        """Dummy. Useful for formatters which want to provide a login page."""
        return await self.api.query(endpoint="/access/ticket", method="GET")

    async def create_ticket(
        self, username: str, password: str, **kwargs
    ) -> AuthenticationTicketResponse | dict:
        """Create an authentication ticket.

        This can also be used to verify an existing ticket.

        Args:
            username:   Username
            password:   Password
        """
        kwargs.update({"username": username, "password": password})
        return await self.api.create(
            endpoint="/access/ticket",
            obj_in=kwargs,
            module_model=("pyproxmox_ve.models.access", "AuthenticationTicket"),
            validate_response=True,
            response_model=(
                "pyproxmox_ve.models.access",
                "AuthenticationTicketResponse",
            ),
        )
