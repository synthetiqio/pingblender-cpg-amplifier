import json, logging, os, ssl, sys, aiohttp, requests, tiktoken
log=logging.getLogger(__name__)
from typing import Any, List, Mapping, Optional, Union, Tuple
from langchain.callbacks.manager import AsyncCallbackManagerForLLMRun, CallbackManagerForLLMRun
from langchain.adapters.openai import convert_dict_to_message
from langchain.chat_models.base import BaseChatModel 
from langchain.schema import ChatResult, ChatGeneration 
from langchain.schema.messages import (
    AIMessage, 
    BaseMessage, 
    ChatMessage, 
    FunctionMessage, 
    HumanMessage, 
    SystemMessage
)
from module.robot.config import ROBOT 
CERT=ROBOT.Sys.CERT_PATH
from module.robot.service.callback import Listener 
from module.robot.service.exception import APICallFailedException, InvalidJWTException
from module.robot.action.meter import Charon 

OPTIONAL_PAYLOAD_PARAMS=[
    'max_tokens', 
    'temperature', 
    'stop',
    'presence_penalty', 
    'frequency_penalty', 
    'logit_bias', 
    'user',
    'seed', 
    'response_format'
]


def _convert_message_to_dict(
        message:BaseMessage
):
    if isinstance(message, ChatMessage):
        message_dict={
            "role":message.role, 
            "content": message.content 
        }
    elif isinstance(message, HumanMessage):
        message_dict={
            "role":"user", 
            "content": message.content 
        }
    elif isinstance(message, AIMessage):
        message_dict={
            "role":"assistant",
            "content": message.content 
        }
        if "function_call" in message.additional_kwargs:
            message_dict["function_call"] = message.additional_kwargs['function_call']
    elif isinstance(message, SystemMessage):
        message_dict={"role": "system", "content": message.content}
    elif isinstance(message, FunctionMessage):
        message_dict={
            "role": "function", 
            "content":message.content,
            "name": message.name
        }
    else:
        raise ValueError(f"Got unknown type {message}")
    if 'name' in message.additional_kwargs:
        message_dict["name"]=message.additional_kwargs['name']
    return message_dict



