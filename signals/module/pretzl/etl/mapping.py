from typing import Dict, List, Any
from sqlalchemy.dialects.postgresql import JSONB
from module.pretzl.config import PRETZL as Localsys
from core.config import Env as Sys
from module.file.config import MATRIX as Dimension

from module.pretzl.parser import PRETZL, Read, Extract
from module.file.action import Map as Mark

class MatrixService:

    class Map: 

        def __init__(
                self, 
                filename : str, 
                graph : JSONB, 
                metadata : Dict[List, Any]
        ):
            self.metadata = metadata