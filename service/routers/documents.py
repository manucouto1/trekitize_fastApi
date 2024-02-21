
from qdrant_client.http import models

from container import Container
from fastapi import APIRouter, Depends
from service.dtos.docs_dto import DocDto
import os

router = APIRouter(
    prefix="/document",
    tags=["document"],
    responses={404: {"description": "Not found"}},
)

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