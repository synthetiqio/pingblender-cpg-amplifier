from enum import Enum 
import tiktoken
import os, base64, requests, time, json, logging, tiktoken
from dotenv import load_dotenv
from typing import Any, Dict, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM 
from langchain.schema import LLMResult, Generation 
from module.robot.config import ROBOT

#tt= tiktoken()
log=logging.getLogger(__name__)

load_dotenv()

auth_jwt=ROBOT.Config.ServiceCredentials.Default

class GPT_Model(Enum):
    GPT_35_TURBO="gpt-35-turbo"
    GPT_35_TURBO_16K="gpt-35-turbo-16k"
    GPT_35_TURBO_0301="gpt-35-turbo-0301"
    GPT_35_TURBO_1106='gpt-35-turbo-1106'
    GPT_4='gpt-4'
    GPT_4_32K='gpt-4-32k'
    GPT_4_128K_1106_PREVIEW="gpt-4-128k-1106-preview"
    GPT_4_128K_VISION_PREVIEW='gpt-4-128k-v1106-preview'
    DALLE='dall-e'

class LLMService(LLM):
    model:str=GPT_Model.GPT_4_32K
    auth_token:str=''
    config = ROBOT.Config.ServiceCredentials()

    endpoint:str = (
        config.Default.B
        +model.value+f'/chat/completions?api-version={config.Default.V}'
    )

    rcm:Optional[str]=None 
    top_p:Optional[float]=0.1
    top_k:Optional[float]=40 
    max_tokens:Optional[int]=30000
    n_threads:Optional[int]=4
    n_predict:Optional[int]=1
    temp:Optional[float]=0.0
    repeat_last_n:Optional[int]=64
    repeat_penalty:Optional[float]=1.18

    def login(self):
        # config=ROBOT.Config.ServiceCredentials()
        # creds=config.Default.U+":"+config.Default.P
        # creds_byes=creds.encode("utf-8")
        # base_creds=base64.b64encode(creds_byes).decode('utf-8')
        # response = requests.post(
        #     config.Default.L, 
        #     data={}, 
        #     headers={
        #         'Mimeo-graffiti-subscription': config.Default.K, 
        #         'Authorization': "Basic "+base_creds
        #     }
        # )
        # if response.status_code != 200:
        #     if response.status_code == 204:
        #         print("Failed Response Headers", response.headers)
        #         raise ValueError(
        #             "204: No content was returned from the login request"
        #         )
        #     print("Failed response Status Code", response.status_code)
        #     print("Failed Response: ", response.text)
        #     print("Failed Respons Headers: ", response.headers)
        #     raise ValueError('Loging failed to Graffiti Metering-=> ', response.text)
        # self.auth_token=response.headers
        return 
    
    def llm_result(
            self, 
            prompt, 
            str
    ):
        config = ROBOT.Config.ServiceCredentials()
        messages=[
            {
                'role':'user', 
                'content':str(prompt)
            }
        ]
        data={
            'max_tokens':self.max_tokens,
            'temperature':self.temp, 
            'n':self.n_predict, 
            'messages': messages
        }
        response = requests.post(
            self.endpoint, 
            json=data, 
            headers={
                'Mimeo-graffiti-subscription': config.Default.K, 
                'Authorization': "Basic "+self.auth_token,
                'Content-Type':"application/json", 
                'Content-Length': str(len(data))
            }
        )
        if response.status_code != 200:
            print("Failed Response Status Code: ", response.status_code)
            print("Failed Response: ", response.text)
            if response.status_code == 429:
                x=20
                print("Waiting due to 429 Error (Seconds Retry) =>"+str(x))
                time.sleep(x)
                response=requests.post(
                    self.endpoint, 
                    json=data, 
                    headers={
                        'Mimeo-graffiti-subscription': config.Default.K,
                        'Authorization': "Basic "+self.auth_token,
                        'Content-Type':"application/json", 
                        'Content-Length': str(len(data))
                    },
                )
                print("Done making secondary request!")
            if response.status_code != 200:
                print("Failed Secondary Response : ", response.text)
                gen:List[Generation]=[{
                    'text':'', 
                    'logprobs':'N/A', 
                    'finish_reason':'ERROR', 
                    'index':'',

                }]
                llm_response:LLMResult=LLMResult(generations=[gen])
                return llm_response
        responses=response.json().get("choices")
        gen:List[Generation] = [{
                    'text':response.get("message").get("content"), 
                    'logprobs':'N/A', 
                    'finish_reason':response.get("finish_reason"), 
                    'index':response.get("index"),
        } 
            for response in responses 
        ]
        llm_response:LLMResult=LLMResult(generations=[gen])
        return llm_response

    @property
    def _llm_type(self)->str:
        return 'custom'
    
    def _call(
            self, 
            prompt:str, 
            stop:Optional[List[str]]=None,
            run_manager:Optional[CallbackManagerForLLMRun]=None, 
            **kwargs:Any,
    )->str:
        if stop is not None:
            print("Stop kwargs were passed in: ", stop)
        self.login()
        result=self.llm_result(prompt)
        return result 
    

    def generate(
            self, 
            prompts, 
            **kwargs
    ):
        return self._call(prompts, **kwargs)
    

    def create_outputs(
            self, 
            llm_result:LLMResult
    )->List[Dict[str,Any]]:
        for generation in llm_result.generations:
            print("GENERATION IS: ", generation)
        result = [
            {
                self.output_key:self.output_parser.parse_result(generation),
                'full_generation': generation 
            }
            for generation in llm_result.generations
        ]
        return result 
    
    @property
    def _identifying_params(self)->Mapping[str,Any]:
        return {'meterDeploymentName': self.model}
    
    @property
    def _get_model_default_parameters(self):
        return {
            'max_tokens': self.max_tokens, 
            'n_predict': self.n_predict,
            'top_k': self.top_k,
            'top_p': self.top_p,
            'temp': self.temp, 
            'n_batch': self.n_batch,
            'repeat_penalty': self.repeat_penalty,
            'repeat_last_n': self.repeat_last_n
        }
    

