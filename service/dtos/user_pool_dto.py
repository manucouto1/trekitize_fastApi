from typing import Any, List, Optional
from pydantic import BaseModel
from pydantic import BaseModel, Field

from container import Container
from model.base_dao import BaseDao
from model.bsom_object import PyObjectId
from bson.objectid import ObjectId

class PoolQueryDto(BaseModel):
    query_num: int
    query_str: str
    pool_list: List[str]
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserPoolDto(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user: PyObjectId
    last_idx: Optional[int] = None
    juicios: List[PoolQueryDto]
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        