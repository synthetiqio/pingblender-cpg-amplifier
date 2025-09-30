from typing import Any, List, Dict, Text, Optional
from uuid import uuid4,UUID 
from pydantic import BaseModel 
from dataclasses import dataclass 
from fastapi import UploadFile
from enum import Enum 

class Controller(BaseModel):
    workspace_id:str='default'
    client_id:str='default'
    actvity_id:str='default'
    batch_id:str='default'
    subject_id:uuid4=None 
    subject_list:List[UUID]=None 


class Datasource(Controller):
    sourcefile_id:UUID 
    filepath:Text 
