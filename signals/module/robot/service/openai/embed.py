import json, os, ssl, requests, aiohttp, asyncio, itertools, logging 
log = logging.getLogger(__name__)
from typing import Optional, Any, List 
import numpy as np 

from langchain.embeddings.base import Embeddings 
from module.robot.service.callback import Listener
from module.robot.control import Config as ConfigControl 
CERT=ConfigControl.Sys.CERT_PATH

from module.robot.service.exception import InvalidJWTException, APICallFailedException
from module.robot.action.meter import Charon 

class AzureOpenAIEmbeddings(Embeddings):
    apikey:str
    api_version:str 
    connection_str:Optional[str]
    message_queue:Optional[str]
    model:str 
    embedding_ctx_length:int=8191 
    chunk_size:int=1000 
    max_retries:int=6
    show_progress_bar:bool=False 

    def __init__(
            self, 
            **kwargs:Any
    ):
        for key, value in kwargs.items():
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
        
    def embed(
            self,
            input_data
    ):
        url=f'{os.getenv("HOST")}/openai/deployments/{self.model}/embeddings?api-version={self.api_version}'
        payload= json.dumps({
            'input': input_data
        })
        log.debug(f'Embdding inputs: {input_data}')
        token=Charon(
            un=self.username, 
            pw=self.password, 
            api_key=self.subscription_key
        ).get_token()
        if token is None:
            raise InvalidJWTException(f"Failed to get JWT Auth Token")
        headers={
            'Authorization': token, 
            'x-request-type': 'sync', 
            'Content-Type':'application/json', 
            'Mimeo-graffiti-subscription': self.apikey
        }
        response = requests.request(
            method='POST', 
            url=url,
            headers=headers, 
            data=payload, 
            verify=CERT
        )
        if response.status_code != 200:
            raise APICallFailedException(f'GenAI API Call returned statuscode: {response.status_code} '
                                         f'Message: {response.text}')
        response = response.json()
        return response 
    

    async def aembed(
            self,
            input_data
    ):
        self._validate_async_params()
        url=f"{os.getenv("HOST")}/openai/deployments/{self.model}/embeddings?api-version={self.api_version}"
        payload={
            'inputs':input_data
        }
        token=Charon(
            un=self.username, 
            pw=self.password, 
            api_key=self.subscription_key
        ).get_token()
        if token is None:
            raise InvalidJWTException("Failed to get JWT Auth Token")
        headers={
            'Authorization': token, 
            'x-request-type': 'async', 
            'Content-Type':'application/json', 
            'Mimeo-graffiti-subscription': self.apikey
        }
        ssl_context = ssl.create_default_context(cafile=CERT)
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_context)
        ) as session:
            async with session.post(
                url=url, 
                headers=headers, 
                json=payload 
            ) as response:
                response_json = await response.json()
                log.debug(f"{response.status}, {response.text}")
        if response.status != 202:
            raise APICallFailedException(
                f'GenAI API call returned statuscode: {response.status}'
                f'Message:{response.text}'
                )
        correlation_id=response_json['correlation_id']
        callback_handler=Listener.AsyncCallback(
            apikey=self.apikey,
            api_version=self.api_version, 
            connection_string=self.connection_str, 
            queue=self.message_queue
        )
        await callback_handler._listen(correlation_id=correlation_id)
        response = callback_handler.response 
        return response 
    

    def _get_len_safe_embeddings(
            self, 
            texts:List[str], 
            *, 
            chunk_size:Optional[int]=None
    )->List[List[float]]:
        embeddings:List[List[float]]=[[] for _ in range(len(texts))]
        try:
            import tiktoken
        except ImportError:
            raise ImportError(
                "Could not import tiktoken python package"
                "This is needed in order for AzureOpenAIEmbeddings"
                "Please install it with 'pip install tiktoken'"
            )
        tokens=[]
        indices=[]
        model_name=self.model 
        try:
            encoding=tiktoken.encoding_for_model(model_name)
        except KeyError:
            log.warning("Warning: model not found. Using cl100k_base encoding.")
            model="cl100k_base"
            encoding=tiktoken.get_encoding(model)
        for i, text in enumerate(texts):
            if self.model.endswith("001"):
                text = text.replace("\n", " ")
            token=encoding.encode(
                text
            )
            for j in range(0, len(token), self.embedding_ctx_length):
                tokens +=[token[j: j+self.embedding_ctx_length]]
                indices += [i]
        batched_embeddings = []
        _chunk_size = chunk_size or self.chunk_size
        if self.show_progress_bar:
            try:
                import tqdm
                _iter=tqdm.tqdm(range(0,len(tokens), _chunk_size))
            except ImportError:
                _iter=range(0, len(tokens), _chunk_size)
        else:
            _iter=range(0, len(tokens), _chunk_size)

        for i in iter:
            response = self.embed(
                tokens[i: i+ _chunk_size],
            )
            batched_embeddings += [r['embedding'] for r in response['data']]
        results: List[List[List[float]]] = [[] for _ in range(len(texts))]
        num_tokens_in_batch: List[List[int]] = [[] for _ in range(len(texts))]
        for i in range(len(indices)):
            results[indices[i]].append(len(tokens[i]))

        for i in range(len(texts)):
            _result = results[i]
            if len(_result) == 0:
                average = self.embed("")['data'][0]['embedding']
            else:
                average = np.average(_result, axis=0, weights=num_tokens_in_batch[i])
            embeddings[i] = (average / np.linalg.norm(average)).tolist()
        return embeddings 
    

    async def _aget_len_safe_embeddings(
            self, 
            texts:List[str], 
            *, 
            chunk_size:Optional[int]=None,
    )->List[List[float]]:
        embeddings:List[List[float]]= [[] for _ in range(len(texts))]
        try:
            import tiktoken
        except ImportError:
            raise ImportError(
                "Could not import tiktoken python package"
                "This is needed in order for AzureOpenAIEmbeddings"
                "Please install it with 'pip install tiktoken'"
            )
        tokens=[]
        indices=[]
        model_name=self.model 
        try:
            encoding=tiktoken.encoding_for_model(model_name)
        except KeyError:
            log.warning("Warning: model not found. Using cl100k_base encoding.")
            model="cl100k_base"
            encoding=tiktoken.get_encoding(model)
        for i, text in enumerate(texts):
            if self.model.endswith("001"):
                text = text.replace("\n", " ")
            token=encoding.encode(
                text
            )
            for j in range(0, len(token), self.embedding_ctx_length):
                tokens +=[token[j: j+self.embedding_ctx_length]]
                indices += [i]
        batched_embeddings = []
        _chunk_size = chunk_size or self.chunk_size
        if self.show_progress_bar:
            try:
                import tqdm
                _iter=tqdm.tqdm(range(0,len(tokens), _chunk_size))
            except ImportError:
                _iter=range(0, len(tokens), _chunk_size)
        else:
            _iter=range(0, len(tokens), _chunk_size)

        for i in iter:
            response = self.aembed(
                tokens[i: i+ _chunk_size],
            )
            batched_embeddings += [r['embedding'] for r in response['data']]
        results: List[List[List[float]]] = [[] for _ in range(len(texts))]
        num_tokens_in_batch: List[List[int]] = [[] for _ in range(len(texts))]
        for i in range(len(indices)):
            results[indices[i]].append(len(tokens[i]))

        for i in range(len(texts)):
            _result = results[i]
            if len(_result) == 0:
                average = self.embed("")['data'][0]['embedding']
            else:
                average = np.average(_result, axis=0, weights=num_tokens_in_batch[i])
            embeddings[i] = (average / np.linalg.norm(average)).tolist()
        return embeddings 
    
    def embed_documents(
            self, 
            texts:List[str], 
            chunk_size:Optional[int]=16
        )->List[List[float]]:
        if chunk_size <= 0 or chunk_size > 16:
            chunk_size=16 
        num_texts=len(texts)
        embedded_texts=[]
        for i in range(0, num_texts, chunk_size):
            chunk = texts[i:i + chunk_size]
            embeddings = self._get_len_safe_embeddings(chunk)
            embedded_texts.extend(embeddings)
        return embedded_texts

    async def aembed_documents(
            self, 
            texts:List[str], 
            chunk_size:Optional[int]=16
        )->List[List[float]]:
        if chunk_size <= 0 or chunk_size > 16:
            chunk_size=16 
        num_texts=len(texts)
        texts_chunk=[texts[i:i + chunk_size] for i in range(0, num_texts, chunk_size)]
        embedded_texts= await asyncio.gather(([self._aget_len_safe_embeddings(chunk) for chunk in texts_chunk]))
        embedded_texts= list(itertools.chain(*embedded_texts))
        return embedded_texts
    

    def embed_query(self, text:str)->List[float]:
        if len(text) > self.embedding_ctx_length:
            return self._get_len_safe_embeddings([text])[0]
        else:
            if self.model.endswith("001"):
                text = text.replace("\n", " ")
            return self.embed([text])['data'][0]['embedding']
        

    async def aembed_query(
            self, 
            text:str, 
    )->List[float]:
        if len(text) > self.embedding_ctx_length:
            return self._aget_len_safe_embeddings([text])[0]
        else:
            if self.model.endswith("001"):
                text=text.replace("\n", " ")
            return (await self.aembed([text]))['data'][0]['embedding']