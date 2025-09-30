from module.azure.wasb.control import AzureController as Operator, ErrorResponse
from typing import Dict,List,Any 

class Standard:

    def __init__(
            self, 
            action:str=None, 
            meta:Dict[List,Any]=None 
    ):
        pass 

    async def ListBlobs(
            self 
    ):
        try:
            st= await Operator().ListBlobs()
            return st 
        except:
            return ErrorResponse('ListBlobs Failed')
        
    async def GetFileFromStorage(
        self
    ):
        try:
            st = await Operator().GetFileFromStorage()
            return st
        except:
            return ErrorResponse('DownloadFile Failed')
        

    async def FileToBlobStorage(
            self
    ):
        try:
            st= await Operator().FileToBlobStorage()
            return st
        except:
            return ErrorResponse('FileToBlobStorage Failed')
        


    async def PositionToBlobStorage(
            self
    ):
        try:
            st= await Operator().PositionToBlobStorage()
            return st
        except:
            return ErrorResponse('PositionToBlobStorage Failed')
        

    async def DeleteBlob(
            self, 
    ):
        try:
            st= await Operator().DeleteBlob()
            return st
        except:
            return ErrorResponse('DeleteBlob eFailed')
        

    async def DeleteContainer (
            self
    ):
        try:
            st= await Operator().DeleteContainer()
            return st
        except:
            return ErrorResponse('DeleteContainer eFailed')