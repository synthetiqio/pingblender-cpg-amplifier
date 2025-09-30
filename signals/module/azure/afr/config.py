import os 
from enum import Enum 
from typing import Dict, List, Any 

class AFR:

    class Default:
        AFR_ENDPOINT:str=os.getenv('AFR_ENDPOINT') or None
        AFR_API_KEY:str=os.getenv('AFR_API_KEY') or None 


    class Action:
        READ:bool=True