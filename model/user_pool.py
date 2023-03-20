from typing import Any, List, Optional
from pydantic import BaseModel
from pydantic import BaseModel, Field

from container import Container
from model.base_dao import BaseDao
from model.bsom_object import PyObjectId
from bson.objectid import ObjectId

class PoolQuery(BaseModel):
    query_num: int
    query_str: str
    pool_list: List[str]
    user_list: Optional[List[str]]
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserPoolModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user: PyObjectId
    last_idx: Optional[int] = None
    juicios: List[PoolQuery]
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
@Container.register_dao('user_pool_model')
class UserPoolDao(BaseDao):
    database = None
    
    @classmethod
    def find_by_userid(cls, user_id:str) -> Any:
        if cls.database != None:
            return cls.database.find_one({"user": ObjectId(user_id)})
        else:
            raise Exception("Dao Not propertly initialized")

    @classmethod
    def find_matching_users(cls, users:List[str]) -> Any:
        if cls.database != None:
            return cls.database.aggregate([
                {"$match": {"$or": list(map(lambda x: {"user": x}, users)) }}
            ])
        else:
            raise Exception("Dao Not propertly initialized")


    

