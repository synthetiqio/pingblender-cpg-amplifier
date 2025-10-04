from typing import Dict, List, Any
from module.lang.config import LANG as Config

class ConfigController:


    def __init__(
            self, 
            cfg : str = None, 
            evt : str = None, 
            proc : str = None, 
            state : str = None
    ):
        
        self.error_msg : Dict[List, Any] = {}

    def Region(self):
        return Config.SYS.getRegionalEnv()
        
    def Filesep(self):
        return Config.Ext().Env()
        
    def Timestamp(self):
        return Config.get_timestamp()
        
    def ErrorMSG(
            self,
            msg:str=None 
    ):
        self.error_msg = Config.ERROR_MSG
        if msg is not None:
            self.error_msg.update({'payload':f'{msg}'}) 
        return self.error_msg
        

    def checkAction(
            self, 
            action:str
    ):
        try:
            check=Config.Action[action.upper()].value 
        except ValueError as err:
            msg=f'Action {action} not found in configurations.'
            self.error_msg.update({'payload':f'{msg}'}) 
            check = self.error_msg 
        return check 
        

class InterfaceController:

    def __init__(
            self, 
            facet:str=None, 
            params:Dict[List,Any]=None 
    ):
        self.error=Config().ERROR_MSG 

    def checkInterface(
                self, 
                interface:str
        ):
            try:
                check=Config.Action[interface.upper()].value 
            except ValueError as err:
                msg=f'Interface {interface} not found in configurations.'
                self.error['payload'] = msg 
                check = self.error 
            return check 
    
class ChatController:

    def __init__(
            self, 

    ):
        pass 

    def runPlan(
            command:str, 
            params:Dict[List,Any]
    )->Dict[List,Any]:
        response:Dict[List,Any]={}
        from module.lang.service.command import CHATComand as Action 
        try:
            ma=Action(
                comm=command, 
                graph=params 
            )
            response=ma.Action(graph=params)
        except Exception as err:
            response={
                    'result':'FAILURE', 
                    'message':'An Error occured while processing the queue ',
                    'payload':f'More information: ERROR CODE = {err}'
                }
        return response 