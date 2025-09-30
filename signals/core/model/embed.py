from enum import Enum
from typing import List, Optional
import uuid
from pydantic import BaseModel as PydanticBM
from dataclasses import dataclass

class EmbedBase(PydanticBM):
    class Config:
        arbitrary_types_allowed = True

@dataclass 
class EmbedModel(Enum):
    DEFAULT = "text-embedding-3-small"  
    LLAMA = "mini-llama"
    TXT_ADA_001 = "text-ada-001"
    SIM_ADA_001 = "text-similarlity-ada-001"
    EMB_ADA_002 = "text-embedding-ada-002"
    SIM_CURIE_001 = "text-similarity-curie-001"
    TXT_CURIE_001 = "text-curie-001"
    TXT_DVINCI_002 = "text-davinci-002"
    TXT_DVINCI_003 = "text-davinci-003"
    COD_DVINCI_002 = "code-davinci-002"