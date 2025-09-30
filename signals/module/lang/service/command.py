from enum import Enum
from typing import Dict, List, Any
from module.lang.control import ConfigController as Config

class CHATComand:

    def __init__(
            self, 
            comm: str, 
            graph: str
    ):
        
        self.comm = comm
        self.meta : Dict[List, Any] = graph
        self.name : str = '[Lang] - Chat Service Interface Command Interpreter'

        self.process_id : str = None
        self.process_label : str = None
        self.process_origin : str = None
        self.process_owner : str = None
        self.process_scope : str = None
        self.process_state : str = None

    def _getCommand(self)->str:
            command = self.comm 
            return command
    
    async def Action(
              self, 
              graph
    )->Dict[List, Any]: 
         
         self.error = Config.ERROR_MSG
         self.meta = self._mapProcedure(graph)
         response: Dict[List, Any] = []
         casestr = self._getCommand()
         self.meta.update({"Action": casestr})

         try: 
              match str(casestr).upper():
                   case 'STATUS':
                        try:
                             result = {
                                       'result' : '', 
                                       'message' : '', 
                                       'payload' : ''
                             }
                        except:
                             result = {
                                       'result' : '', 
                                       'message' : '', 
                                       'payload' : ''
                             }
                        response = result
         except ValueError as e:
              msg = f'Action {casestr} not found in configuration and a ValueError of {e} is returned'
              self.error['payload'] = msg
              response.update(self.error)
              raise ValueError(msg)
         

         self.response = response 
         return response

        

                   