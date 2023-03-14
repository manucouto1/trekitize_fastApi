
from model.user_model import UserDao, UserModel
from model.pools_model import QueryPoolDao, QueryPoolModel
from model.user_pool import PoolQuery, UserPoolModel, UserPoolDao
from model.query_model import QueryDao, QueryModel

def add_user_pools(username: str):
    
    user = UserModel(**UserDao.find_by_username(username))
    query_pools = list(QueryPoolDao.findAll())
    
    user_pool = UserPoolDao.find_by_userid(user.id)
    if user_pool:
       UserPoolDao.delete(user_pool["_id"])
    
    juicios = []
    
    for query in query_pools:
        del query["_id"]
        poolModel = QueryPoolModel(**query)
        queryModel = QueryModel(**QueryDao.findById(poolModel.query_id))
        del query["query_id"]
        
        pool = PoolQuery(query_str=queryModel.query_str, **query)
        juicios.append(pool)
        
    userPool = UserPoolModel(user=user.id, juicios=juicios)
    UserPoolDao.create(userPool)
    
        
