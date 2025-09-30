from typing import Any, List, Dict, Text, Optional
from uuid import uuid4,UUID 
from pydantic import BaseModel 
from dataclasses import dataclass
from fastapi import UploadFile
from enum import Enum 

class Controller(BaseModel):
    workspace_id:str='default'
    client_id:str='default'
    engagement_id:str='default'
    batch_id:str='default'
    subject_id:uuid4=None 
    subject_list:List[UUID]=None


class File(Controller):
    files:List[UploadFile]=None 
    wasburl:List[str]=None 
    sfid:str=None
    metadata:Dict[List,Any]=None 
    collection_name:str=None 
    label:str=None 
    name:str=None
    type:str=None 


class evt(BaseModel):
    evt_name:str
    evt_id:UUID 

class status(BaseModel):
    status_code:str 
    status_type:Enum=['success','failure','pending','complete']
    status_message:str|None=None 
    

class error(Controller, evt):
    error_code:str|None=None 
    error_message:str|None=None 
    error_data:dict|None={}


class Document:

    class Body(BaseModel):
        content:dict|None=None 
        action:str|None=None 


    class Batch(BaseModel):
        batch_id:UUID
        batch_name:str 
        batch_type:str
        batch_status:Enum=['open', 'closed', 'sealed', 'archived']

    @dataclass 
    class Load(Controller, Body, evt):
        subjects:List[UUID]
        headers:dict|None=None 
        command:str|None=None 
        data:Dict[List,Any]={}
        message:str|None=None 
        dynamic_attributes:dict|None=None 

    @dataclass 
    class Search(Controller, Body, evt):
        sfid:List[UUID]
        headers:Dict[List,Any]
        command:str
        data:Dict[List,Any]={}
        message:str|None=None 
        dynamic_attributes:dict|None=None 

    @dataclass
    class Details(Controller, Body,evt):
        sfid:List[UUID]
        headers:Dict[List,Any]
        command:str
        data:Dict[List,Any]={}
        message:str|None=None 
        dynamic_attributes:dict|None=None 

    @dataclass
    class List(Controller, Body, evt):
        sfid:List[UUID]
        headers:Dict[List,Any]
        command:str
        data:Dict[List,Any]={}
        message:str|None=None 
        dynamic_attributes:dict|None=None 

    @dataclass
    class Select(Controller):
        sfid:List[UUID]
        headers:Dict[List,Any]
        command:str
        data:Dict[List,Any]={}
        message:str|None=None 
        dynamic_attributes:dict|None=None 



class Retrievers:

    class Chat:


        @dataclass
        class Question(Controller, evt):
            sfid:List[UUID]
            headers:Dict[List,Any]
            command:str
            data:Dict[List,Any]={}
            message:str|None=None 
            dynamic_attributes:dict|None=None 

        @dataclass 
        class Scoping(Controller, evt):
            sfid:List[UUID]
            headers:Dict[List,Any]
            command:str
            data:Dict[List,Any]={}
            message:str|None=None 
            dynamic_attributes:dict|None=None 

        
        @dataclass 
        class Persona(Controller, evt):
            sfid:List[UUID]
            headers:Dict[List,Any]
            command:str
            data:Dict[List,Any]={}
            message:str|None=None 
            dynamic_attributes:dict|None=None 