import os, sys, json
from typing import Dict, List, Any, Optional
from enum import Enum
from uuid import UUID
from dotenv import load_dotenv
load_dotenv()

class PRETZL: 
    class Default(Enum):
        OWDIR = str(os.getcwd())
        
        
    class Params:

        def __init__(
            self, 
            target:str=None,
            params:Dict[List,Any]=None    
            ):
            self.params = {}

        def get(
            self
            ):
            self.params = self._access()
            return self.params
        
        def _access(self):
            from module.pgvector.connect import Client 
            self.db = Client()
            return self.db.getConnectionString()

    class Sector(Enum):
        HEALTH:bool=True
        FINANCE:bool=True
        OPERATIONS:bool=False
        ENTERTAINMENT:bool=False
    class Conn:
        class PGVector:
            
            def __init__(self):
                from module.pgvector.connect import Client as DbService
                self.conn = DbService()

            async def get(self):
                dbobj:object=self.conn
                return dbobj



    class MClient: 

        class Default(Enum):
            AZURE_CONDUIT:Dict[List, Any] = ""#AuthController.getKey()