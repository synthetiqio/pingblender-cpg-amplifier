import requests, os, json, logging, ssl, aiohttp 
log = logging.getLogger(__name__)
from typing import List, Optional, Any, Dict 
from module.robot.config import ROBOT as ConfigController
from module.robot.action.meter import Charon
from module.robot.service.bedrock.utils import LLMIO_Adapter, Bedrock_Base
from module.robot.service.callback import Listener as CallbackListener
from module.robot.service.exception import APICallFailedException, InvalidJWTException

from langchain.chat_models.base import BaseChatModel 
from langchain.pydantic_v1 import Extra 
from langchain.schema.messages import AIMessage, BaseMessage
from langchain.schema.output import ChatGeneration,ChatResult
from langchain.chat_models.bedrock import ChatPromptAdapter
from langchain.callbacks.manager import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun
from langchain.utilities.anthropic import (
    get_num_tokens_anthropic, 
    get_token_ids_anthropic
)

class BedrockChat(
    BaseChatModel, 
    BaseChatModel
):
    model_id:str 
    api_key:str 
    connection_str:Optional[str]
    message_queue:Optional[str]

    def __init__(
            self, 
            **kwargs,
    ):
        super().__init__(**kwargs)
        self._validate_parameter()

    @property 
    def _llm_type(self)->str:
        return 'amazon_bedrock_chat'
    
    class Config:
        extra = Extra.forbid

    def _generate(
            self, 
            messages:Optional[List[str]]=None,
            stop:Optional[List[str]]=None, 
            run_manager:Optional[CallbackManagerForLLMRun]=None, 
            **kwargs:Any,
    )->ChatResult:
        completion=""
        provider=self._get_provider()
        prompt=ChatPromptAdapter.convert_messages_to_prompt(
            provider=provider, 
            messages=messages
        )
        _model_kwargs=self.model_kwargs or {}
        params:Dict[List,Any]={**kwargs}
        if stop:
            params['stop_sequences']=stop 
        params={**_model_kwargs, **params}

        #default temp 0 
        if "temperature" not in params:
            params['temperature'] = 0.0

        input_body=LLMIO_Adapter.prepare_input(provider, prompt, params)
        payload=json.dumps(input_body)
        host=ConfigController.get("HOST")
        url=f'{host}/amazon-bedrock/models/{self.model_id}'
        token = Charon(
            un=self.username,
            pw=self.password, 
            api_key=self.subscriber_key
        ).get_token()
        headers={
            'Authorization':token, 
            "x-request-type":'sync',
            'Content-Type': 'application/json', 
            'Mimeo-graffiti-subscription': self.subscriber_key
        }
        response=requests.request(
            method="POST", 
            url=url, 
            headers=headers, 
            data=payload, 
            verify=ConfigController.Sys.CERT_PATH
        )
        if response.status_code != 200:
            raise APICallFailedException(
                {
                    'result':"FAILURE", 
                    'message': f'GenAI API call returned status_code: {response.status_code}', 
                    'payload': f'{response.text}'
                }
            )
        log.debug(f"{response.status_code}, {response.text}")
        raw_response =response.json()
        text= LLMIO_Adapter.prepare_output(provider, raw_response)
        message=AIMessage(content=text)
        return ChatResult(
            generations=[ChatGeneration(message=message)]
        )


    async def _agenerate(
            self, 
            messages:List[BaseMessage], 
            stop:Optional[List[str]]=None, 
            run_manager:Optional[AsyncCallbackManagerForLLMRun]=None, 
            **kwargs:Any,
    )->ChatResult:
            self._validate_async_params()
            _model_kwargs=self.model_kwargs or {}
            params:Dict[str, Any]={**kwargs}
            if stop:
                params['stop_sequences']=stop 
            params={**_model_kwargs, **params}
            if "temperature" not in params:
                params['temperatire']=0.0
            provider=self._get_provider()
            prompt= ChatPromptAdapter.convert_messages_to_prompt(
                provider=provider, 
                messages=messages
            )
            payload=LLMIO_Adapter.prepare_input(
                provider=provider, 
                prompt=prompt, 
                params=params
            )
            host=ConfigController.get("HOST")
            url=f'{host}/amazon-bedrock/models/{self.model_id}'
            token=Charon(
                un=self.username, 
                pw=self.password, 
                api_key=self.subscriber_key
            ).get_token()
            if token is None:
                raise InvalidJWTException("Failed to get JWT auth token")
            headers={
                'Authorization':token, 
                "x-request-type":'async',
                'Content-Type': 'application/json', 
                'Mimeo-graffiti-subscription': self.api_key
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
            await callback.response 
            response=callback.response 
            text= LLMIO_Adapter.prepare_output(provider, response)
            log.debug(response)
            return ChatResult(generations=[ChatGeneration(message=AIMessage(content=text))])
    
    def get_num_tokens(self, text)->int:
        if self._model_is_anthropic:
            return get_num_tokens_anthropic(text)
        else: 
            return super().get_num_tokens(text)
        
    def _validate_async_params(self):
        if self.message_queue is None or self.connection_str is None:
            raise ValueError("Both the message queue and the connection string must be set for async api.")
        
    def get_token_ids(self, text:str)->List[int]:
        if self._model_is_anthropic:
            return get_token_ids_anthropic(text)
        else:
            return super().get_token_ids(text)
        

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

    