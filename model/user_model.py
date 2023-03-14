from typing import Any, List
from pydantic import BaseModel
from pydantic import BaseModel, Field
from container import Container
from model.base_dao import BaseDao
from model.bsom_object import PyObjectId
from bson.objectid import ObjectId

class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    hash_code: str
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

@Container.register_dao('user_model')
class UserDao(BaseDao):
    database = None
    
    @classmethod
    def find_by_username(cls, username:str) -> Any:
        if cls.database != None:
            return cls.database.find_one({"username": username})
        else:
            raise Exception("Dao Not propertly initialized")
        