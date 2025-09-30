from core.auth.config import (
    Route, 
    METER as MeterConfig
)
from module.robot.action.meter import Charon
import json, os, jwt
import requests
from fastapi import HTTPException
from core.model.embed import Embed
from core.config import CORE as Config

MODULE_ROUTE=Route.getRoute()
class AuthController:

    def __init__(
            self,
            auth_token:str=None, 
            secret:str=None,
    ):
        self.secret:str=secret 
        self.auth_token:str=None, 
        self.route=MODULE_ROUTE 

        self.component_name:str=""
        self.user_id:str=''
        self.email_address:str=''
        self.roles:list=[]

    def testPosition(p):
        isExist=os.path.exists(p)
        return isExist
    
    def readJSON(filename):
        with open(filename) as data_file:
            data = json.load(data_file)
        return data 
    
    def createDirectory(p):
        try:
            os.makedirs(p)
        except OSError:
            pass 
        return True 
    
    def _readConfigFile(
            self,
            filename:str
    ):
        with open(self.route+'params/'+filename, 'r') as file:
            data=file.read().replace('\n','')
        return data 
    

    def _createSessionTime():
        import calendar 
        import time 
        current_GMT=time.gmtime()
        ts=calendar.timegm(current_GMT)+1800  
        return ts 
    

    def _readPrivateKey(
            self,
    ):
        key:str=''
        if self.secret != None:
            key=self.secret
        else:
            key=self._readConfigFile('private.key')
        return key
    

    def _buildLocalOS(self):
        roots:list=['assets','artifacts','log']
        try:
            for root in roots:
                path=root 
                isExist=os.path.exists(path)
                if not isExist:
                    os.makedirs(path)
            return True
        except:
            raise Exception("OS System Error: Unable to create directories")
        
    def _createParamsJSON(
            self,
            data,
            jf
    ):
        filename=jf
        json_obj=data 
        with open(self.route+'params/'+filename+'.json', 'w') as outfile:
            outfile.write(json_obj)
        return True 
    

    async def setAuthToken(
            self,
    ):
        self._buildLocalOS()
        #TODO: do not leave these environment variables in this setup.
        audstr=os.getenv("AUTH_API_URL")+'GenerateToken'
        subkey=os.getenv("AUTH_API_KEY")
        headers={
            "Content-Type":'application/json',
            'Mimeo-graffiti-subscription': subkey
        }
        data={
            'componentName': self.component_name,
            'userId': self.user_id,
            'email': self.email_address, 
            'roles': self.roles 
        }
        result=requests.post(
            audstr, 
            headers=headers, 
            json=data 
        )
        token= json.loads(result.text)
        output_string:str=str(token.get('jwtToken'))
        return f'Bearer {output_string}'

    # async def testRoles(
    #         self,
    # ):
    #     subkey=os.get

    def _createJWTPayload(
            self,
    ):  
        tpl=self._createSessionTime()
        ps=self._osParamsJSON(f'{self.route}/params/client.json')
        audstr="###"+ps['params']['CLIENT_ID']
        pl={
            "###":True,
        }
        jwt=json.loads(pl)
        jwt["exp"]=self._createSessionTime()
        jwttoken=jwt.encode(jwt)
        return jwttoken 
    

    def _getHTTPHeader(
            self,
    ):
        ps=self._osParamsJSON(f'{self.route}/params/client.json')
        headers={
            "Accept":"text/plain",
            "Authorization": f'Bearer {self._getAuthToken()}', 
            "Content-Type": "application/json", 
            "x-sandbox-name": "mimeograph"
        }
        return headers 
    

    def _setBatchHeaders(
            self,
    ):
        ps=self._osParamsJSON(f'{self.route}/params/client.json')
        headers={
            "Authorization": f'Bearer {self._getAuthToken()}', 
            "Content-Type": "application/json", 
            "x-sandbox-name": "mimeograph"
        }
        return headers 
    

    def _setDataStreamHeaders(
            self,
    ):
        ps=self._osParamsJSON(f'{self.route}/params/client.json')
        headers={
            "Authorization": f'Bearer {self._getAuthToken()}', 
            "Content-Type": "application/octet-stream", 
            "x-api-key": ps['params']['CLIENT_ID'],
            "x-sandbox-name": "mimeograph"
        }
        return headers 
    

    def _getAuthToken(
            self,
    ):
        params= self._getAuthParams()
        return params['jwtToken']
                
    
    def _getAuthParams(
            self,
    ):
        n= self._readJSON(f'{self.route}/params/auth.json')
        return n 
    

    def _decode():
        pass 

    async def readToken(
            self,
            auth_token:str=None, 
            algo:str='HS256'
    ):
        ISSUER=os.getenv("TOKEN_ISSUER")
        AUDIENCE=os.getenv("TOKEN_AUDIENCE")
        SECRET=os.getenv("TOKEN_SECRET")
        auth:str=auth_token
        ext:str=auth.split('Bearer ')[1]
        result=jwt.decode(
            jwt=ext, 
            key=SECRET,
            alorithms=[algo], 
            issuer=ISSUER,
            audience=AUDIENCE 
        )
        return result 
    
    async def validate(
            self,
            algo:str='HS256'
    )->str:
        try:
            ISSUER=os.getenv("TOKEN_ISSUER")
            AUDIENCE=os.getenv("TOKEN_AUDIENCE")
            SECRET=os.getenv("TOKEN_SECRET")
            auth:str=self.auth_token
        except:
            raise HTTPException(
                status_code=401,
                detail="ENV VARIABLES : Token Configuration Error"
            )
        if auth is None:
            response = {
                    'status_code':401,
                    'result':"Unauthorized",
                    'message':"NO AUTH Bearer provided in HTTP Header", 
                    'payload':None 
            }
            return response 
        else:
            try:
                #ext=auth.split("Bearer ")[1]
                #result = await self.testRoles()
                # if result.status_code == 200:
                response={
                        'status_code':200, 
                        'result':'SUCCESS', 
                        'message':'Authorized Service User Session Token Start', 
                        'payload': None 
                }
                # else:
                #     response={
                #         'status_code':result.status_code, 
                #             'result':'FAILURE', 
                #             'message':'Roles AUTH failed.', 
                #             'payload': None 
                #     }
                return response 
            except jwt.ExpiredSignatureError:
                response={
                    'status_code':401,
                        'result':'Unauthorized', 
                        'message':'This token is expired', 
                        'payload':None
                }
                return response 


