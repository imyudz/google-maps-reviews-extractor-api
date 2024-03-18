from urllib.parse import urljoin as _urljoin

from httpx import AsyncClient as __AsyncClient
from httpx import Response as _AsyncAPI__Response


class AsyncAPI(__AsyncClient):
    def __init__(self, base_url: str | None) -> None:
        self.url = base_url
        super().__init__()
        
    async def request(self, method: str | bytes, url: str | bytes, *args, **kwargs) -> _AsyncAPI__Response:
        joined_url = _urljoin(self.url, url)
        return await super().request(method, joined_url, *args, **kwargs)
