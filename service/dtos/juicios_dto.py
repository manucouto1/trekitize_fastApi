from typing import List, Optional
from pydantic import BaseModel
from fastapi import Query

class JuicioDto(BaseModel):
    user_pool_id:str 
    juicio_idx:int 
    user_rels: Optional[List[int]]
    user_posi: Optional[List[int]]