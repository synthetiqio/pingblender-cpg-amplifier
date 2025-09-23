from typing import Dict, List, Any
from enum import Enum
class FILE:

    ERROR_MSG:Dict[List, Any]={
        'result' : 'Failure', 
        'message' : '[FILE] : Service failure - Configuration Level [Root]',
        'payload': None
    }

    class Timestamp:

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
        

    class Action(Enum):
        REVIEW : bool = True
        UPLOAD : bool = True
        COLLECT : bool = True
        DETAILS : bool = True
        GETLOC : bool = True
        DELETE : bool = False
        ANALYZE : bool = True
        EMBED : bool = False
        MANAGE : bool = False 
        DOWNLOAD:bool=False 


    class SYS(Enum):
        from module.storage.azure.wasb.config import WASB as Config
        AFS: Dict[List, Any] = Config.Default.getEnvVariables()

        def getRegionalEnv()->Dict[List, Any]:
            r = {
                'tz' : "America/New_York", 
                'ln' : 'English-USA', 
                'cc' : 'US', 
                'cr' : 'USD'
            }
            return r
        
        def getWASBVariable(self)->Dict[List,Any]:
            return self.AFS.value 

        def getStorageVariable(self)->Dict[List, Any]:
            return self.AFS.values
        


    class PLAN:

        def ProducePlan()->Dict[List, Any]:
            response : Dict[List, Any] = {
                'plan':'', 
                'headers':'', 
                'package':'', 
                'chunks':'', 
                'labels':'',
                'assets':'', 
                'tokens':''
            }
            return response 
        

        def AnalyzeFile()->Dict[List, Any]: 
            response = {
                'plan' : {
                    'headers':'true'
                }
            }
            return response
        

        def CollectOp()->Dict[List, Any]:
            response = {
                'plan' : {
                    'response' : 'SUCCESS',
                    'details':{ 
                        'Controller' : 'Action.runPlan()', 
                        'COMMAND' : 'COLLECT', 
                        'Location' : 'Default'
                    }
                }
            }
            return response       
        
        def BuildReport()->Dict[List, Any]:
            response = {
                'plan' : {
                    'headers' : 'run',
                }
            
            }
            return response    
        


        def Cleanup()->Dict[List, Any]:
            response : Dict[List, Any] = {
                'plan': '', 
                'headers' : '', 
                'package' : '', 
                'chunks' : '', 
                'labels' : '',
                'assets' : '', 
                'tokens' : ''
            }
            return response 
        
        def CollectRun()->Dict[List, Any]:
            response : Dict[List, Any] = {
                'plan': '', 
                'headers' : '', 
                'package' : '', 
                'chunks' : '', 
                'labels' : '',
                'assets' : '', 
                'tokens' : ''
            }
            return response 
        
        def CollectActions()->Dict[List, Any]:
            response : Dict[List, Any] = {
                'plan': '', 
                'headers' : '', 
                'package' : '', 
                'chunks' : '', 
                'labels' : '',
                'assets' : '', 
                'tokens' : ''
            }
            return response 
        

class MATRIX:

    ERROR_MSG:Dict[List,Any]={
        'result':'FAILURE', 
        'message':'[MATRIX] : Service failure - Configuration Level [Root]', 
        'payload': None
    }

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
        

    class Action(Enum):
        GENERATE: bool = True
        DOWNLOAD: bool = True
        EDIT: bool = True
        VIEW: bool = True
        CREATE : bool = True
        UPDATE : bool = True
        CHAT : bool = True
        DOCIMG : bool = True
        DETAILS : bool = True
        ACCEPT : bool = True
        ASSIGN: bool= True
        SCORE : bool = False
        DELETE : bool = False
        ANALYZE : bool = False


    class Region:

        def getTimestampLocal(tmz:str= "America/New_York")->str:
            from datetime import datetime
            from pytz import timezone
            fmt='%Y-%m-%dT%H:%M:%S'
            c=timezone(tmz)
            loc_dt= datetime.now(c)
            fd= loc_dt.strftime(fmt)
            return fd 
        
        def getRegionalEnv()->Dict[List,Any]:
            return {
                'tz': 'America/New_York', 
                'ln': 'English-USA', 
                'cc': 'US', 
                'cr': 'USD'
            }
        


class DOC:

    ERROR_MSG:Dict[List,Any]={
        'result':'FAILURE', 
        'message':'[DOC] : Service failure - Configuration Level [Root]', 
        'payload': None
    }

    class Timestamp:

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
        
    class SYS(Enum):
        from module.storage.config import STORAGE as Config
        AFS: Dict[List, Any] = Config.Default.getEnvVariables()

        def getRegionalEnv()->Dict[List, Any]:
            r = {
                'tz' : "America/New_York", 
                'ln' : 'English-USA', 
                'cc' : 'US', 
                'cr' : 'USD'
            }
            return r

        def getStorageVariable(self)->Dict[List, Any]:
            return self.AFS.values

    class Action(Enum):
        STORE: bool = True
        PROCESS:bool = True
        DOWNLOAD: bool = True
        EDIT: bool = True
        VIEW: bool = True
        LOAD: bool = True
        CHAT: bool = True 
        LIST: bool = True
        SEARCH : bool = True