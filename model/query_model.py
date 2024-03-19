from typing import Any, List, Annotated, Optional
from pydantic import BaseModel, Field
from container import Container
from model.base_dao import BaseDao
from model.bsom_object import PyObjectId
from bson.objectid import ObjectId

class QueryModel(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    query_num: int
    query_str: str
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

@Container.register_dao('query_model')
class QueryDao(BaseDao):
    database = None
    
    @classmethod
    def find_query_by_query_num(cls, query_num:int) -> Any:
        if cls.database != None:
            return cls.database.find_one({"query_num": query_num})
        else:
            raise Exception("Dao Not propertly initialized")
        