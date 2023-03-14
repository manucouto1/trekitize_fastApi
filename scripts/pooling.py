import pandas as pd
import os
from os import walk
import pandas as pd
from app.model.pools_model import QueryPoolModel, QueryPoolDao
from app.model.query_model import QueryModel, QueryDao

def insert_pools(folder='../runs'):
    pools = dict()
    for (root, dirs, files) in walk(folder):
        for name in files:
            path = os.path.join(root, name)
            df = pd.read_csv(path)
            df = df[df['position_in_ranking']<100]
            for query in df['symptom_number']:
                queryRank = df[df['symptom_number'] == query]
                aux_set = pools.get(query, set())
                aux_list = queryRank['sentence-id'].tolist()
                aux_set.update(set(aux_list))
                pools[query] = aux_set
    
    QueryPoolDao.drop()
    for query, pool in pools.items():
        aux = list(pool)
        query_doc = QueryModel(**QueryDao.find_query_by_query_num(query))
        doc = QueryPoolModel(query_num=query, pool_list=aux, query_id=query_doc.id)
        QueryPoolDao.create(doc)


