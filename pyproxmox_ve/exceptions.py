class ProxmoxAPIAuthenticationError(Exception):
    def __init__(self):
        super().__init__("Authentication Error (No ticket or API key)")


class ProxmoxAPINoJSONReturnedError(Exception):
    def __init__(self):
        super().__init__(
            "No JSON body/data was found while extracting the body of the request"
        )


class ProxmoxAPIJSONKeyError(Exception):
    def __init__(self, key: str):
        super().__init__(
            f"Key `{key}` was not found while trying to extract the JSON body from the response"
        )
