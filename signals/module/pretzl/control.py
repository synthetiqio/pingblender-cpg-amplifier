import os, json
from typing import List, Dict, Optional, Any
from enum import Enum
from module.pretzl.config import PRETZL as Config

class PRETZL: 

    class ToggleController:

        def __init__(self):
            pass 

        def getSector(
                self, 
                sector:str
                )->bool:
            a=Config.Sector[sector].value
            return a


    class DbController:

        def __init__(
                self
        ):
            self.client = Config.Conn.PGVector()

        def connString(self)->str:
            c:str=self.client.conn.getConnectionString()
            return c

        def getClient(self):
            return self.client

    class ContainerController:

        def __new__(
                cls,
                name : Optional[str] = None
        ): 
            instance = super().__new__(cls)
            return instance
        
        def __init__(
                self, 
                name : str = ''
        ):
            self.container = name
            self.dockerize = self._dockedOS()
            self.owkd = os.curdir()


        def getContainerOS(
                self
        )->Dict[List, Any]:
            return self.dockerize
        

        def dockedOS(
                self
        )->Dict[List, Any]:
            docker : Dict[list]
            fss : str = ''
            if os.environ.get("DOCKERIZED" == 'true'):
                fss = '/'
            else:
                fss = '\\'
            docker = {
                "ENV" : os.environ.get("DOCKERIZED"), 
                "UNX" : fss,
                "OWD" : self.owkd
            }
            return docker