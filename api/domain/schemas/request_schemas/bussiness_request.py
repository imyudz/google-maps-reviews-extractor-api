from pydantic import BaseModel
class CreateBussinessRequest(BaseModel):
    maps_name: str
    simple_name: str
    full_address: str