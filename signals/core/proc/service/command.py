from enum import Enum
from typing import Dict, List, Any
from core.proc.control import ConfigController as Config

class PROCommand:

    def __init__(
            self, 
            comm, 
            graph
    ):
        
        self.comm = comm
        self.meta: Dict[List, Any] = graph
        self.name = "[PROC] : Process Command Unit."


        self.process_id: str = None
        self.process_label: str = None
        self.process_origin: str = None
        self.process_owner: str = None
        self.process_scope: str = None
        self.process_state: str = None

        def _mapProcedure(self):
            pass

        def _getCommand(self)->str:
            command = self.comm 
            return command 
        

        async def Action(
                self, 
                graph
        )->Dict[List, Any]:
            self.error = Config.ERROR_MSG
            self.meta = self._mapProcedure(graph)
            response: Dict[List, Any] = {}
            casestr = self._getCommand()
            self.meta.update({'Action': casestr})

            try: 
                match str(casestr).upper():

                    case 'STATUS':
                        try:
                            result = {
                                    'result' : 'STATUS: Success', 
                                    'message': 'STATUS method is approved'
                                } 
                        except:
                            result = {

                                    'result' : 'STATUS: Success', 
                                    'message': 'STATUS method is not approved'
                                } 
                        response = result

                    case _:
                        try:
                            result = {

                                    'result' : 'DEFAULT: Success', 
                                    'message': 'DEFAULT method is approved'
                                } 
                        except:
                            result = {

                                    'result' : 'DEFAULT: Failure', 
                                    'message': 'FAILURE method is not approved.'
                                } 
                        response = result
            except ValueError as e:
                msg = f'Action {casestr} not found in the configuration as value error of {e} is returned'          
                self.error['payload'] = msg
                response.update(self.error)
                raise ValueError(msg)

            self.response = response
            return response