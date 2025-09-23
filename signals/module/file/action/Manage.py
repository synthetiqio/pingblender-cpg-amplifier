from fastapi import UploadFile
from typing import Dict, List, Any
from uuid import UUID

class Position: 

    def __init__(
            self, 
            plan : Dict[List, Any], 
            file: UploadFile, 
            source: str = None, 
            target: str = None, 
            uuid : UUID = None
        ):     
        self.sourcecontrol = source 
        self.plancontrol = plan 
        self.filecontrol = file
        self.targetcontrol = target
        self.entitycontrol = uuid


    def _setCurrentLocation(
            self,
            newurl : str = None
        )->str:
        self.source = newurl 
        return self.source 
    

    def _checkPlan(
            self
        )->bool:
        plan = self.plancontrol 
        return True
    
    
    def moveFile(
            self, 
            target: str
        )->Dict[List, Any]:
        plan = self.plancontrol
        file = self.filecontrol