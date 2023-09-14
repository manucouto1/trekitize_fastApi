from typing import List
from fastapi import APIRouter

from service.dtos.juicios_dto import JuicioDto
from service.dtos.user_pool_dto import UserPoolDto
from model.user_pool import PoolQuery, UserPoolModel, UserPoolDao
from fastapi.encoders import jsonable_encoder

import logging

router = APIRouter(
    prefix="/user_pool",
    tags=["user_pool"],
    responses={404: {"description": "Not found"}},
)

@router.get("/by/{user_id}", response_model=UserPoolModel)
def get_by_user_id(user_id:str):
    return UserPoolModel(**UserPoolDao.find_by_userid(user_id))


@router.get("/juicios/by/{user_id}")
def get_juicios_by_user_id(user_id:str):
    return UserPoolDto(**UserPoolDao.find_by_userid(user_id))

@router.get("/filtered/{user_id}/{query_idx}", response_model=JuicioDto)
def update_user_pool_filtered(user_id:str, query_idx:int):
    response = list(UserPoolDao.find_by_userid_query(user_id, query_idx))
    response = response[0]
    response["juicio_idx"] = query_idx - 1
    print(response)
    response["user_pool_id"] = str(response["_id"])
    dto = JuicioDto(**response)
    return dto
    

@router.post("/update")
def update_user_pool_juicios(juicio:JuicioDto):
    logging.info(jsonable_encoder(juicio))
    response = UserPoolDao.update(juicio.user_pool_id, {
        f"juicios.{juicio.juicio_idx}.user_list":juicio.user_list, 
        f"juicios.{juicio.juicio_idx}.grel_list":juicio.grel_list, 
        "last_idx":juicio.juicio_idx,
    })
    
    if response.modified_count > 0:
        return {"ok": True}
    else:
        return {"ok": False}
    
    