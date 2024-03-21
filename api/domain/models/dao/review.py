from pydantic import BaseModel, Field, validator
from decimal import Decimal
from typing import Annotated
from datetime import datetime

class InsertReviewModel(BaseModel):
    author_name: str
    rating: float
    time: datetime
    description: str
    fk_bussiness_id: int

class ReviewModel(InsertReviewModel):
    id: int = Field(alias="id")