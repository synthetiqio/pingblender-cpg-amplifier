#/signals/core/svc/map - interface.py
#standard mapping interface for semi/structured data.
#devise on a matrix principle of coverage for fields/tables and listed entries.
from typing import Dict, List, Any 
from module.file.config import MATRIX as Config
from module.file.control import MatrixControl as Controller 
from module.file.control import MatrixAction as Action 

class matrix_interface:

    def __init__(
            self,
            action:str,
            format:str,
            metadata:Dict[List,Any]
    ):
        
        self.exec = action.upper()
        self.meta = metadata 
        self.graph = format 

        self.locale:Dict[List,Any]=Config.Region.getRegionalEnv()
        self.meta.update({'region':f'{self.locale}'})

        #timestamp controls engaged
        self.check = Config.Action[action.upper()].value #validate on bool flag.
        self.timer = Config.Region.getTimestampLocal(self.locale['tz'])
        self.meta.update({'command': self.exec})
        self.meta.update({'control': self.timer})

    def map_action(
            self,
    )->Dict[List,Any]:
        self.meta['inputs'] = Controller.Metadata(
            metadata=self.meta
        ).get_attr()
        start_time = self.timer 
        self.meta.update({
            'action_start':start_time
        })
        if self.check == True:
            print(f'MAPPING ACTION: {self.exec}')
            action = Controller.run_plan(
                command = self.exec,
                graph = self.graph, 
                meta = self.meta 
            )
            result = action
            stop_time=self.timer 
            self.meta.update({'action_complete':stop_time})
        else:
            stop_time = self.timer 
            result = Config.ERROR_MSG
            self.meta.update({'action_failed':stop_time})
        response:Dict[List,Any]={
            'response':{
                'result':result
            }
        }
        self.result = response 
        return self.result 


    def map_response(
            self,
    )->Dict[List,Any]:
        response : Dict[List,Any]=self.result 
        return response 