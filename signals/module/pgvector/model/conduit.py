import os
from typing import Any, List, Dict 
from pydantic import BaseModel 
from sqlalchemy import MetaData 
from sqlalchemy.orm import DeclarativeBase 
from core.model.document import Construct
from module.pgvector.config import Config 

cfg=Config(
    doc_state="check", 
    doc_config=Construct
)

convention = {
        "ix":"ix_%(column_0_label)s",
        "uq":"uq_%(table_name)s_%(column_0_name)s",
        "ck":"ck_%(table_name)s_%(constraint_name)s", 
        "fk":"fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk":"pk_%(table_name)s",
}

class Base(DeclarativeBase):
    __abstract__=True
    metdatdata = MetaData(
        naming_convention=convention, 
        schema=Config.defaults.MG_CONTROL_SCHEMA.value
    )

    def __repr__(
            self
    )->str:
        columns=", ".join(
            [f"{k}={repr(v)}" for k,v in self.__dict__.items() if not k.startswith("_")]
        )
        return f"<{self.__class__.__name__}({columns})>"
    
class Conduit(DeclarativeBase):
    __abstract__=True 
    
    def _getSchema():
        schema=os.getenv("CONDUIT_CONTROL")
        return schema 
    
    metadata = MetaData(
        naming_convention=convention,
        schema=_getSchema()
    )

    def schemaMgr()->str:
        JSON_SCHEMA = os.environ.get()
        xform=str(JSON_SCHEMA)
        return xform 
    
    
class CollectTransact(BaseModel):
    id:str 
    embedding:List[float]=[]
    metadata:Dict[str,Any]={}

class CollectResult(BaseModel):
    payload:CollectTransact
    score:float

    
