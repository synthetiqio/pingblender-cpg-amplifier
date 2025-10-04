from typing import List, Dict, Any
from fastapi import UploadFile
from uuid import uuid4
from io import BytesIO

from module.file.config import DOC as ConfigControl 
from core.model.request import DocManage as RequestControl 
from module.file.response.document import Response as ResponseControl 
from module.file.control import (
    View as MetaControl, 
    Document as ActionControl,
    Interface as InterfaceControl
)

class Lookup:
    class Package:

        def __init__(
                self, 
                action:str, 
                meta
            ):
            self.local : Dict[List, Any] = ConfigControl.SYS.getRegionalEnv()
            self.check = ConfigControl.Action[action.upper()].value
            self.timer = ConfigControl.Timestamp

            self.m = meta
            self.result = None


        def exhibit(
                self 
            ):
            from module.file.control import Retrieve
            check = Retrieve(metadata=self.m)
            result = check.Details()
            self.result = result
            return result
        

        def responseHandler(
                self
            ):
            response : Dict[List, Any] = self.result
            response.update({self.m})
            return response 
            
class Interface:
    class Meta:

        def __new__(
                cls, 
                file : UploadFile, 
                meta : Dict[List, Any], 
                dest:str=None,
            ):
            msg=str(f'Document interface created for COMMANDS')
            instance = super().__new__(cls)
            return instance
            
        def __init__(
                self, 
                file : UploadFile = None, 
                meta : Dict[List, Any] = None, 
                dest:str=None 
            ):
            self.file = file
            self.meta = meta


        def fromSubject(self)->str:
            if 'subject' in self.meta:
                sfid=self.meta['subject']
                file=MetaControl().Document(params=self.meta).getLocation()
                return file 
            else:
                return str(f'No Location Available.')
            

        def fromDocument(self):
            response:Dict[List,Any]={}
            if self.file == None:
                response.update({"file":"No File Provided."})

        def File(self):
            response : Dict[List, Any]={}
            if self.file == None:
                response.update({"FILE : No File Provided"})
            else: 
                filename = self.file.filename
                goho:Dict[List, Any] = {"package" : {}}
                mmme = {"file" : filename }
                goho["package"] = mmme
                goho.update({"datasource" : 'upload'})
                response = goho
            return response
        
    class List:

        def __init__(
                self, 
                filename : str
            ):
            self.fn = filename 

        def allFiles(
                    self
            ):
            lister = InterfaceControl()
            result = lister.Manager.getAllFilesStore()
            return result
        


class Action:

    def __init__(
            self,
            databody
    ):
        self.singleton=databody
        self.attributes={}

        self.timer=ConfigControl.Timestamp
        self.locale:Dict[List,Any]=ConfigControl.SYS.getRegionalEnv()
        self.error:Dict[List,Any]=ConfigControl.ERROR_MSG


        self.sub=databody['subject']
        self.comm:str=databody['command']
        self.meta:Dict[List,Any]=databody['inputs']

        self.response:ResponseControl={}
        self.request:RequestControl={}

        try:
            if 'data' in databody['inputs']:
                self.payload=self.meta['data']
                if 'dynamic_attr' in self.payload:
                    self.attributes=self.payload
                    self.response.update({
                        'dynamic': self.attributes['dynamic_attr']
                    })
        except:
            self.attributes.update({'dynamic':'Default'})
        
        #ready timer and metadata for transition to active event.
        self.response.update({
            'region':self.locale, 
            'command':self.comm.upper(), 
            'timer_start':self.timer, 
            'subject':self.sub 
            })

        self.check=ConfigControl.Action[self.comm.upper()].value

    async def ActionHandler(
            self
    )->Dict[List,Any]:
        self.response:Dict[List,Any]={}
        #begins logical execution of the command.
        starttime=self.timer.getTimestampLocal(self.locale['tz'])
        self.response.update({'action_start':starttime})
        try:
            if self.check == True:
                print("DOCACTION"+self.comm.upper())
                action = await ActionControl.runPlan(
                    command=self.check,
                    params=self.singleton,
                )
                result=action 
                #completes action and rings the bell.
                stoptime = self.timer.getTimestampLocal(self.locale['tz'])
                self.response.update({
                    'action_complete':stoptime
                })
            else:
                stoptime=self.timer.getTimestampLocal(self.locale['tz'])
                result=ConfigControl.ERROR_MSG.values 
                self.response.update({
                    'action_error': stoptime
                })
        except Exception as err:
            self.error['payload']='Action Failed : {}'.format(err)
            result=self.error['payload']
        response:Dict[List,Any]={
            'result' : result 
        }
        self.result=response 
        return response 
    

    async def ResponseHandler(
            self
    )->Dict[List,Any]:
        try:
            response:Dict[List,Any]=self.result 
            response.update(self.response)
        except:
            out:str='FAILURE'
            msg:str=SystemError('DOCACTION - ResponseHandler Failure')
            payload = self.error['payload']
            response = {
                    'result': out, 
                    'msg':msg, 
                    'payload':payload 
                }
        return response 






