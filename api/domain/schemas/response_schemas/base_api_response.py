from pydantic import BaseModel

class BaseApiResponse(BaseModel):
    status: str
    content: str