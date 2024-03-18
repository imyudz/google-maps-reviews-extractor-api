from pydantic import BaseModel

class BaseApiResponse(BaseModel):
    status: int
    content: str