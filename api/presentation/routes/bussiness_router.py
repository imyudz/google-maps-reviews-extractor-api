from fastapi import APIRouter as __APIRouter, status as __status, BackgroundTasks as __BackgroundTasks
from api.domain.schemas.request_schemas.bussiness_request import CreateBussinessRequest as _CreateBussinessRequest
from api.domain.schemas.response_schemas.bussiness_response import CreateBussinessResponse as _CreateBussinessResponse
from fastapi.responses import JSONResponse as __JSONResponse
from api.usecases.bussiness_usescases import create_new_bussiness as _create_new_bussiness_usecase
from scraper.routines.run import run_google_scraper
from fastapi import status, HTTPException
import threading

bussiness_router = __APIRouter(
    prefix="/bussiness",
    tags=["Coin Routes"],
)

@bussiness_router.post("/create")
async def create_new_bussiness(req_body: _CreateBussinessRequest, background_tasks: __BackgroundTasks) -> _CreateBussinessResponse:
    try:
        new_bussiness = _create_new_bussiness_usecase(req_body)
        if new_bussiness:
            threading.Thread(target=run_google_scraper, args=(new_bussiness.bussiness_base_url, new_bussiness.bussiness_id)).start()
            background_tasks.add_task(run_google_scraper, new_bussiness.bussiness_base_url, new_bussiness.bussiness_id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return _CreateBussinessResponse(status=status.HTTP_201_CREATED, content=new_bussiness)

