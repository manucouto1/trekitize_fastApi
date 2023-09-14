index_path='./wt2g_index/data.properties'

import pyterrier as pt

from container import Container
from fastapi import APIRouter, Depends
from service.dtos.docs_dto import DocDto
import os

router = APIRouter(
    prefix="/document",
    tags=["document"],
    responses={404: {"description": "Not found"}},
)

@router.get('/one/{docno}')
def get_doc(docno:str):
    print(docno)
    # index = pt.IndexFactory.of(index_path)
    meta = Container.index.getMetaIndex()
    
    doc_id = meta.getDocument("docno", docno)
    text = meta.getItem("text", doc_id)
    return text

@router.post('/many')
def get_docs(docs:DocDto = Depends()):
    # index = pt.IndexFactory.of(index_path)
    meta = Container.index.getMetaIndex()
    
    response = []
    for docno in docs.docs:
        doc_id = meta.getDocument("docno", docno)
        if doc_id > 0:
            text = meta.getItem("text", doc_id)
            response.append(text)
        
    return list(zip(docs.docs, response))