import os

from dotenv import load_dotenv
from fastapi import FastAPI
from api.presentation.routes.bussiness_router import bussiness_router

from mangum import Mangum

load_dotenv()

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

app = FastAPI(
    title="Google Maps Reviews API",
    description="API de acesso ao PlayCrypto",
    root_path=openapi_prefix
)

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(bussiness_router)

handler = Mangum(app=app)