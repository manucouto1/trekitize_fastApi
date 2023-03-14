from typing import List, Optional

import pyterrier as pt
from fastapi import APIRouter
from model.user_model import UserModel, UserDao
from scripts.add_user_pools import add_user_pools

if not pt.started():
        pt.init()
        
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/all", response_model=List[UserModel])
def get_queries():
    return list(UserDao.findAll())

@router.get('/{user_name}', response_model=Optional[UserModel])
def get_querie(user_name:str):
    return UserDao.find_by_username(user_name)

@router.post('/new')
def new_user(user:UserModel):
    result = UserDao.create(user)

    if result.inserted_id:
        add_user_pools(user.username)
        return {"ok":True}
    else:
        return {"ok":False}