import os 
from enum import Enum 
from typing import Dict, List, Any 
from dotenv import load_dotenv
load_dotenv()


class API:

    CL = os.environ.get("CORS_URLS") or ""

    ERROR_MSG:Dict[List,Any]={
            'result':'FAILURE',
            'message':'[API Service] - Unable to process request', 
            'payload':None 
        }

    class Default(Enum):
        URLS : List= [
            'http://localhost:3000', 
            'https://localhost:5173',
            'https://local.pingblender.com'
        ]


    class Action(Enum):
        EXTRACT:bool=True 
        EVENT:bool=True
        PROCESS:bool=True
        REPORT:bool=True 
        MESSAGE:bool=True 
        SET:bool=True 
        SUPPLY:bool=True
        ASSIGN:bool=True 

    
    class Timestamp:

        def getTimestampLocal(tmz:str="America/New_York")->str:
            from datetime import datetime 
            from pytz import timezone 

            fmt='%Y-%m-%dT%H:%M:%S'
            c=timezone(tmz)
            loc_dt=datetime.now(c)
            fd=loc_dt.strftime(fmt)
            return fd 
        

    class SYS(Enum):
        from module.azure.wasb.config import WASB as Config 
        AFS:Dict[List,Any]=Config.Default.getEnvVariables()

        def getWASBVariables(self)->Dict[List,Any]:
            return self.AFS.value 
        
        def getRegionalEnv()->Dict[List,Any]:
            r:Dict[List,Any]={}
            r={
                'tz':"America/New_York", 
                'ln':'English-USA', 
                'cc':'US', 
                'cr':'USD'
            }
            return r 
    