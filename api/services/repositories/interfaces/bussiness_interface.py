from typing import Generic, TypeVar
from api.domain.models.dao.bussiness import InsertBussinessModel as _InsertBussinessModel 
T = TypeVar('T')

class BussinessInterface(Generic[T]):
    def insert_bussiness(self, bussiness: _InsertBussinessModel) -> T:
        raise NotImplementedError
    
