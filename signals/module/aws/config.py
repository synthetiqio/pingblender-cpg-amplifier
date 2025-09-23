import os, json, logging
from typing import Dict, List, Any, Optional
from enum import Enum
from load_dotenv import load_dotenv
log=logging.getLogger(__name__)
load_dotenv()

#aws storage and lambda SDK - native Amazon.
import boto3, botocore 

from sqlalchemy import text, types, DateTime
from sqlalchemy.orm import (
    DeclarativeBase, 
    MappedAsDataclass,
    mapped_column
)
import os, sys, datetime, uuid

class AWS:

    ERROR_MSG:Dict[List,Any]={
        'result':'FAILURE', 
        'message':f'{__name__} failed in AWS Config', 
        'payload':None
    }

    class Action(Enum):
        S3:bool=True
        LAMBDA:bool=True
        REDSHIFT:bool=True

    class Env:

        class Dock(Enum):
            BOOL : bool = os.environ.get('DOCKERIZE')
            FS : str = '\\' if os.environ.get('DOCKERIZE') == "true" else "/"

        class Control(
                MappedAsDataclass, 
                DeclarativeBase
            ):
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

        class Timestamp: 

            def getTimeStampeLocal(tmz : str = "America/New_York")->str:
                from datetime import datetime
                from pytz import timezone
                fmt = '%Y-%m-%dT%H:%M:%S'
                c = timezone(tmz)
                loc_dt = datetime.now(c)
                fd = loc_dt.strftime(fmt)
                return fd

        class SYS:

            def getRegionalEnv()->Dict[List, Any]:
                r : Dict[List, Any] = {
                    'tz' : 'America/New_York', 
                    'ln' : 'English-USA',
                    'cc' : 'US', 
                    'cr' : 'USD'
                }

        class Default(Enum):
            USER: str = os.environ.get("SIQ_USER") or None
            PASS: str = os.environ.get("SIQ_ PASS") or None
            ENDB: str = os.environ.get("SIQ_EPB") or None
            KEY: str = os.environ.get("SIQ_KEY") or None
            ENV: str = os.environ.get("SIQ_ENV") or None
            TIK: str = os.environ.get("SIQ_TIK") or None
            TOK: str = os.environ.get("SIQ_TOK") or None
            VER: str = os.environ.get("SIQ_VER") or None

            def Settings()->Dict:
                core : Dict[List, Any]
                try:
                    core = {
                    'user' :AWS.Default.USER.value,
                    'pass' :AWS.Default.PASS.value,
                    'key' : AWS.Default.KEY.value,
                    'env' : AWS.Default.ENV.value,
                    'tik' : AWS.Default.TIK.value,
                    'tok' : AWS.Default.TOK.value,
                    'ver' : AWS.Default.VER.value
                    }
                except: 
                    core = {
                        'error_code' : AWS.ERROR_MSG.values
                    }



    class Route:

        class Default(Enum):
            AWS_ACCOUNT:Dict[List,Any]={
                #replace with env variables.
                'Region': os.environ.get("AWS_REGION"),
                'keyId' : os.environ.get("AWS_ACCESS_KEY_ID"),
                'sKeyId' : os.environ.get("AWS_SECRET_ACCESS_KEY")
            }
            S3:Dict[List,Any]={
                'bucket_name':os.environ.get("SIQ_VER"),
                'stream_name':os.environ.get("SIQ_VER"),
                'secret_key' :os.environ.get("SIQ_VER"),
                'access_key' :os.environ.get("SIQ_VER")
            }

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

