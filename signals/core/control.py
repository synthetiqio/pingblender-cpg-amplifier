from core.config import Network as Config
from typing import List, Dict, Any
from module.pretzl.parser import Read as ReaderService
from core.svc.cmd import BatchCommand as EntityAction


class EnvController: 

    class get:

        def __init__(
                self
        ): 
            pass 

        def urls(
                self, 
        ):
            """
            Sets up a default URL set and tests for new items
            added to the listing for complicated architectures.
            """
            li = Config.CL
            cors : list = self._default()
            if li != "":
                for i in li:
                    cors.append()
                return cors
            else:
                return cors

        def _default(self)->List[str]:
            listing = Config.Default['URLS'].value
            return listing


class APIUnit: 

    def __init__(
            self
    ): 
        pass 

    def runPlan(
            command: str, 
            params: Dict[List, Any]
    )->Dict[List, Any]:
        params.update({
            'command' : str(command)
        })
        ma = EntityAction(
            comm=command,
            graph=params
        )
        response: Dict[List, Any] = ma.Action(graph=params)
        return response
    

class ActionController:

    def __init__(
            self,
    ):
        pass 

    def runPlan(
            command : str, 
            params: Dict[List, Any]
    )->Dict[List, Any]:
        ma = EntityAction(
            comm=command, 
            graph=params
        )
        response : Dict[List, Any] = ma.Action(graph=params)
        return response
    
 
class ErrorResponse:

    def __init__(
            self, 
            err : str
    ):
        self.err = err

    def __str__(self):
        errobj = {
            'result' : 'FAILURE', 
            'message' : f'a CORE Controller module object has failed'
        }
        return errobj


class ConfigController:

    def __init__(
            self, 
            cfg : str = None, 
            evt : str = None, 
            proc : str = None, 
            state : str = None
    ): 
        #self.e = Evt()
        self.error : Dict[List, Any] = Config.ERROR_MSG

    def Region(self):
        return Config.Ext.Sys().SYS.getRegionalEnv()
    
    def Filesep(self):
        return Config.Ext.Env().Dock.FS
    
    def Timestamp(self):
        return Config.Ext.Sys().Timestamp
    
    def ErrorMSG(
            self, 
            msg : str = None,
    ):
        try:
            self.error['payload'] = msg
            return self.error
        except ErrorResponse as e:
            raise e