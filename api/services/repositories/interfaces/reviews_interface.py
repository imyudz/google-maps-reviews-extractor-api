from typing import Generic, TypeVar
from api.domain.models.dao.review import InsertReviewModel as _InsertReviewModel 
T = TypeVar('T')

class ReviewsInterface(Generic[T]):
    def insert_reviews(self, reviews: _InsertReviewModel | list[_InsertReviewModel]) -> T:
        raise NotImplementedError
    
    def get_reviews_by_bussiness_id(self, bussiness_id: int) -> T:
        raise NotImplementedError
    
    def drop_all_reviews(self, bussiness_id: int) -> bool:
        raise NotImplementedError