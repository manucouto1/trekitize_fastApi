
from model.user_model import UserDao, UserModel
# from model.pools_model import QueryPoolDao, QueryPoolModel
from model.pools_pre_post_model import PrePostQueryPoolDao
from model.user_pool import QueryJuiciosModel, UserPoolModel, UserPoolDao
from model.query_model import QueryDao, QueryModel


def add_user_pools(username: str):
    user = UserModel(**UserDao.find_by_username(username))
    pools = list(PrePostQueryPoolDao.findAll())
    
    user_pool = UserPoolDao.find_by_userid(user.id)
    if user_pool:
       UserPoolDao.delete(user_pool["_id"])
    
    userPool = UserPoolModel(user=user.id, juicios=list(map(lambda x: QueryJuiciosModel(), range(len(pools)))))
    
    print(UserPoolDao.create(userPool))
    
