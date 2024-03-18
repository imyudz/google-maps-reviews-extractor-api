from config.api import API as _API
from api.domain.schemas.request_schemas.maps_api import PlacesRequest as _PlacesRequest
from api.domain.schemas.response_schemas.maps_api import PlacesResponse as _PlacesResponse, ReviewsResponse as _ReviewsResponse
import os
class MapsAPIConnector: 
    def __init__(self) -> None:
        self.__apikey = os.getenv("MAPS_API_KEY")
    
    def get_place_id(self, body: _PlacesRequest) -> _PlacesResponse:
        api = _API("https://places.googleapis.com")
        headers = {
            "Content-Type": "application/json",
            "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress",
            "X-Goog-Api-Key": f"{self.__apikey}"
        }
        response = api.request('POST', "/v1/places:searchText", json=body.model_dump(), headers=headers)
        return _PlacesResponse(**response.json())
    
    
    def get_place_rating(self, place_id: str) -> _ReviewsResponse:
        api = _API("https://maps.googleapis.com")
        url = f"/maps/api/place/details/json?place_id={place_id}&fields=rating,reviews,user_ratings_total&key={self.__apikey}&reviews_sort=newest&language=pt-BR"
        response = api.request('GET', url=url)
        return _ReviewsResponse(**response.json())
        
        