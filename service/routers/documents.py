index_path='./wt2g_index/data.properties'

import pyterrier as pt
from fastapi import APIRouter, Depends
from service.dtos.docs_dto import DocDto
import os

if not pt.started():
        pt.init()

router = APIRouter(
    prefix="/document",
    tags=["document"],
    responses={404: {"description": "Not found"}},
)

@router.get('/one/{docno}')
def get_doc(docno:str):
    index = pt.IndexFactory.of(index_path)
    meta = index.getMetaIndex()
    
    doc_id = meta.getDocument("docno", docno)
    text = meta.getItem("text", doc_id)
    return text

@router.post('/many')
def get_docs(docs:DocDto = Depends()):
    index = pt.IndexFactory.of(index_path)
    meta = index.getMetaIndex()
    
    response = []
    for docno in docs.docs:
        doc_id = meta.getDocument("docno", docno)
        text = meta.getItem("text", doc_id)
        response.append(text)
        
    return list(zip(docs.docs, response))