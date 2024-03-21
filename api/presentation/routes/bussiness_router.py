from fastapi import APIRouter as __APIRouter
from fastapi import BackgroundTasks as __BackgroundTasks
from fastapi import HTTPException
from fastapi import status
from fastapi import status as __status
from fastapi.responses import JSONResponse as __JSONResponse

from api.domain.models.dao.bussiness import BussinessModel
from api.domain.schemas.request_schemas.bussiness_request import \
    CreateBussinessRequest as _CreateBussinessRequest
from api.domain.schemas.request_schemas.bussiness_request import \
    ExtractBussinessReviewsRequest as _ExtractBussinessReviewsRequest
from api.domain.schemas.response_schemas.base_api_response import \
    BaseApiResponse as __BaseApiResponse
from api.domain.schemas.response_schemas.bussiness_response import \
    CreateBussinessResponse as _CreateBussinessResponse
from api.usecases.bussiness_usescases import bussiness_info as _bussiness_info
from api.usecases.bussiness_usescases import \
    create_new_bussiness as _create_new_bussiness_usecase
from api.usecases.bussiness_usescases import \
    extract_all_bussiness_reviews as _extract_bussiness_reviews
from api.usecases.bussiness_usescases import \
    get_latest_bussiness_reviews as _get_latest_bussiness_reviews

bussiness_router = __APIRouter(
    prefix="/bussiness",
    tags=["Bussiness Routes"],
)

@bussiness_router.post("/create")
async def create_new_bussiness(req_body: _CreateBussinessRequest, background_tasks: __BackgroundTasks) -> _CreateBussinessResponse:
    try:
        new_bussiness = _create_new_bussiness_usecase(req_body)
        if new_bussiness:
            _extract_bussiness_reviews(new_bussiness.bussiness_id, background_tasks)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return _CreateBussinessResponse(status=status.HTTP_201_CREATED, content=new_bussiness)


@bussiness_router.post("/extract-reviews")
def crawl_bussiness_reviews(req_body: _ExtractBussinessReviewsRequest, background_tasks: __BackgroundTasks) -> __BaseApiResponse:
    try:
        _extract_bussiness_reviews(req_body.bussiness_id, background_tasks)
        response = __BaseApiResponse(
            status=__status.HTTP_200_OK,
            content="Task Successfully Running in Background. Wait some time while we proccess your reviews"
        )
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@bussiness_router.get("/update-reviews/{bussiness_id}/{maps_place_id}")
def update_bussiness_reviews(bussiness_id: int, maps_place_id: str):
    try:
        reviews = _get_latest_bussiness_reviews(bussiness_id, maps_place_id)
        if len(reviews) == 0:
            return __JSONResponse(status_code=status.HTTP_200_OK, content={"status": "no new reviews", "reviews": reviews})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return __JSONResponse(status_code=status.HTTP_200_OK, content={"status": "success", "reviews": reviews})

@bussiness_router.get("/info/{bussiness_id}")
def bussiness_information(bussiness_id: int) -> BussinessModel:
    try:
        bussiness = _bussiness_info(bussiness_id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return __JSONResponse(status_code=status.HTTP_200_OK, content=bussiness.model_dump())

