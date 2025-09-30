from pydantic import BaseModel
from dataclasses import dataclass
from typing import Dict, List, Any

#dataclass for requests
@dataclass
class Request(BaseModel):
    request: Dict[List, Any]


    