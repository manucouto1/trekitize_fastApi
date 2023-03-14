import pyterrier as pt
import pandas as pd

# symptom_number, Q0, sentence-id, position_in_ranking, score, system_name.
def generate_ranks(index_path='./wt2g_index/data.properties', queries_path="bdi21.pkl", out_path="query_ranks.yaml", models=['BM25', 'Tf', 'PL2']):
    if not pt.started():
        pt.init()

    indexref = pt.IndexFactory.of(index_path)
    models = dict(map(lambda x: (x, (pt.BatchRetrieve(indexref, wmodel=x) >> pt.text.get_text(indexref, "text"))), models))

    df = pd.read_pickle(queries_path)
    queries = [[q,str(line.replace('\'', ''))] for q, line in enumerate(df.tolist())]

    for (m_name, model) in models.items():
        df = pd.DataFrame(model.transform(pd.DataFrame(queries, columns=['qid','query'])))
        pd.set_option('display.max_rows', df.shape[0]+1)
        
        df = df[['qid','docno', 'rank', 'score']]
        df.head()
        df = df.rename(columns={'qid': 'symptom_number', 'docno': 'sentence-id', 'rank': 'position_in_ranking'})
        df = df.assign(system_name=m_name)
        df = df.assign(Q0='Q0')
        
        df.to_csv(f'runs/{m_name}.csv')

