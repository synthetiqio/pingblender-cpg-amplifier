import json, logging, os, ssl, requests, aiohttp
from typing import Any, List, Mapping, Optional, Union
from langchain.callbacks.manager import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun
from langchain.llms.base import LLM 
from module.robot.service.callback import Listener
from module.robot.control import Config as ConfigControl 
from module.robot.service.exception import InvalidJWTException, APICallFailedException
from module.robot.action.meter import Charon 
log=logging.getLogger(__name__)

OPTIONAL_PAYLOAD_PARAMS={
    'max_tokens', 
    'temperature', 
    'top_p', 
    'logit_bias',
    'user', 
    'logprobs', 
    'suffix',
    'echo',
    'stop',
    'presence_penalty', 
    'frequency_penalty'
}


class AzureOpenAI(LLM):
    api_key:str
    model:str 
    api_version:str 
    connection_str:Optional[str]
    message_queue:Optional[str]
    max_tokens:Optional[int]
    temperature:Optional[float]
    top_p:Optional[float]
    logit_bias:Optional[dict]
    user:Optional[str]
    logprobs:Optional[int]
    suffix:Optional[str]
    echo:Optional[bool]
    stop:Optional[Union[str,list]]
    presence_penalty:Optional[float]
    frequency_penalty:Optional[float]
    username:Optional[str]
    password:Optional[str]
    subscription_key:Optional[str]

    OPTIONAL_PARAMS={
        'model':'text=davinci-003'
    }

    def __init__(
            self,
            **kwargs
    ):
        
        super().__init__(**kwargs)

        for key,value in self.OPTIONAL_PARAMS.items():
            if key not in kwargs:
                setattr(self,key,value)

        self.message_queue=kwargs.get('message_queue', ConfigControl.Sys.MessageQueue.NAME)
        self.connection_str=kwargs.get('connection_str', ConfigControl.Sys.MessageQueue.CONN_STR)
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.subscription_key = kwargs.get("subscription_key", None)

        if not os.getenv("HOST"):
            raise ValueError("Env var HOST is not set")
        if not os.getenv("ID_BROKER_HOST"):
            raise ValueError("Env var ID_BROKER_HOST is not set")

    def _validate_async_params(self):
        if self.message_queue is None or self.connection_str is None:
            raise ValueError("Both the message_queue and connection_str must be set to use async api")
        
    @property 
    def _llm_type(self)->str:
        return 'AzureOpenAI'
    
    def _call(
            self,
            prompt:str,
            stop:Optional[List[str]]=None, 
            run_manager: Optional[CallbackManagerForLLMRun]=None,
            **kwargs:Any
    )->str:
        host=os.getenv("HOST")
        url=f'{host}/openapi/deployments/{self.model}/completions?api-version{self.api_version}'
        token=Charon(
            un=self.username,
            pw=self.password, 
            api_key=self.subscription_key
        ).get_token()

        if token is None:
            raise InvalidJWTException(f'Failed to get JWT Auth Token')
        headers={
            'Authorization': token, 
            'x-request-type': 'sync', 
            'Content-Type': 'application/json', 
            'Mimeo-graffiti-subscription': self.api_key
        }
        payload = {
            'prompt': prompt, 
        }

        for param in OPTIONAL_PAYLOAD_PARAMS:
            val=getattr(self,param)
            if val is not None:
                payload[param]=val
        log.debug(f"Sending payload: {payload}")
        payload=json.dumps(payload)
        response= requests.request(
            method='POST', 
            url=url, 
            headers=headers, 
            data=payload,
            verify=ConfigControl.Sys.CERT_PATH
        )
        log.debug(f"{response.status_code}, {response.text}")
        if response.status_code !=200:
            raise APICallFailedException(
                f'GenAI API call returned statuscode: {response.status_code}'
                f'Message:{response.text}'
            )
        response=response.json()
        return response['choices'][0]['text']
    

    async def _acall(
            self,
            prompt:str,
            stop:Optional[List[str]]=None, 
            run_manager:Optional[AsyncCallbackManagerForLLMRun]=None, 
            **kwargs:Any,
    ):
        self._validate_async_params()
        host=os.getenv("HOST")
        url=f'{host}/openai/deployments/{self.model}/completions?api-version{self.api_version}'
        token=Charon(
            un=self.username, 
            pw=self.password,
            api_key=self.subscription_key
        ).get_token()

        if token is None:
            raise InvalidJWTException(f'Failed to get JWT Auth Token')
        headers={
            'Authorization': token, 
            'x-request-type': 'async', 
            'Content-Type': 'application/json', 
            'Mimeo-graffiti-subscription': self.api_key
        }
        payload={
            "prompt":prompt
        }
        for param in OPTIONAL_PAYLOAD_PARAMS:
            val=getattr(self,param)
            if val is not None:
                payload[param]=val
        log.debug(f'Sending payload {payload}')
        ssl_context = ssl.create_default_context(cafile=ConfigControl.Sys.CERT_PATH)
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_context)
            ) as session:
            async with session.post(
                url=url, 
                headers=headers,
                json=payload
            ) as response:
                response_json= await response.json()
                log.debug(f'{response.status}, {response.text()}')
        if response.status != 202:
            raise APICallFailedException(f"GenAI API call returned statuscode: {response.status} "
                                         f'Message:{response.text}')
        correlation_id=response_json['correlation_id']
        callback_handler=Listener.AsyncCallback(
            apikey=self.api_key,
            api_version=self.api_version,
            connection_string=self.connection_str, 
            queue=self.message_queue
        )
        await callback_handler._listen(correlation_id=correlation_id)
        response = callback_handler.response 
        return response['choices'][0]['text']

    @property 
    def _identifying_params(self)->Mapping[str,Any]:
        return {'model': self.model}
    
                          



        
