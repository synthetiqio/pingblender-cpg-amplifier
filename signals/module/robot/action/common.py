#/
import logging,json,os,ssl,sys, aiohttp, tiktoken
import requests 
log=logging.getLogger(__name__)
from core.evt.ctrl import EventExceptionController as EX
from typing import Dict,List,Any,Tuple,Union,Optional
from module.robot.control import RobotController as RC
from module.robot.action.meter import Charon as TC 
from module.robot.service.callback import Listener as LC

from langchain.callbacks.manager import AsyncCallbackManagerForLLMRun, CallbackManagerForLLMRun
from langchain.adapters.openai import convert_dict_to_message
from langchain.chat_models.base import BaseChatModel
from langchain.schema import ChatResult,ChatGeneration
from langchain.schema.messages import (
    AIMessage, 
    BaseMessage, 
    ChatMessage, 
    FunctionMessage, 
    HumanMessage, 
    SystemMessage
)

OPTIONAL_PAYLOAD_PARAMS:Dict[List,Any]=RC().getPayloadParams()

#message conversion for build 1
def _convert_message_to_dict(message:BaseMessage)->dict:
    if isinstance(message,ChatMessage):
        message_dict={
            'role': message.role, 
            'content':message.content
            }
    elif isinstance(message,HumanMessage):
        message_dict={
            'role': 'user', 
            'content':message.content
            }
    elif isinstance(message,AIMessage):
        message_dict={
            'role': 'assistant', 
            'content':message.content
            }
        if "function_call" in message.additional_kwargs:
            message_dict=message.additional_kwargs['function_call']
    elif isinstance(message,SystemMessage):
        message_dict={
            'role': 'system', 
            'content':message.content
            }
    elif isinstance(message,FunctionMessage):
        message_dict={
            'role': 'function', 
            'content':message.content, 
            'name': message.name
            }
    else:
        raise ValueError(f'Got unknown type {message}')
    if 'name' in message.additional_kwargs:
        message_dict['name']=message.additional_kwargs['name']
    return message_dict
    


