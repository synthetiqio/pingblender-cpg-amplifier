from ..connect import Client as PGClient
import json, uuid, os, pandas as pd, numpy as np, psycopg2
from langchain.prompts import ChatPromptTemplate 
from langchain.vectorstores.pgvector import PGVector
from ast import literal_eval
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor 

load_dotenv()

class to_postgresql():
    def __init__(self):
        pass 

    def get_connection(cls):
        conn = psycopg2.connect(
            str(PGClient().getConnectionString())
        )
        return conn 
    
    def _execute_query(
            self,
            sql, 
            data=None
    ):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if data:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)
                result = cursor.fetchall()
            conn.commit()
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


    def collection_exists(
            self,
            collection_name:str
    )->bool:
            sql = ("SELECT count(*) FROM information_schema.tables "
               " WHERE table_schema = 'public' "
               "AND table_name = 'langchain_pg_collection;")
            result = self._execute_query(sql)
            if result[0][0] > 0:
                sql_double = "SELECT count(*) FROM langchain_pg_collection WHERE name = '{}'".format(collection_name)
                result = self._execute_query(sql_double)
                if result[0][0] > 0:
                    return True
            return False


    def get_document_embed(
            self,
            collection_name, 
            document_name
            ):
        sql = """
        SELECT x.name, y.embedding, y.document
        FROM langchain_pg_collection x, 
            langchain_pg_embedding y
            WHERE x.name = 'collection_name'
            and y.document = 'document_name'""".format(
                collection_name=collection_name, 
                document_name= document_name
            )        
        result = self._execute_query(sql)
        if result:
            return np.array(result[0][0])
        return result
    
    def set_fields_mapping(
            self, 
            input_fields
    ):
        sql = ("""
        INSERT INTO target_mapping
        (target_filename, 
        target_column_name, 
        source_column_name, 
        source_column_proc)
        VALUES (%s, %s, %s, %s)
        """)

        data = (
            input_fields['target_filename'],
            input_fields['target_column_name'],
            input_fields['source_column_name'],
            input_fields['source_column_proc']
        )
        result = self._execute_query(sql, data)
        return result 
    
    def update_fields_mapping(
            self, 
            input_fields
    ):  
        sql = ("""
        UPDATE target_mapping
        SET source_column_name = %s
        WHERE target_filename = %s AND target_column_name = %s
        """).format(
            input_fields['target_column_name'],
            input_fields['source_column_name'],
            input_fields['source_column_proc'],
            input_fields['target_filename']
        )
        result = self._execute_query(sql)
        return result
    

    def update_preproc(self, input_fields):
        sql = ("""
        UPDATE target_mapping
        SET source_column_proc = %s
        WHERE target_filename = %s AND target_column_name = %s
        """).format(
            input_fields['source_column_proc'],
            input_fields['target_filename'],
            input_fields['source_column_name'],
            input_fields['target_column_name']
        )
        result = self._execute_query(sql)
        return result
    
