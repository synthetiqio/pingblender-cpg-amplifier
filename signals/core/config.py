from enum import Enum
from typing import List, Optional, Dict, Any
from sqlalchemy import text, types, DateTime
from sqlalchemy.orm import (
    DeclarativeBase, 
    MappedAsDataclass,
    mapped_column
)
import os, sys, datetime, uuid

class Env:

    ERROR_MSG: Dict[List, Any]  = {
        'result' : 'FAILURE',
        'msg':'A CORE Function has failed without further detail.'
    }

    class Dock(Enum):
        BOOL : bool = os.environ.get('DOCKERIZE')
        FS : str = '\\' if os.environ.get('DOCKERIZE') == "true" else "/"


    class Control(MappedAsDataclass, DeclarativeBase):
        pass 


    class HasTrace:
        trace_id = mapped_column(
            types.Uuid, 
            init=False,
            server_default=text("gen_random_uuid()")
        )

    class HasTimestamp:
        timestamp = mapped_column(
            DateTime, 
            default = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")
        )

class System: 

    class timestamp: 

        def getTimeStampLocal(tmz : str = "America/New_York")->str:
            from datetime import datetime
            from pytz import timezone
            fmt = '%Y-%m-%dT%H:%M:%S'
            c = timezone(tmz)
            loc_dt = datetime.now(c)
            fd = loc_dt.strftime(fmt)
            return fd

    class system_variables:

        def getRegionalEnv()->Dict[List, Any]:
            r : Dict[List, Any] = {
                'tz' : 'America/New_York', 
                'ln' : 'English-USA',
                'cc' : 'US', 
                'cr' : 'USD'
             }

class CORE:

    ERROR_MSG : Dict[List, Any] = {
        'result' : 'Failure',
        'msg' : '[CORE SERVICES] : A systematic failure at the CORE SERVICE level is detected.', 
        'payload' : None
    }


    class Default(Enum):
        USER: str = os.environ.get("SIQ_USER")
        PASS: str = os.environ.get("SIQ_ PASS")
        ENDB: str = os.environ.get("SIQ_EPB")
        KEY: str = os.environ.get("SIQ_KEY")
        ENV: str = os.environ.get("SIQ_ENV")
        TIK: str = os.environ.get("SIQ_TIK")
        TOK: str = os.environ.get("SIQ_TOK")
        VER: str = os.environ.get("SIQ_VER")

        def Settings()->Dict:
            core : Dict[List, Any]
            try:
                core = {
                'user' : CORE.Default['USER'].value,
                'pass' : CORE.Default['PASS'].value,
                'key' : CORE.Default['KEY'].value,
                'env' : CORE.Default['ENV'].value,
                'tik' : CORE.Default['TIK'].value,
                'tok' : CORE.Default['TOK'].value,
                'ver' : CORE.Default['VER'].value
                }
            except: 
                core = {
                    'error_code' : CORE.ERROR_MSG.values
                }



class Route:

    class Default(Enum):
        LCHAIN : str = ''

    class Auth(Enum):
        pass

    class Service(Enum):
        LCHAIN = 'string of langchain url constructed for configs from ENV' 

    class Params:
    
        def __init__(
                self, 
                inputs : Dict[List, Any],
                update : Dict[List, Any] = None
            ):
            self.parsed = Dict[List, Any] = {}
            if update != None:
                self.switchset = True
                self.updates = update
            else:
                self.switchset = False
        
        def Get(self)->Dict[List, Any]:
            return self.parsed

class Network:

    ERROR_MSG : Dict[List, Any] = {
        'result' : "Failure", 
        "msg" : "[Network Module - CORE] - An Issue prevented the executions of variables in the CORE Unit.", 
        "payload" : None
    }

    CL = os.environ.get("CORS_URLS") or ""

    class Default(Enum):
            URLS : List = [
                "http://localhost:3000",
                "https://pingblender.local:1010" #OOTB Scrambler host.
                "http://local.pingblender.com", 
                "https://localhost:5173"
            ]

    class Action(Enum):
         EXTRACT : bool = True
         EVENT : bool = True
         PROCESS : bool = True
         REPORT : bool = True
         MESSAGE : bool = True

    class Timestamp:

        def getTimestampLocal(
                  tmz : str = "America/New_York"
            )->str:
             from datetime import datetime 
             from pytz import timezone 
            
             fmt='%Y-%m-%dT%H:%M:%S'
             c = timezone(tmz)
             loc_dt = datetime.now(c)
             fd = loc_dt.strftime(fmt)
            
             return fd

    class SYS(Enum):
         from module.azure.wasb.config import WASB as Config
         AFS : Dict[List, Any] = Config.Default.getEnvVariables()

         def getWASBVariable(self)->Dict[List, Any]: 
              return self.AFS.values
         
         def getRegionalEnv()->Dict[List, Any]:
              r : Dict[List, Any] 
              r = {
                   'tz' : "America/New_York",
                   'ln' : 'English-USA', 
                   'cc' : 'US', 
                   'cr' : 'USD'
              }
              return r