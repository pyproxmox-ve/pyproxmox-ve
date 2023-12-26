from __future__ import annotations

import importlib
import json
from ssl import SSLContext
from types import TracebackType
from typing import TYPE_CHECKING

from aiohttp import BaseConnector, ClientResponse, ClientSession, TCPConnector
from yarl import URL

if TYPE_CHECKING:
    from pyproxmox_ve.models.base import ProxmoxBaseModel

from pyproxmox_ve import exceptions
from pyproxmox_ve.auth import PVEAPITokenAuth
from pyproxmox_ve.resources import AccessAPI, VersionAPI

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
        username:       Username to authenticate with <username>@<realm>
        password:       Password to authenticate with if not using API authentication
        api_token_id:   API Token ID to authenticate with
        api_token:      API Token to authenticate with
        api_version:    API Version (only `api2` is currently supported)
        api_type:       API Type (only `json` is currently supported)
        ssl_context:    SSL Context object to pass to the aiohttp session
        connector:      Connector object to pass to the aiohttp session (only `TCPConnector` is currently supported)
        session:        ClientSession object to pass if you want to override anything
        use_pydantic:   Use the Pydantic library for data validation and accessing data via Python objects
        kwargs:         kwargs are passed to the ClientSession that is automatically created if `session` is not used
    """

    def __init__(
        self,
        url: str,
        username: str,
        password: str = "",
        otp: str = "",
        api_token_id: str = "",
        api_token: str = "",
        api_version: str = "api2",
        api_type: str = "json",
        ssl_context: SSLContext | None = None,
        verify_ssl: bool = False,
        connector: BaseConnector | None = None,
        session: ClientSession | None = None,
        use_pydantic: bool = False,
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
        self.password = password
        self.otp = otp
        self.api_token_id = api_token_id
        self.api_token = api_token
        self.api_version = api_version
        self.api_type = api_type

        try:
            self.url = URL(url).joinpath(self.api_version, self.api_type)
        except (ValueError, TypeError) as err:
            raise err

        self._ticket_cookie = None
        self._csrf_token = None
        self._auth = None
        if not self.password and not self.api_token:
            raise exceptions.ProxmoxMisconfigurationError(
                message="A Password or API Token must be provided to authenticate with the Proxmox API"
            )

        if self.password:
            # Setup Cookie Token
            ...
        else:
            # Setup API token
            self._auth = PVEAPITokenAuth(
                login=f"{self.username}!{self.api_token_id}",
                password=self.api_token,
            )

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
                auth=self._auth,
                connector=self.connector,
                **kwargs,
            )

        self.use_pydantic = use_pydantic
        if self.use_pydantic:
            module_found = importlib.util.find_spec("pydantic")
            if not module_found:
                raise exceptions.ProxmoxAPIPydanticNotInstalledError

        # APIs
        self.access = AccessAPI(self)
        self.version = VersionAPI(self)

    async def __aenter__(self) -> ProxmoxVEAPI:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        if self.session:
            await self.session.close()

    async def http_request(
        self,
        endpoint: str,
        method: str,
        data: dict = None,
        data_key: str = "",
        **kwargs,
    ) -> dict | None:
        """aiohttp request shorthand function to handle simple logic.

        Args:
            endpoint:   API Endpoint
            method:     HTTP Method (GET, POST, PUT, DELETE)
            data_key:   nested key to export info if present
        """
        ctx = None
        match method.upper():
            case "GET":
                ctx = self.session.get
            case "POST":
                ctx = self.session.post
            case "PUT":
                ctx = self.session.put
            case "DELETE":
                ctx = self.session.delete
            case _:
                raise KeyError(f"Method `{method}` is not valid")

        r = await ctx(
            url=f"/{self.api_version}/{self.api_type}" + endpoint,
            data=data,
            **kwargs,
        )
        if not r.ok:
            r.raise_for_status()

        data = await r.json()
        if data_key:
            data = data.get(data_key)

        return data

    async def delete(self, endpoint: str, **kwargs) -> dict | None:
        """Delete a resource on the Proxmox VE API.

        Args:
            endpoint:   API Endpoint
        """
        return await self.http_request(endpoint=endpoint, method="DELETE", **kwargs)

    # update() and create() functions seem like its just duplicated code, but in the event we need to change any logic
    # for one of the operations, I've separated the code to allow flexibility in the future otherwise it could be
    # considered a very major breaking change
    async def update(
        self,
        endpoint: str,
        obj_in: dict | ProxmoxBaseModel = None,
        module_model: tuple[str, str] = None,
        data_key: str = "",
        validate_response: bool = False,
        response_model: tuple[str, str] = None,
        **kwargs,
    ) -> ProxmoxBaseModel | dict | None:
        """Update a resource on the Proxmox VE API. As of PVE v8.1, most if not all PUT endpoints
        return null, however when data is returned you can pass a Pydantic model to validate the response
        body if validate_response is set to True. It also appears that the PUT response isn't the new updated
        object but the old object before the update.

        Args:
            endpoint:           API Endpoint
            obj_in:             Resource
            data_key:           Proxmox API typically returns everything in 'data' key, this is
                used to extract the relevant data directly from the ClientResponse
            module_model:       Path to module and model to dynamically load if using Pydantic validation library
            validate_response:  Validate the response using Pydantic
            response_model:     Path to module and model to dynamically validate the response using Pydantic library
                if this model is the same as the original model to update the object, leave this blank and we will
                automatically use the `module_model` to validate the response.
        """
        data = None
        if obj_in:
            data = self._normalize_data(
                obj_in=obj_in,
                module_model=module_model,
                exclude_unset=True,  # Exclude unset to prevent default values updating unset values
            )

        r_data = await self.http_request(
            endpoint=endpoint,
            method="PUT",
            data=data,
            data_key=data_key,
            **kwargs,
        )  # data will automatically set application/x-www-form-urlencoded which Proxmox API is expecting

        # If Pydantic is used, we can validate the response returned back to the user,
        # we can either pass in a separate model using `response_model`, otherwise if this is empty we assume
        # the same model passed to update the data can be used to validate the response.
        # Be careful using the same data model to validate the response as it could be a unique field required
        # when creating the resource, but is never returned in the object back from the API
        if self.use_pydantic and validate_response:
            if not response_model:
                response_model = module_model  # Use same Model that was used to update, to validate response
            validation_model = self._get_pydantic_model(*response_model)
            r_data = self._model_validate(obj_in=r_data, model=validation_model)

        return r_data

    async def create(
        self,
        endpoint: str,
        obj_in: dict | ProxmoxBaseModel,
        module_model: tuple[str, str] = None,
        data_key: str = "",
        validate_response: bool = False,
        response_model: tuple[str, str] = None,
        **kwargs,
    ) -> ProxmoxBaseModel | dict | None:
        """Create a resource on the Proxmox VE API. As of PVE v8.1, most if not all POST endpoints
        return null, however when data is returned you can pass a Pydantic model to validate the response
        body if validate_response is set to True.

        Args:
            endpoint:           API Endpoint
            obj_in:             Resource
            data_key:           Proxmox API typically returns everything in 'data' key, this is
                used to extract the relevant data directly from the ClientResponse
            module_model:       Path to module and model to dynamically load if using Pydantic validation library
            validate_response:  Validate the response using Pydantic
            response_model:     Path to module and model to dynamically validate the response using Pydantic library
                if this model is the same as the original model to create the object, leave this blank and we will
                automatically use the `module_model` to validate the response.
        """
        data = self._normalize_data(obj_in=obj_in, module_model=module_model)
        r_data = await self.http_request(
            endpoint=endpoint,
            method="POST",
            data=data,
            data_key=data_key,
            **kwargs,
        )  # data will automatically set application/x-www-form-urlencoded which Proxmox API is expecting

        # If Pydantic is used, we can validate the response returned back to the user,
        # we can either pass in a separate model using `response_model`, otherwise if this is empty we assume
        # the same model passed to update the data can be used to validate the response.
        # Be careful using the same data model to validate the response as it could be a unique field required
        # when creating the resource, but is never returned in the object back from the API
        if self.use_pydantic and validate_response:
            if not response_model:
                response_model = module_model  # Use same Model that was used to create, to validate response
            validation_model = self._get_pydantic_model(*response_model)
            r_data = self._model_validate(obj_in=r_data, model=validation_model)

        return r_data

    async def query(
        self,
        endpoint: str,
        data_key: str = "data",
        module_model: tuple[str, str] = None,
        **kwargs,
    ) -> ProxmoxBaseModel | dict | None:
        """Basic function to return the JSON directly from any HTTP operation. As of PVE v8.1, most if not all GET
        endpoints will return the data nested inside the response in a key called `data`.

        Args:
            method:         GET, POST, PUT or DELETE
            endpoint:       API Endpoint
            data_key:       This is used to extract the relevant data directly from the ClientResponse body
            module_model:   Path to module and model to dynamically load if using Pydantic library
        """
        data = await self.http_request(endpoint=endpoint, data_key=data_key, **kwargs)

        # Most PVE endpoints return null if it doesn't exist, so this logic should be handled by each function
        # if its expecting some returned data.
        if not data:
            return None

        if self.use_pydantic:
            pydantic_model = self._get_pydantic_model(*module_model)
            data = self._model_validate(obj_in=data, model=pydantic_model)

        return data

    async def _extract_response_json(
        self, response: ClientResponse, root_keys: list[str] = None
    ) -> dict:
        """Attempts to extract JSON from a response and check for various root keys exist in the body.

        Args:
            response:   ClientResponse object
            root_keys:  List of keys to check in the initial JSON body
        """
        if root_keys is None:
            root_keys = []
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
        """Builds parameters according to how Proxmox VE API wants it. Boolean logic in the API
        will require an integer and doesn't attempt to convert based on `yes`, `true, `y`, etc...

        Args:
            kwargs:     dict of arguments
        """
        params = {}
        for k, v in kwargs.items():
            if v is None:
                continue

            # Handle Logic for PVE API
            if isinstance(v, bool):
                params[k] = int(v)
            elif isinstance(v, str):
                # this is here for future implementation :) this obviously needs work since str(v) is just pointless
                params[k] = str(v)

        return params

    def _get_pydantic_model(
        self, module_name: str, model_name: str
    ) -> ProxmoxBaseModel:
        """Attempts to find a Pydantic Model and return it.

        Args:
            module_name:        Name of the module
            model_name:         Name of the Pydantic model
        """
        try:
            pydantic_model: ProxmoxBaseModel = getattr(
                importlib.import_module(module_name), model_name
            )
        except AttributeError as err:
            raise err
        except Exception as err:
            raise err

        return pydantic_model

    def _model_validate(
        self, obj_in: dict | list[dict], model: ProxmoxBaseModel, **kwargs
    ) -> ProxmoxBaseModel | list[ProxmoxBaseModel]:
        """Shorthand function to validate Pydantic model(s).

        Args:
            obj_in:     Data
            model:      Pydantic Model
        """
        if isinstance(obj_in, dict):
            data = model.model_validate(obj_in, **kwargs)
        elif isinstance(obj_in, list):
            data = [model.model_validate(d, **kwargs) for d in obj_in]
        else:
            raise exceptions.ProxmoxAPIPydanticModelError

        return data

    def _model_dump(
        self,
        obj_in: ProxmoxBaseModel | list[ProxmoxBaseModel],
        model: ProxmoxBaseModel,
        exclude_none: bool = True,
        exclude_unset: bool = False,
        by_alias: bool = True,
        **kwargs,
    ) -> dict | list[dict]:
        """Shorthand function to dump Pydantic model(s) with relevant logic to make sure
        Proxmox PVE API is happy (eg. alias is already required to ensure underscore are replaced with hyphens).

        Args:
            obj_in:     Data
            model:      Pydantic Model
        """
        if isinstance(obj_in, model):
            return obj_in.model_dump(
                exclude_none=exclude_none,
                by_alias=by_alias,
                exclude_unset=exclude_unset,
                **kwargs,
            )
        elif isinstance(obj_in, list):
            return [
                m.model_dump(
                    exclude_none=exclude_none,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    **kwargs,
                )
                for m in obj_in
            ]
        else:
            raise exceptions.ProxmoxAPIPydanticModelError

    def _normalize_data(
        self,
        obj_in: ProxmoxBaseModel | dict,
        module_model: tuple[str, str] = None,
        exclude_none: bool = True,
        exclude_unset: bool = False,
        by_alias: bool = True,
    ) -> ProxmoxBaseModel | dict:
        """Shorthand function to return data from either a dict or Pydantic Object.

        If pydantic isn't used then we simply use json.dumps, otherwise if it is used we need to pass in module_model which is a tuple
        that attempts to dynamically load the Pydantic model (module_path, model_name) eg. ("pyproxmox_ve.models.user", "UserCreate"),
        this assumes there is a Pydantic model called `UserCreate` inside the file `pyproxmox_ve.models.user.py`.

        exclude_none, exclude_unset and by_alias are all functionality of Pydantic model_validation and model_dump. We pass this between functions
        to avoid accidentally setting default values on specific operations (eg. updating a user) because if the field is not provided during a PUT,
        we don't want to explicitly update the field back to the default as we might for example, reenable a disabled user. So we tend to set `exclude_unset`
        to True when we are performing PUT operations instead of writing all the logic for this command just for PUT operations.

        Args:
            obj_in:         Dict or Pydantic Object
            module_model:   Tuple of module_name and model_name to dynamically load Pydantic object
            exclude_none:   Passed to Pydantic functions
            exclude_unset:  Passed to Pydantic functions
            by_alias:       Passed to Pydantic functions
        """
        if self.use_pydantic:
            if not module_model:
                raise exceptions.ProxmoxAPIPydanticModelError

            pydantic_model = self._get_pydantic_model(*module_model)

            # Check if the model has already been validated otherwise manually validate the data against the Pydantic model
            # Technically you can load data while bypassing validation, so this part here is risky... It's expected that the user
            # has already performed the `.model_validate()` function on the Pydantic Model.
            if isinstance(obj_in, pydantic_model):
                obj = obj_in
            elif isinstance(obj_in, (list, dict)):
                obj = self._model_validate(obj_in=obj_in, model=pydantic_model)
            else:
                raise TypeError

            data = self._model_dump(
                obj_in=obj,
                model=pydantic_model,
                exclude_none=exclude_none,
                exclude_unset=exclude_unset,
                by_alias=by_alias,
            )
        else:
            data = json.dumps(obj_in)

        return data
