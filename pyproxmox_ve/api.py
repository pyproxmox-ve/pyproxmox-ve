from aiohttp import ClientSession, BaseConnector, TCPConnector, ClientResponse
from types import TracebackType
from typing import Type
from ssl import SSLContext
from yarl import URL

from pyproxmox_ve.auth import PVEAPITokenAuth
from pyproxmox_ve.resources import VersionAPI, AccessAPI
from pyproxmox_ve.exceptions import (
    ProxmoxAPINoJSONReturnedError,
    ProxmoxAPIJSONKeyError,
)
from pyproxmox_ve.models.base import ProxmoxBaseModel

SUPPORTED_API_VERSIONS = ["api2"]
SUPPORTED_API_TYPES = ["json"]


class ProxmoxVEAPI:
    """aiohttp wrapper which handles a lot of the heavy lifting to interact with
    the Proxmox VE API (only http(s) protocol is supported).

    Majority if not all endpoint groups will be modelled under their respective name, for
    example the `/access/users` endpoint is modelled as:
        api.access.users.get_users()

    When there is a large nested endpoint like `/nodes/{node_id}/qemu/{qemu_id}/firewall/rules/{id}`, nested required path variables
    are required in the called function, this is modelled as:
        api.nodes.qemu.firewall.get_qemu_firewall(node_id=1, qemu_id=2, id=3)

    Args:
        url:            ProxmoxVE API Url (eg. https://localhost:8086)
        username:       Username to authenticate with
        realm:          Realm to authenticate with
        api_token_id:   API Token ID to authenticate with
        api_token:      API Token to authenticate with
        api_version:    API Version (only `api2` is currently supported)
        api_type:       API Type (only `json` is currently supported)
        ssl_context:    SSL Context object to pass to the aiohttp session
        connector:      Connector object to pass to the aiohttp session (only `TCPConnector` is currently supported)
        session:        ClientSession object to pass if you want to override anything
        kwargs:         kwargs are passed to the ClientSession that is automatically created if `session` is not used
    """

    def __init__(
        self,
        url: str,
        username: str,
        realm: str,
        api_token_id: str,
        api_token: str,
        api_version: str = "api2",
        api_type: str = "json",
        ssl_context: SSLContext | None = None,
        verify_ssl: bool = False,
        connector: BaseConnector | None = None,
        session: ClientSession | None = None,
        **kwargs,
    ) -> None:
        if api_version not in SUPPORTED_API_VERSIONS:
            raise NotImplementedError(
                f"API version {api_version} is not supported in this release."
            )

        if api_type not in SUPPORTED_API_TYPES:
            raise NotImplementedError(
                f"API type {api_type} is not supported in this release."
            )

        self.username = username
        self.realm = realm
        self.api_token_id = api_token_id
        self.api_token = api_token
        self.api_version = api_version
        self.api_type = api_type

        try:
            self.url = URL(url).joinpath(self.api_version, self.api_type)
        except (ValueError, TypeError) as err:
            raise err

        self.ssl_context = ssl_context
        self.verify_ssl = verify_ssl
        self.connector = connector
        if not self.connector:
            self.connector = TCPConnector(
                ssl_context=self.ssl_context, ssl=self.verify_ssl
            )

        self.session = session
        if not self.session:
            self.session = ClientSession(
                base_url=self.url,
                auth=PVEAPITokenAuth(
                    login=f"{self.username}@{self.realm}!{self.api_token_id}",
                    password=self.api_token,
                ),
                connector=self.connector,
                **kwargs,
            )

        # APIs
        self.access = AccessAPI(self)
        self.version = VersionAPI(self)

    async def __aenter__(self) -> "ProxmoxVEAPI":
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        if self.session:
            await self.session.close()

    async def post(self, endpoint: str, **kwargs) -> ClientResponse:
        """aiohttp poor implementation of base_url requires us to build the path endpoint on every API call, been going on since 2022, pretty awful..."""
        return await self.session.post(
            url=f"/{self.api_version}/{self.api_type}" + endpoint, **kwargs
        )

    async def get(self, endpoint: str, **kwargs) -> ClientResponse:
        """aiohttp poor implementation of base_url requires us to build the path endpoint on every API call, been going on since 2022, pretty awful..."""
        return await self.session.get(
            url=f"/{self.api_version}/{self.api_type}" + endpoint,
            **kwargs,
        )

    async def put(self, endpoint: str, **kwargs) -> ClientResponse:
        """aiohttp poor implementation of base_url requires us to build the path endpoint on every API call, been going on since 2022, pretty awful..."""
        return await self.session.put(
            url=f"/{self.api_version}/{self.api_type}" + endpoint, **kwargs
        )

    async def delete(self, endpoint: str, **kwargs) -> ClientResponse:
        """aiohttp poor implementation of base_url requires us to build the path endpoint on every API call, been going on since 2022, pretty awful..."""
        return await self.session.delete(
            url=f"/{self.api_version}/{self.api_type}" + endpoint, **kwargs
        )

    async def query(
        self, method: str, endpoint: str, data_key: str = "data", **kwargs
    ) -> dict:
        """Basic function to return the JSON directly from any HTTP operation

        Args:
            method:         GET, POST, PUT or DELETE
            endpoint:       API Endpoint
            data_key:       Proxmox API typically returns everything in 'data' key, this is
                used to extract the relevant data directly from the ClientResponse
        """
        match method.upper():
            case "GET":
                m = self.get
            case "POST":
                m = self.post
            case "PUT":
                m = self.put
            case "DELETE":
                m = self.delete
            case _:
                raise KeyError(f"Method `{method}` is not valid")

        r = await m(endpoint=endpoint, **kwargs)
        data = await r.json()

        if data_key:
            return data.get(data_key)

        return data

    async def query_with_model(
        self, model: ProxmoxBaseModel, **kwargs
    ) -> ProxmoxBaseModel | None:
        """Similar to `query` function, but attempts to validate a model and return it

        Args:
            model:      Pydantic ProxmoxBaseModel to validate against
            kwargs:     Passed to `query` function
        """
        r = await self.query(**kwargs)

        if isinstance(r, dict):
            data = model.model_validate(r)
        elif isinstance(r, list):
            data = [model.model_validate(d) for d in r]
        else:
            return None

        return data

    async def _extract_response_json(
        self, response: ClientResponse, root_keys: list[str] = []
    ) -> dict:
        """Attempts to extract JSON from a response and check for various root keys exist in the body

        Args:
            response:       ClientResponse object
            root_keys:      List of keys to check in the initial JSON body
        """
        try:
            data = await response.json()
        except Exception as err:
            raise err

        if not all(k in data for k in root_keys):
            raise KeyError(
                f"JSON Body is missing one of the following required keys: {root_keys}"
            )

        return data

    def _build_params(self, **kwargs):
        params = {}
        for k, v in kwargs.items():
            if v == None:
                continue

            # Handle Logic for PVE API
            if isinstance(v, bool):
                params[k] = int(v)
            elif isinstance(v, str):
                # this is here for future implementation :) this obviously needs work since str(v) is just pointless
                params[k] = str(v)

        return params
