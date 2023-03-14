
from typing import List
from pydantic import BaseModel
from fastapi import Query

class DocDto(BaseModel):
    docs: List[str] = Query(...)