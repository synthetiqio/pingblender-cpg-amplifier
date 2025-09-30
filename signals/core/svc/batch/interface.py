#/signals/rcm/core/service/batch/interface.py
from typing import List, Dict, Any
from core.routes.config import API as ConfigControl
from core.routes.control import APIUnit as ActionControl 

class BatchAction:


    def __init__(
            self, 
            databody
    ):
        self.singleton= databody 
        self.procqueue= databody['queue']
        self.subj= databody['queue']['activity_id']
        self.response= {}

        self.timer= ConfigControl.Timestamp
        self.locale:Dict[List, Any] = ConfigControl.SYS.getRegionalEnv()
        self.error:Dict[List, Any] = ConfigControl.ERROR_MSG
        self.comm:str = databody['command']
        self.meta:Dict[List, Any]= databody['queue']
        
        self.response.update({'region': self.locale})
        self.response.update({'command': self.comm.upper()})
        self.response.update({'timer_start': self.timer.getTimestampLocal(self.locale['tz'])})
        self.response.update({'subject': self.subj})

        self.check= ConfigControl.Action[self.comm.upper()].value

    async def ActionHandler(
        self
    )->Dict[List, Any]:
        starttime= self.timer.getTimestamplocal(self.locale['tz'])
        self.response.update({'action_start': starttime})
        try:
            if self.check == True:
                print("BATCH ACTION: "+self.comm.upper())
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
                'result' : result, 
                'message': {}, 
                'payload': None
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