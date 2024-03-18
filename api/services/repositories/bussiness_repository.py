import os
from api.domain.models.dao.bussiness import InsertBussinessModel as _InsertBussinessModel, BussinessModel as _BussinessModel
from api.services.repositories.interfaces.bussiness_interface import BussinessInterface as _BussinessInterface
from api.services.connectors.supabase_connector import SupabaseConnector
from fastapi.encoders import jsonable_encoder as _encoder
from postgrest import APIResponse as __ApiResponse

class BussinessRepository(_BussinessInterface):
    def __init__(self) -> None:
        self.__client = SupabaseConnector(
            os.getenv("SUPABASE_URL"), 
            os.getenv("SUPABASE_ADMIN_KEY")).get_supabase_client()
        
    def insert_bussiness(self, bussiness: _InsertBussinessModel) -> _BussinessModel:
        query = self.__client.table("bussinesses").insert(bussiness.model_dump(), returning="representation")
        print(query)
        try:
            response: __ApiResponse = query.execute()
        except Exception as e:
            print("erro ao inserir")
            raise e
        return _BussinessModel(**response.data[0])
