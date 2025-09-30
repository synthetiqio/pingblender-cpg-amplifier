import json 
from requests import Response 
from typing import List, Dict, Any  
from core.auth.config import BADGE as Config 
from core.model.document import Embed as EM 

class BadgeController:

    class SettingStore:

        def __init__(self):
            self.token=''
            self.embedurl=''
            self.service=''
            self.version=''

        async def getSettings(
                self,
                target:Dict[List,Any]
        ):
            collection:Dict[List,Any]={}
            if target:
                collection.update({target['k']:target['v']})
            return {'params': collection}
        
    class ErrorResponse:
        

        def __init__(
                self,
                unit:str
        ):
            self.router = unit.upper()

        def Message(self):
            s:str=self.router 
            return s 
        
    class TokenController:

        def __init__(
                self, 
                command:str=None
        ):
            return 
        

    class EmbedController:

        class Format:

            def __init__(
                    self,
                    lines
            ):
                self.lines = lines 

            def to_dict(
                    self
            ):
                m={'lines':self.lines}
                return m 
            
            
            class Encode(json.JSONEncoder):
                def default(self,obj):
                    if isinstance(obj, BadgeController.EmbedController.Format):
                        return {'lines':obj.lines}
                    return super().default(obj)
                

            def embedStatic(
                    self,
                    endpoint:str,
                    token:str, 
                    payload
            )->Response:
                import requests 
                epk=Config.Default.EPTOKEN.value 
                try:
                    response=requests.post(
                        endpoint, 
                        json=payload, 
                        headers={
                            'Mimeo-graffiti-subscription':epk,
                            'Authorization':token, 
                            'Content-Type':"application/json",
                            'Content-Length': str(len(payload))
                        }
                    )
                    return response 
                except: 
                    BadgeController.ErrorResponse(unit='EmbedSTATIC')
                    raise 

    class AuthController:
        def __init__(
                self, 
                command:str=None
        ):
            from core.auth.action.standard import MeterAuth
            self.action=MeterAuth
            self.instruction=command.upper()

        def route(
                self,
        ):
            if self.instruction == 'LOGIN':
                result=self.action.authenticate()
            return result 


    
    class ModelController:


        def __init__(
                self,
                command:str=None,
        ):
            self.model=EM

        def getDefault():
            return Config.Default.DEFMODEL.value
        
        def getEmbeddingModel(
                self,
                name:str=None,
        ):
            if name != None:
                result=self.model[{name}].value
            else:
                result=self.getDefault()
            return 
        

    class ServiceController:

        def __init_(
                self,
                command:str=None,
        ):
            self.cfg=Config.Default.Settings()

        def getBaseUrl()->str:
            url=Config.Default.ENDPOINT.value
            return url 
        
        async def computeLoginEndpoint()->str:
            return 
        
        async def computeEndpoint()->str:
            return 
        
        async def computeLogEndpoint()->str:
            return 
        

        
