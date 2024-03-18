from pydantic import BaseModel
class CreateBussinessRequest(BaseModel):
    maps_name: str
    simple_name: str
    full_address: str

class ExtractBussinessReviewsRequest(BaseModel):
    bussiness_id: int