class MeteredChat:
    model:str = GPT_Model.GPT_4_32K
    access_token:str=''
    config = ROBOT.Config.ServiceCredentials()
    endpoint:str = (
        config.Default.B
        +model.value+f'/chat/completions?api-version={config.Default.V}'
    )
    rcm:Optional[str]=None 
    top_p:Optional[float]=0.1
    top_k:Optional[float]=40 
    n_threads:Optional[int]=4
    n_predict:Optional[int]=1
    temp:Optional[float]=0.0
    repeat_last_n:Optional[int]=64
    repeat_penalty:Optional[float]=1.18

    def login(self):
        config=ROBOT.Config.ServiceCredentials()
        creds=config.Default.U+":"+config.Default.P
        creds_byes=creds.encode("utf-8")
        base_creds=base64.b64encode(creds_byes).decode('utf-8')
        response = requests.post(
            config.Default.L, 
            data={}, 
            headers={
                'Mimeo-graffiti-subscription': config.Default.K, 
                'Authorization': "Basic "+base_creds
            }
        )
        if response.status_code != 200:
            if response.status_code == 204:
                print("Failed Response Headers", response.headers)
                raise ValueError(
                    "204: No content was returned from the login request"
                )
            print("Failed response Status Code", response.status_code)
            print("Failed Response: ", response.text)
            print("Failed Respons Headers: ", response.headers)
            raise ValueError('Loging failed to Graffiti Metering-=> ', response.text)
        self.auth_token=response.headers
        return 
    
    def chat(
            self, 
            prompt, 
            str
    ):
        config = ROBOT.Config.ServiceCredentials()
        messages=[
            {
                'role':'user', 
                'content':str(prompt)
            }
        ]
        data={
            'temperature':self.temp, 
            'n':self.n_predict, 
            'messages': messages
        }
        response = requests.post(
            self.endpoint, 
            json=data, 
            headers={
                'Mimeo-graffiti-subscription': config.Default.K, 
                'Authorization': "Basic "+self.auth_token,
                'Content-Type':"application/json", 
                'Content-Length': str(len(data))
            }
        )
        if response.status_code != 200:
            print("Failed Response Status Code: ", response.status_code)
            print("Failed Response: ", response.text)
            if response.status_code == 429:
                x=20
                print("Waiting due to 429 Error (Seconds Retry) =>"+str(x))
                time.sleep(x)
                response=requests.post(
                    self.endpoint, 
                    json=data, 
                    headers={
                        'Mimeo-graffiti-subscription': config.Default.K,
                        'Authorization': "Basic "+self.auth_token,
                        'Content-Type':"application/json", 
                        'Content-Length': str(len(data))
                    },
                )
                print("Done making secondary request!")
            if response.status_code != 200:
                print("Failed Secondary Response : ", response.text)
                gen:List[Generation]=[{
                    'text':'', 
                    'logprobs':'N/A', 
                    'finish_reason':'ERROR', 
                    'index':'',

                }]
                llm_response:LLMResult=LLMResult(generations=[gen])
                return llm_response
        responses=response.json().get("choices")
        gen:List[Generation] = [{
                    'text':response.get("message").get("content"), 
                    'logprobs':'N/A', 
                    'finish_reason':response.get("finish_reason"), 
                    'index':response.get("index"),
        } 
            for response in responses 
        ]
        llm_response:LLMResult=LLMResult(generations=[gen])
        return llm_response

    @property
    def _llm_type(self)->str:
        return 'custom'
    
    def _call(
            self, 
            prompt:str, 
            stop:Optional[List[str]]=None,
            run_manager:Optional[CallbackManagerForLLMRun]=None, 
            **kwargs:Any,
    )->str:
        if stop is not None:
            print("Stop kwargs were passed in: ", stop)
        self.login()
        result=self.llm_result(prompt)
        return result 
    

    def generate(
            self, 
            prompts, 
            **kwargs
    ):
        return self._call(prompts, **kwargs)
    

    def create_outputs(
            self, 
            llm_result:LLMResult
    )->List[Dict[str,Any]]:
        for generation in llm_result.generations:
            print("GENERATION IS: ", generation)
        result = [
            {
                self.output_key:self.output_parser.parse_result(generation),
                'full_generation': generation 
            }
            for generation in llm_result.generations
        ]
        return result 
    
    @property
    def _identifying_params(self)->Mapping[str,Any]:
        return {'meterDeploymentName': self.model}
    
    @property
    def _get_model_default_parameters(self):
        return {
            'max_tokens': self.max_tokens, 
            'n_predict': self.n_predict,
            'top_k': self.top_k,
            'top_p': self.top_p,
            'temp': self.temp, 
            'n_batch': self.n_batch,
            'repeat_penalty': self.repeat_penalty,
            'repeat_last_n': self.repeat_last_n
        }
    


                



