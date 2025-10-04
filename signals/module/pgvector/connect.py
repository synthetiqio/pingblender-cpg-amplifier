import os
from dotenv import load_dotenv
from typing import (
    Any, 
    Dict,
    Callable, 
    Iterable,
    List, 
    Optional, 
    Tuple

)
#editable local units.
from core.model.document import Construct
from module.pgvector.config import Config
from module.pgvector.action.embed import (
    BADGE as Request, 
    Entity as Body
)
from core.model.embed import Embed


from fastapi import Depends
import sqlalchemy
from sqlalchemy.ext.asyncio import (
    AsyncEngine, 
    AsyncSession, 
    create_async_engine
)

#langchain dependencies.
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_community.document_loaders import text

load_dotenv()

cfg = Config(
        state = "start", 
        meta = Construct
    )

class Client:

   def __init__(
         self, 
         meta : Optional[Construct]
      ):
      self.configs = meta
      self.embed_model = self.modelControl()
   
   
   def _getConfigs(self):
      return self.configs
   


   def modelControl(
           self, 
           update:str= None
        )->str:
        a = Request.Setting()
        if update == None:
            output:Dict[List, Any]= a.getConfigs()['model']
        else:
            output:Dict[List, Any]= a.setConfigs({'model': update})
        self.embed_model = output
        return self.embed_model

             
   
   ###need openai interface model here.
   def embedDocs(
         self, 
         data:text, 
         chunk:Optional[int]= 100
      ):
      result = Body.Embed.embed_documents(
          data, 
          chunk_size=chunk
          )
      return result
   

   def embedChunks(
           self, 
           data : text,
           chunk : Optional[int] = 100
      )->list:
       result = Body.Embed.embed_chunk(
           texts=data, 
           chunk_size=chunk, 
           model=self.embed_model
       )
       return result


   def createEmbeddings(
         self, 
         data: text, 
         runner: Body.Embed, 
         chunk: Optional[int] = 100
      ):
      return runner.embed_chunk(data, chunk_size=chunk)
   

   def getConnectionString(
         self,
      )->str:
      from module.pgvector.config import PGVECTOR as shuf
      self.connectionstring = shuf.getConnectionString()
      return self.connectionstring



class Interface: 

   def __init__(
            self, 
            metadatas: Dict[list, Any], 
            collection_name: str,
            configs: Construct = Depends(Construct),
            documents: list = None,
            pre_delete_collection: bool = False,
            relevance_score_fn: Optional[Callable[[float], float]] = None,
            *,
            connection: Optional[sqlalchemy.engine.Connection] = None,
            engine_args: Optional[dict[str, Any]] = None
      ):

      self.cfgs = Dict[list] = configs
      self.client = Client(self.cfgs)
      self.connect = self.client.getConnectionString()


      self.collection = collection_name 
      self.documents = List[Document] = documents
      self.meta = metadatas
      self.emb_model : str = self.client.modelControl()
      self.embeddings : Embeddings = []
      self.engine = connection 
      self.relevance_score = relevance_score_fn
      self.engine_args = engine_args

      self.filter : dict = {}
      
      self.db = PGVector(
         embedding_function=self.embeddings, 
         collection_name=self.collection,
         collection_metadata=self.meta, 
         connection_string = self.connect, 
         relevance_score_fn=self.relevance_score,
         connection=self.engine, 
         engine_args=self.engine_args
      )


   async def setEmbeddings(
           self, 
           embeddtings : Embeddings
   )->bool:
       self.embeddings : Embeddings = Embeddings
       return True


   def getPGEngine(
           self,
   )->AsyncEngine:
      engine : AsyncEngine 
      conn = self.connect
      engine = create_async_engine(
          conn, 
          pool_pre_ping=True
      )
      self.engine : AsyncEngine = engine
      return self.engine
   

   def loadEmbeddingsFromDocument(
            self
        )->bool:
        self.db.from_documents(
           embedding=self.embeddings, 
           documents= self.documents,
           collection_name=self.collection, 
           connection_string=self.connect
        )
        return True


   def loadDocuments(
           self, 
           chunk
   )->bool:
       result = self.db.add_documents([chunk])
       print(f'Stored id: {result} in {self.collection}')
       return result


   def appendEmbeddings(
            self, 
            texts: Iterable[str],
            ids: Optional[List[str]] = None
         )->List[str]:
         result = self.db.add_embeddings(
            text = texts,
            embeddings=self.embeddings,
            metadatas=self.meta,
            ids = ids
         )
         return result
   

   def deleteObjects(
            self,
            ids: Optional[List[str]] = None,
            collection_only: bool = False
         )->bool:
         self.db.delete(ids, collection_only)
         return True
   

   def createPGCollection(
            self,
         )->bool:
         print("Collection "+self.collection+" created")
         return True
   


   def retrieverInvocation(
           self
   )->PGVector:
      ret = self.db.from_documents(
           embedding=self.embeddings,
           documents=self.documents, 
           collection_name = self.collection, 
           connection_string = self.connect
         )
      return ret.as_retriever()

   def runSimilaritySearch(
           self, 
           asking: str,
           fileter : Optional[dict] = None
   )->List:
       pass


   def runScoredSimilaritySearch(
           self, 
           asking: str, 
           filter: Optional[dict] = None
   )->List [Tuple[Document, float]]:
         result = self.db.similarity_search_with_score(
            query=asking, 
            k = 10,
            filter=filter
         )
         return result
   
   def constructPromptTemplate(
           self, 
           selected : int
   ):
       from langchain_core.prompts import PromptTemplate
       prom = PromptTemplate.from_template(selected)
       return prom

   def chainBuilder():
       return 