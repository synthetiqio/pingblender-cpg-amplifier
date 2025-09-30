from enum import Enum
import os, base64, requests, time, json
from dataclasses import dataclass
from typing import Dict, List, Mapping, Optional, Any
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.schema import LLMResult, Generation
from dotenv import load_dotenv
load_dotenv()

class ROBOT:

    ERROR_MSG:Dict[List, Any] = {
        'result' : 'FAILURE', 
        'message' : '[ROBOT] : Service failure - Configuration Level [Root]', 
        'payload': None
        }
    
    class Options:
        PAYLOAD_PARAMS:Dict[List,Any]={
                'max_tokens', 
                'temperature', 
                'stop', 
                'presence_penalty', 
                'frequency_penalty', 
                'logit_bias', 
                'user', 
                'seed'
        }

    class Sys:
        CERT_PATH:str=os.path.join(os.path.dirname(__file__), 'cacert.pem')

    class Region:

        def getTimestampLocal(
                tmz : str = 'America/New_York'
            )->str:
            from datetime import datetime
            from pytz import timezone
            fmt = '%Y-%m-%dT%H:%M:%S'
            c = timezone(tmz)
            loc_dt = datetime.now(c)
            fd = loc_dt.strftime(fmt)
            return fd
        
        def getRegionalEnv()->Dict[List, Any]:
            r = {
                'tz' : "America/New_York", 
                'ln' : 'English-USA', 
                'cc' : 'US', 
                'cr' : 'USD'
            }
            return r
        

    class Config:

        def __init__(self):
            pass 

        ENV=os.environ.items()
        class OpenAI:
            """
            Config.OpenAI is the root account permissions setting attained from
            the vault or according to the settings in the ENV file. If you do not 
            have an OPENAI_API_KEY variable, much of the capabilities of these 
            application management functions will be unstable.
            """
            def __init__(
                    self,
            ):
                pass 
            
            def Client(self):
                    from openai import OpenAI
                    service_agent=OpenAI(
                        api_key=self.Account.OPENAPI_KEY.value()
                    )
                    return service_agent 

            

            @dataclass
            class Settings:
                    embed_model:str='text-embedding-ada-002'
                    embed_user:str='SynthetIQ-Embedding-Agent'


            @dataclass
            class Account(Enum):
                OPENAPI_KEY=os.environ.get('OPENAI_API_KEY')



        class ServiceCredentials:

            def __init__(
                    self,
                    diffuser:str=None
            ):
                self.updtu = diffuser
                self.suser = os.environ.get("METER_USER")
                self.passw = os.environ.get("METER_PASS")

            def getUser(self):
                if self.updtu is not None:
                    self.suser = self.updtu
                return self.suser
            
            def getPass(self):
                if self.updtu:
                    auth=self._getAuth(self.updtu)
                    return auth 
                else:
                    return self.passw
            
            def _getAuth(
                    self
            ):
                pass 

            @dataclass
            class Default(Enum):
                U:str=os.getenv("METER_USER")
                P:str=os.getenv("METER_PASS")
                T:str=os.getenv("METER_STOKEN")
                L:str=os.getenv("METER_LOGIN_URL")
                K:str=os.getenv("METER_LTOKEN")
                E:str=os.getenv("METER_ENDPOINT")
                B:str=os.getenv("METER_BASE_URL")
                V:str=os.getenv("METER_VERSION")

                


                


    class Model:

        @dataclass
        class GPT(Enum):
            TURBO_35="gpt-35-turbo"
            TURBO_35_16="gpt-35-turbo-16k"
            TURBO_35_0301="gpt-35-turbo-0301"
            TURBO_35_1106="gpt-35-turbo-1106"
            GPT_4="gpt-4"
            GPT_4_32="gpt-4-32k"
            GPT_4_128_1106_PRE="gpt-4-128k-1106-preview"
            GPT_4_128_VIZ_PRE="gpt-4-128k-v1106-preview"
            DALL_E= "dall-e"