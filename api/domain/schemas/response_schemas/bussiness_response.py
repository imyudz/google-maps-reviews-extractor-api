from api.domain.schemas.response_schemas.base_api_response import BaseApiResponse
from pydantic import BaseModel

class CreateBussiness(BaseModel):
    bussiness_id: int
    bussiness_name: str
    status: str
    total_reviews: int
    medium_reviews_rate: float
    bussiness_base_url: str

class CreateBussinessResponse(BaseApiResponse):
    content: CreateBussiness 
        
