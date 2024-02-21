from typing import Any, List, Optional
from pydantic import BaseModel, Field

from model.user_pool import QueryJuiciosModel
from model.base_dao import BaseDao
from model.bsom_object import PyObjectId
from bson.objectid import ObjectId


class UserPoolDto(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    user: PyObjectId
    last_idx: Optional[int] = None
    juicios: List[QueryJuiciosModel]
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        