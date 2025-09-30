from enum import Enum
from typing import Dict, List, Any
from langchain.docstore.document import Document
from dataclasses import dataclass

from core.auth.control import MeterController as Control 
from core.model.embed import Embed

class Embeddings:


    class Service(Enum):
        Embeddings : Dict[List, Any]  = {
            'service' : 'embeddings', 
            'endpoint' : Control.ServiceController.getBaseUrl(), 
            'aimodel' : Embed.DEFAULT.value
        }


    class Model(Enum):
        DEFAULT="text-embedding-ada-002"
        MINI_LLAMA='mini-llama'
        TEXT_SIMILARITY_ADA_001='text-similarity-ada-001'
        TEXT_EMBEDDING_ADA_002='text-embedding-ada-002'
        TEXT_SIMILARITY_CURIE_001='text-similarity-curie-001'
        TEXT_CURIE_001='text-curie-001'
        TEXT_DAVINVCI_002='text-davinci-002'
        TEXT_ADA_001='text-ada-001'
        CODE_DAVINCI_002='code-davinci-002'


class BADGE:
    """
    Metered AUTH Use within the rcm systems for analytics filters.
    """

    class Setting:


        def __init__(
                self
            ):

            self.loggedin = False
            self.updates = Dict[List, Any] = {}

            self.token : str = ''
            self.endpoint : str = Control.ServiceController.getBaseUrl()
            self.model : str = Control.ModelController.getDefault()

            self.configs : Dict[List, Any] = {}


        def setConfigs(
                self, 
                params : Dict[List, Any]
            ):
            result = {}
            self.token = params['token']
            self.endpoint = params['emb']
            self.model = params['model']
            self.updated = True
            self.configs = result
            return result
        

        def getConfigs(
                self,
            ):
            params : Dict[List, Any] = {
                'status' : 'loggedout'
            }
            params.update({'token' : self.token})
            params.update({'emb' : self.endpoint})
            params.update({'model' : self.model})
            return params
        

        def setModel(
                self, 
                model : str
            )->bool:
            if model != None:
                self.setConfigs(params={
                    'model' : model
                })
                self.model = model
            else:
                self.setConfigs(params={
                    'model' : self.model
                })
            return True
            

        def getModel(
                self
            )->str:
            return self.model
        

        def Login(
                self,
                service:str, 
                emb:Embeddings=None 
            ):
            from core.auth.action.standard import MeteredAuth as Meter
            auth = Meter()
            params:Dict[List,Any]={}
            action = auth.authenticate()
            token:str=action['auth_token']
            self.model = self.getModel()

            embedurl = auth.getServiceEndpoint(
                subscription=service,
                model=self.model
            )
            params.update({'token':token})
            params.update({'emb':embedurl})
            params.update({'model':self.model})
            self.setConfigs(params)

            try:
                if params['token'] != None:
                    self.loggedin=True 
                    return params 
                
                else:
                    return params 
            except:
                raise Exception 
            
    
class Entity(Embeddings, BADGE):
    def __init__(
            self, 
            model=None
        ):
        if model == None:
            self.model = Embed.DEFAULT.value
        self.AUTH : Dict[List, Any] = BADGE.Setting().Login(
            emb = Embeddings.Service.Embeddings.value.get('endpoint'), 
            service = Embeddings.Service.Embeddings.value.get('service')
        )


    def singleton(self)->Dict[List, Any]:
        return self.AUTH
    

    class Crud:

        from core.auth.control import MeterController as Control

        def __init__(
                self
            ):
            default = Embed.DEFAULT.value
            self.thisinstance = Entity().singleton()
            self.token : str = self.thisinstance['token']
            self.service : str = self.thisinstance['service']
            self.model : str = self.thisinstance['model']
            if self.model == None:
                self.model = default


        def createEmbeddings(
                self, 
                input : str, 
                model : str = None
            ):
            control = Control.EmbedController 
            message = {'input' : str(input)}
            if model==None:
                self.model=self.model 
            else:
                self.model=model 
            if self.model==Embeddings.Model.MINI_LLAMA.value:
                if isinstance(input,str):
                    req=control.Format(
                        lines=[input]
                    )
                elif isinstance(input, Document):
                    req=control.Format(
                        lines=[input.page_content]
                    )
                else:
                    Control.ErrorController(unit="MINILLAMA")
                response=control.embedSpecial(
                    Control.ErrorController(unit="MINILLAMA"),
                    data=req 
                )
            else:
                response = Control.EmbedController.embedStandard(
                        endpoint=self.service.replace('None', self.model),
                        token=self.token, 
                        payload=message 
                )
                if response.status_code != 200:
                    print("Failed Response: ", response.text)
                if response.status_Code == 200:
                    em=response.json().get("data", [])[0]
                    emb=em.get("embedding", []) if em else []
                    return emb 
                

    class Embed:

        def embed_documents(
                texts, 
                chunk_size:int=None
        ):
            embeddings=[]
            for index, text in enumerate(texts):
                embedding_result = Entity.Crud().createEmbeddings(
                    input=text, 
                    chunk_size=chunk_size
                )
                embeddings.append(embedding_result)
                print(f"Embedded: {index+1}/{len(texts)}")
            return embeddings
        
        @staticmethod
        def embed_chunk(
            chunk:str
        ):
            embeddings=Entity.Crud().createEmbeddings(input=chunk)
            return embeddings



    