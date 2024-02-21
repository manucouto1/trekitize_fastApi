from typing import Annotated, Any, List, Optional
from pydantic import BaseModel, Field

from container import Container
from model.base_dao import BaseDao
from model.bsom_object import PyObjectId
from bson.objectid import ObjectId

class QueryJuiciosModel(BaseModel):
    user_rels: List[int] = []
    user_posi: List[int] = []

class UserPoolModel(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    user: Optional[PyObjectId] = None
    last_idx: Optional[int] = 0
    juicios: Optional[List[QueryJuiciosModel]] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
@Container.register_dao('user_pool_model')
class UserPoolDao(BaseDao):
    database = None
    
    @classmethod
    def find_by_userid(cls, user_id:str) -> Any:
        if cls.database != None:
            return cls.database.find_one({"user": str(user_id)})
        else:
            raise Exception("Dao Not propertly initialized")
        
        
    @classmethod
    def find_by_userid_and_querynum(cls, user_id:str, query_no:int) -> Any:
        if cls.database != None:
            query_str = {'_id':0,  f'juicios.{query_no}':1,  f'juicios.user_rels':1, f'juicios.user_posi':1}
            print(query_str)
            return cls.database.find_one(filter={"user": str(user_id)}, projection=query_str)
        else:
            raise Exception("Dao Not propertly initialized")
        
    # @classmethod
    # def find_by_userid_query(cls, user_id:str, query_num:int) -> Any:
    #     if cls.database != None:
    #         return cls.database.aggregate([
    #             {"$unwind": "$juicios"},
    #             {"$match":
    #                 {
    #                     "$and": [
    #                         {"user": ObjectId(user_id)},
    #                         {"juicios.query_num": query_num}
    #                     ]
    #                 }
    #             },
    #             {
    #                 "$project": {
    #                     "user_pool_id": "_id",
    #                     "user_list": "$juicios.user_list",
    #                     "grel_list": "$juicios.grel_list",
    #                 }
    #              },
    #             { "$limit": 1 }
    #         ])
    #     else:
    #         raise Exception("Dao Not propertly initialized")

    # @classmethod
    # def find_matching_users(cls, users:List[str]) -> Any:
    #     if cls.database != None:
    #         return cls.database.aggregate([
    #             {"$match": {"$or": list(map(lambda x: {"user": x}, users)) }}
    #         ])
    #     else:
    #         raise Exception("Dao Not propertly initialized")


    