class OpenAILLMChat:

    apikey:str 
    model:str
    conn:Optional[str]
    queue:Optional[str]
    max_tokens:Optional[int]
    temperature:Optional[float]
    stop:Optional[Union[list,str]]
    presence_penalty:Optional[float]
    frequency_penalty:Optional[float]
    logit_bias:Optional[dict]
    user:Optional[str]
    seed:Optional[int]
    username: Optional[str]
    password:Optional[str]
    subscription_key:Optional[str]

    OPTIONAL_PARAMS={'model':'gpt-35-turbo'}

    def __init__(
            self, 
            **kwargs
    ):
        super().i__init__(**kwargs)
        for key, value in self.OPTIONAL_PARAMS.items():
            if key not in kwargs:
                setattr(self, key, value)
        from module.pgvector.connect import Client
        self.queue=kwargs.get('queue','DEFAULT')
        self.conn=kwargs.get("conn", Client.getConnectionString())
        self.username=kwargs.get('username', None)
        self.password=kwargs.get('password', None)
        self.subscription_key=kwargs.get("subscription_key", None)

    def _validate_async_params(self):
        if self.queue is None or self.conn is None:
            raise ValueError('Both event_hub_name and conn must be used for the async api')


    def _generate(
            self, 
            messages:List[BaseMessage], 
            stop:Optional[List[str]]=None,
            run_mgr:Optional[CallbackManagerForLLMRun]=None,
            **kwargs:Any,
    )->ChatResult:
        response= self._call(
            messages,
            stop=stop,
            run_mgr=run_mgr,
            **kwargs
        )
        return self._create_chat_result(response)
    

    def _call(
            self, 
            messages:List[BaseMessage],
            stop:Optional[List[str]]=None, 
            run_mgr:Optional[CallbackManagerForLLMRun]=None,
            **kwargs:Any
    )->dict:
        url=".."
        token=RC().getToken()
        if token is None:
            raise EX(f'failed to get JWT auth token')
        headers={
            "Authentication":token,
            "x-request-type":'sync', 
            'Content-Type': 'application/json', 
            'Mimeo-graffiti-subscriber': self.subscription_key
        }
        payload={"messages":messages}
        for param in OPTIONAL_PAYLOAD_PARAMS:
            val = getattr(self,param)
            if val is not None:
                payload[param]=val
        if stop is not None:
            payload['stop']=stop 
        payload={**payload, **kwargs}
        log.debug(f'Sending payload: {payload}')
        payload=json.dumps(payload)
        response = requests.request(
            "POST", 
            url, 
            headers=headers,
            data=payload, 
            verify=RC.certPath()
            )
        log.debug(f"{response.status_code}, {response.text}")
        if response.status_code != 200:
            msg = {
                    'result':'FAILURE',
                    'message':f'{response.status_code} | additional: {response.text}', 
                    'payload':None
            }
            raise EX(msg)
        response=response.json()
        return response 
    

    async def _acall(
            self, 
            messages:List[BaseMessage],
            stop:Optional[List[str]]=None, 
            run_mgr:Optional[CallbackManagerForLLMRun]=None,
            **kwargs:Any
    )->dict:
        self._validate_async_params()
        url:str='..'
        token=RC.getToken(
            un=self.username, 
            pw=self.password, 
            sub=self.subscription_key
        )
        if token is None:
            raise EX(f'failed to get JWT auth token')
        headers={
            "Authentication":token,
            "x-request-type":'sync', 
            'Content-Type': 'application/json', 
            'Mimeo-graffiti-subscriber': self.subscription_key
        }
        payload={"messages":messages}
        for param in OPTIONAL_PAYLOAD_PARAMS:
            val = getattr(self,param)
            if val is not None:
                payload[param]=val
        if stop is not None:
            payload['stop']=stop 
        payload={**payload, **kwargs}
        log.debug(f"Sending payload: {payload}")
        ssl_set=ssl.create_default_context(cafile=RC.certPath())
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_set)
        ) as session:
            async with session.post(
                url, 
                headers=headers,
                json=payload
            ) as response:
                response_json= await response.json()
            log.debug(f"{response.status_code}, {response.text}")
            if response.status_code != 202:
                msg = {
                        'result':'FAILURE',
                        'message':f'{response.status_code}', 
                        'payload':f'Error Details: {response.text}'
                }
                raise EX(msg)
            correlation_id= response.json['correlation_id']
            callback_handler= LC.AsyncCallback(
                apikey=self.apikey, 
                conn=self.conn, 
                queue=self.queue
            )
            await callback_handler._listen(correlation_id=correlation_id)
            response = callback_handler.response 
            return response 
        

    async def _agenerate(
            self, 
            messages:List[BaseMessage], 
            stop:Optional[List[str]]=None, 
            run_mgr:Optional[AsyncCallbackManagerForLLMRun]=None,
            **kwargs:Any,
    )->ChatResult:
        response= await self._acall(messages=messages,stop=stop, run_mgr=run_mgr, **kwargs)
        return self._create_chat_result(response)
    
    @property
    def _llm_type(self)->str:
        return "OpenAILLMChat"
    
    def _get_encoding_model(self)->Tuple[str,tiktoken.Encoding]:
        model=self.model.replace("gpt-35-turbo", "gpt-3.5-turbo")
        if self.model=="gpt-3.5-turbo":
            model="gpt-3.5-turbo-0301"
        elif self.model=="gpt-4":
            model="gpt-4-0314"
        try:
            encoding=tiktoken.encoding_for_model(model)
        except KeyError:
            log.warning("Warning: A model was not found which matches; use cl100k encoding")
            model="cl100k_base"
            encoding=tiktoken.get_encoding(model)
        return model, encoding
    

    def get_token_ids(
            self, 
            text:str
    )->List[int]:
        if sys.version_info[1] <= 7:
            return super().get_token_ids(text)
        _, encoding_model=self._get_encoding_model()
        return encoding_model.encode(text)
    
    def get_num_tokens_from_messages(
            self,
            messages:List[BaseMessage]
    )->int:
        if sys.version_info[1] <= 7:
            return super().get_num_of_tokens_from_messages(messages)
        model, encoding=self._get_encoding_model()
        if model.startswith("gpt-3.5-turbo-0301"):
            tokens_per_message=4
            tokens_per_name=-1
        elif model.startswith("gpt-3.5-turbo") or model.startswith("gpt-4"):
            tokens_per_message=3
            tokens_per_name=1
        else:
            raise NotImplementedError()
        num_tokens=0
        messages_dict=[_convert_message_to_dict(m) for m in messages]
        for message in messages_dict:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(str(value)))
                if key == 'name':
                    num_tokens += tokens_per_name
        num_tokens +=3
        return num_tokens
    
    def _create_chat_result(
            self, 
            response:dict
    ):
        for res in response["choices"]:
            if res.get("finish_reason", None) == "content_filter":
                raise ValueError(
                    "Azure has not provided the response due to content filter"
                )
        generations=[]
        for res in response["choices"]:
            message = convert_dict_to_message(res['message'])
            gen = ChatGeneration(
                message=message,
                generation_info=dict(finish_reason=res.get("finish_reason")), 

            )
            generations.append(gen)
        token_usage = response.get("usage", {})
        llm_output = {"token_usage": token_usage}
        chat_result = ChatResult(
            generations=generations, 
            llm_output=llm_output
        )
        if "model" in response:
            model=response['model']
            if chat_result.llm_output is not None and isinstance(
                chat_result.llm_output, dict
            ):
                chat_result=llm_output['model_name']=model
        return chat_result

        


        
    



