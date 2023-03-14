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

@router.get('/{querie_idx}', response_model=QueryModel)
def get_querie(querie_idx:int):
    return QueryDao.find_query_by_query_num(querie_idx)
