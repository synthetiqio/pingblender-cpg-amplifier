from fastapi import UploadFile
from pydantic import BaseModel
from dataclasses import dataclass 
from typing import Dict, List, Any
from uuid import uuid4

class Matrix(BaseModel):
    sfid:str
    data:list 

class Assign(BaseModel):
    sfid:str 
    data:list 

class DocManage(BaseModel):
    file:UploadFile=None
    documents:list=None 
    path:str=None 
    attr:Dict=None
    label:str=None
    type:str=None
    name:str=None 
    meta:Dict[List,Any]=None
    authorization:str=None
    subscription_key:str=None
    collection:str=None 

class ChatManage(BaseModel):
    documents:list=None 
    path:str=None 
    attr:Dict=None
    label:str=None
    type:str=None
    name:str=None 
    meta:Dict[List,Any]=None
    authorization:str=None
    subscription_key:str=None
    collection:str=None 

class AzureManage(BaseModel):
    documents:list=None 
    path:str=None 
    attr:Dict=None
    label:str=None
    type:str=None
    name:str=None 
    meta:Dict[List,Any]=None
    collection:str=None 

class ProcManage(BaseModel):
    file:UploadFile=None
    documents:list=None 
    prid:str=None
    batch_id:str=None 
    data:dict=None
    path:str=None 
    attr:Dict=None
    label:str=None
    type:str=None
    name:str=None 
    meta:Dict[List,Any]=None
    authorization:str=None
    subscription_key:str=None
    collection:str=None 
    background_tasks:list=None