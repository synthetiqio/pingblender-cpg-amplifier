import io, re 
from io import BytesIO 
from enum import Enum
from typing import Dict, List, Any 
from fastapi import UploadFile 
from module.azure.wasb.config import WASB as Config 



class WCommand:

    def __init__(
            self,
            comm:str,
            meta:Dict[List,Any], 
            file:UploadFile=None,
            path:str=None, 
            name:str=None, 
            spot:str=None
    ):
        
        self.comm = comm
        self.name:str=name
        self.file:UploadFile=None
        self.meta:Dict[List,Any]=meta 


        try:
            if path != None:
                self.path = path 
                self.file:BytesIO = io.BytesIO(path)


            if file !=- None:
                stu:UploadFile=file 
                self.meta['headers']=stu.content_type
                self.name:str=stu.filename
                self.file:BytesIO=io.BytesIO(stu.file.read())

            if 'file_obj' in meta:
                self.file:BytesIO=meta['file_obj']['file']

        except:
            self.file=None 
            raise FileExistsError('File is not available to process')
        
    def _getCommand(self)->str:
        try:
            command=self.comm 
            return command
        except:
            raise ValueError('No valid command was provided')
        


    async def Action(
            self,
            metadata:Dict[List,Any]=None
    )->Dict[List,Any]:
        data:Dict[List,Any]= {}
        response:Dict[List,Any]={}
        if hasattr(metadata['inputs'], 'dynamic_attributes'):
            response.update({'dynamic': metadata['inputs']['dynamic_attributes']})
        self.meta.update(metadata)
        casestr = self._getCommand()
        configs = self.meta 
        try:

            match str(casestr).upper():

                case 'LIST':
                    from module.azure.wasb.action.list import Standard as AC
                    try:
                        filectrl= await AC().ListBlobs()
                        response=filectrl
                    except:
                        response={
                                'result': 'FAILURE', 
                                'message': 'ListBlobs failed in command unit',
                                'payload': None
                        }

                case 'VIEWFILE':
                    from module.file.control import Retrieve as RL 
                    try:
                        ctrl=self.meta['subject']
                        runner:str=RL(metadata=self.meta).Url()
                        response={
                                'result':'SUCCESS',
                                'search': self.meta['subject'], 
                                'url': runner 
                        }
                    except:
                        response={
                                'result':'FAILURE',
                                'search': self.meta['subject'], 
                                'message': 'DownloadFile failed'
                        }


                case 'STORE':
                    from module.azure.wasb.client import Azure 
                    try:
                        filectrl= await Azure().Storing(
                            file=self.file, 
                            meta=self.meta
                        ).UploadFile()
                        response= filectrl
                    except:
                        response={
                                'result':'FAILURE',
                                'message': 'UploadFile failed', 
                                'payload': None
                        }


                case _:
                    response ={
                                'result':'FAILURE',
                                'message': 'No VALID ACTION was provided to Command', 
                                'payload': None 
                        }

        except ValueError:
            from module.azure.wasb.control import ErrorResponse
            response = ErrorResponse({ValueError})
        self.response = response 
        return response 
    
    