from pydantic import BaseModel, validator
from datetime import datetime
import pytz
from api.utils.date_utils import calcular_data

class ScrapyReviewsModel(BaseModel):
    bussiness_id: int
    review_date: datetime
    review_rating: float
    description: str
    reviewer: str
    
    @validator('review_date', pre=True)
    def parse_review_date(cls, v: str) -> datetime:
        parsed_date = calcular_data(v)
        return parsed_date.astimezone(pytz.timezone('America/Sao_Paulo'))

    @validator('review_date')
    def format_review_date(cls, v: datetime) -> str:
        return v.isoformat()
