from typing import Dict, List, Any
from uuid import uuid4, UUID
from module.lang.model.request import Request as RequestControl 
from module.lang.model.response import Response as ResponseControl 
from module.lang.control import (
    ChatController as ActionControl, 
    ConfigController as ConfigControl, 
    InterfaceController as InterfaceControl
)

class ChatConfig:

    class Package:

        def __init__(
                self, 
                action: str, 
                meta: Dict[List, Any] = None
        ):
            
            self.error = ConfigControl().error_msg
            self.m = meta 
            self.result = None

        def responseHandler(
                self
        ):
            try:
                response : Dict[List, Any] = self.result
                response.update(self.m)
            except Exception as e:
                msg=f'Response Failed due to {e}'
                self.error['payload'] = msg
                response = Dict[List, Any] = self.error
            return response 
        

class ChatInterface:

    class LoadMeta: 

        def __new__(
                cls, 
                id: str = uuid4(),
        ):
            msg = "ChatInterface Created for RUN COMMANDS"
            instance = super().__new__(cls)
            return instance
        

        def __init__(
                self, 
                sfid: uuid4=None, 
                meta: Dict[List, Any]= None, 
        ):
            self.sfile = sfid



        def fromProcessID(
                self
        )->Dict[List, Any]:
            pass


class ChatAction:

    def __init__(
            self, 
            databody
    ):
        self.singleton = databody 
        configs = ConfigControl()
        self.timer= ConfigControl.Timestamp()
        self.locale: Dict[List,Any]= configs.Region()
        self.error: Dict[List, Any]= configs.error_msg

        self.subj= databody['subject']
        self.comm : str = databody['command']
        self.attr:Dict[List,Any] = databody['inputs']['data']
        self.response: ResponseControl = {}
        self.request : RequestControl = {}

        if 'dynamic_attr' in self.attr:
            self.response.update({'dynamic': self.attr['dynamic_attr']})

        self.response.update({'region': self.locale})
        self.response.update({'command' : self.comm})
        self.response.update({'timer_start' : self.timer()})
        self.response.update({'subject' : self.subj})

        self.check = ConfigControl().checkAction(self.comm.upper())


    async def ActionHandler(
        self
    )->Dict[List, Any]:
        starttime= self.timer
        self.response.update({'action_start': starttime})
        try:
            if self.check == True:
                print("LANGCHAIN ACTION: "+self.comm.upper())
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
            handler= self.result
            handler.update(self.response)
        except:
            handler= self.error['payload'] = SystemError('RESPONSE Failed')
        return handler