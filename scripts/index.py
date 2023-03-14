import pyterrier as pt


def index_data(data_path="../new_data", out_path="./wt2g_index"):
    if not pt.started():
        pt.init()

    files = pt.io.find_files(data_path)
    indexer = pt.TRECCollectionIndexer(out_path, overwrite=True, verbose=True, blocks=False, meta={'docno': 20, 'text': 4096}, meta_tags = {'text' : 'ELSE'})
    # indexer = pt.TRECCollectionIndexer(out_path, overwrite=True, meta= {'docno' : 26, 'text' : 2048}, meta_tags = {'text' : 'ELSE'}, verbose=True)
    # indexer = pt.TRECCollectionIndexer(out_path, overwrite=True, verbose=True, blocks=False, meta={'docno': 20, 'text': 4096})
    indexref = indexer.index(files)

    index = pt.IndexFactory.of(indexref)
    print(index.getCollectionStatistics().toString())
