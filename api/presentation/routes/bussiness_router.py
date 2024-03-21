from cgi import test
from urllib import response
from fastapi import APIRouter as __APIRouter, status as __status, BackgroundTasks as __BackgroundTasks
from api.domain.schemas.request_schemas.bussiness_request import CreateBussinessRequest as _CreateBussinessRequest, ExtractBussinessReviewsRequest as _ExtractBussinessReviewsRequest
from api.domain.schemas.response_schemas.bussiness_response import CreateBussinessResponse as _CreateBussinessResponse
from fastapi.responses import JSONResponse as __JSONResponse
from api.domain.schemas.response_schemas.base_api_response import BaseApiResponse as __BaseApiResponse
from api.usecases.bussiness_usescases import create_new_bussiness as _create_new_bussiness_usecase, extract_all_bussiness_reviews as _extract_bussiness_reviews
from fastapi import status, HTTPException

bussiness_router = __APIRouter(
    prefix="/bussiness",
    tags=["Coin Routes"],
)

@bussiness_router.post("/create")
async def create_new_bussiness(req_body: _CreateBussinessRequest) -> _CreateBussinessResponse:
    try:
        new_bussiness = _create_new_bussiness_usecase(req_body)
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

