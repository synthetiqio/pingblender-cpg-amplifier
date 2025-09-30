import os 
from enum import Enum 
from typing import Dict, List, Any 
from dotenv import load_dotenv
load_dotenv()

class ADI:

    ERROR_MSG:Dict[List,Any]={
        
            'result':'FAILURE', 
            'message': '[Azure ADI Service] - an issue prevented execution of ADI', 
            'payload': None,
        }

    class Action(Enum):
        """
        @Action -> permit/rejection of service actions available in this module.
        """
        LIST:bool=True 
        LOAD:bool=True
        DOWNLOAD:bool=True 
        STORE:bool=True 
        CHAT:bool=True 
        EDIT:bool=True


    class Default(Enum):
        CERT_PATH=os.path.join(os.path.dirname(__file__), 'cert/cacert.pem')
        ENDPOINT=os.getenv("ADI_ENDPOINT")
        KEY=os.getenv("ADI_API_KEY")


        def Settings()->Dict:
            adi:Dict 
            try:
                adi ={
                    'key':ADI.Default.KEY.value, 
                    'endpoint':ADI.Default.ENDPOINT.value,
                }
            except:
                adi={
                    'error_code':ADI.ERROR_MSG
                }
            return {'adi':adi}
        

    class Region:

        def getTimestampLocal(
                tmz : str = 'America/New_York'
            )->str:
            from datetime import datetime
            from pytz import timezone
            fmt = '%Y-%m-%dT%H:%M:%S'
            c = timezone(tmz)
            loc_dt = datetime.now(c)
            fd = loc_dt.strftime(fmt)
            return fd
        
        def getRegionalEnv()->Dict[List, Any]:
            r = {
                'tz' : "America/New_York", 
                'ln' : 'English-USA', 
                'cc' : 'US', 
                'cr' : 'USD'
            }
            return r
        