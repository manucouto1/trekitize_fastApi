from typing import List
from fastapi import APIRouter

from model.pools_pre_post_model import PrePostQueryPoolDao, PrePostQueryPoolModel
        
router = APIRouter(
    prefix="/pool",
    tags=["pool"],
    responses={404: {"description": "Not found"}},
)

@router.get("/all", response_model=List[PrePostQueryPoolModel])
def get_queries():
    return list(PrePostQueryPoolDao.findAll())

@router.get('/{query_num}', response_model=PrePostQueryPoolModel)
def get_querie(query_num:int):
    return PrePostQueryPoolDao.find_query_by_query_num(query_num)
