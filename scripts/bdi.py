import PyPDF2 
import re
# creating a pdf file object 
pdfFileObj = open('BDI.pdf', 'rb') 
    
# creating a pdf reader object 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

text1 = pdfReader.getPage(0).extractText()
text2 = pdfReader.getPage(1).extractText()
text3 = pdfReader.getPage(2).extractText()


bdi_queries = []
pre_num = False
for text in [text1, text2, text3]:
    for quest in re.split(r'([0-9])+\.[ \t\n]*', text):
        for resp in re.split(r'[^\-]([0-9])+[ ]+', quest):
            if resp.isnumeric():
                pre_num = True
            elif pre_num:
                if 'INTERPRETING THE BECK DEPRESSION INVENTORY' in resp:
                    bdi_queries.append(" ".join(re.sub(r'^[0-9]', '', resp.split('.')[0]).strip().split()))
                    break;
                else:
                    bdi_queries.append(" ".join(re.sub(r'^[0-9]', '', resp).strip().split()))
                pre_num = False

f = open("bdi.txt", "w")
f.writelines("\n".join(bdi_queries))


