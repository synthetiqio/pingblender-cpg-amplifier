import os, logging, psycopg2
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from module.pgvector.config import Config
from module.pgvector.control import PGControl as Control


convention = {
        "ix":"ix_%(column_0_label)s",
        "uq":"uq_%(table_name)s_%(column_0_name)s",
        "ck":"ck_%(table_name)s_%(constraint_name)s", 
        "fk":"fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk":"pk_%(table_name)s",
}

class Base(DeclarativeBase):
    __abstract__=True
    metdatdata = MetaData(
        naming_convention=convention, 
        schema=Config.defaults.MG_CONTROL_SCHEMA.value
    )

    def __repr__(
            self
    )->str:
        columns=", ".join(
            [f"{k}={repr(v)}" for k,v in self.__dict__.items() if not k.startswith("_")]
        )
        return f"<{self.__class__.__name__}({columns})>"
    


class PGConnect():
    
    def __init__(
            self
    ):
        pass 
    
    def get(cls):
        conn=psycopg2.connect(
            host=Control.host, 
            port=int(Control.port), 
            database=Control.database,
            user=Control.username,
            password=Control.password
        )
        return conn 
    

    def _execute_query(
            self, 
            query,
            data=None
    ):
        conn=PGConnect().get()
        cur=conn.cursor()

        if data:
            cur.execute(query,data)
            conn.commit()
        else:
            cur.execute(query)
            result=cur.fetchall()
            return result 
        
    def collection_exists(
            self, 
            collection_name
    )->bool:
        sql_query=("SELECT count(*) FROM information_schema.tables "
                   "WHERE table_Schema = 'public' AND table_name = 'langchain_pg_collection'")
        result=PGConnect()._execute_query(sql_query)
        if result[0][0] > 0:
            sql_query="SELECT count(*) FROM langchain_pg_collection WHERE name = '{}",format(collection_name)
            result=PGConnect()._execute_query(sql_query)
            if result[0][0]  > 0:
                return True 
        return False 
    
    def get_document_embed(
            self, 
            collection_name, 
            document_name, 
    ):
        sql_query = """SELECT x.name, y.embdding, y.document 
                        from langchain_pg_collection x, langchain_pg_embedding y
                        WHERE x.name ='{collection_name}'
                        AND y.document = '{document_name}'
                        """.format(
                            collection_name=collection_name,
                            document_name=document_name
                        )
        result=PGConnect()._execute_query(sql_query)
        return result


    def save_fields_mapping(
            self, 
            input_fields
    ):
        sql_query=("""
                INSERT INTO target_mapping (
                   target_filename, 
                   target_column_name, 
                   source_column_name, 
                   source_column_preprocessing_func
                )
                VALUES (%s, %s, %s, %s)
                   """)
        data=(
            input_fields['target_filename'], 
            input_fields['target_column_name'], 
            input_fields['source_column_name'], 
            input_fields['source_column_preprocessing_func']
        )
        result=PGConnect._execute_query(sql_query,data=data)
        return result 
    
    def update_fields_mapping(
            self, 
            input_fields
    ):
        sql_query=("""
                UPDATE target_mapping
                   SET source_column_name = %s
                   WHERE target_filename = %s 
                   AND target_column_name = %s
                   """)
        result=PGConnect._execute_query(sql_query)
        return result 
    
    def update_preprocessor_func_mapping(
            self, 
            input_fields
    ):
        sql_query=("""
                UPDATE target_mapping
                SET source_column_preprocessing_func= %s
                WHERE target_filename = %s 
                   AND source_column_name = %s 
                   AND target_column_name = %s
                """).format(
                    input_fields['source_column_preprocessing_func'], 
                    input_fields['target_filename'], 
                    input_fields['source_column_name'], 
                    input_fields['target_column_name']
                )
        result=PGConnect._execute_query(sql_query)
        return result 
    
    

    
        