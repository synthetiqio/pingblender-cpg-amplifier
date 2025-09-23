# signals/rcm/module/file/action/subroutine/local.py
#checked and validated 17 January 2025
from module.file.control import File as FLO
#TODO: add file manager level dynamic controls to positions.

from module.pgvector.control import Collection as R 
from module.storage.azure.wasb.client import Azure as AzureClient
from typing import List, Dict, Any 
from fastapi import UploadFile 

class Put:

    def __init__(
            self, 
            blob_name:str,
            metadata:Dict[List,Any]=None 
    ):
        self.blob =blob_name
        self.file:UploadFile=None 
        self.local=None 

    async def load(self):
        f=await self.set_file()
        return f
    

    async def set_file(self):
        import os 
        self.filename = self.blob.split('data-in/')[1]
        os.makedirs(os.path.dirname(
            self.filename
        ), 
        exist_ok=True
        )
        blob_client= await AzureClient().Manage().getBlobFileData(
            blobname=self.blob
        )
        with open(f'{self.filename}', 'wb') as fdata:
            fdata.write(blob_client)
            fdata.close()
        return f'{self.blob}'
    
