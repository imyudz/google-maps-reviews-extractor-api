import os
from api.domain.models.dao.review import InsertReviewModel
from api.services.repositories.interfaces.reviews_interface import ReviewsInterface as _ReviewsInterface
from api.domain.models.dao.review import ReviewModel as _ReviewModel
from api.services.connectors.supabase_connector import SupabaseConnector
from fastapi.encoders import jsonable_encoder as _encoder
from postgrest import APIResponse as __ApiResponse

class ReviewsRespository(_ReviewsInterface):
    def __init__(self) -> None:
        self.__client = SupabaseConnector(
            os.getenv("SUPABASE_URL"), 
            os.getenv("SUPABASE_ADMIN_KEY")).get_supabase_client()
        
    def insert_reviews(self, reviews: InsertReviewModel | list[InsertReviewModel]) -> list[_ReviewModel]:
        query = self.__client.table("reviews").insert(_encoder(reviews), returning='representation')
        try:
            response: __ApiResponse = query.execute()
            print(response)
        except Exception as e:
            raise e
        return [_ReviewModel(**review) for review in response.data]