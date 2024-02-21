from typing import List
import pyterrier as pt
from fastapi import APIRouter

from model.query_model import QueryDao, QueryModel

if not pt.started():
        pt.init()
        
router = APIRouter(
    prefix="/query",
    tags=["query"],
    responses={404: {"description": "Not found"}},
)

@router.get("/all", response_model=List[QueryModel])
def get_queries():
    return list(QueryDao.findAll())

@router.get('/one/{query_id}', response_model=QueryModel)
def get_querie(query_id:str):
    print(query_id)
    data = QueryDao.findById(query_id)
    print(data)
    return data