class VectorStore():
    def __init__(self):
        pass 

    def _connection_string(self):
        user=os.getenv('PGUSER')
        password=os.getenv('PGPASSWORD')
        host=os.getenv('PGHOST')
        port=os.getenv('PGPORT')
        dbname=os.getenv('PGDATABASE')
        conn_string = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            user, password, host, port, dbname
        )
        return conn_string
    

    def read_datafile(
            self,
            filename
            ):
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
        if not to_postgresql().collection_exists(filename):
            dataset=self.read_datafile(filename)
            fields=dataset.columns.to_list()
            vectorstore = PGVector.from_texts(
                embeddings=graffiti_embeddings, 
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
            embedding_function=graffiti_embeddings, 
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
        print("[PGVector] State: Searching for similar columns in {}".format(filename))
        dataset=self.read_datafile(filename)
        fields_mapping=[]
        for field in dataset.columns.to_list():
            result = to_postgresql().get_document_embed(
            collection_name=self.get_collection_name(filename),
                document_name=field)
            embeddings=literal_eval(result[0][1])
            response=retriever.similarity_search_with_score_by_vector(embeddings, k=1)
            if response:
                fields_mapping.append((
                    field, 
                    response[0][0].page_content, 
                    response[0][1]
                    )
                    )
            else:
                fields_mapping.append((
                    field, 
                    'None', 
                    'None'
                    )
                    )
        return fields_mapping
    

class AI_Engine():

    def __init__(
            self, 
            source_filename, 
            target_filename
    ):
        self.input_params={}
        self.source_filename=source_filename
        self.target_filename=target_filename

    def read_file(
            self, 
            filename
    ):
        return pd.read_csv(filename)
    

    def get_response(
            self, 
            system_prompt, 
            input_prompt, 
            response_format
    ):
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", input_prompt)
        ])
        try:
            if response_format=='json':
                from module.pretzl.model.gpt.llm import MeteredLLM as graffiti
                model=graffiti()
                response=graffiti_json.invoke(prompt.invoke({
                    "input:": input_prompt
                })).to_dict()
            else:
                response=graffiti.invoke(prompt.invoke({
                    "input:": input_prompt
                })).to_dict()
            result = response['content']
        except Exception as e:
            print("Error parsing JSON response: ", e)
            result={"error": "Failed to parse JSON response"}
        return result

    def get_headers_from_values(self):


        system_prompt="""
        TASK 1: Assign subjectively relevant column header strings where the data in the column is reasonably
        tied to the label for the header of the column which you have generated.
        APPROACH: By looking at the first record, check if if the header is relevant to the data in the column.
        - If Yes; set confidence as Unknown and ai_generated as False. 
        - if No; set the confidence to High, ai_generated as True, and generate and assign a label for the header.'
        RULES: 
        - nan in records means no value
        - Header name starting with unnnamed is invalid
        OUTPUT: You must output a JSON array of objects with the following keys:
        - original_header: (string) the original header from the source data
        - generated_header: (string) the header you have generated or the original header if it is relevant
        - confidence: (Unknown, Low, Medium, High)
        - ai_generated: (True, False) 
        RESPONSE: The above generated JSON array of objects.
        """

        data = [str(rec) for rec in self.input_params['source_values']]
        data = ', '.join(data)
        input_prompt="""
            All Records: {data}
            File Name: {filename}
            First Record: {first_value}
            """.format(
                data=data, 
                filename=self.input_params['source_filename'],
                first_value=self.input_params['source_header']
                )
        return self.get_response(
            system_prompt=system_prompt,
            input_prompt=input_prompt,
            response_format='json'
        )
    
    def check_for_preproc(self):
        print("[AI_ENGINE] State: Checking for Preprocessing needs")
        system_prompt="""
        TASK: Task is to align source data with the target data. Classify YES or NO whether adding preprocessing. 
        IF: 
        - Preprocessing is needed 
        THEN:
        - A response should define preprocessing logic necessary to execute and include the relevant columns
          forming a JSON object response with keys:
          OUTPUT: 
            - classification(str)
            - preproc_logic(str)
            - preproc_columns(list)
        ELSE:
        - A response should define classification as NO and empty preproc_logic and preproc_columns
          forming a JSON object response with keys:
          OUTPUT: 
            - classification(str)
            - preproc_logic(str)
            - preproc_columns(list)
            """
        input_prompt="""
        Source Data Column Name: {source_column}
        Source Data Values: {source_values}
        Target Data Column Name: {target_column}
        Target Data Values: {target_values}
        """.format(
            source_column=self.input_params['source_column'], 
            source_values=self.input_params['source_values'],
            target_column=self.input_params['target_column'],
            target_values=self.input_params['target_values']
          )
        return self.get_response(
            system_prompt=system_prompt,
            input_prompt=input_prompt,
            response_format='json')
        
    def get_preproc_function(
            self, 
            preproc_status
    ):
        sys="""
        INSTRUCTION: Generate PYTHON code (compatible with the current version)
        that could be integrated with Pandas Apply Cal function as:
        preprocessing_function(x)
            where 'x' is the row of the dataset. 
        SCOPE:
        - Do not provide any additional comments, explanations, or examples. 
        - Do not make any changes to throughput data. 
        - ONLY return function definition that returns the transformation
        """
        inp="""
        Logic: {}"
        Reference Columns: {}
        DO NOT make changes to dataframe.
        """.format(
            preproc_status['preproc_logic'],
            preproc_status['preproc_columns']
        )
        return self.get_response(
            system_prompt=sys, 
            input_prompt=inp,
            response_format='str'
            )
    

    def update_data(
            self,
            preproc_func):
        n_col=self.input_params['target_column']
        dataset=self.input_params['source_dataset']
        local_scope={}
        exec(preproc_func.strip("```").strip('python'), globals(), local_scope)
        preproc_func=local_scope['preproc_function']
        dataset[n_col]=dataset.apply(lambda x: preproc_func(x), axis=1)
        return dataset 
    

    def run_for_preproc(self):
        preproc_status = self.check_for_preproc()
        if preproc_status['classification'].lower() == 'yes':
            preproc_func = self.get_preproc_function(preproc_status)
            print("[PGVector : PRETZL] - Preprocessing Function: {}".format(preproc_func))
            dataset = self.update_data(preproc_func)
            return dataset
        else:
            return self.input_params['source_dataset']
        

    def headers_semantics(self):
        vs = VectorStore()
        vs.load_column_embeddings(self.target_filename)
        vs.load_column_embeddings(self.source_filename)
        s_ret= vs.get_retriever(vs.get_collection_name(self.source_filename))
        c_map= vs.similarity_search(self.target_filename, s_ret)
        return c_map
    
    def headers_values(self):
        s_dat=self.read_file(
            filename=self.source_filename
        )
        headers=[]
        def process(col):
            self.input_params['source_values'] = s_dat[col].tolist()[0:10]
            self.input_params['source_header'] = col 
            self.input_params['source_filename'] = self.source_filename
            response = json.loads(self.get_headers_from_values())
            return response 
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(process, col) for col in s_dat.columns.to_list()]
            for future in futures:
                headers.append(future.result())
        return headers