from evaluate import load
import os
from os import walk
import pandas as pd
from trectools import TrecQrel, procedures, TrecRun


def old_trec_eval(eval_file, runs_path, remove_first_column=True):
    trec_eval = load("trec_eval")
    qrel = pd.read_csv(eval_file)
    print(qrel)
    if remove_first_column:
        qrel = qrel.values[:,1:5]
    qrel = {
        "query":qrel[:,0],
        "q0":qrel[:,1],
        "docid": qrel[:,2],
        "rel":qrel[:,3]
    }
    
    for (root, dirs, files) in walk(runs_path):
        for name in files:
            path = os.path.join(root, name)
            df = pd.read_csv(path)
            if remove_first_column:
                df = df.values[:,1:7]
            run = {
                "query": df[:,0],
                "q0": df[:,5],
                "docid": df[:,1],
                "rank": df[:,2],
                "score": df[:, 3],
                "system": df[:,4]
            }
            
            results = trec_eval.compute(predictions=[run], references=[qrel])
            
            print(results)
            
def trec_eval(eval_file, runs_path, remove_first_column=True):
    qrel = pd.read_csv(eval_file, index_col=0)
    qrel = qrel.rename(columns={"queryID":"query", "Q0":"q0", "DOCNO":"docid"})
    print(qrel)
    
    if "docid" in qrel:
        qrel["docid"] = qrel["docid"].astype(str)
    if "q0" in qrel:
        qrel["q0"] = qrel["q0"].astype(str)
    if "query" in qrel:
        qrel["query"] = qrel["query"].astype(str)

    qrel = qrel[qrel["rel"] >= 0]
    
    qr = TrecQrel(eval_file)
    qr.qrels_data = qrel
    
    runs = procedures.list_of_runs_from_path(runs_path)
    
    # for run in runs:
    #     results = trec_eval.compute(predictions=[run], references=[qrel])
    #     print(results)
        
    
    # runs = []
    # for (root, dirs, files) in walk(runs_path):
    #     for name in files:
    #         path = os.path.join(root, name)
    #         run = TrecRun(path)
    #         runs.append(run)
    
    result = procedures.evaluate_runs(runs, qr, per_query=True)        
    
   