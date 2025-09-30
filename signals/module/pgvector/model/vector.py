from core.auth.control import MeterController
from .base import PGConnect
from langchain.vectorstores.pgvector import PGVector 
import pandas as pd 
from ast import literal_eval

class Store():

    def __init__(self):
        pass 

    def _connection_string(self):
        conn_string=PGVector.connection_string_from_db_params(
            driver="psycopg2", 

        )
        return conn_string 
    

    def read_datafile(self,filename):
        return pd.read_csv(filename)
    
    def get_collection_name(
            self, 
            filename,
    ):
        collection_name = filename.replace('.csv','')
        return collection_name 
    
    def load_column_embeddings(
            self,
            filename 
    ):
        print('[PGVector] State: Loading Embeddings for file: {}'.format(filename))
        collection_name=self.get_collection_name(filename)
        if not PGConnect().collection_exists(filename):
            dataset=self.read_datafile(filename)
            fields=dataset.columns.to_list()
            vectorstore = PGVector.from_texts(
                embeddings=MeterController.OpenAILLM.get_embed, 
                collection_name=collection_name, 
                connection_string=self._connection_string(),
                texts=fields,
                use_jsonb=True
            )

    def get_retriever(
            self, 
            collection_name,
    ):
        print("[PGVector] State: Getting retriever collection for {}".format(collection_name))
        retriever=PGVector(
            embedding_function=MeterController.OpenAILLM.get_embed, 
            connection_string=self._connection_string(), 
            collection_name=collection_name,
            use_jsonb=True 
        )
        return retriever 
    

    def similarity_search(
            self, 
            filename, 
            retriever
    ):
        print("[PGVector] State: Identify similarity of colums for the file {}".format(filename))
        col_mapping=[]
        dataset = self.read_datafile(filename)
        for col in dataset.columns.to_list():
            result=PGConnect().get_document_embed(
                collection_name=self.get_collection_name(filename), 
                document_name=col,
            )
            embeddings= literal_eval(result[0][1])
            response=retriever.similarity_search_with_score_by_vector(
                embeddings, 
                k=1
            )
            if response:
                col_mapping.append((col, response[0][0].page_content, response[0][1]))
            else:
                col_mapping.append((col, 'None', 'None'))
        return col_mapping
    
    
              