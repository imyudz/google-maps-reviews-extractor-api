from api.domain.schemas.request_schemas.bussiness_request import CreateBussinessRequest as _CreateBussinessRequest
from api.domain.schemas.response_schemas.bussiness_response import CreateBussiness as _CreateBussiness
from api.services.connectors.maps_api_connector import MapsAPIConnector as __MapsAPIConnector
from api.domain.schemas.request_schemas.maps_api import PlacesRequest as _PlacesRequest
from api.utils.url_utils import mount_bussiness_base_url as _mount_bussiness_base_url
from api.services.repositories.bussiness_repository import BussinessRepository as _BussinessRepository
from api.domain.models.dao.bussiness import InsertBussinessModel as _InsertBussinessModel
import logging
__maps_api = __MapsAPIConnector()


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

def create_new_bussiness(bussiness: _CreateBussinessRequest) -> _CreateBussiness:
    try:
        place_id_and_real_address = _get_place_id_and_real_address(bussiness.full_address, bussiness.maps_name)
        reviews_general_data = _get_reviews_general_data(place_id_and_real_address["place_id"])
        
        bussiness_general_data = {**place_id_and_real_address, **reviews_general_data}
        
        link = _mount_bussiness_base_url(bussiness.maps_name)
        
        new_bussiness = _InsertBussinessModel(
            maps_name=bussiness.maps_name,
            simple_name=bussiness.simple_name,
            formatted_address=bussiness_general_data["address"],
            maps_place_id=bussiness_general_data["place_id"],
            maps_reviews_url=link,
            medium_rate=bussiness_general_data["medium_rate"],
            total_ratings=bussiness_general_data["total_reviews"],
        )
        
        inserted_bussiness = _BussinessRepository().insert_bussiness(
            bussiness=new_bussiness
        )
        
        return _CreateBussiness(
            bussiness_id=inserted_bussiness.id,
            bussiness_name=inserted_bussiness.simple_name,
            status="CREATED",
            medium_reviews_rate=inserted_bussiness.medium_rate,
            bussiness_base_url=inserted_bussiness.maps_reviews_url,
            total_reviews=inserted_bussiness.total_ratings
        )       
    except Exception as e:
        raise e
