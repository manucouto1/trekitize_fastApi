from typing import List
from pydantic import BaseModel
from fastapi import Query

class JuicioDto(BaseModel):
    user_pool_id:str 
    juicio_idx:int 
    user_list:List[str]