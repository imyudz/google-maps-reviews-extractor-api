from pydantic import BaseModel
from typing import List

class _DisplayName(BaseModel):
    text: str
    languageCode: str

class _Place(BaseModel):
    id: str
    formattedAddress: str
    displayName: _DisplayName

class PlacesResponse(BaseModel):
    places: List[_Place]

class _Review(BaseModel):
    author_name: str
    author_url: str
    profile_photo_url: str
    rating: float
    relative_time_description: str
    text: str = ""
    time: int
    translated: bool

class _Result(BaseModel):
    rating: float
    reviews: List[_Review]
    user_ratings_total: int

class ReviewsResponse(BaseModel):
    html_attributions: List[str] = []
    result: _Result
    status: str