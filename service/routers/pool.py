from typing import List
import pyterrier as pt
from fastapi import APIRouter

from  model.pools_model import QueryPoolModel, QueryPoolDao


if not pt.started():
        pt.init()
        
router = APIRouter(
    prefix="/pool",
    tags=["pool"],
    responses={404: {"description": "Not found"}},
)

@router.get("/all", response_model=List[QueryPoolModel])
def get_queries():
    return list(QueryPoolDao.findAll())

@router.get('/{query_num}', response_model=QueryPoolModel)
def get_querie(query_num:int):
    return QueryPoolDao.find_query_by_query_num(query_num)
