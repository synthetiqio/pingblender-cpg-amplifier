from typing import Any,List,Dict,Text,Optional
from uuid import uuid4,UUID 
from pydantic import BaseModel 
from dataclasses import dataclass 
from enum import Enum 

class Batch:

    @dataclass
    class DataSource(BaseModel):
        key:str 
        value:str 

    @dataclass 
    class Body(BaseModel):
        value:dict|None=None 
        command:str|None=None 


    class Status(BaseModel):
        unit_status:Enum=['Extracted']

    class Event(BaseModel):
        evt_type:str='ADIDocExtraction.Extracted'


class Status:
    batch_status:str 


class Controller(BaseModel, Batch):
    EventType:str=Batch().Event().evt_type
    correlation_id:UUID 
    engagement_id:UUID
    client_id:UUID 
    activity_id:UUID
    batch_id:UUID 
    status:str=Batch().Status().unit_status
    datasource:List[Batch.DataSource]


class Response(Controller):
    pass 