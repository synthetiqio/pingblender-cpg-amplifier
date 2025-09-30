from enum import Enum 
from pydantic import BaseModel
import os
from typing import Dict,Any,List

CERT_PATH=os.getenv("CA_BUNDLE")

class Route:
    
    def getRoute():
        return os.environ.get("ENV_AUTH_ROUTE") or "/signals/module/core/auth"
    
class BADGE:
    """
    BADGE Configs for users making use of AI Services on tiktoken metering and AUTH
    """

    ERROR_MSG:Dict[List,Any]={
                'result': 'FAILURE',
                'message': '[AUTH - BADGE] - Configurations are invalid in AUTH unit.',
                'payload': None,
        }
    
    class Route:
        
        def getRoute():
            return os.environ.get("ENV_AUTH_ROUTE") or "/signals/module/core/auth"

    class Default(Enum):
        USER:str=os.getenv("BADGE_USER") or 'DEMO'
        PASS:str=os.getenv("BADGE_PASS") or 'DEMOP@55WORD'
        KEY:str=os.getenv("BADGE_LOC_KEY")
        MIM:str=os.getenv("BADGE_MIM_KEY")
        EPTOKEN=MIM 
        ACTOKEN=''
        VERSION:str='0.1.0'
        ENDPOINT=os.getenv("MIM_ENDPOINT_BASE")
        AUTHURL=os.getenv("MIM_ENDPOINT_LOGIN")
        SERVICE:str="embeddings"
        DEFMODEL:str="text=embedding-ada-002"


        def Settings()->Dict:
            mim:Dict
            try:
                mim={
                    'user':BADGE.Default.USER.value,
                    'pass':BADGE.Default.PASS.value,
                    'key':BADGE.Default.KEY.value,
                    'endpoint_token':BADGE.Default.EPTOKEN,
                    'access_token':BADGE.Default.ACTOKEN.value,
                    'version':BADGE.Default.VERSION.value,
                    'endpoint':BADGE.Default.ENDPOINT.value,
                    'auth_url':BADGE.Default.AUTHURL.value
                }
            except:
                mim={
                    'error_code':BADGE.ERROR_MSG.values
                }

class METER:

    ERROR_MSG:Dict[List,Any]={
                'result': 'FAILURE',
                'message': '[AUTH - METER] - Configurations are invalid in AUTH unit.',
                'payload': None,
        }