class MeterController: 

    UnitConfig=MeterConfig()

    class OpenAILLM:
        
        def __init__(
                self,
        ):

            from module.robot.action.common import OpenAILLMChat
            from module.robot.service.openai.completion import AzureOpenAI
            from module.robot.service.openai.embed import AzureOpenAIEmbeddings
            from module.robot.service.openai.custom import AzureChatOpenAIJSON
            #TODO: Missing function reference here.
            self.credentials=MeterController.UnitConfig.credentials()
            manager=Charon()
            jwt_auth_token=manager.get_token()

            API_VERSION:str="2024-07-01-preview"
            GPT_35_TURBO:str='gpt-35-turbo-1106'
            GPT_4o='gpt-4o'
            GPT_4o_mini='gpt-4o-mini'
            GPT_4='gpt-4'
            EMBEDDING_ADA='text-embedding-ada-002'

            self.graff_llm= AzureOpenAI(
                apikey=self.credentials['ADI_KEY'], 
                api_version=API_VERSION, 
                model=GPT_4o_mini
            )

            self.graff_chatllm=OpenAILLMChat(
                apikey=self.credentials['ADI_KEY'], 
                api_version=API_VERSION,
                model=GPT_35_TURBO,
                response_format={
                    'type':'json_object'
                }
            )

            self.graff_chatllm_json=AzureChatOpenAIJSON(
                apikey=self.credentials['ADI_KEY'], 
                api_version=API_VERSION, 
                model=GPT_35_TURBO, 
                response_format={'type': 'json_object'}
            )

            self.graff_embedllm=AzureOpenAIEmbeddings(
                apikey=self.credentials['ADI_KEY'], 
                api_version=API_VERSION,
                model=EMBEDDING_ADA
            )


        def get_model(
                self
        ):
            return self.graff_llm


        def get_chat(
                self
        ):
            return self.graff_chatllm


        def get_embed(
                self
        ):
            return self.graff_embedllm





    class AuthController:
        #check

        def __init_(
                self, 
                command : str = None, 
                step : str = None
            ):
            from core.model.entity.Identity import Identity
            self.instruction = command.upper()
            self.action = Identity
            self.state = step

        def route(
                self
            ):
            if self.instruction == "LOGIN":
                result = self.action.authorize(check=self.state)
            return result
            
            
    class RequestController:
        pass

    class ResponseController:
        pass

    class ErrorController:
        #check
        
        def __init__(
                self, 
                unit : str
            ):
            self.router = unit.upper()

        def Message(self)->dict:
            s : dict = Config.ErrorHandler(exc = self.router)
            return s



    class EmbedController:
        #check

        class Format:

            def __init__(
                    self, 
                    lines
                ):
                self.lines = lines

            def to_dict(self):
                return {'lines': self.lines}
            
        class Encode(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, MeterController.EmbedController.Format):
                    return {'lines': obj.lines}
                return super().default(obj)
            


        def embedStandard(self, data: json)->requests.Response:
            import requests
            try:
                request_data = json.dumps(
                    data, 
                    clse=self.Encode
                )
                headers = {
                    "Content-Type": "application/json"
                }
                response = requests.post(
                    Route.Default.LCHAIN.value, 
                    data=request_data, 
                    headers=headers
                )
                return response
            except Exception as ex:
                MeterController.ErrorController(unit="embedStandard")



        def embedOpenAI(
                endpoint: str, 
                token : str, 
                payload : str
            )->requests.Response:
            import requests 
            epk = Route.Default.LCHAIN["token"].value
            try:
                response = requests.post(
                    endpoint, 
                    json=payload, 
                    headers={
                        "Mimeo-graffiti-subscription" : epk, 
                        "Authorization" : token, 
                        "Content-Type" : "application/json",
                        "Content-length": str(len(payload)),
                    }
                )
                return response
            except:
                MeterController.ErrorController(unit="embedOpenAI")



        


    class TokenHandler:
    
        def __init__(
                self, 
                command : str = None
            ):
            pass

    class ServiceController:
        #check
        basurl : str
        service : str
        version : str

        def __init__(
                self, 
                command : str = None
            ):
            self.cfg = Config.Default.Settings()

        def getBaseUrl()->str:
            url = Config.Default.ENDB.value
            return url
        
    class ModelController:
        #check
        basurl : str
        service : str
        version : str

        def __init__(
                self, 
                commannd : str = None
            ):
            self.model = Embed 

        def getDefault():
            return Embed.DEFAULT.value

        def getEmbedModel(
                self, 
                name : str = None
            ):
            if name != None:
                result = self.model[{name}].value
            else:
                result = self.getDefault()
            return result

        def getBaseUrl(service: str)->str:
            url = Route.Service[service].value
            return url

    class EndpointController:
        pass