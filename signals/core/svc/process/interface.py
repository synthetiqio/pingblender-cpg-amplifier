from module.file.config import MATRIX as ConfigController
from typing import Dict, List, Any
from uuid import uuid4

from core.proc.model.request import Request as RequestControl
from core.proc.model.response import Response as ResponseControl
from core.proc.control import(
    ProcessController as ActionControl, 
    ConfigController as ConfigControl, 
    InterfaceController as InterfaceControl
)


class Collect:

    class Package:

        
        def __init__(
                self,
                action:str, 
                meta:Dict[List,Any]=None,
        ):
            self.error=ConfigControl().ERROR_MSG
            self.m=meta 
            self.result=None 

        
        def exhibit(
                self,
        ):
            from module.core.proc.action import Queue
            check=Queue(metadata=self.m)
            result=check.Details()
            self.result=result
            return result 
        
        def responseHandler(
                self
        )->Dict[List,Any]:
            try:
                response:Dict[List,Any]=self.result
                response.update(self.m)
            except Exception as e:
                msg=f'Response Failed: {e}'
                self.error['payload']=msg
                response:Dict[List,Any]=self.error 
            return response 
        

class Interface:

    class LoadMeta:

        def __new__(
                cls,
                prid:str=uuid4(),
        ):
            msg="ProcessInterface Created for RUN COMMANDS"
            instance=super().__new__(cls)
            return instance 
        
        def __init__(
                self,
                prid:uuid4=None, 
                meta:Dict[List,Any]=None,
        ):
            self.file=prid 


        def fromProcessID(
                self
        )->Dict[List,Any]:
            pass 


    class getList:

        def __init__(
                self,
                prid:str
        ):
            self.fn=prid

        def allFiles(
                self,
        ):
            listed=InterfaceControl()
            result=''
            return result 


class ProcessAction:

    def __init__(
            self, 
            databody
    ):
        self.singleton= databody 
        configs= ConfigControl()

        self.timer= configs.Timestamp()
        self.locale:Dict[List, Any] = configs.Region()
        self.error:Dict[List, Any] = configs.ERROR_MSG()

        self.subj=databody['subject']
        self.comm:str=databody['command']
        self.attributes=databody['inputs']['data']
        self.response:ResponseControl={}
        self.request:RequestControl={}
        try:
            if 'data' in databody['inputs']:
                self.payload=self.meta['data']
                if 'dynamic_attributes' in self.payload:
                    self.attributes=self.payload 
                    self.response.update({'dynamic':self.attributes['dynamic_attributes']})
        except:
            self.attributes.update({
                'dynamic': 'Default'
            })
        self.response.update({
            'region':self.locale,
            'command':self.comm.upper(),
            'timer_start':self.timer.getTimestampLocal(self.locale['tz']), 
            'subject':self.subj

        })
        try:
            if 'prid' in self.attributes:
                self.prid=self.attributes['prid']
                self.metadata=Interface.LoadMeta(
                    prid=self.prid,
                    meta=self.singleton
                ).fromProcessID()

        except ChildProcessError as e:
            self.prid=None
            self.error['payload']=f'Process ID Not Found in Ledger: {e}'


    async def ActionHandler(
        self
    )->Dict[List, Any]:
        starttime= self.timer.getTimestamplocal(self.locale['tz'])
        self.response.update({'action_start': starttime})
        try:
            if self.check == True:
                print("PROCACTION: "+self.comm.upper())
                action= await ActionControl.runPlan(
                    command=self.comm.upper(),
                    params= self.singleton 
                )
                result= action
                stoptime= self.timer.getTimeStamplocal(self.locale['tz'])
                self.response.update({'action_complete': stoptime})
            else:
                stoptime= self.timer.getTimeStamplocal(self.locale['tz'])
                result.ConfigControl.ERROR_MSG.values
                self.response.update({'action_error': stoptime})
        except Exception as err:
            self.error['payload']= 'Action failed: {}'.format(err)
            result= self.error
        response:Dict[List, Any]= {
                'result' : 'SUCCESS', 
                'msg': {}, 
                'payload': result
            }
        self.result = response
        return response 
    
    async def ResponseHandler(
            self,
    )->Dict[List, Any]:
        handler:Dict[List, Any]={}
        try:
            handler= self.result
            handler.update(self.response)
        except:
            handler= self.error['payload'] = SystemError('RESPONSE Failed')
        return handler
