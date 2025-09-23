from typing import Dict, List, Any
from module.file.control import Collect as C 
runner:Dict[List,Any]={}

class Get:

    def __init__(
            self,
            meta:Dict[List,Any]
    ):
        self.meta=meta
        self.runner=None 


    async def package(self):
        try:
            results=C(metadata=self.meta).getFilesList
            if len(results) > 0:
                for key,value in enumerate(results):
                    runner.update({key:value})
                response=runner
                return response 
        except Exception as err:
            response = {
                    'result':'FAILURE',
                    'message':'No files found in the source directory', 
                    'payload': f'Fired an error in the subroutine - details are: {err}'
                }
