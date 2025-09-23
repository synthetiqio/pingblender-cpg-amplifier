from pydantic import BaseModel 
from dataclasses import dataclass
from typing import Dict, List, Any 
from uuid import uuid4

@dataclass
class Response(BaseModel):
    response: Dict[List,Any]