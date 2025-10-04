#signals/rcm/core/service/file/interface.py
from typing import List, Dict, Any
from fastapi import UploadFile, File
from module.file.config import FILE as ConfigControl
from module.file.control import (
    Action as ActionControl, 
    Interface as InterfaceControl, 
    File as InputControl
    )


class FileLookup:

    class Package:


        def __init__(
                self, 
                action:str, 
                meta
            ):
            self.local:Dict[List, Any]=ConfigControl.SYS.getRegionalEnv()
            self.check= ConfigControl.Action[action.upper()].value
            self.timer= ConfigControl.Timestamp

            self.m= meta
            self.result= None


        def exhibit(
                self 
            ):
            from module.file.control import Retrieve
            check= Retrieve(metadata=self.m)
            result= check.Details()
            self.result= result
            return result
        

        def responseHandler(
                self
            ):
            response:Dict[List, Any]= self.result
            response.update(self.m)
            return response 
            
class FileInterface:

    class LoadMeta:

        def __new__(
                cls, 
                file : UploadFile, 
                meta : Dict[List, Any], 
                dest:str=None,
            ):
            msg:str= 'FILEObject Created for Commands'
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
            self.dest:str=dest 

        def fromFile(self):
            response : Dict[List, Any]
            if self.file == None:
                response = {"FILE : No File Provided"}
            else: 
                filename = self.file.filename
                goho:Dict[List, Any] = {"package" : {}}
                mmme = {"file" : filename }
                goho["package"] = mmme
                goho.update({"datasource" : 'upload'})
                response = goho
            return response
        
    class getList:

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
        

class GET_Handler:

    def __init__(
            self, 
            databody:Dict[List,Any]
        ):
        self.singleton=databody
        self.attributes=databody['inputs']
        self.metadata=databody

        self.response:Dict[List,Any]={}
        self.request:Dict[List,Any]={}

        self.locale=ConfigControl.SYS.getRegionalEnv()
        self.error:Dict[List,Any]=ConfigControl.ERROR_MSG
        self.timer=ConfigControl.Timestamp()

        self.subj=databody['subject']
        self.comm:str=databody['command']

        self.attributes=databody['inputs']
        self.response:Dict[List,Any]={}
        self.request:Dict[List,Any]={}

        if 'dynamic_attributes' in self.attributes:
            self.response.update({
                'dynamic': self.attributes['dynamic_attributes']
            })
        
        self.response.update({
            'region':self.locale, 
            'command':self.comm.upper(), 
            'timer_start':self.timer, 
            'subject':self.subj 
            })

        self.check=ConfigControl.Action[self.comm.upper()].value


    async def ActionHandler(
        self
    )->Dict[List, Any]:
        starttime= self.timer.getTimestampLocal(self.locale['tz'])
        self.metadata.update({'action_start': starttime})
        try:
            if self.check == True:
                print("GET Request Handler: "+self.check)
                action= await ActionControl.runPlan(
                    command=self.check,
                    meta=self.singleton 
                )
                result= action
                stoptime= self.timer.getTimestampLocal(self.locale['tz'])
                self.metadata.update({'action_complete': stoptime})
            else:
                stoptime= self.timer.getTimestampLocal(self.locale['tz'])
                result= ConfigControl.ERROR_MSG
                self.metadata.update({'action_error': stoptime})
        except Exception as err:
            self.error['payload']= 'Action failed: {}'.format(err)
            result= self.error['payload']
        response:Dict[List, Any]= {
                'result' : 'SUCCESS', 
                'message': {}, 
                'payload': result
        }
        self.result = response
        return response 

    async def ResponseHandler(
            self,
    )->Dict[List, Any]:
        handler:Dict[List, Any]={}
        try:
            handler=self.result
            handler.update(self.response)
        except:
            handler= self.error['payload'] = SystemError('RESPONSE Failed')
        return handler


class FileAction:


    def __init__(
            self, 
            action:str,
            file:UploadFile= None, 
            metadata:Dict[List, Any]= None, 
            terminus:str = None
        ):
        self.file = file 
        self.exec = action.upper()
        metadata = InputControl.MetadataController(
            meta=metadata
        ).clean_keys()
        self.metadata = metadata 
       
        #regional metadata appended 
        self.locale : Dict[List, Any] = ConfigControl.SYS.getRegionalEnv()
        self.metadata.update({
            'region' : self.locale
            })

        #timestamp controls created. 
        self.check = ConfigControl.Action[action.upper()].value
        self.timer = ConfigControl.Timestamp
        self.metadata.update({
            'command' : self.exec
            })
        self.metadata.update({
            'control' : self.timer.getTimestampLocal(
                self.locale['tz']
                )
            })

        if file != None:
            file.filename = file.filename.replace(' ','_')
            self.file = file 
            self.metadata.update({
                'file_meta' : FileInterface.LoadMeta(
                    file=file, 
                    meta=metadata
                    ).fromFile()
            })
            self.metadata.update({
                'event_metadata' : ActionControl.MetaData(
                    file, 
                    self.exec
                    )
            })


    async def ActionHandler(
        self
    )->Dict[List, Any]:
        starttime= self.timer.getTimestampLocal(self.locale['tz'])
        self.metadata.update({'action_start': starttime})

        if self.check == True:
            print("FILE ACTION: "+self.exec.upper())
            action= await ActionControl.runPlan(
                command=self.exec,
                file=self.file,
                meta= self.metadata 
            )
            result= action
            stoptime= self.timer.getTimestampLocal(self.locale['tz'])
            self.metadata.update({'action_complete': stoptime})
        else:
            stoptime= self.timer.getTimestampLocal(self.locale['tz'])
            result= ConfigControl.ERROR_MSG
            self.metadata.update({'action_error': stoptime})
        
        response:Dict[List, Any]= {
                'metadata':{
                    'details':result
                }
            }
        self.result = response
        return response 

    async def ResponseHandler(
            self,
    )->Dict[List, Any]:
        response:Dict[List,Any]=self.result 
        response.update(self.metadata)
        return response
        # handler:Dict[List, Any]={}
        # try:
        #     handler= self.result
        #     handler.update(self.response)
        # except:
        #     handler= self.error['payload'] = SystemError('RESPONSE Failed')
        # return handler

