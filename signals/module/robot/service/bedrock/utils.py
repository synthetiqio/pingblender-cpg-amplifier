import json 
from typing import  Dict, Any, List, Optional, Mapping 
from abc import ABC
from langchain_community.llms.bedrock import _human_assistant_format 
from langchain.pydantic_v1 import BaseModel 

class LLMIO_Adapter:

    provider_to_output_key_map={
        "anthropic":"completion", 
        "amazon":"outputText", 
        "cohere":"text",
    }

    @classmethod
    def prepare_input(
        cls, 
        provider:str, 
        prompt:str, 
        model_kwargs:Dict[List,Any]
    )->Dict[str, Any]:
        input_body={**model_kwargs}
        if provider == "anthropic":
            input_body['prompt']= _human_assistant_format(prompt)
        elif provider == 'ai21' or provider == 'cohere':
            input_body['prompt']=prompt 
        elif provider == 'amazon':
            input_body=dict()
            input_body['inputText']=prompt 
            input_body['textGenerationConfig']= {**model_kwargs}
        else:
            input_body['inputText']=prompt 
        if provider =='anthropic' and 'max_tokens_to_sample' not in input_body:
            input_body['max_tokens_to_sample']  = 256 
        return input_body
    
    @classmethod
    def prepare_output(
        cls, 
        provider:str, 
        response:Any 
    ):
        if provider == 'anthropic':
            return response.get("completion")
        elif provider in ['ai21', 'amazon']:
            response_body = response 
        else: 
            response_body = json.loads(response.get("body").read())

        if provider == 'ai21':
            return response_body.get("completions")[0].get("data").get("text")
        elif provider == "cohere":
            return response_body.get("generations")[0].get("text")
        else: 
            return response_body.get("results")[0].get("outputText")
        

class Bedrock_Base(BaseModel, ABC):
    model_id:str 
    model_kwargs:Optional[Dict]=None 

    provider_stop_sequence_key_name_map:Mapping[str, str]={
        "anthropic":"stop_sequences", 
        "amazon":"stopSequences", 
        "ai21":"stop_sequences", 
        "cohere":"stop_sequences"
    }

    username:Optional[str]=None 
    password:Optional[str]=None 
    dataplatform_apikey:Optional[str]=None 

    @property 
    def _identifying_params(self)->Mapping[str, Any]:
        _model_kwargs=self.model_kwargs or {}
        return {
            **{"model_kwargs":_model_kwargs}
        }

    def _get_provider(self)->str:
        return self.model_id.split(".")[0]
    
    @property 
    def _model_is_anthropic(self)->bool:
        return self._get_provider()=="anthropic"
    