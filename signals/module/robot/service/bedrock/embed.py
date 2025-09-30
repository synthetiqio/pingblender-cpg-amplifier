import requests, json, os, logging, ssl, aiohttp, asyncio 
from langchain.schema.embeddings import Embeddings
from langchain.pydantic_v1 import BaseModel 
from typing import Optional,List,Dict 
log = logging.getLogger(__name__)

from module.robot.config import ROBOT as ConfigController
from module.robot.action.meter import Charon
from module.robot.service.callback import Listener as CallbackListener
from module.robot.service.exception import APICallFailedException, InvalidJWTException

class BedrockEmbeddings(BaseModel, Embeddings):
    model_id:str 
    model_kwargs:Optional[Dict]=None 
    api_key:str
    connection_str:Optional[str]=None 
    message_queue:Optional[str]=None 
    username:Optional[str]=None 
    password:Optional[str]=None 
    subscriber_key:Optional[str]=None

    def __init__(
            self, 
            **kwargs
    ):
        super().__init__(**kwargs)
        self._validate_param()


    def _embedding_func(
            self, 
            text:str
    )->List[float]:
        text=text.replace(os.linesep, " ")
        _model_kwargs=self.model_kwargs or {}
        input_body={**_model_kwargs, "inputText":text}
        payload=json.dumps(input_body)
        host=ConfigController.Options("HOST")
        url=f'{host}/amazon-bedrock/models/{self.model_id}'
        token=Charon(
            un=self.username, 
            pw=self.password, 
            api_key=self.subscriber_key
        )
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
            raise APICallFailedException(f'GenAI API call returned status code: {response.status_code}')
        log.debug(f'{response.status_code}, {response.text}')
        raw_response = response.json()
        log.debug(raw_response)
        return raw_response
    
    async def _aembedding_func(
            self, 
            text:str
    )->List[float]:
        text=text.replace(os.linesep, " ")
        _model_kwargs=self.model_kwargs or {}
        input_body={**_model_kwargs, "inputText":text}
        payload=json.dumps(input_body)
        host=ConfigController.Options("HOST")
        url=f'{host}/amazon-bedrock/models/{self.model_id}'
        token=Charon(
            un=self.username, 
            pw=self.password, 
            api_key=self.subscriber_key
        )
        headers={
            'Authorization':token, 
            "x-request-type":'async',
            'Content-Type': 'application/json', 
            'Mimeo-graffiti-subscription': self.subscriber_key
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
        correlation_id=response_json['correlation_id']
        callback = CallbackListener.AsyncCallback(
            apikey=self.api_key, 
            connection_string=self.connection_str, 
            message_queue=self.message_queue,
        )
        await callback._listen(correlation_id=correlation_id)
        response = callback.response 
        log.debug(response)
        return response['embedding']
    

    def embed_documents(self, texts):
        results=[]
        for text in texts:
            response = self._embedding_func(text)
            results.append(response)
        return results 
    
    def embed_query(self, text:str)->List[float]:
        return self._embedding_func(text)
    
    async def aembed_query(self, text:str)->List[float]:
        return self._aembedding_func(text)
    
    async def aembed_documents(
            self, 
            texts:List[str]
    )->List[List[float]]:
        result = await asyncio.gather(*[self.aembed_query(text) for text in texts])
        return list(result)
    
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
        
    def _get_provider(self)->str:
        return self.model_id.split('.')[0]
    