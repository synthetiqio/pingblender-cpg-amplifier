import uuid
from typing import List, Any, Dict
from module.pretzl.mapper.operate import Structure,Engine
from module.pgvector.connect import PGVector as Db
from module.pgvector.model.base import PGConnect 

class Chat:

    def __init__(
            self, 
            targetFile : str, 
            inputDataFile : str, 
            meta : Dict[List, Any] = None
    ):
        
        self.ob = targetFile
        self.id = inputDataFile
        self.meta = meta
       
    def getMapping(self):
        g = Engine(
            target_filename=self.ob,
            source_filename=self.id
        )
        headers_map = g.run_for_headers_semantics()
        psql = PGConnect()
        data_map = {}
        for match in headers_map:
            data_map['target_filename'] = self.ob
            data_map['target_column_name'] = match[0]
            data_map['source_column_name'] = match[1]
            data_map['source_column_preprocessing_func'] = None
            psql.save_fields_mapping(data_map)
        return headers_map


    def getPreprocessing(self):
        g=Engine(src_input=self.id, set_target=self.ob)
        headers_map=g.getHeaders()
        return headers_map