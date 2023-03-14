import os
import xml.etree.ElementTree as ET
import spacy
from atpbar import atpbar
from app.scripts.model import Sentence
import json
import yaml

def JSON_LOADER(*args, **kargs): return json.load(*args, **kargs)
def YAML_LOADER(*args, **kargs): return yaml.load(*args, **kargs, Loader=yaml.CLoader)
def JSON_DUMPER(*args, **kargs): return json.dump(*args, **kargs)
def YAML_DUMPER(*args, **kargs): return yaml.dump(*args, **kargs, Dumper=yaml.CDumper)

def save_file(path, data, fun=YAML_DUMPER):
    with open(path, 'w+') as f:
        return fun(data, f)

def get_user_id(path):
    user_raw = path.strip('.xml')    
    return user_raw


def recursive_read_dir(files:list, path:str):
    for el in os.listdir(path):
        new_path = f'{path}{el}'
        if os.path.isdir(new_path):
            recursive_read_dir(files, new_path + '/')
        elif os.path.isfile(new_path):
            old_user_id = get_user_id(el)
            files.append((old_user_id, new_path))

    return files


def read_xml(xml):
        rows = []
        post_number = 0
        f = lambda x: x.text if x is not None else ""
        try:
            if xml.endswith('.xml'):
                tree = ET.parse(xml)
                root = tree.getroot()
                id = root.find("ID")
                for writing in root.findall("WRITING"):
                    date = writing.find("DATE")
                    text = writing.find("TEXT")
                    title = writing.find("TITLE")
                    info = writing.find("INFO")
                    rows.append(
                        {
                            "id": f(id),
                            "date": f(date),
                            "title": f(title),
                            "info": f(info),
                            "text": f(text),
                            "post": post_number,
                        }
                    )
                    post_number += 1
            return rows
        except Exception as ex:
            print('Broken path > {} '.format(xml))
            raise Exception("Some error during xml parsing process:", ex)

def split_post(text, nlp):
    aux = None
    if text is not None:
        aux = nlp(text)
    if aux is None:
        return [text]
    else:
        return aux.sents


def trekitize(path, out_path):
    
    try:
        nlp = spacy.load('en_core_web_lg', disable=['tagger', 'parser', 'ner', 'lemmatizer','tok2vec', 'attribute_ruler'])
    except Exception as ex:
        spacy.cli.download('en_core_web_lg')
        nlp = spacy.load('en_core_web_lg', disable=['tagger', 'parser', 'ner', 'lemmatizer','tok2vec', 'attribute_ruler'])

    nlp.add_pipe('sentencizer')

    user_idx_map = dict()
    res = recursive_read_dir([], path)
    for (idx,(old_user_id, path)) in atpbar(list(enumerate(res)), name="Reading xmls"):
        aux = ''
        id_list = []
        for post_count, row in enumerate(read_xml(path)):
            texts = [
                text for text in list(split_post(row['title'], nlp)) + list(split_post(row['text'], nlp)) 
                if text is not None and len(str(text)) > 10
            ]
            
            for sent_count, sentence in enumerate(texts):
                sent = Sentence(idx, post_count, sent_count, sentence)
                id_list.append(sent.id)
                aux += sent.toTREC()
        
        new_user_id = f's_{idx}'
        user_idx_map[new_user_id] = old_user_id

        f = open(f'{out_path}{new_user_id}.trec', "w")
        f.write(aux)
        f.close()
    
    save_file('users_idx_map.yaml', user_idx_map)