from pydantic import BaseModel

class PlacesRequest(BaseModel):
    textQuery: str