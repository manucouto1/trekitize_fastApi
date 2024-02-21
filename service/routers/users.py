from typing import List, Optional

import pyterrier as pt
from fastapi import APIRouter
from model.user_model import UserModel, UserDao
from scripts.add_user_pools import add_user_pools

import traceback

        
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
    doc = UserDao.find_by_username(user_name)
    if doc is None:
        return None
    return UserModel(id=doc["_id"],**doc)

    
@router.post('/new')
def new_user(user:UserModel):
    try:
        if UserDao.find_by_username(user.username) is not None:
            return {"ok": False, "msg": "Username already taken"}
        if UserDao.find_by_email(user.email) is not None:
            return {"ok": False, "msg": "Selected email already has an account"}

        response = UserDao.create(user)
        print(response)
        if response is None:
            return {"ok": False, "msg": "Somthing happened, couldn't create user"}
        
        add_user_pools(user.username)
        print("User created!")
        return {"ok":True, "message": {"username":user.username, "id": str(response.inserted_id)}}
    except Exception as ex:
        print(traceback.format_exc())
        return {"ok":False}