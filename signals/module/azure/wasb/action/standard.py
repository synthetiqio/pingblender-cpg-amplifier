import os 
from uuid import uuid4
from fastapi import UploadFile, File, Depends
from typing import Dict, List, Optional, Any

from module.azure.wasb.control import (
    AzureController, 
    ConfigController, 
    InterfaceController
)

import logging
logging.basicConfig(level=logging.INFO)

class Manage:

    class Source:

        def __init__(
                self,
                ctrl:uuid4=None, 
                file_list:list[uuid4,uuid4]=None,
                meta:Dict[List,Any]=None,
        ):
            self.coll=ctrl 
            self.list=file_list
            self.error=ConfigController().ErrorMSG
            self.result=None 

            self.meta=meta 
            self.meta.update({'event_state', str(__class__)})

        def load_result(
                self,
        ):
            try:
                self.result=AzureController(metadata=self.meta).load(self.coll)
            except Exception as e:
                self.error['payload']=str(e)
                self.result=self.error 
            return self.result 
        
    class Config:
        pass 