# class Action:

#     def __init__(
#             self, 
#             action:str,
#             file:UploadFile= None, 
#             metadata:Dict[List, Any]= None, 
#             terminus:str = None
#         ):

#         self.exec = action.upper()
#         self.file = file 
        
#         metadata = InterfaceControl.Metadata(meta=metadata).cleanKeys()
#         self.metadata = metadata
#         if 'file' not in metadata:self.file=None
        
        
#         self.error:Dict[List,Any]=ConfigControl.ERROR_MSG
        
#         #regional metadata appended 
#         self.locale : Dict[List, Any] = ConfigControl.SYS.getRegionalEnv()
#         self.metadata.update({'region' : self.locale})

#         #timestamp controls created. 
#         self.check = ConfigControl.Action[action.upper()].value
#         self.timer = ConfigControl.Timestamp
#         self.metadata.update({'command' : self.exec})
#         self.metadata.update({'control' : self.timer.getTimestampLocal(self.locale['tz'])})

#         if file != None:
#             file.filename = file.filename.replace(' ','_')
#             self.file = file 
#             self.metadata.update({'file_meta' : Interface.Meta(file=file, meta=metadata).File()})
#             self.metadata.update({'event_metadata' : ActionControl.MetaData(file, self.exec)})


#     async def ActionHandler(
#         self
#     )->Dict[List, Any]:
#         starttime= self.timer.getTimestampLocal(self.locale['tz'])
#         self.metadata.update({'action_start': starttime})
#         try:
#             if self.check == True:
#                 print("DOCUMENT Interface-> ACTION: "+self.exec.upper())
#                 action= await ActionControl.runPlan(
#                     command=self.exec.upper(),
#                     meta= self.metadata 
#                 )
#                 result= action
#                 stoptime= self.timer.getTimestampLocal(self.locale['tz'])
#                 self.metadata.update({'action_complete': stoptime})
#             else:
#                 stoptime= self.timer.getTimestampLocal(self.locale['tz'])
#                 result= ConfigControl.ERROR_MSG
#                 self.metadata.update({'action_error': stoptime})
#         except Exception as err:
#             self.error['payload']= 'Action failed: {}'.format(err)
#             result= self.error['payload']
#         response:Dict[List, Any]= {
#                 'result' : 'SUCCESS', 
#                 'message': {}, 
#                 'payload': result
#             }
#         self.result = response
#         return response 

#     async def ResponseHandler(
#             self,
#     )->Dict[List, Any]:
#         handler:Dict[List, Any]={}
#         try:
#             handler= self.result
#             handler.update(self.response)
#         except:
#             handler= self.error['payload'] = SystemError('RESPONSE Failed')
#         return handler
