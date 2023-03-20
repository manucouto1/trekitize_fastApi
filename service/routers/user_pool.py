from typing import List
from fastapi import APIRouter

from service.dtos.juicios_dto import JuicioDto
from model.user_pool import PoolQuery, UserPoolModel, UserPoolDao

router = APIRouter(
    prefix="/user_pool",
    tags=["user_pool"],
    responses={404: {"description": "Not found"}},
)

@router.get("/by/{user_id}", response_model=UserPoolModel)
def get_by_user_id(user_id:str):
    print(user_id)
    print(UserPoolDao.find_by_userid(user_id))
    return UserPoolModel(**UserPoolDao.find_by_userid(user_id))

@router.post("/update")
def update_user_pool_juicios(juicio:JuicioDto):
    print(juicio)
    response = UserPoolDao.update(juicio.user_pool_id, {f"juicios.{juicio.juicio_idx}.user_list":juicio.user_list, "last_idx":juicio.juicio_idx})
    
    print(response.modified_count)
    if response.modified_count > 0:
        return {"ok": True}
    else:
        return {"ok": False}
    
    