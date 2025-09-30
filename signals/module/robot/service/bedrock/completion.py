import requests, json, os, logging, ssl, aiohttp
log=logging.getLogger(__name__)
from typing import Optional, List, Any, Dict 
from langchain.llms.base import LLM 
from langchain.callbacks.manager import (
    CallbackManagerForLLMRun, 
    AsyncCallbackManagerForLLMRun
)
from module.robot.config import ROBOT as ConfigController
from module.robot.action.meter import Charon as TokenManager
from module.robot.service.bedrock.utils import LLMIO_Adapter, Bedrock_Base
from module.robot.service.callback import Listener as CallbackListener
from module.robot.service.exception import APICallFailedException, InvalidJWTException

class BedrockCompletion(
    Bedrock_Base, 
    LLM,
):
    model_id:str
    apikey:str 
    connection_str:Optional[str]
    message_queue:Optional[str]
    
    def __init__(
            self,
            **kwargs
    ):
        super().__init__(**kwargs)
        self._validate_parameter()


    def _llm_type(self)->str:
        return 'amazon_bedrock'
    
    def _call(
            self, 
            prompt:str, 
            stop:Optional[List[str]]=None,
            run_manager:Optional[CallbackManagerForLLMRun]=None,
            **kwargs:Any,
    ):
        _model_kwargs=self.model_kwargs or {}
        provider=self._get_provider()
        params={**_model_kwargs, **kwargs}
        if 'temperature' not in params:
            params['temperature']=0.0

        input_body=LLMIO_Adapter.prepare_input(
            provider=provider, 
            prompt=prompt, 
            params=params
        )
        payload=json.dumps(input_body)
        host=ConfigController.Options("HOST")
        url=f'{host}/amazon-bedrock/models/{self.model_id}'
        token = TokenManager(
            un=self.username, 
            pw=self.password, 
            api_key=self.subscription_key 
        ).get_token()

        if token is None:
            raise InvalidJWTException(f'Failed to get JWT Token')
        headers={
            'Authorization': token, 
            'x-request-type': 'sync', 
            'Content-Type': 'application/json',
            'Mimeo-graffiti-subscription': self.subscription_key 
        }
        response = requests.post(
            'POST', 
            url, 
            headers=headers, 
            data=payload, 
            verify=ConfigController.Sys.CERT_PATH
        )
        if response.status_code != 200:
            raise APICallFailedException(f'GenAI API returned status_code: {response.status_code}')
        log.debug(f'{response.status_code}, {response.text}')
        raw_resp = response.json()
        text=LLMIO_Adapter.prepare_output(
            provider=provider, 
            response=raw_resp
        )
        log.debug(raw_resp)
        return text 


    async def _acall(
            self, 
            prompt:str, 
            stop:Optional[List[str]]=None,
            run_manager:Optional[AsyncCallbackManagerForLLMRun]=None,
            **kwargs:Any,
    ):
        self._validate_async_params()
        _model_kwargs=self.model_kwargs or {}
        provider=self._get_provider()
        params={**_model_kwargs, **kwargs}

        if 'temperature' not in params:
            params['temperature']=0.0
        payload=LLMIO_Adapter.prepare_input(
            provider=provider, 
            prompt=prompt, 
            params=params
        )
        host=ConfigController.Options("HOST")
        url=f'{host}/amazon-bedrock/models/{self.model_id}'
        token = TokenManager(
            un=self.username, 
            pw=self.password, 
            api_key=self.subscription_key 
        ).get_token()

        if token is None:
            raise InvalidJWTException(f'Failed to get JWT Token')
        headers={
            'Authorization': token, 
            'x-request-type': 'async', 
            'Content-Type': 'application/json',
            'Mimeo-graffiti-subscription': self.subscription_key 
        }
        log.debug(f'Sending payload: {payload}')
        ssl_context=ssl.create_default_context(cafile=ConfigController.Sys.CERT_PATH)
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_context)
        ) as session:
            async with session.post(
                url=url, 
                headers=headers, 
                json=payload 
            )as response:
                response_json = await response.json()
                log.debug(f'{response.status}, {response.text}')
        if response.status_code != 202:
            raise APICallFailedException(
                {
                    'result':"FAILURE", 
                    'message': f'GenAI API call returned status_code: {response.status_code}', 
                    'payload': f'{response.text}'
                }
            )
        log.debug(f"{response.status_code}, {response.text}")
        correlation_id = response_json['correlation_id']
        callback=CallbackListener.AsyncCallback(
            apikey=self.api_key,
            connection_string=self.connection_str, 
            message_queue=self.message_queue
        )
        await callback._listen(correlation_id)
        response=callback.response 
        text= LLMIO_Adapter.prepare_output(provider, response)
        log.debug(response)
        return text


    def _validate_parameter(self)->None:
        if ConfigController.Options("MESSAGE_QUEUE_STR") and (
            not hasattr(self, "connection_str") or 
            not self.connection_str):
            self.connection_str = ConfigController.Options("MESSAGE_QUEUE_STR") 
        if ConfigController.Options("MESSAGE_QUEUE") and (
            not hasattr(self, "message_queue") or not self.message_queue):
            self.message_queue = ConfigController.Options("MESSAGE_QUEUE")
        if not ConfigController.Options("HOST"):
            raise ValueError("Env var HOST is not set")
        if not ConfigController("ID_BROKER_HOST"):
            raise ValueError("Env var ID_BROKER_HOST is not set.")

    
    def _validate_async_params(self):
        if self.message_queue is None or self.connection_str is None:
            raise ValueError("Both Message Queue and Connection String must be set for async api")

