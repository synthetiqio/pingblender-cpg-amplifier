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
    

class Field:

    class Entity: 

        from sqlalchemy import event
        from sqlalchemy.sql import column
        from sqlalchemy.orm import Session

        class Entry(Env.HasTimestamp, Control):
            __tablename__= "field_control"

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
            __tablename__ = 'field_trace'

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

        class Field(Env.HasTimestamp, Env.HasTrace, Control):

            __tablename__ = "field_values"

            field_index : Mapped[Integer] = mapped_column(
                types.Integer, 
                autoincrement=True, 
                nullable=False, 
                primary_key=True
            )

            field_source : Mapped[StoreID] = mapped_column(
                types.Uuid, 
                nullable = False
            )

            field_trace : Mapped[String] = mapped_column(
                types.Uuid, 
                nullable = False
            )

            field_conf : Mapped[Float] = mapped_column(
                types.Float, 
                nullable=True
            )

            field_recc : Mapped[JSONB] = mapped_column(
                types.JSON,
                nullable=True
            )

            field_type : Mapped[String] = mapped_column(
                types.String,
                nullable=False
            )

            field_model: Mapped[String] = mapped_column(
                types.String,
                nullable=False
            )
            
            field_sample : Mapped[JSONB] = mapped_column(
                types.JSON, 
                nullable=True
            )

            field_attr : Mapped[JSONB] = mapped_column(
                types.JSON, 
                nullable=True
            )

            field_name: Mapped[String] = mapped_column(
                types.String,
                nullable=False
            )

            field_data : Mapped[JSONB] = mapped_column(
                types.JSON, 
                nullable=True
            )

            entity_event : Mapped[String] = mapped_column(
                types.String, 
                nullable=False
            )


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
            

            def GetSourceSamples(
                    self
            ):
                from module.file.control import RetrievalController as RC
                start : Dict[List, Any] = self.pack
                runner : Dict[List, Any] = RC(
                    metadata = start
                ).Details()

                sampler : Dict[List, Any] = Field.Entity.Query(
                    lookup_key = runner['entity_label']
                ).mapping_assoc()

                return sampler
            

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
                from module.file.action.Map import Matrix as M
                from module.pgvector.control import Collection as C
                connect = ORM.Db.getConnectionString()
                engine = create_engine(connect)

                self.Session = sessionmaker(bind=engine)
                self.session = self.Session()
                self.lookup = lookup_key
                self.body = {}
                self.result = {}

                self.lu = {
                    'eo' : Field.Entity.Entry.entity_sfid, 
                    'en' : Field.Entity.Entry.entity_trace,
                    'el' : Field.Entity.Entry.entity_label,
                    'es' : Field.Entity.Field.field_source,
                    'ma' : M.Entity.Entry.entity_sfid,
                    'mt' : M.Entity.Trace.entity_trace, 
                    'ml' : M.Entity.Entry.entity_label,
                    'cl' : C.Entity.Entry.entity_label
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
                

            def mapping_label(
                    self, 
                    geturl : bool = False
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

            def _getFields(
                    self, 
                    params : Dict[List, Any],
                    search: str , 
                    vector: str
                )->Dict[List, Any]:
                table = Field.Entity.Field
                session = self.Session()
                stt = select(
                    table.field_index, 
                    table.field_type, 
                    table.field_name, 
                    table.field_data, 
                    table.field_conf, 
                    table.field_recc
                ).where(
                    vector == search
                )
                runquery = session.execute(stt)
                results = runquery.fetchall()
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
                table = Field.Entity.Mapping
                session = self.Session()
                stt = select(
                    table.field_index, 
                    table.field_conf, 
                    table.field_meta, 
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
                table = Field.Entity.Field
                session = self.Session()
                stt = select(
                    table.field_index, 
                    table.field_type,
                    table.field_name, 
                    table.field_data, 
                    table.field_conf, 
                    table.field_recc, 
                    table.field_source
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
            


            def pullTargetFields(
                    self, 
                    package, 
                    recomm
            )->Dict[List, Any]:
                getcheck = self.lookup
                params = locals()

                speak : list = []
                ok_computer : Dict[List, Any] = recomm['robot_reads']
                for i, item in enumerate(ok_computer):
                    speak.append(item)

                result = self._getFields(
                    search = getcheck, 
                    params = params, 
                    vector= self.lu['es']
                )

                response = {}

                for i, row in enumerate(result):
                    rownum = i+1
                    rowbot = speak[i]
                    core_field : str = rowbot[0]
                    recc_field : str = rowbot[1]
                    conf_conv : float = 1 - rowbot[2]
                    conf_conv : float = 100*conf_conv
                    if conf_conv >= 90:
                        conf_tier = 'High'
                    elif conf_conv <= 70:
                        conf_tier = 'Low'
                    else:
                        conf_tier = 'Medium'
                    
                    rowobj = {
                        "id" : row[0],
                        "confidence" : conf_tier,
                        "confidenceIndex" : conf_conv,
                        "column_holder" : core_field, 
                        "column_header" : recc_field,
                        "format" : {
                            "value" : row[1],
                            "label" : row[1]
                        }, 
                        "description" : "<PLACEHOLDER>",
                        "value" : row[3], 
                        "department" : "<PLACEHOLDER>"
                    }
                    response.update({rownum : rowobj})
                return response
                                    

                    


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
                Field.Entity.Trace
            ).where(
                Field.Entity.Trace.entity_key.like(getcheck)
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
                        results = Field.Entity.Query(
                            lookup_key=receiver['key']
                        ).mapping_name()
                        result = results
                    return result
                except:
                    return {'ENTITY : MATRIX > Mapping - Command = [RETRIEVE]'}
                
            
            case 'INITIATE':
                Control.metadata.create_all(Transact.engine)
                from module.pretzl.etl import GRAPH
                result : Dict[List, Any] = {}
                with Transact.Session() as session:
                    receiver : Dict[List, Any] = payload['graph']

                    format = Field.Entity.Field(
                        field_index=None, 
                        field_source=receiver['graph_sfid'], 
                        field_model ='',
                        field_sample='',
                        field_trace=receiver['graph']['graph_tracer'],
                        field_name=receiver['graph_name'],
                        field_type=receiver['graph_type'], 
                        field_data=receiver['graph_data'], 
                        field_conf=receiver['graph_conf'], 
                        field_recc=receiver['graph_recc'],
                        field_attr=receiver['graph_attr'],
                        entity_event='initiate'
                    )

                    session.add_all([format])
                    session.commit()
                    fieldnumber : Integer = format.field_index
                    traceid : uuid.UUID = format.field_source.urn.split(':')[2]
                    receiver.update({ 'graph_map_key' : traceid })
                    fieldentry =  Field.Entity.Entry(
                        entity_name=receiver['graph_name'], 
                        entity_trace=traceid, 
                        #entity_attr=receiver['result'],
                        entity_label=receiver['graph_attr']['entity_label'], 
                        entity_type='field', 
                        entity_pack=receiver['graph']
                    )
                    session.add_all([fieldentry])
                    session.commit()
                    controlid : uuid.UUID = fieldentry.entity_sfid.urn.split(':')[2]
                    receiver.update({'graph_map_id': controlid })
                    fieldtrace = Field.Entity.Trace(
                        trace_index=None, 
                        entity_key=receiver['graph']['graph_key'],
                        entity_trace =controlid,
                        entity_event=transact.lower()
                    )
                    session.add_all([fieldtrace])
                    session.commit()
                    result = {
                        "field_id" : fieldnumber,
                        "event_logged" : receiver, 
                        "source_sfid"  : receiver['graph_sfid'], 
                        "entity_sfid"  : controlid, 
                        "entity_label" : fieldentry.entity_label, 
                        "entity_name"  : format.field_name
                    }
                    receiver.update({'graph_origin' : result})
                    session.close()
                    response = Field.Entity.Origin(package=receiver).receiveFieldControls()
                    holdingset = response
                return result
