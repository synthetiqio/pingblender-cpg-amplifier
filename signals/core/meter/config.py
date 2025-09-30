import os 
from enum import Enum 
from typing import Dict, List, Any 
from dotenv import load_dotenv 
load_dotenv()

class METER:


    ERROR_MSG:Dict[List,Any]={
        'result': 'FAILURE', 
        'message': '[METER] Service Configuration Failure',
        'payload': None 
    }

    class Default(Enum):
        USER:str=os.getenv('METER_USER') or 'DEMO'
        PASS:str=os.getenv('METER_PASS') or 'PASS'
        KEY:str=os.getenv('METER_AUTH') or 'AUTH'
        FLUX:str=os.getenv('METER_FLUX') or 'FLUX'
        ACTOKEN:str='' 
        SETOKEN:str=os.getenv("METER_RUNT") or 'SETN'
        VERSION:str=os.getenv("METER_VERSION") or "VERS"
        ENDPOINT:str=os.getenv("METER_ENDP") or "NONE"
        AUTHURL:str=os.getenv("METER_VURL") or "VURL"
        SERVICE:str="embeddings"
        DEFMODEL:str="text-embedding-ada-002"


    def Settings()->Dict:
        met: Dict 
        try:
            met={
                'user':METER.Default.USER.value, 
                'pass':METER.Default.PASS.value, 
                'key':METER.Default.KEY.value, 
                'endpoint_token':METER.Default.SETOKEN.value, 
                'access_token':METER.Default.ACTOKEN.value, 
                'version':METER.Default.VERSION.value, 
                'endpoint':METER.Default.ENDPOINT.value, 
                'auth_url':METER.Default.AUTHURL.value,
            }
        except:
            met ={
                'error_code': METER.ERROR_MSG.values 
            }

    

    class Embed(Enum):
        CHUNK_SIZE:int=1000 
        CHUNK_OVERLAP:int=0
        VCORE_ENDPOINT:str=os.environ.get("VCORE_ENDPOINT") or 'STANDARD'