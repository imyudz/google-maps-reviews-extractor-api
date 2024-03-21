from fastapi.background import BackgroundTasks as __BackgroundTasks
import datetime

from numpy import insert
from api.domain.models.dao.bussiness import \
    InsertBussinessModel as _InsertBussinessModel
from api.domain.models.dao.review import InsertReviewModel, ReviewModel
from api.domain.schemas.request_schemas.bussiness_request import \
    CreateBussinessRequest as _CreateBussinessRequest
from api.domain.schemas.request_schemas.maps_api import \
    PlacesRequest as _PlacesRequest
from api.domain.schemas.response_schemas.bussiness_response import \
    CreateBussiness as _CreateBussiness
from api.domain.schemas.response_schemas.maps_api import \
    ReviewsResponse as _ReviewsResponse
from api.services.connectors.maps_api_connector import \
    MapsAPIConnector as __MapsAPIConnector
from api.services.repositories.bussiness_repository import \
    BussinessRepository as _BussinessRepository
from api.services.repositories.reviews_repository import \
    ReviewsRespository as _ReviewsRespository
from api.utils.date_utils import timestamp_to_date as _timestamp_to_date
from api.utils.url_utils import \
    mount_bussiness_base_url as _mount_bussiness_base_url
from scraper.routines.run import run_google_scraper as _run_google_scraper
import pandas as pd

__maps_api = __MapsAPIConnector()
__bussiness_repository = _BussinessRepository()
__reviews_repository = _ReviewsRespository()

def _get_place_id_and_real_address(bussiness_full_address: str, bussiness_maps_name: str) -> dict[str, str]:
    text_search = f"{bussiness_maps_name} {bussiness_full_address}"
    response = __maps_api.get_place_id(_PlacesRequest(textQuery=text_search))
    return {
        "place_id": response.places[0].id, 
        "address": response.places[0].formattedAddress
    }
def _get_reviews_general_data(place_id: str) -> dict[str,str]:
    response = __maps_api.get_place_rating(place_id)
    return {
        "total_reviews": response.result.user_ratings_total,
        "medium_rate": response.result.rating
    }

def _search_last_reviews(place_id: str):
    response: _ReviewsResponse = __maps_api.get_place_rating(place_id)
    return response.result.reviews
    
def _verify_diff_reviews(reviews: list[ReviewModel], new_reviews: list[ReviewModel]) -> list[InsertReviewModel]:
    df_reviews = pd.DataFrame.from_records([review.dict(exclude=["id", "time"]) for review in reviews])
    df_new_reviews = pd.DataFrame.from_records([new_review.dict() for new_review in new_reviews], exclude=["id"])
    
    # print(df_new_reviews)
    # print(df_reviews)

    df_reviews["description"] = df_reviews["description"].str.replace(r": 5/5", "", regex=True)

    print(df_new_reviews)
    print(df_reviews)
    
    merged = pd.merge(df_reviews, df_new_reviews, on=["author_name", "rating", "description", "fk_bussiness_id"], how="outer", indicator=True)
    new_reviews_df = merged[merged["_merge"] == "right_on"]
    
    insert_reviews = [InsertReviewModel(**r) for r in new_reviews_df.to_dict(orient="records")]

    return insert_reviews
    
    

def create_new_bussiness(bussiness: _CreateBussinessRequest) -> _CreateBussiness:
    try:
        place_id_and_real_address = _get_place_id_and_real_address(bussiness.full_address, bussiness.maps_name)
        reviews_general_data = _get_reviews_general_data(place_id_and_real_address["place_id"])
        
        bussiness_general_data = {**place_id_and_real_address, **reviews_general_data}
        
        link = _mount_bussiness_base_url(bussiness.maps_name, place_id_and_real_address["address"])
        
        new_bussiness = _InsertBussinessModel(
            maps_name=bussiness.maps_name,
            simple_name=bussiness.simple_name,
            formatted_address=bussiness_general_data["address"],
            maps_place_id=bussiness_general_data["place_id"],
            maps_reviews_url=link,
            medium_rate=bussiness_general_data["medium_rate"],
            total_ratings=bussiness_general_data["total_reviews"],
        )
        
        inserted_bussiness = __bussiness_repository.insert_bussiness(
            bussiness=new_bussiness
        )
        
        return _CreateBussiness(
            bussiness_id=inserted_bussiness.id,
            bussiness_name=inserted_bussiness.simple_name,
            status="New Bussiness Created, Extracting reviews ocurring in background",
            medium_reviews_rate=inserted_bussiness.medium_rate,
            bussiness_base_url=inserted_bussiness.maps_reviews_url,
            total_reviews=inserted_bussiness.total_ratings
        )       
    except Exception as e:
        raise e
    



def extract_all_bussiness_reviews(bussiness_id: int, background_tasks: __BackgroundTasks) -> None:
    try:
        if len(__reviews_repository.get_reviews_by_bussiness_id(bussiness_id)) > 0:
            __reviews_repository.drop_all_reviews(bussiness_id)
        
        bussiness_url: str = __bussiness_repository.get_bussiness_info_by_id(bussiness_id).maps_reviews_url
        
        background_tasks.add_task(_run_google_scraper, bussiness_id, bussiness_url)
        
        return True
    except Exception as e:
        raise e

def get_latest_bussiness_reviews(bussiness_id: int, maps_place_id: str) -> list[ReviewModel]:
    try:
        existent_reviews = __reviews_repository.get_reviews_by_bussiness_id(bussiness_id, latest=True)
        
        if len(existent_reviews) == 0:
            raise ValueError("No historic reviews for this bussiness")

        maps_new_reviews = _search_last_reviews(maps_place_id)
        
        maps_reviews_formatted = [ReviewModel(
            id=0,
            rating=review.rating,
            author_name=review.author_name,
            description=review.text,
            time=_timestamp_to_date(review.time),
            fk_bussiness_id=bussiness_id,
        ) for review in maps_new_reviews]
        
        
        diff_reviews = _verify_diff_reviews(existent_reviews, maps_reviews_formatted)
        
        if len(diff_reviews) == 0:
            return []
        
        print(diff_reviews)
        
        response = __reviews_repository.insert_reviews(diff_reviews)
        return response
    except Exception as e:
        raise e

def bussiness_info(bussiness_id: int) -> _CreateBussiness:
    try:
        return __bussiness_repository.get_bussiness_info_by_id(bussiness_id)
    except Exception as e:
        raise e