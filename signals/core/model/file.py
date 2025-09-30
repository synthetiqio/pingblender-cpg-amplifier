from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class BaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True