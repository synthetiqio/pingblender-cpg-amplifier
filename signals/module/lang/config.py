from enum import Enum
from typing import Dict, List, Any
import core.config as Core

class LANG:

    ERROR_MSG: Dict[List, Any] = {
                'result' : 'Failure', 
                'message' : '[Lang] : OpenAI Module Generic Failure', 
                'payload' : None
    }

    class Ext:

        def ErrorMSG():
            return Core.Env.ERROR_MSG
        
        def Env():
            return Core.Env
        
        def Sys():
            return Core.System
        
    
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
        

        
    '''
    Feature flag controls for services.
    '''
    class Action(Enum):
        SCOPE : bool = True
        PERSONA : bool = True
        QUESTION : bool = True
        TEST : bool = True
        LIST : bool = False
        DETAIL : bool = False