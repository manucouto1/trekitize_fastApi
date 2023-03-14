from app.model.user_pool import UserPoolDao, UserPoolModel
import pandas as pd

def generate_q_rels():
    allUsersPools = UserPoolDao.find_matching_users([""])
    queries_juicios = dict()
    queries_pools = dict()
    
    for user_pool in allUsersPools:
        doc = UserPoolModel(**user_pool)
        for juicio in doc.juicios:
            queries_pools[juicio.query_num] = juicio.pool_list
            query_list = queries_juicios.get(juicio.query_num, [])
            query_list += [] if juicio.user_list is None else juicio.user_list
            queries_juicios[juicio.query_num] = query_list

    final_qrels = []
    for query, rels in queries_juicios.items():
        for pool_doc in queries_pools[query]:
                if rels.count(pool_doc) >= 2:
                    final_qrels.append([query, "Q0", pool_doc, 1])
                else:
                    final_qrels.append([query, "Q0", pool_doc, 0])

    df = pd.DataFrame(final_qrels, columns = ['query', 'q0' , 'docid', 'rel'])
    df.to_csv('g_qrels.csv')

    print(df)