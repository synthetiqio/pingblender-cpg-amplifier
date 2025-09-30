from fastapi import Depends
from core.model.document import Construct
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession, 
    async_sessionmaker
)
from langchain_community.vectorstores.pgvector import PGVector as Client
from typing import Dict, List, Any
from enum import Enum
import os
from dotenv import load_dotenv
load_dotenv()


if os.environ.get("DOCKERIZED") == "true" and os.environ.get("POSTGRES_HOST"):
    hostname = os.environ.get("POSTGRES_HOST", "host.docker.internal")
    stringslash = "/"
else:
    hostname = "localhost"


class PGVECTOR:

    ERROR_MSG : Dict[List, Any] = {
        'result' : 'Failure',
        'message' : '[PGVector Interface | Client | Service] : an issue prevented exec unit',
        'payload' : None
    }

    def getConnectionString()->str:
        o = Client.connection_string_from_db_params(
            driver= os.environ.get("POSTGRES_DRIVER", "psycopg2"),
            host= hostname,
            port= os.environ.get("POSTGRES_PORT", 5432),
            database=os.environ.get("POSTGRES_DB", "postgres"),
            user=os.environ.get("POSTGRES_USER", "postgres"),
            password=os.environ.get("POSTGRES_PASSWORD", "password")
        )
        return o


class ORM:
    class Db:
        class P(Enum):
            HO:str= hostname
            DR:str= os.environ.get("POSTGRES_DRIVER")
            PO:str= os.environ.get("POSTGRES_PORT", 5432)
            DB:str= os.environ.get("POSTGRES_DB")
            US:str= os.environ.get("POSTGRES_USER")
            PW:str= os.environ.get("POSTGRES_PASSWORD")

    def getConnectionString(
            ssl:str=False
        ):
        if ssl==True:
            mode = ''
        else:
            host=ORM.Db.P['HO'].value
            if host in ['postgres', 'localhost']:
                mode = '?sslmode=disable'
            else:
                mode=''
        user: str = ORM.Db.P["US"].value
        passw: str = ORM.Db.P["PW"].value
        host: str = ORM.Db.P["HO"].value
        port: str = ORM.Db.P["PO"].value
        schema: str = ORM.Db.P["DB"].value
        connstr: str = "postgresql://"+user+":"+passw+"@"+host+":"+port+"/"+schema+mode
        return connstr



    class ORMConnect:

        async def GetSession()->AsyncSession:
            engine = create_async_engine(str(PGVECTOR.getConnectionString()))
            Session = async_sessionmaker(bind=engine)
            session = await Session()
            return session
        
class Config: 

    def __init__(
            self, 
            state : str, 
            meta : Construct = Depends(Construct)
    ):
        self.current_config = meta
        self.current_state = state

    class Connect(Enum):
            PGVSTRING : str = PGVECTOR.getConnectionString()
            ORMSTRING : str = ORM.getConnectionString()

    
    class defaults(Enum):
        COLL_NAME_DEFAULT : str = 'data_store'
        SCHEMA_JSON_DEFAULT : str = 'episodiq_schema'
        MG_CONTROL_SCHEMA : str = ORM.Db.P['DB'].value

    class variable(Enum):
        COLL_NAME_DEFAULT : str = 'data_store'
        SCHEMA_JSON_DEFAULT : str = 'episodiq_schema'

    class evaluate(Enum):
        COLL_NAME_DEFAULT : str = 'data_store'
        SCHEMA_JSON_DEFAULT : str = 'episodiq_schema'


    class Custom:
        pass