import uuid, base64
from fastapi import UploadFile as Subject
from typing import Dict, List, Any
from enum import Enum
from sqlalchemy import (
    create_engine, 
    select, text, 
    types, Integer, 
    UUID as StoreID, 
    String,
    Float, ARRAY
)

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    DeclarativeBase, 
    Mapped, 
    MappedAsDataclass, 
    mapped_column, 
    sessionmaker
)


from module.core.config import Env, System as CoreSys
from module.pgvector.config import ORM
from module.pgvector.connect import Interface

class Control(MappedAsDataclass, DeclarativeBase):
    pass

class System(CoreSys):

    def __init__(
            self, 
            timezone : str = None
    ):
        if timezone:
            self.region = timezone

    def getTimeStamp(self):
        return CoreSys.Timestamp.getTimeStampeLocal(tmz=self.region)
    
    def getRegionEnv(self):
        self.region = CoreSys.SYS.getRegionalEnv()
        return self.region
    

class Matrix:

    class Entity: 

        from sqlalchemy import event
        from sqlalchemy.sql import column
        from sqlalchemy.orm import Session

        class Action(Enum):
            ACQUIRE=''

        class Entry(Env.HasTimestamp, Control):
            __tablename__= "mapping_control"

            entity_sfid: Mapped[uuid.UUID] = mapped_column(
                    types.UUID, 
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



        class Trace(Env.HasTimestamp, Env.HasTrace, Control):
            __tablename__ = 'mapping_trace'

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
            entity_event : Mapped[String] = mapped_column(
                types.String, 
                nullable = False
            )

        class Mapping(Env.HasTimestamp, Env.HasTrace, Control):

            __tablename__ = "mapping_values"

            mapping_index : Mapped[Integer] = mapped_column(
                types.Integer, 
                autoincrement=True, 
                nullable=False, 
                primary_key=True
            )

            mapping_source : Mapped[StoreID] = mapped_column(
                types.Uuid, 
                nullable = False
            )

            mapping_trace : Mapped[String] = mapped_column(
                types.Uuid, 
                nullable = False
            )

            mapping_conf : Mapped[Float] = mapped_column(
                types.Float, 
                nullable=True
            )

            mapping_recc : Mapped[JSONB] = mapped_column(
                types.JSON,
                nullable=True
            )

            mapping_meta : Mapped[JSONB] = mapped_column(
                types.JSON, 
                nullable=True
            )

            mapping_data : Mapped[JSONB] = mapped_column(
                types.JSON, 
                nullable=True
            )

            entity_event : Mapped[String] = mapped_column(
                types.String, 
                nullable=False
            )
            

        class Update:

            def __new__(
                    cls,
                    meta:Dict[List,Any]
            ):
                msg='Update Object created for holding instruction'
                instance= super().__new__(cls)
                return instance 

        class Origin:

            def __init__(
                    self, 
                    package : Dict[List, Any]
            ):
                self.pack = package

            def CreateGraph(
                    self
            ):
                from module.file.control import RetrievalController as Arcee
                from module.pgvector.control import Collection
                result : Dict[List, Any] = {}
                graph : Dict[List, Any] = {}
                start : Dict[List, Any] = self.pack
                runner : Dict[List, Any] = Arcee(metadata=start).Details()
                tracer : str = Collection.Entity.Query(
                        lookup_key=runner['entity_sfid']
                    ).entity_trace()
                input : Dict[List, Any] = start['inputs']
                samples : Dict[List, Any] = self.GetSourceSamples()
                del input ['command'], input['meta']
                for items in start['document_list'][2]:
                    jdoc = {
                        'page_content' : items.page_content, 
                        'metadata' : items.metadata
                    }
                graph['inputs'] = input
                graph['region'] = start['region']
                graph['graph_sfid'] = runner['entity_sfid'].urn.split(':')[2]
                graph['graph_conf'] = 0
                graph['graph_recc'] = None
                graph['graph_meta'] = start['column_data']
                graph['graph_data'] = jdoc
                graph['graph_label'] = input['label']
                graph['entity_label'] = runner['entity_label']
                graph['entity_type'] = input['type']
                graph['graph_key'] = tracer[0]['entity_key']
                graph['graph_tracer'] = tracer[0]['trace_id'].urn.split(':')[2]

                result.update({'graph' : graph})
                self.graph = result 
                return result
            

            def GetSourceList(
                    self,
            )->Dict[List,Any]:
                from module.file.control import Retrieve 
                start:Dict[List,Any]=self.pack 
                runner:Dict[List,Any]= Retrieve(
                    metadata=start 
                ).Details()
                try:
                    sampler:Dict[List,Any]= Matrix.Entity.Query(
                        lookup_key=runner['entity_label']
                    ).mapper_sources()
                except:
                    raise {'result': 'FAILURE', 'message': 'GetSourceList Failed'}
                return sampler

            

            def GetSourceSamples(
                    self
            ):
                from module.file.control import Retrieve
                from module.core.encode import Tool as ET 
                import pandas as dfp 
                start : Dict[List, Any] = self.pack
                runner : Dict[List, Any] = Retrieve(
                    metadata = start
                ).Details()
                try:
                    sampler : Dict[List, Any] = Matrix.Entity.Query(
                        lookup_key = runner['entity_label']
                    ).mapping_assoc()
                except Exception as err:
                    raise {'result': 'FAILURE', 'message':f'{(__name__)} experienced {err}'}
                response:Dict[List,Any]= {}
                if sampler == 0:
                    response.update({
                        'result': 'FAILURE',
                        'message': 'no matching samples for that label'
                    })
                for i,row in enumerate(sampler):
                    r:Dict[List,Any]=dict(row[1])
                    sohid:str=str(row[0])
                    origin=r['headers']['genesis']
                    url:str=str(r['headers']['action_event'][0])
                    hurl=Matrix.Help().getLocalPath()
                    firstrow= dfp.read_csv(hurl, nrows=4)
                    firstrow= firstrow.fillna('').unstack().to_dict()
                    firstfields=dfp.read_csv(hurl).dtypes.to_dict()

                    vars = []
                    for field in firstfields:
                        vars.append(field)

                    clean = list(set(vars))
                    fields={}
                    for key in clean:
                        values=[]
                        for rowdata in firstrow:
                            if rowdata[0] == key:
                                values.append(firstrow[rowdata])
                            fields.update({key:values})
                    settings={
                        'column_meta': list(firstfields), 
                        'sample_data': dict(fields), 
                        'source': sohid, 
                        'values':list(firstrow),
                        'origin': origin, 
                        'url': hurl 
                    }
                    response.update({i:settings})
                return response 
            

            def getMatrixControls(
                    self, 
                    map : Dict[List, Any] = None
                )->Dict[List, Any]: 
                if map != None:
                    self.graph = map

                result : Dict[List, Any] = Transact.router(
                    transact='ORGINATE',
                    payload = self.graph
                )
                return result
            

        class Query:

            def __init__(
                    self, 
                    lookup_key
            ):
                from module.pgvector.control import Collection
                connect = ORM.getConnectionString()
                engine = create_engine(connect)

                self.Session = sessionmaker(bind=engine)
                self.session = self.Session()
                self.lookup = lookup_key
                self.body = {}
                self.result = {}

                self.lu = {
                    'go' : Matrix.Entity.Mapping.mapping_source, 
                    'oh' : Matrix.Entity.Mapping.mapping_trace,
                    'eo' : Matrix.Entity.Entry.entity_sfid,
                    'en' : Matrix.Entity.Entry.entity_name,
                    'el' : Matrix.Entity.Entry.entity_label,
                    'la' : Collection.Entity.Entry.entity_label
                }

            def mapping_assoc(
                    self
            )->Dict[List, Any]:
                getcheck = self.lookup
                params = locals()
                try:
                    result = self._getSourceList(
                        search = getcheck,
                        vector = self.lu['la']
                    )
                    return result
                except:
                    return f'File lookup for label {self.lu['la']} failed'
                


            def mapped_assoc(
                    self, 

            )->Dict[List,Any]:
                getcheck = self.lookup
                params=locals()
                result = self._getSourceList(
                    search=getcheck, 
                    vector=self.lu['la']
                )
                return result 
            
            def mapped_sources(
                    self,
            )->Dict[List,Any]:
                getcheck=self.lookup
                params=locals()
                result=self._getSourceList(
                    search=getcheck,
                    vector=self.lu['la']
                )
                return result 
            

            def source_by_sfid(
                    self,
            )->Dict[List,Any]:
                getcheck=self.lookup 
                params=locals()
                result = self._getSourceUrls(
                    search=getcheck,
                    vector=self.lu['la']
                )
                return result 

            def mapping_label(
                    self, 
                    geturl : bool = False
            )->Dict[List, Any]:
                getcheck = self.lookup
                params = locals()
                try:
                    result = self._getUnit(
                        search = getcheck,
                        params = params,
                        vector = self.lu['el']
                    )
                    return result
                except:
                    return f'File lookup for label {self.lu['el']} failed'
                

            def entity_sfid(
                    self
            )->Dict[List,Any]:
                getcheck=self.lookup
                params=locals()
                result=self._getMappings(
                    search=getcheck,
                    params=params,
                    vector=self.lu['eo']
                )
                return result 
                
            def graph_sfid(
                    self
            )->Dict[List, Any]:
                getcheck = self.lookup
                params = locals()
                try:
                    result = self._getSourceList(
                        search = getcheck,
                        params = params,
                        vector = self.lu['eo']
                    )
                    return result
                except:
                    return f'File lookup for label {self.lu['eo']} failed'
                
            def mapping_name(
                    self
            )->Dict[List, Any]:
                getcheck = self.lookup
                params = locals()
                try:
                    result = self._getSourceList(
                        search = getcheck,
                        params = params,
                        vector = self.lu['mn']
                    )
                    return result
                except:
                    return f'File lookup for label {self.lu['mn']} failed'
                
            def mapping_label(
                    self
            )->Dict[List, Any]:
                getcheck = self.lookup
                params = locals()
                try:
                    result = self._getSourceList(
                        search = getcheck,
                        params = params,
                        vector = self.lu['el']
                    )
                    return result
                except:
                    return f'File lookup for label {self.lu['el']} failed'

            def _getMappings(
                    self, 
                    params : Dict[List, Any],
                    search: str , 
                    vector: str
                )->Dict[List, Any]:
                table = Matrix.Entity.Mapping
                session = self.Session()
                stt = select(
                    table.mapping_index, 
                    table.mapping_conf, 
                    table.mapping_meta, 
                    table.mapping_data, 
                    table.mapping_source, 
                    table.mapping_recc
                ).where(
                    vector == search
                )
                runquery = session.execute(stt)
                results = runquery.fetchone()._asdict()
                session.commit()
                session.flush()
                self.result = results
                result : Dict[List, Any] = self.result
                session.close()
                return result     


            def _getUnit(
                    self, 
                    params : Dict[List, Any],
                    search: str , 
                    vector: str
                ):
                table = Matrix.Entity.Mapping
                session = self.Session()
                stt = select(
                    table.mapping_index, 
                    table.mapping_conf, 
                    table.mapping_meta, 
                    table.mapping_data, 
                    table.mapping_source
                ).where(
                    vector == search
                )
                runquery = session.execute(stt)
                results = runquery.fetchone()
                session.commit()
                session.flush()
                self.result = results
                result : Dict[List, Any] = self.result
                return result      

            def _getList(
                    self, 
                    search: str , 
                    vector: str
                ):
                from module.pgvector.control import Collection
                table = Matrix.Entity.Mapping
                session = self.Session()
                stt = select(
                    table.mapping_index, 
                    table.mapping_conf, 
                    table.mapping_meta, 
                    table.mapping_data, 
                    table.mapping_source
                ).where(
                    vector == search
                )
                runquery = session.execute(stt)
                results = runquery.fetchall()
                session.commit()
                session.flush()
                self.result = results
                result : Dict[List, Any] = self.result
                return result       
            
            def _getSourceList(
                    self, 
                    search: str , 
                    vector: str
                ):
                from module.pgvector.control import Collection
                table = Collection.Entity.Entry
                session = self.Session()
                stt = select(
                    table.entity_sfid, 
                    table.entity_pack
                ).where(
                    vector == search
                ).filter(
                    table.entity_type == 'source'
                ).distinct(
                    table.entity_sfid
                )
                runquery = session.execute(stt)
                results = runquery.fetchall()
                session.commit()
                session.flush()

                self.result = results
                result : Dict[List, Any] = self.result
                return result
        

            def _getSourceUrls(
                    self,
                    search:str, 
                    vector:str,
            ):
                from module.pgvector.control import Collection
                table=Collection.Entity.Entry
                session=self.Session() 
                stt=select(
                        table.entity_pack
                    ) \
                    .where(
                        vector==search
                    ).filter(
                        table.entity_type=='source'
                    ).distinct(
                        table.entity_sfid
                    )
                runquery=session.execute(stt)
                results=runquery.fetchall()
                session.commit()
                session.flush()

                #store result in instance 
                self.result = results 
                result:Dict[List,Any]= self.result 
                return result



        class Retrieve:

            def __init__(
                    self, 
                    package: Dict[List, Any]
            )->Dict[List, Any]:
                self.package = package

            async def getFields(
                    self
            ):
                result : Dict[List, Any] = Transact.router(
                    transact="RETRIEVE", 
                    payload = self.package
                )
                return result
            

        class Create:

            def __init__(
                    self,
                    package : Dict[List, Any]
            )->Dict[List, Any]:
                self.package = package

            async def setFields(
                self
            ):
                result = Dict[List, Any] = Transact.router(
                    transact = "CREATE", 
                    payload = self.package
                )
                return result

        class Field:

            def __init__(
                    self, 
                    metadata:Dict[List,Any]
            ):
                self.m = metadata 


            class Length:

                def __init__(
                        self,
                        metadata:Dict[List,Any]
                ):
                    self.operators:Dict[List,Any]= metadata['operators']

                def buildFormulaString(
                        self,
                ):
                    operation=self.operators 
                    return operation
                
            class Formula:

                def __init__(
                        self,
                        metadata:Dict[List,Any]
                ):
                    self.operators:Dict[List,Any]= metadata['operators']
                    
                def buildFormulaString(
                        self,
                ):
                    operation = self.operators 
                    return operation 
                

            class Type:

                def __new__(
                        cls,
                        meta:Dict[List,Any]
                ):
                    msg='TYPE Object created for Column Fields'
                    instance = super().__new__(cls)
                    return instance 


class Transact: 

    connect = ORM.Db.getConnectionString()
    engine = create_engine(connect)
    Session = sessionmaker(bind=engine)

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
    


    def validate(checksum)->bool:
        from sqlalchemy import select
        getcheck : str = checksum 
        print(getcheck)
        session = Transact.Session()
        stt = select(
                Matrix.Entity.Trace
            ).where(
                Matrix.Entity.Trace.entity_key.like(getcheck)
            )
        result = session.execute(stt)
        session.commit()
        response = result.fetchone()._asdict()
        print(response)
        return True
    

    def router(
            transact : str, 
            payload : Dict[List, Any]
        )->Dict[List, Any]:
        """

        """
        match str(transact).upper():

            case 'RETRIEVE':
                Control.metadata.create_all(Transact.engine)
                try:
                    with Transact.Session() as session:
                        receiver : Dict[List, Any] = payload
                        results = Matrix.Entity.Query(
                            lookup_key=receiver['key']
                        ).mapping_name()
                        result = results
                    return result
                except:
                    return {'ENTITY : MATRIX > Mapping - Command = [RETRIEVE]'}
                
            
            case 'ORIGINATE':
                Control.metadata.create_all(Transact.engine)
                from module.pretzl.etl import GRAPH
                from module.file.model.Field import Field
                result : Dict[List, Any] = {}
                with Transact.Session() as session:
                    receiver : Dict[List, Any] = payload['graph']

                    create = Matrix.Entity.Mapping(
                        mapping_index=None, 
                        mapping_source=receiver['graph_sfid'], 
                        mapping_conf=receiver['graph_conf'], 
                        mapping_recc=['graph_recc'],
                        mapping_meta=receiver['graph_meta'], 
                        mapping_data=receiver['graph_data'], 
                        #mapping_key=receiver['graph_key'],
                        mapping_trace=receiver['graph_tracer'], 
                        entity_event='create'
                    )

                    session.add_all([create])
                    session.commit()
                    traceid : uuid.UUID = create.mapping_source.urn.split(':')[2]
                    receiver.update({ 'graph_map_key' : traceid })
                    accept =  Matrix.Entity.Entry(
                        entity_name=receiver['graph_label'], 
                        entity_trace=traceid, 
                        #entity_attr=receiver['result'],
                        entity_label=receiver['entity_label'], 
                        entity_type='schema', 
                        entity_pack=payload
                    )
                    session.add_all([accept])
                    session.commit()
                    controlid : uuid.UUID = accept.entity_sfid.urn.split(':')[2]
                    receiver.update({'graph_map_id': controlid })
                    trace = Matrix.Entity.Trace(
                        trace_index=None, 
                        entity_key=receiver['graph_key'],
                        entity_trace =controlid,
                        entity_event=transact.lower()
                    )
                    session.add_all([trace])
                    label = accept.entity_label
                    session.commit()
                    session.flush()
                    result = {
                        "event_logged" : receiver, 
                        "source_sfid"  : receiver['graph_sfid'], 
                        "entity_sfid"  : controlid, 
                        "entity_label" : label, 
                        "entity_name"  : accept.entity_name
                    }
                    receiver.update({'graph_origin' : result})
                    session.close()
                    response = Field.Entity.Origin(package=receiver).receiveFieldControls()
                    holdingset = response
                return result
