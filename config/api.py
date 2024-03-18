from requests import Session as __Session, Response as _Response
from urllib.parse import urljoin as _urljoin

class API(__Session):
    def __init__(self, base_url: str | None) -> None:
        self.url = base_url
        super().__init__()
    
    def request(self, method: str | bytes, url: str | bytes, *args, **kwargs) -> _Response:
        joined_url = _urljoin(self.url, url)
        return super().request(method, joined_url, *args, **kwargs)