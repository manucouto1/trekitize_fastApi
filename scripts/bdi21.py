import PyPDF2 
import re
import pandas as pd
from app.model.query_model import QueryModel, QueryDao

# creating a pdf file object 

def parse_bdi(path='../BDI21.pdf'):
    pdfFileObj = open(path, 'rb') 
        
    # creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 


    text1 = pdfReader.getPage(0).extractText()
    text2 = pdfReader.getPage(1).extractText()
    text3 = pdfReader.getPage(2).extractText()


    bdi_queries = []
    pre_num = False

    all_sections = []
    all_queries = []
    for text in [text1, text2, text3]:
        for section in re.findall(f'[0-9]+[\.a-b]([\w \'\-]+[^0-9])0', text):
            all_sections.append(section.strip())
        for idx,querie in enumerate(re.findall(f'([0-9]+)[\.a-b] ([\w \'\-,]+[^0-9])(?<![\.  ])',text)):
            all_queries.append(re.sub(r'\s{2,}',' ', querie[1].strip()))


    final = []    
    text = all_queries[0] + ":\n"
    for querie in all_queries[1:]:
        if querie not in all_sections:
            text = text + "\t" + querie + "\n"
        else: 
            final.append(text)
            text = querie + ":\n"
    final.append(text)

    QueryDao.drop()
    for q_num, text in enumerate(final):
        doc = QueryModel(query_num=q_num, query_str=text)
        QueryDao.create(doc)
    



