from pydantic import BaseModel
from dataclasses import dataclass 
from typing import Dict, List, Any

@dataclass 
class Response(BaseModel):
    response : Dict[List,Any]