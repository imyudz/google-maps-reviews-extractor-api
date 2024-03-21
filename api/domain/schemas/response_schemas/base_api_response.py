from typing import Any, Dict
from pydantic import BaseModel

class BaseApiResponse(BaseModel):
    status: int
    content: str | Dict[str, Any]