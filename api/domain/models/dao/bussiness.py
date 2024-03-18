from pydantic import BaseModel

class InsertBussinessModel(BaseModel):
    maps_name: str
    simple_name: str
    maps_place_id: str
    maps_reviews_url: str | None
    formatted_address: str
    total_ratings: int
    medium_rate: float

class BussinessModel(InsertBussinessModel):
    id: int
