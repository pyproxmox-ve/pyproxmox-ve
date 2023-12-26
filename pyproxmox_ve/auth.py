from aiohttp import BasicAuth


class PVEAPITokenAuth(BasicAuth):
    def encode(self) -> str:
        return f"PVEAPIToken={self.login}={self.password}"
