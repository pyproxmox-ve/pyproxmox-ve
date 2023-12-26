from aiohttp import BasicAuth


class PVECookieTokenAuth(BasicAuth):
    def encode(self) -> str:
        return f"PVEAuthCookie={self.login}"


class PVEAPITokenAuth(BasicAuth):
    def encode(self) -> str:
        return f"PVEAPIToken={self.login}={self.password}"
