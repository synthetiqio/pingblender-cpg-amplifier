from typing import Any, Dict, List 
from pgvector.sqlalchemy import Vector
from .conduit import Base 
from sqlalchemy import String, text 
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import AbstractConcreteBase 
from sqlalchemy.orm import Mapped, mapped_column 

class VectorCollectTable(AbstractConcreteBase, Base):
    __abstract__=True 

    id:Mapped[str]=mapped_column(
        "id", 
        String, 
        autoincrement=False, 
        nullable=False, 
        unique=True, 
        primary_key=True
    )

    def embedding(cls)->Mapped[List[float]]:
        return mapped_column(
            "embedding", 
            Vector(), 
            nullable=False 
        )
    
    metadatas:Mapped[Dict[str, Any]]=mapped_column(
        'metadata', 
        JSONB, 
        server_default=text("'{}'::jsonb"), 
        nullable=False
    )