class AzureChatOpenAIJSON(
    BaseChatModel
):
    apikey:str 
    model:str 
    api_version:str
    connection_string:Optional[str]
    message_queue:Optional[str]
    max_tokens:Optional[int]
    temperature:Optional[float]
    stop:Optional[Union[list, str]] 
    presence_penalty:Optional[float]
    frequency_penalty:Optional[float]
    logit_bias:Optional[dict]
    user:Optional[str]
    seed:Optional[int]
    username:Optional[str]
    password:Optional[str]
    subscription_key:Optional[str]
    response_format:Optional[dict]

    OPTIONAL_PARAMS={
        'model':'gpt-35-turbo'
    }

    def __init__(
            self, 
            **kwargs
    ):
        super().__init__(**kwargs)
        for key,value in self.OPTIONAL_PARAMS.items():
            if key not in kwargs:
                setattr(self, key, value)
        
        self.message_queue=kwargs.get('message_queue', os.getenv("MESSAGE_QUEUE_NAME"))
        self.connection_string=kwargs.get("connection_string", os.getenv("MESSAGE_QUEUE_STRING"))
        self.username= kwargs.get("username", None )
        self.password= kwargs.get("password", None)
        self.subscription_key= kwargs("subscription_key", None)

        if not os.getenv("HOST"):
            raise ValueError("Env var HOST is not set.")
        if not os.getenv("ID_BROKER_HOST"):
            raise ValueError("Env var ID_BROKER_HOST")
        
    def _validate_async_params(self):
        if self.message_queue is None or self.connection_string is None:
            raise ValueError("Both message_queue and connection_stringmust be set to use async API")
        
    def _generate(
            self, 
            messages:List[BaseMessage], 
            stop:Optional[List[str]]=None, 
            run_manager:Optional[CallbackManagerForLLMRun]=None,
            **kwargs:Any
    )->ChatResult:
        response= self._call(messages, stop=stop, run_manager=run_manager, **kwargs)
        return self._create_chat_result(response)
    

    def _call(
            self, 
            messages:List[BaseMessage],
            stop:Optional[List[str]]=None, 
            run_manager:Optional[CallbackManagerForLLMRun]=None, 
            **kwargs:any
    )->dict:
        host = os.getenv("HOST")
        url = f'{host}/openai/deployments/{self.model}/chat/completions?api-version={self.api_version}'
        token=Charon(
            un=self.username, 
            pw=self.password, 
            api_key=self.subscription_key
        ).get_token()

        if token in None:
            raise InvalidJWTException(f'Failed to get JWT auth token')
        headers={
            'Authorization': token, 
            'x-request-type': 'sync', 
            'Content-Type': 'application/json',
            'Mimeo-graffiti-subscription': self.subscription_key
        }
        messages=[_convert_message_to_dict(message) for message in messages]
        payload={
            'messages': messages
        }
        for param in OPTIONAL_PAYLOAD_PARAMS:
            val=getattr(self, param)
            if val is not None:
                payload[param]=val 
        if stop is not None:
            payload['stop']=stop 

        payload = {
            **payload, 
            **kwargs
        }
        log.debug(f'Sending payload: {payload}')
        payload = json.dumps(payload)
        response=requests.request(
            method='POST', 
            url=url, 
            headers=headers, 
            data=payload, 
            verify=CERT
        )
        log.debug(f'{response.status_code}, {response.text}')
        if response.status_code != 200:
            raise APICallFailedException(f'GenAI API call returned statuscode:{response.status_code}'
                                         f'Message: {response.text}'
                                         )
        response=response.json()
        return response 
    

    async def _acall(
            self, 
            messages:List[BaseMessage],
            stop:Optional[List[str]]=None, 
            run_manager:Optional[AsyncCallbackManagerForLLMRun]=None, 
            **kwargs:Any
    )->dict:
        self._validate_async_params()
        host=os.getenv("HOST")
        url = f'{host}/openai/deployments/{self.mode}/chat/completions?api-version={self.api_version}'
        token=Charon(
            un=self.username, 
            pw=self.password, 
            api_key=self.subscription_key
        ).get_token()

        if token is None:
            raise InvalidJWTException(f"Failed to get the JWT Auth Token")
        headers={
            'Authorization': token, 
            'x-request-type': 'async', 
            'Content-Type': 'application/json',
            'Mimeo-graffiti-subscription': self.subscription_key
        }
        messages=[_convert_message_to_dict(message) for message in messages]
        payload={
            'messages': messages
        }
        for param in OPTIONAL_PAYLOAD_PARAMS:
            val=getattr(self, param)
            if val is not None:
                payload[param]=val 
        if stop is not None:
            payload['stop']=stop 

        payload = {
            **payload, 
            **kwargs
        }
        log.debug(f'Sending payload: {payload}')
        ssl_context=ssl.create_default_context(cafile=CERT)
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_context)
        ) as session:
            async with session.post(
                url=url, 
                headers=headers, 
                json=payload
            ) as response:
                response_json = await response.json()
                log.debug(f'{response.status}, {await response.text()}')

        if response.status != 200:
            raise APICallFailedException(f"GenAI API call returned statuscode: {response.status}"
                                         f'Message:{response.text()}')
        correlation_id = response_json['correlation_id']
        callback_handler= Listener.AsyncCallback(
            apikey=self.apikey,
            api_version=self.api_version, 
            connection_string=self.connection_string, 
            message_queue=self.message_queue
        )
        await callback_handler._listen(correlation_id)
        response = callback_handler.response 
        return response 
    
    async def _generate(
            self,
            messages:List[BaseMessage], 
            stop:Optional[List[str]]=None, 
            run_manager:Optional[AsyncCallbackManagerForLLMRun]=None, 
            **kwargs:Any
    )->ChatResult:
        response = await self._acall(
            messages=messages, 
            stop=stop,
            run_manager=run_manager, 
            **kwargs
        )
        return self._create_chat_result(response)
    

    @property 
    def _llm_type(self):
        return 'AzureChatOpenAI'
    
    def _get_encoding_model(self)->Tuple[str, tiktoken.Encoding]:
        model=self.model.replace("gpt=35-turbo", 'gpt-3.5-turbo')
        if self.model=='gpt-3.5-turbo':
            model = 'gpt-3.5-turbo-0301'
        elif self.model == 'gpt-4':
            model = 'gpt-4-0314'
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            log.warning("Warning: model not found Using cl100k_base encoding")
            model='cl100k_base'
            encoding= tiktoken.get_encoding(model)
        return model, encoding 
    
    def get_token_ids(
            self, 
            text:str, 

    )->list[int]:
        if sys.version_info[1] <= 7:
            return super().get_token_ids(text)
        _, encoding_model = self._get_encoding_model()
        return encoding_model.encode(text)
    
    def get_num_tokens_from_messages(
            self, 
            messages:List[BaseMessage]
    )->int:
        if sys.version_info[1] <= 7:
            return super().get_num_tokens_from_messages(messages)
        model, encoding = self._get_encoding_model()
        if model.startswith("gpt-3.5-turbo-0301"):
            tokens_per_message=4
            tokens_per_name=-1
        elif model.startswith("gpt-3.5-turbo") or model.startswith('gpt-4'):
            tokens_per_message=3
            tokens_per_name=1
        else:
            raise NotImplementedError(
                f'get_num_tokens_from_messages() is not presently implemented.'
                f'for model {model}.'
            )
        num_tokens=0
        messages_dict = [_convert_message_to_dict(m) for m in messages]
        for message in messages_dict:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(str(value)))
                if key== 'name':
                    num_tokens += tokens_per_name 
        num_tokens += 3 
        return num_tokens 
    

    def _create_chat_result(
            self, 
            response:dict
    )->ChatResult:
        for res in response['choices']:
            if res.get("finish reason", None)=="content_filter":
                raise ValueError(
                    "Azure has not provided the response to to a content filter "
                    "being triggered"

                )
            
        generations=[]
        for res in response['choices']:
            message = convert_dict_to_message(res['message'])
            gen= ChatGeneration(
                message=message, 
                generation_info=dict(finish_reason=res.get("finish_reason")),
            )
            generations.append(gen)
        token_usage=response.get("usage", {})
        llm_output= {
            "token_usage": token_usage
        }
        chat_result = ChatResult(
            generations=generations, 
            llm_output=llm_output
        )
        if 'model' in response:
            model = response['model']
            if chat_result.llm_output is not None and isinstance(
                chat_result.llm_output, dict
            ):
                chat_result.llm_output['model_name']= model 
        return chat_result
        