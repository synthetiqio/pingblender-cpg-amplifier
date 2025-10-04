from enum import Enum
from uuid import uuid4
from typing import Any, Optional, Dict, List
#from module.core.evt.ctrl import EventController as Evt 
#from azure.core.credentials import AzureSasCredential
from module.azure.wasb.client import Azure
from module.azure.wasb.config import WASB 
from module.pretzl.model.reader import Router

class AzureController:

    def __init__(
            self,
            metadata:Dict[List,Any]=None
    ):
        self.orig=metadata
        self.error=WASB().ERROR_MSG
        if 'file' in metadata:
            self.file=metadata['file']
        if 'path' in metadata:
            self.path=metadata['path']
        if 'sfid' in metadata:
            self.sfid = metadata['sfid']

    async def getWasbAddr(
            self, 
            sfid:str=None, 

    )->str:
        from module.pgvector.control import Collection 
        try:
            st= await Collection.Entity.Query(
                lookup_key=sfid
            ).bySfid()
            return st
        except:
            raise ErrorResponse("getWasbAddr Failed in AzureController")
        

    async def getList(
            self
    ):
        try:
            st= await Azure.Manage().List.items()
            return st
        except:
            raise ErrorResponse("Listing Blobs failed in AzureController")
        
    async def load(
            self, 
            coll:uuid4=None,
    ):
        filename=f'{coll}.json'
        c= await Azure.Manage.getBlobFile(filename=filename)
        return c
    

    async def ListBlobs(
            self,
    ):
        try:
            st= await Azure.Manage().List.items()
            return st 
        except:
            raise ErrorResponse("ListBlobs Failed in AzureController.")
        

    async def load(
            self,
            coll:uuid4=None
    ):
        filename=f'{coll}.json'
        c= await Azure.Manage.getBlobFile(file_name=filename)
        return c
    
    async def GetFileFromStorage(
            self
    ):
        try: 
            st = await Azure.Manage(
                file=self.file
            ).downloadFile()
            return st 
        except:
            return ErrorResponse("[STORAGE] : WASB - DownloadFile failed in AzureController.")       

    async def PositionToBlobStorage(
        self
    )->Dict[List,Any]:
        try:
            st = await Azure.Moving(
                file=self.file 
            ).setBlobPosition()
            return st 
        except:
            return ErrorResponse("UploadFile Failed")

        
    async def FileToBlobStorage(
            self, 
            overwrite=False
    ):
        try:
            st= await Azure.Storing(
                file=self.file 
            ).UploadFile(overwrite=overwrite)
            return st 
        except Exception as err:
            return ErrorResponse(f'UploadFile Failed: {err}')
        



class DeeplinkController:

    def __init__(
            self,
            metadata:Dict[List,Any]
    ):
        self.m=metadata
        #default enabled 
        self.u='graffiti-json'

    def _getFirstChild(
            self
    ):
        try:
            st=self.m['headers'].get('Mimeo-graffiti-susbcription')
            return st 
        except:
            return 'subscription-id'
        
    def _getSecondChild(
            self,
    ):
        try: 
            st=self.m['headers'].get('engagementID')
            return st 
        except:
            return 'engagement-id'
        
    def _getThirdChild(
            self,
    ):
        try:
            st=self.m['headers'].get('correlationID')
            return st
        except:
            return 'correlation-id'
        

    def path(
            self
    ):
        try:
            pattern=[
                self._getFirstChild(),
                self._getSecondChild(), 
                self._getThirdChild(),
            ]
            path_sep='/'
            wasburl_str=path_sep.join(pattern)
            return wasburl_str
        except:
            raise ErrorResponse('Path failed to render')



class ClientController:

    def __init__(
            self, 

    ):
        pass


    def getSasToken(
            self, 
            bloburl:str=None 
    ):
        ac=Azure.Manage().downloadURL(url=bloburl)
        return ac 
    
    def closeClient(object):
        object.close()
        return True 

class SetupController:

    def __init__(
            self,
    ):
        pass 

        self.container_list=[]

    def setupContainers(self):
        try: 
            st=Azure.Container(
                name="graffiti-blackbook", 
                permit={
                    'read':True,
                    'write':True, 
                    'delete':True
                }
            ).create()
            return st 
        except:
            raise ErrorResponse('Setup Containers failed')

class BlobController:

    def __init__(
            self, 
            filename=str 
    ):
        
        #self.e=Evt()
        from module.pretzl.model.reader import Router
        self.route=Router()
        self.name=filename
        self.ext= filename.split('.')[1]

        self.wasbpath:str=None
        self.container:str=None 
        self.token:str=None 

    def setWasbPath(
            self, 
            path:str='PRETZL', 
            dyno:dict='Empty'
    ):
        strext:str=self.ext 
        wasbpath=None 
        droot=WASB.ROUTES["DATA_IN"].value 
        name=self.name.split('.')[0]
        try:
            if self.ext=='pdf':
                wasbpath=f'{droot}/{path}/PARSABLE_PDF/{name}.{strext}'
            if self.ext=='csv':
                wasbpath=f'{droot}/{path}/CSV_TXT/{name}.{strext}'
            else:
                wasbpath=f'{droot}/{name}.{strext}'
        except:
            WASB.ERROR_MSG['payload']='An error occured when setting WASB path'
            return WASB.ERROR_MSG
        print("[STORAGE] Azure Blob (WASB) path set to: ", wasbpath)
        return wasbpath 
    

    def get(
            self, 

    ): 
        wp=self.setWasbPath()
        st=ClientController().getSasToken(
            bloburl=wp
        )
        convert=str(st)
        return convert 
    

class InterfaceController:
    pass 


class ConfigController:

    def __init__(
            self,
            cfg:str=None, 
            evt:str=None, 
            proc:str=None, 
            state:str=None 
    ):
        self.error=WASB.ERROR_MSG

    def Region(self):
        return WASB.Ext.Sys().SYS.getRegionalEnv()
    
    def Filesep(self):
        return WASB.Ext.Env().Dock.FS 
    
    def Timestamp(self):
        return WASB.Ext.Sys().Timestamp
    
    def ErrorMSG(
            self, 
            msg:str=None
    )->Dict[List,Any]:
        try:
            self.error['payload']=msg
            return self.error
        except Exception as e:
            raise e 
        
    def checkAction(
            self, 
            action:str 
    ):
        try:
            check = WASB.Action[action.upper()].value
        except:
            msg=f'Action {action} not found in the Configuration Vars'
            self.error['payload']=msg
            check = self.error 
        return check 

    
class EventController:

    def __init__(
            self,
    ):
        #self.e = Evt()
        pass

    def runPlan(
            command:str, 
            params:Dict[List,Any]
    )->Dict[List,Any]:
        response:Dict[List,Any]={}
        from module.azure.wasb.service.command import WCommand as WAction
        try:
            ma = WAction(
                comm=command, 
                meta=params)
            response=ma.Action(metadata=params)
        except:
            response= {
                    'result':'FAILURE',
                    'message': 'WASB EventController Failed', 
                    'payload': None

            }
        return response 


class ErrorResponse: 

    def __init__(
            self,
            err:str 
    ):
        self.err=err

    def __str__(self):
        erroobj={
                'result':'FAILURE', 
                'message': f'Azure Storage Blob Error indicates {self.err}'
        }
        return erroobj 


# class Storage(Control):


    # class WASB:


    #     class BlobController(HasTimestamp):
