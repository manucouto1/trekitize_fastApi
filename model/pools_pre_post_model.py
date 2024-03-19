from typing import Annotated, Any, List, Optional
from pydantic import BaseModel, Field
from container import Container
from model.base_dao import BaseDao
from model.bsom_object import PyObjectId
from bson.objectid import ObjectId

class PrePostDocModel(BaseModel):
    doc_id:str
    text_pre:str
    text:str
    text_post:str

class PrePostQueryPoolModel(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    query_id: Optional[PyObjectId] = None
    pool_list: List[PrePostDocModel]
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

@Container.register_dao('pre_post_query_pool_model')
class PrePostQueryPoolDao(BaseDao):
    database = None

    @classmethod
    def find_query_by_query_num(cls, query_num:int) -> Any:
        if cls.database != None:
            return cls.database.find_one({"query_num": query_num})
        else:
            raise Exception("Dao Not propertly initialized")
    
