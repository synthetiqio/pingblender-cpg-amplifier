from typing import Dict, List, Any
from module.core.proc.config import PROC as Cfg

class ConfigController:

    def __init__(
            self, 
            cfg:str = None, 
            evt:str = None, 
            proc:str = None, 
            state:str = None,
    ):
        self.error: Dict[List, Any]= Cfg.ERROR_MSG

        def Region(self):
            return Cfg.Ext.Sys().SYS.getRegionalEnv()
        
        def filesep(self):
            return Cfg.Ext.Env().Dock.FS
        
        def Timestamp(self):
            return Cfg.Ext.Sys().Timestamp
        
        def ErrorMSG(
                self, 
                msg:str=None
        )->Dict[List, Any]:
            self.error['payload'] = msg
            return self.error
        
        def checkAction(
                self, 
                action:str
        ):
            try:
                check = Cfg.Action[action.upper()].value
            except:
                msg = f'Action {action} not found in configuration'
                self.error['payload']= msg
                check = self.error
            return check
        


class InterfaceController:

        def __init__(
                self, 
                facet:str = None, 
                params:Dict[List, Any]=None
        ):
            self.error= Cfg().ERROR_MSG

        async def checkInterface(
                self, 
                interface:str
        ):
            try:
                check= Cfg.Action[interface.upper()].value
            except ValueError as e:
                msg = f'Interface {interface} not found in configuration'
                self.error['payload'] = msg
                check = self.error
            return check
        

class ProcessController:

    def __init__(
            self, 
        ):
        pass

        self.error = Cfg().ERROR_MSG

    def runPlan(
            self, 
            command:str,
            params:Dict[List, Any]
    )->Dict[List, Any]:
        from core.proc.service.command import PROCommand as Action
        try:
            ma = Action(
                comm=command, 
                graph=params,
            )
            response:Dict[List, Any] = ma.Action(graph=params)
        except ValueError as e:
            msg = f'[PROC]:Process {e} not found in configuration'
            self.error['payload'] = msg
            response = self.error
        return response