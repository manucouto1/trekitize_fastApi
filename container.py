from typing import Any, Dict, Type
from pymongo import MongoClient
import pprint
from dotenv import load_dotenv

import os

load_dotenv()

class Container:
    FACTORIES: Dict[str, Type[Any]] = dict()
    ENTITIES: Dict[str, Any] = dict()
    PLUGINS: Dict[str, Type[Any]] = dict()
    
    DAOS: Dict[str, Any] = dict()
    client: MongoClient[Dict[str, Any]] = MongoClient(os.environ["HOST"])
    
    def __init__(self, mongo_host):
        self.call_initializer()
        self.pp = pprint.PrettyPrinter(indent=4)
        self.main_window = None
        self.max_dock_heigh = 0
        self._storage = dict()
        self.runs = []
        
    @staticmethod
    def register_dao(collection):
        def fun_decorator(fun):
            fun()(Container.client['pooling-eval'][collection])
            Container.DAOS[fun.__name__] = fun 
            return fun
        return fun_decorator
    
   



