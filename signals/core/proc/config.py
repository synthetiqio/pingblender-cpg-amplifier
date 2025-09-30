from enum import Enum
from typing import Dict, List, Any
from core.config import CORE as SystemConfig

class PROC:

    ERROR_MSG: Dict[List, Any]= {
            'result' : 'Failure', 
            'message' : '[CORE - Sys Process] - an issue prevented execution of the PROC unit.',
            'payload' : None,
        }
    
    class Ext:

        def ErrorMSG():
            return SystemConfig.ERROR_MSG
        
        def Env():
            return SystemConfig.Env
        
        def Sys():
            return SystemConfig.System
        
    class Action(Enum):
        QUEUE:bool = True
        DETAIL:bool = True
        STATUS:bool = True
        UPDATE:bool = True
        PAUSE:bool = False
        CANCEL:bool = False
        