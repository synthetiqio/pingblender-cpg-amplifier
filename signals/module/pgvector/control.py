import os, uuid, datetime, json, base64
from fastapi import UploadFile as Subject 
from typing import Dict, List, Any
from enum import Enum
from sqlalchemy import (
    create_engine, 
    Index,
    select, 
    text, 
    types,
    Integer, 
    String, 
    DateTime, 
    UUID as StoreID, 
    Row, func
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm  import (
    DeclarativeBase, 
    Mapped, 
    MappedAsDataclass, 
    mapped_column,
    sessionmaker
)



from core.config import System as CoreSys
from module.pgvector.config import ORM
from module.pgvector.connect import Interface 

class Control(MappedAsDataclass, DeclarativeBase):
    pass 

class System(CoreSys):

    def __init__(
            self, 
            timezone:str= None
    ): 
        if timezone:
            self.region= timezone

    def getTimeStamp(self):
        return CoreSys.SYS.getRegionalEnv(tmz=self.region)
    
    def getRegionEnv(self):
        self.region = CoreSys.SYS.getRegionalEnv()
        return self.region
    

class Collection: 
    class Entity:

        from sqlalchemy import event
        from sqlalchemy.sql import column
        from sqlalchemy.orm import Session


        class Query:

            def __init__(
                    self, 
                    lookup_key
                ):
                
                connect = ORM.getConnectionString()
                engine = create_engine(connect)

                self.Session= sessionmaker(bind=engine)
                self.session= self.Session()
                self.lookup= lookup_key 
                self.body:Dict[List, Any] = {}
                self.result= {}

                self.lu = {
                    'o' : Collection.Entity.Entry.entity_sfid, 
                    'l' : Collection.Entity.Entry.entity_label, 
                    'n' : Collection.Entity.Entry.entity_name, 
                    't' : Collection.Entity.Entry.entity_type,
                    'trace' : Collection.Entity.Trace.entity_trace, 
                    'process': Collection.Entity.Processed.entity_sfid
                }

            def getFileList(
                        self, 
                        metadata
                ):
                self.case = metadata['inputs']['type']
                result = self._getUnits(
                    search=self.case, 
                    vextor=self.lu['t']
                )
                return result
            

            def getTargetList(
                    self, 
                    metadata
                ): 
                self.case = 'target'
                result = self._getUnits(
                    search=self.case, 
                    vector = self.lu['t']
                )
                return result
            

            def getReadablesList(
                    self,
            ):
                self.case='.pdf'
                result=self._getList(
                    search=self.case,
                    vector=self.lu['n']
                )
                return result 
            

            def entity_trace(
                    self, 
                    geturl: bool = False
                )->Dict[List, Any]:
                getcheck = self.lookup
                params = locals()
                result = self._getTracer(
                    search=getcheck, 
                    params=params, 
                    vector=self.lu['trace']
                )
                return result
            
            def entity_label(
                    self, 
                    geturl : bool = False
                )->Dict[List, Any]:
                getcheck = self.lookup
                params = locals()
                result = self._getTracer(
                    search=getcheck, 
                    params=params, 
                    vector=self.lu['l']
                )
                return result
            
            def entity_labels(
                    self, 
                    geturl:bool=False
            ):
                getcheck=self.lookup
                params=locals()
                result=self._getUnits(
                    search=getcheck, 
                    vector=self.lu['l']
                )
                return result 
            

            def filename(
                    self,
            ):
                getcheck=self.lookup
                params=locals()
                result=self._getAttr(
                    search=getcheck, 
                    params=params,
                    vector=self.lu['o']
                )
                return result 
            
            
            def entity_sfid(
                    self, 
                    geturl : bool = False
                )->Dict[List, Any]:
                getcheck = self.lookup
                params = locals()
                result = self._getTracer(
                    search=getcheck, 
                    params=params, 
                    vector=self.lu['o']
                )
                return result
            
            def entity_name(
                    self, 
                    geturl : bool = False
                )->Dict[List, Any]:
                getcheck = self.lookup
                params = locals()
                result = self._getUnit(
                    search=getcheck, 
                    params=params, 
                    vector=self.lu['n']
                )
                return result
            
            def process_record(self)->Dict[List,Any]:
                entity_sfid=self.lookup
                params=locals()
                result=self._getProcessUnit(
                    search=entity_sfid, 
                    vector=self.lu['process']
                )
                return result 
            
            def _getProcessUnit(
                    self, 
                    vector:str, 
                    search
            ):
                table=Collection.Entity.Processed
                session=self.Session()
                stt=(
                    select(
                        table.entity_sfid, 
                        table.process_type, 
                        table.process_id
                    ).where(
                        vector==search
                    ).order_by(table.timestamp.desc())
                    .limit(1))
                runquery=session.execute(stt)
                result=runquery.fetchone()
                session.commit()
                session.flush()
                if result:
                    return result._asdict()
                else:
                    return result                 


            def _getTracer(
                    self, 
                    search : str, 
                    params : Dict[List, Any], 
                    vector : str
            ):
                settings = params
                table = Collection.Entity.Trace
                session = self.Session()
                stt = select(
                    table.entity_trace, 
                    table.entity_key, 
                    table.trace_id, 
                    table.timestamp, 
                    table.entity_event) \
                .where(
                    vector == search
                )
                runquery= session.execute(stt)
                result= runquery.fetchall()
                session.commit()
                session.flush()
                packupdate:list[dict]= []
                for row in result:
                    packupdate.append(row._asdict())
                return packupdate
                
            def _getUnits(
                    self, 
                    search : str, 
                    vector : str
                ):
                table = Collection.Entity.Entry
                session = self.Session()
                stt = select(
                        table.entity_sfid, 
                        table.entity_name, 
                        table.entity_label,
                        table.entity_type, 
                        table.entity_trace,
                        table.timestamp,
                        table.entity_pack) \
                    .where(
                    vector == search
                    )
                runquery = session.execute(stt)
                result = runquery.fetchall()
                session.commit()
                session.flush()
                packupdate : list[dict] = []
                for row in result:
                    packupdate.append(row._asdict())
                return packupdate
            
            def _getUnit(
                    self,
                    params : Dict[List, Any], 
                    search : str, 
                    vector : str
                ):
                table = Collection.Entity.Entry
                session = self.Session()
                stt = select(
                    table.entity_sfid, 
                    table.entity_name, 
                    table.entity_label,
                    table.entity_type,
                    table.entity_trace,
                    table.timestamp,
                    table.entity_pack
                ).where(
                    vector == search
                )
                runquery = session.execute(stt)
                result = runquery.fetchone()
                session.commit()
                session.flush()
                self.result = result 
                if self.result != None:
                    packupdate : Dict[List, Any] = self.result._asdict()
                else:
                    packupdate : Dict[List, Any] = {'RESULT' : 'File not found.'}
                return packupdate
            

            def _getList(
                    self,
                    search:str,
                    vector:str,
            ):
                table=Collection.Entity.Entry 
                session=self.Session()
                stt=select(
                    table.entity_sfid,
                    table.entity_name, 
                    table.entity_label, 
                    table.entity_pack ) \
                .where(
                    vector.like(f'%{search}')
                    )
                runquery=session.execute(stt)
                result=runquery.fetchall()
                session.commit()
                session.flush()
                self.result=result 
                if self.result !=None:
                    packupdate:Dict[List,Any]=self.result
                else:
                    packupdate:Dict[List,Any]={'SEARCH RESULT : Files not found.'}
                return packupdate 
            
            def _getAttr(
                    self,
                    params:Dict[List,Any],
                    search:str, 
                    vector:str, 
                    attribute:str=None
            ):
                table=Collection.Entity.Entry
                session=self.Session()
                stt=select(
                    table.entity_sfid, 
                    table.entity_name 
                    )\
                    .where(
                        vector==search 
                    )
                runquery=session.execute(stt)
                result=runquery.fetchone()
                session.commit()
                session.flush()
                self.result=result 
                if self.result !=None:
                    packupdate:Dict[List,Any]= self.result._asdict()
                else:
                    packupdate:Dict[List,Any]={'SEARCH RESULT : File not found.'}
                return packupdate 
            

            def bySfid(
                    self
                )->str:
                sot=Collection.Entity.Entry
                getcheck=self.lookup
                session=self.Session()
                try:
                    stt=select(
                        sot.entity_label, 
                        sot.entity_pack,
                    )\
                    .where(Collection.Entity.Entry.entity_sfid == getcheck)
                    result=session.execute(stt)
                except:
                    result=None 
                    packupdate={"ENTITY QUERY: an issue exists in the Sfid Search [PGVECTOR-CONTROLS]"}
                session.commit()
                session.flush()
                self.result=result.fetchone()
                if self.result !=None:
                    packupdate:Dict[List,Any]=self.result._asdict()
                    return packupdate['entity_pack']['result']['action_event'][0]
                else:
                    return "File not found."

                

            def byFilename(
                    self, 
                    geturl : bool = False, 
                    getpack : bool = False,
                    getlist : bool = False, 
                )->Dict[List, Any]:
                sot = Collection.Entity.Entry 
                getcheck = self.lookup
                print(getcheck)
                session = self.Session()
                try:
                    stt = select(
                        sot.entity_label, 
                        sot.entity_pack
                    ).where(
                        Collection.Entity.Entry.entity_name == getcheck
                    )
                    result = session.execute(stt)
                except:
                    result = None
                    packupdate = {"ENTITY QUERY" : f'an issue exists in the filename search or the term {getcheck}'}
                session.commit()
                session.flush()
                self.result = result.fetchone()
                if self.result != None:
                    packupdate : Dict[List, Any] = self.result._asdict()
                    return packupdate
                else: 
                    return "File Not Found"
                

        class Receive:

            def __init__(
                    self, 
                    package: Dict[List, Any]
                )->Dict[List, Any]:
                self.package = package

            
            async def getCollectionControls(
                    self
                ):
                result : Dict[List, Any]  = Transact.router(
                    transact="RECEIVE", 
                    payload = self.package
                )
                return result
            
        class Process:

            def __init__(
                    self, 
                    package:Dict[List,Any]
            ):
                self.package=package 

            async def setStatusAsProcessing(self):
                result:Dict[List,Any]=Transact.router(
                    transact='PROCESSING', 
                    payload=self.package 
                )
                return result 
            
            async def setStatusAsProcessed(
                    self
            ):
                result:Dict[List,Any]= Transact.router(
                    transact='PROCESSED', 
                    payload=self.package 
                )
                return result 
            
            async def setStatusAsFailed(self):
                result:Dict[List,Any]= Transact.router(
                    transact='FAILED', 
                    paylad=self.package,
                )
                return result 
            
            async def setStatusAsBatchReceive(self):
                result:Dict[List,Any]=Transact.router(
                    transact='BATCH_RECEIVE', 
                    payload=self.package 
                )


        class Embed:

            def __init__(
                    self, 
                    package : Dict[List, Any]
                ):
                self.package = package

            async def getEmbeddingControls(
                self
                ):
                result : Dict[List, Any] = Transact.router(
                    transact="CREATE", 
                    payload = self.package
                )
                return result
            

        class Entry(Control):
            __tablename__= "collection_control"

            entity_sfid: Mapped[uuid.UUID] = mapped_column(
                    types.Uuid, 
                    primary_key=True, 
                    init=False, 
                    server_default=text("gen_random_uuid()")
                )
            entity_name : Mapped[String] = mapped_column(
                types.String, 
                nullable=True
            )
            entity_type : Mapped[String] = mapped_column(
                types.String, 
                nullable = False
            )
            # entity_attr : Mapped[JSONB] = mapped_column(
            #     types.JSON, 
            #     nullable=True
            # )
            entity_label : Mapped[String] = mapped_column(
                types.String, 
                nullable = True
            )
            entity_trace : Mapped[StoreID] = mapped_column(
                types.Uuid, 
                nullable = True
            )
            entity_pack : Mapped[JSONB] = mapped_column(
                types.JSON, 
                nullable=True
            )
            timestamp:Mapped[DateTime]=mapped_column(
                DateTime,
                default=func.now()
            )


        class Processed(Control):
            __tablename__="collection_processed"
            process_index:Mapped[Integer]=mapped_column(
                types.Integer,
                autoincrement=True,
                nullable=False, 
                primary_key=True
            )
            entity_sfid:Mapped[uuid.UUID]=mapped_column(
                types.Uuid, 
                nullable=False
            )
            process_type:Mapped[String]= mapped_column(
                types.String, 
                nullable=True
            )
            process_id:Mapped[String]=mapped_column(
                types.Uuid, 
                nullable=True
            )
            timestamp:Mapped[DateTime]=mapped_column(
                DateTime, 
                default=func.now()
            )


        class Trace(Control):
            from sqlalchemy import text, types, DateTime, func
            __tablename__ = 'collection_trace'

            trace_index : Mapped[Integer] = mapped_column(
                types.Integer, 
                autoincrement=True, 
                nullable=False, 
                primary_key=True
            )
            entity_key : Mapped[String] = mapped_column(
                String(1024), 
                nullable=False
            )
            entity_trace : Mapped[StoreID] = mapped_column(
                types.Uuid, 
                nullable=False,
                server_default=text("gen_random_uuid()")
            )
            entity_event:Mapped[String]=mapped_column(
                types.String,
                nullable=False
            )
            timestamp:Mapped[DateTime]=mapped_column(
                DateTime, 
                default=func.now()
            )
            trace_id=mapped_column(
                types.Uuid, 
                init=False, 
                server_default=text("gen_random_uuid()")
            )
                

class Transact: 

    #checked
    connect = ORM.getConnectionString()
    engine = create_engine(connect)
    Session = sessionmaker(bind=engine)
    session=Session()

    #checked
    def makeChecksum(
            fileheaders : Dict[List, Any]
    )->str:
        code : str = ''
        for item in fileheaders:
            code += str(fileheaders[item])
        checksum : str = code
        checksum_bytes = checksum.encode('ascii')
        checksum = base64.b64encode(checksum_bytes)
        return checksum
    

    def exists(
            fileheaders:Dict[List,Any]
    )->bool:
        pass 

        #checked
    def validate(checksum)->bool:
        from sqlalchemy import select
        getcheck:str= checksum 
        print(getcheck)
        session= Transact.Session()
        stt= select(
                Collection.Entity.Trace
            ).where(
                Collection.Entity.Trace.entity_key.like(getcheck)
            )
        result= session.execute(stt)
        session.commit()
        response= result.fetchone()._asdict()
        print(response)
        return True
    
    #checked
    def deleteKey(
            evals
    ):
        keypops = ['Action', 'meta', 'file', 'files', 'action', 'metadata']
        for item in keypops:
            if item not in evals['file_trace']['inputs']:
                cleanmet = evals
            else:
                del evals['file_trace']['inputs'][item]
                cleanmet = evals
        return cleanmet
    
    #checked
    def defaults(
            evals : Dict[List, Any], 
            getkey : str, 
            steady : str
        ):
        try: 
            if evals[getkey] != None:
                return evals[getkey]
        except:
            return steady
        

    def router(
            transact : str, 
            payload : Dict[List, Any]
        ):
        match str(transact).upper():
            case 'RECEIVE':
                Control.metadata.create_all(Transact.engine)
                with Transact.Session() as session:
                    receiver : Dict[List, Any] = payload
                    checksum = Transact.makeChecksum(
                        fileheaders = receiver['headers']
                    )
                    stead = receiver['headers']['genesis'].split('.')[0]
                    clean = Transact.deleteKey(evals=payload)
                    print(checksum)
                    print(clean)

                    open =  Collection.Entity.Entry(
                        entity_name = clean['headers']['genesis'], 
                        entity_trace = None, 
                        #entity_attr=receiver['result']['culture']
                        entity_label = clean['file_trace']['inputs']['label'], 
                        entity_type=clean['file_trace']['inputs']['type'],
                        entity_pack=clean
                    )
                    session.add_all([open])
                    session.commit()
                    controlid: uuid.UUID = open.entity_sfid.urn.split(':')[2]
                    note = Collection.Entity.Trace(
                        trace_index = None, 
                        entity_key = checksum, 
                        entity_trace = controlid, 
                        entity_event = transact.lower()
                    )
                    session.add_all([note])
                    label = open.entity_label
                    session.commit()
                    checkhash : str = note.entity_key
                    result = {
                        "event_logged" : clean,
                        "entity_sfid" : controlid, 
                        "entity_label" : label, 
                        "trace_hash" : checkhash, 
                        #"event_trace":tracer.items() - future trace states.
                    }
                    session.flush()
                    session.close()
                return result



            case 'CREATE':
                Control.metadata.create_all(Transact.engine)
                from module.pretzl.parser import PACK
                result : Dict[List, Any] = {}         
                with Transact.Session() as session:
                    receiver : Dict[List, Any] =  payload
                    checksum : str = receiver['token']
                    #verify:int=PRETZL.verifyPackage(receiver['sfid'])

                    build = Collection.Entity.Trace(
                        trace_index = None, 
                        entity_key = checksum,
                        entity_trace=receiver['tracer'], 
                        entity_event=transact.lower()
                    )
                    session.add_all([build])
                    session.commit()
                    control = PACK(box=payload)
                    manage : Dict[List, Any] = control.set()
                    create = Interface(
                        metadatas=manage['shaper'], 
                        collection_name=manage['name'], 
                        documents=manage['body'], 
                        config=manage['selections']
                    )
                    deliver = create.loadEmbeddingsFromDocument()
                    result = control.trackPackage(deliver)
                return print(result)
                

            case 'PROCESSING':
                Control.metadata.create_all(Transact.engine)
                result:Dict[List,Any]={}
                checksum=Transact.makeChecksum(fileheaders=payload['headers'])
                entity_trace=payload['headers']['sfid']
                with Transact.Session() as session:
                    build=Collection.Entity.Trace(
                        trace_index=None, 
                        entity_key=checksum, 
                        entity_trace=entity_trace,
                        entity_event=transact.lower()
                    )
                    session.add_all([build])
                    session.commit()
                return result 
            
            case 'PROCESSED':
                Control.metadata.create_all(Transact.engine)
                result:Dict[List,Any]={}
                checksum=Transact.makeChecksum(fileheaders=payload['headers'])
                sfid=payload['headers']['sfid']
                procesed_json_id=payload['headers']['processed_json_id']
                with Transact.Session() as session:
                    build= Collection.Entity.Trace(
                        trace_index=None,
                        entity_key=checksum,
                        entity_trace=sfid, 
                        entity_event=transact.lower()
                    )
                    session.add_all([build])
                with Transact.Session() as session:
                    tracing=Collection.Entity.Processed(
                        process_index=None, 
                        entity_sfid=sfid, 
                        process_type='Second State Linotype process for JSON', 
                        process_id=procesed_json_id
                    )
                    session.add_all([tracing])
                    session.commit()
                return result 
            

            case 'FAILED':
                Control.metadata.create_all(Transact.engine)
                result:Dict[List,Any]={}
                checksum=Transact.makeChecksum(fileheaders=payload['headers'])
                entity_trace=payload['headers']['sfid']
                with Transact.Session() as session:
                    failed=Collection.Entity.Trace(
                        trace_index=None, 
                        entity_key=checksum, 
                        entity_trace=entity_trace,
                        entity_event=transact.lower()
                    )
                    session.add_all([failed])
                return result 
            
            case 'BATCH_RECEIVE':
                from urllib.parse import urlparse 
                Control.metadata.create_all(Transact.engine)
                result:Dict[List,Any]={}
                data_payload=payload['data']
                timestamp=datetime.datetime.now()
                with Transact.Session() as session:
                    for data in data_payload['datasource']:
                        coll_control=Collection.Entity.Entry(
                            entity_name=urlparse(data['filepath']).path.split('/')[-1],
                            entity_trace=data['sourcefile_id'].lower(), 
                            entity_label=data_payload['batch_id'].lower(),
                            entity_type='batch', 
                            entity_pack=payload, 
                            timestamp=timestamp
                        )
                        session.add_all([coll_control])
                        session.commit()
                        coll_trace=Collection.Entity.Trace(
                            trace_index=None, 
                            entity_key=Transact.makeChecksum(fileheaders=data),
                            entity_trace=coll_control.entity_sfid.urn.split(':')[2], 
                            entity_event='receive'
                        )
                        session.add_all([coll_trace])
                        session.commit()
                    return result 

                            

            


    
    
        #             response = result
        #         except:
        #             response = {"FAILURE" : "the Collection manager failed to transform the data unit."}
    
    
        # return response
    