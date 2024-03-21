import logging
import os
from urllib import response

from fastapi.encoders import jsonable_encoder as _encoder
from postgrest import APIResponse as __ApiResponse
from postgrest.exceptions import APIError as __APIError

from api.domain.models.dao.review import InsertReviewModel
from api.domain.models.dao.review import ReviewModel
from api.domain.models.dao.review import ReviewModel as _ReviewModel
from api.services.connectors.supabase_connector import SupabaseConnector
from api.services.repositories.interfaces.reviews_interface import \
    ReviewsInterface as _ReviewsInterface


class ReviewsRespository(_ReviewsInterface):
    def __init__(self) -> None:
        self.__client = SupabaseConnector(
            os.getenv("SUPABASE_URL"), 
            os.getenv("SUPABASE_ADMIN_KEY")).get_supabase_client()
        
    def insert_reviews(self, reviews: InsertReviewModel | list[InsertReviewModel]) -> list[_ReviewModel]:
        query = self.__client.table("reviews").insert(_encoder(reviews), returning='representation')
        try:
            response: __ApiResponse = query.execute()
        except Exception as e:
            raise e
        return [_ReviewModel(**review) for review in response.data]
    
    def get_reviews_by_bussiness_id(self, bussinees_id: str, latest: bool = False) -> list[_ReviewModel]:
        query = self.__client.table("reviews").select("*", count="exact").eq("fk_bussiness_id", bussinees_id).order("time", desc=True)
        if latest:
            query = query.limit(5)
        try:
            response: __ApiResponse = query.execute()
            if response.count == 0:
                return []
        except __APIError as e:
            logging.error("Error searching for existing reviews: ", e)
            raise e
        except Exception as e:
            logging.error("Unexpected Error searching for existing reviews: ", e)
            raise e
        return [_ReviewModel(**review) for review in response.data]
    
    def drop_all_reviews(self, bussiness_id: int) -> bool:
        query = self.__client.table("reviews").delete(count="exact").eq("fk_bussiness_id", bussiness_id)
        try:
            response: __ApiResponse = query.execute()
        except Exception as e:
            logging.error("Error deleting all reviews: ", e)
            raise e
        return response.count > 0
