import uuid, datetime, json, base64
from enum import Enum
from fastapi import UploadFile as Subject 
from typing import Dict, List, Any
from sqlalchemy import (
    create_engine, 
    Index, 
    select, 
    text, 
    types, Integer, String, DateTime, 
    UUID as StoreID, Float, ARRAY
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    DeclarativeBase, 
    Mapped, 
    MappedAsDataclass, 
    mapped_column, 
    sessionmaker, 
)
from module.core.config import Env, System as CoreSys
from module.pgvector.config import ORM
from module.pgvector.connect import Interface as VectorInterface

class Control(MappedAsDataclass, DeclarativeBase):
    pass 

class System(CoreSys):

    def __init__(self, timezone:str=None):
        if timezone:
            self.region = timezone 

    def getTimeStamp(self):
        return CoreSys.Timestamp.getTimeStampeLocal(tmz=self.region)
    
    def getRegionEnv(
            self,
    ):
        self.region = CoreSys.SYS.getRegionalEnv()
        return self.region 
    
class Attribute:


    class Entity:

        from sqlalchemy import event
        from sqlalchemy.sql import column 
        from sqlalchemy.orm import Session 

        class Origin:

            def __init__(
                    self, 
                    package:Dict[List,Any]
            ):
                self.pack = package 

            def GetGraff(
                    self,
            ):
                from module.file.control import Retrieve 
                from module.pgvector.control import Collection 

                result:Dict[List,Any]={}
                graph:Dict[List,Any]={}
                start:Dict[List,Any]= self.pack 
                runner:Dict[List,Any]=Retrieve(metadata=start).Details()
                tracer:str=Collection.Entity.Query(lookup_key=runner['entity_sfid']).entity_trace()
                input:Dict[List,Any]=start['inputs']

                samples:Dict[List,Any]=self.GetSourceSamples()

                graph['graph_sfid']=runner['entity_sfid'].urn.split(':')[2]
                graph['graph_label']=runner['entity_label']
                graph['entity_label']=runner['entity_label']
                graph['entity_type']='attribute'
                graph['entity_sample']= samples 
                graph['graph_key']=tracer[0]['entity_key']
                graph['graph_tracer']=tracer[0]['trace_id'].urn.split(':')[2]
                result.update({
                    'graph':graph
                })
                self.graph = result 
                return result 
            

            def GetSourceSamples(
                    self,
            )->Dict[List,Any]:
                from module.file.control import Retrieve 
                start:Dict[List,Any]=self.pack 
                runner:Dict[List,Any]=Retrieve(
                    metadata=start
                ).Details()
                sampler:Dict[List,Any]=Attribute.Entity.Query(
                    lookup_key=runner['entity_label']
                ).attribute_assoc()
                return sampler 
            

            def receiveAttributeControls (
                    self,
                    attributes:Dict[List,Any]=None
            )->Dict[List,Any]:
                self.graph=self.GetGraff()
                self.attributes=self.graph['graph']
                if attributes != None:
                    self.graph = attributes['graph']
                stack=[]
                del self.pack['graph_origin']['event_logged']
                for index, (key, value) in enumerate(self.pack['graph_meta'].items()):
                    dataattribute=self.pack['graph_data']['page_content'].split("\n")[index].split(": ")[1]
                    self.graph['graph_name']=key 
                    self.graph['graph_conf']=self.pack['graph_conf']
                    self.graph['graph_recc']=self.pack['graph_recc']
                    self.graph['graph_type']=value 
                    self.graph['graph_data']=dataattribute
                    self.graph['graph_attr']= self.pack 

                    result:Dict[List,Any]= Transact.router(
                        transact='INITIATE', 
                        payload= self.graph
                    )
                    stack.append(result)
                return stack 


            async def pruneAttributes(
                    self,
                    dataobj:Dict[List,Any]=None,
            )->Dict[List,Any]:
                if dataobj == None:
                    sweeper = self.pack 
                else:
                    sweeper = dataobj 
                del sweeper ['event_logged']['graph_origin']
                return sweeper 
            

            async def updateAttributeControls(
                    self,
                    attributes:Dict[List,Any]=None 
            ):
                if attributes != None:
                    self.graph=attributes 
                result:Dict[List, Any]= Transact.router(
                    transact='UPDATE', 
                    payload=self.graph 
                )
                return result 
            

        class Query:

            def __init__(
                    self, 
                    lookup_key
            ):
                from module.file.action.Map import Matrix as M 
                from module.pgvector.control import Collection as C 
                connect = ORM.getConnectionString()
                engine = create_engine(connect)


                self.Session = sessionmaker(bind=engine)
                self.session = self.Session()
                self.lookup = lookup_key
                self.body:Dict[List,Any]={}
                self.result = {}

                self.lu={
                    'eo':Attribute.Entity.Entry.entity_sfid,
                    'en':Attribute.Entity.Entry.entity_name, 
                    'el':Attribute.Entity.Entry.entity_label,
                    'es':Attribute.Entity.Entry.attribute_source,
                    'ma':M.Entity.Entry.entity_sfid,
                    'mt':M.Entity.Entry.entity_trace,
                    'ml':M.Entity.Entry.entity_label,
                    'cl':C.Entity.Entry.entity_label,
                }

            def attribute_assoc(
                        self,
            )->Dict[List,Any]:
                getcheck=self.lookup
                params=locals()
                result=self._getSourceList(
                    search=getcheck,
                    vector=self.lu['cl']
                )
                return result 
            

            def attribute_label(
                    self, 
                    geturl:bool=False,
            )->Dict[List,Any]:
                getcheck=self.lookup
                params=locals()
                result=self._getUnit(
                    search=getcheck, 
                    params=params, 
                    vector=self.lu['el']
                )
                return result 
            

            def graph_sfid(
                    self,
            )->Dict[List,Any]:
                getcheck=self.lookup 
                params=locals()
                result=self._getAttributes(
                    search=getcheck,
                    params=params, 
                    vector=self.le['go']
                )
                return result 
            

            def entity_sfid(
                    self,
            )->Dict[List,Any]:
                getcheck=self.lookup
                params=locals()
                result= self._getAttributes(
                    search=getcheck, 
                    params=params, 
                    vector=self.lu['eo']
                )
                return result 
            

            def attribute_name(
                    self,
            )->Dict[List,Any]:
                getcheck= self.lookup
                params=locals()
                result= self._getAttributes(
                    search=getcheck, 
                    params=params, 
                    vector=self.lu['mn']
                )
                return result 
            

            def attribute_label(
                    self,
            )->Dict[List,Any]:
                getcheck= self.lookup
                params=locals()
                result= self._getAttributes(
                    search=getcheck, 
                    params=params, 
                    vector=self.lu['el']
                )
                return result 
            
            def _getAttribute(
                    self,
                    params:Dict[List,Any], 
                    search:str, 
                    vector:str,
            )->Dict[List,Any]:
                table=Attribute.Entity.Attribute
                session=self.Session()
                stt= select(
                    table.attribute_index, 
                    table.attribute_type, 
                    table.attribute_name, 
                    table.attribute_data, 
                    table.attribute_conf,
                    table.attribute_recc 
                ) \
                .where(
                    vector==search
                )
                runquery=session.execute(stt)
                results=runquery.fetchone()._asdict()
                session.commit()
                session.flush()
                self.result = results 
                result:Dict[List,Any]=self.result 
                session.close()
                return result 
            
            def _getAttributes(
                    self,
                    params:Dict[List,Any], 
                    search:str, 
                    vector:str,
            )->Dict[List,Any]:
                table=Attribute.Entity.Attribute
                session=self.Session()
                stt= select(
                    table.attribute_index, 
                    table.attribute_type, 
                    table.attribute_name, 
                    table.attribute_data, 
                    table.attribute_conf,
                    table.attribute_recc 
                ) \
                .where(
                    vector==search
                )
                runquery=session.execute(stt)
                results=runquery.fetchall()
                session.commit()
                session.flush()
                self.result = results 
                result:Dict[List,Any]=self.result 
                session.close()
                return result 
            

            def _getUnit(
                    self,
                    params:Dict[List,Any], 
                    search:str, 
                    vector:str,
            )->Dict[List,Any]:
                table=Attribute.Entity.Attribute
                session=self.Session()
                stt= select(
                    table.attribute_index, 
                    table.attribute_type, 
                    table.attribute_name, 
                    table.attribute_data, 
                    table.attribute_conf,
                    table.attribute_recc 
                ) \
                .where(
                    vector==search
                )
                runquery=session.execute(stt)
                results=runquery.fetchone()
                session.commit()
                session.flush()
                self.result = results 
                result:Dict[List,Any]=self.result 
                return result 
            

            def _getList(
                    self,
                    search:str, 
                    vector:str,
            )->Dict[List,Any]:
                table=Attribute.Entity.Attribute
                session=self.Session()
                stt= select(
                    table.attribute_index, 
                    table.attribute_type, 
                    table.attribute_name, 
                    table.attribute_data, 
                    table.attribute_conf,
                    table.attribute_recc, 
                    table.attribute_source
                ) \
                .where(
                    vector==search
                )
                runquery=session.execute(stt)
                results=runquery.fetchall()
                session.commit()
                session.flush()
                self.result = results 
                result:Dict[List,Any]=self.result 
                return result 
            
            def setTargetAttributes(
                    self,
                    package, 
                    recomm
            )->Dict[List,Any]:
                getcheck = self.lookup
                params=locals()
                result=self._getAttributes(
                    search=getcheck,
                    params=params,
                    vector=self.lu['es']
                )
                response = {}
                for i, row in enumerate(result):
                    rownum=i+1
                    core_attribute:str=row[2]
                    rowobj = {
                        'id':row[0],
                        'attributes': [
                            {
                                'column_name':core_attribute
                            }, 
                            {
                                'format':{
                                    'value':row[3], 
                                    'type': row[1]
                                }},]}
                    response.update({rownum:rowobj})
                return response 
            
            def pullTargetAttributes(
                    self,
                    package,
                    recomm
            )->Dict[List,Any]:
                getcheck = self.lookup 
                params=locals()
                result=self._getAttributes(
                    search=getcheck, 
                    params=params,
                    vector=self.lu['es']
                )
                response={}
                for i, row in enumerate(result):
                    rownum=i+1
                    core_attribute:str=row[2]
                    rowobj={
                        'id':row[0],
                        'attributes': [
                            {
                                'column_name':core_attribute
                            }, 
                            {
                                'format':{
                                    'value':row[3], 
                                    'type': row[1]
                                }},]}
                    response.update({rownum:rowobj})
                return response 
            

            def pullAttributesAndSampling(
                    self, 
                    package, 
                    recomm
            )->Dict[List,Any]:
                getcheck=self.lookup
                params=locals()
                speak:list=[]
                ok_computer:Dict[List,Any]=recomm['robot_reads']
                for i, item in enumerate(ok_computer):
                    speak.append(item)
                result=self._getAttributes(
                    search=getcheck, 
                    params=params, 
                    vector=self.lu['es']
                )
                sampleiter=recomm['graph']['graph_samples']
                response={}
                for i, row in enumerate(result):
                    rownum=i+1
                    rowbot=speak[i]
                    core_attribute:str=rowbot[0]
                    recc_attribute:str=rowbot[1]
                    conf_conv:float=1-rowbot[2]
                    conf_conv:float=100*conf_conv
                    conf_tier:str = ''
                    if conf_conv >= 90.00000:
                        conf_tier='High'
                    elif conf_conv <= 70.0000:
                        conf_tier = 'Low'
                    else:
                        conf_tier= 'Medium'

                    rowobj = {
                        'attribute_id':row[0], 
                        'confidence':conf_tier,
                        'confidenceIndex': conf_conv,
                        #'column_holder': core_attribute,
                        'column_header':recc_attribute,
                        'format':{
                            'value':row[1], 
                            'label':row[1]
                        },
                        'sample':[]
                    }
                    response.update({rownum:rowobj})


            def _getSourceList(
                    self, 
                    search:str, 
                    vector:str,
                    ):
                from module.pgvector.control import Collection 
                table=Collection.Entity.Entry 
                session=self.Session()
                stt=select(
                    table.entity_sfid, 
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
                result:Dict[List,Any]={}
                for row in runquery.fetchall():
                    serial=str(row[0])
                    rowie=json.dumps(row[1]['result']['action_event'])
                    result.update({serial:rowie})
                results=result 
                session.commit()
                session.flush()
                session.close()
                self.result = results 
                responder:Dict[List,Any]=self.result 
                return responder 
            

        class Retrieve:

            def __init__(
                    self,
                    package:Dict[List,Any]
            )->Dict[List, Any]:
                self.package=package 

            async def getAttributes(
                    self,
            ):
                result:Dict[List,Any]= Transact.router(
                    transact='RETRIEVE',
                    payload=self.package,
                )
                return result 
            

        class Create:

            def __init__(
                    self,
                    package:Dict[List,Any]
            )->Dict[List,Any]:
                result:Dict[List,Any]= Transact.router(
                    transact='CREATE',
                    payload=self.package,
                )
                return result 
            

        class Attribute:

            def __init__(
                    self, 
                    metadata:Dict[List,Any]
            ):
                self.m=metadata 

            class Length:

                def __init__(
                        self,
                        metadata:Dict[List,Any]
                ):
                    self.operators:Dict[List,Any]=metadata['operators']

                def buildFormulaString(
                        self
                ):
                    operation=self.operators 
                    return operation 
                
            class Formula:

                def __init__(
                        self,
                        metadata:Dict[List,Any]
                ):
                    self.operators:Dict[List,Any]=metadata['operators']

                def buildFormulaString(
                        self
                ):
                    operation=self.operators 
                    return operation 
                

            class Type:

                def __new__(
                        cls,
                        meta:Dict[List,Any]
                ):
                    msg='TYPE Object Creted for Column Attributes'
                    instance = super().__new__(cls)
                    return instance 
                
        
        class Entry(Env.HasTimestamp, Control):
            __tablename__="attribute_control"

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
            # entity_attr : Mapped[JSONB] = mapped_column(
            #     types.JSON, 
            #     nullable=True
            # )
            entity_label : Mapped[String] = mapped_column(
                types.String, 
                nullable = True
            )
            entity_type : Mapped[String] = mapped_column(
                types.String, 
                nullable = False
            )
            entity_trace : Mapped[StoreID] = mapped_column(
                types.Uuid, 
                nullable = False
            )
            entity_pack : Mapped[JSONB] = mapped_column(
                types.JSON, 
                nullable=True
            )



        class Trace(Env.HasTimestamp, Env.HasTrace, Control):
            __tablename__ = 'attribute_trace'

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

        class Attribute(Env.HasTimestamp, Env.HasTrace, Control):

            __tablename__ = "attribute_values"

            attribute_index : Mapped[Integer] = mapped_column(
                types.Integer, 
                autoincrement=True, 
                nullable=False, 
                primary_key=True
            )

            attribute_source : Mapped[StoreID] = mapped_column(
                types.Uuid, 
                nullable = False
            )

            attribute_trace : Mapped[String] = mapped_column(
                types.Uuid, 
                nullable = False
            )

            attribute_conf : Mapped[Float] = mapped_column(
                types.Float, 
                nullable=True
            )

            attribute_recc : Mapped[JSONB] = mapped_column(
                types.JSON,
                nullable=True
            )

            attribute_type : Mapped[String] = mapped_column(
                types.String,
                nullable=False
            )

            attribute_model: Mapped[String] = mapped_column(
                types.String,
                nullable=False
            )
            
            attribute_sample : Mapped[JSONB] = mapped_column(
                types.JSON, 
                nullable=True
            )

            attribute_attr : Mapped[JSONB] = mapped_column(
                types.JSON, 
                nullable=True
            )

            attribute_name: Mapped[String] = mapped_column(
                types.String,
                nullable=False
            )

            attribute_data : Mapped[JSONB] = mapped_column(
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
                msg="Update Object Creted for Holding Instruction"
                instance = super().__new__(cls)
                return instance 
            
        class Action(Enum):
            ACQUIRE=''



class Transact:

    connect = ORM.getConnectionString()
    engine = create_engine(connect)
    Session=sessionmaker(bind=engine)
    session=Session()

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
                Attribute.Entity.Trace
            ).where(
                Attribute.Entity.Trace.entity_key.like(getcheck)
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
                with Transact.Session() as session:
                    receiver:Dict[List,Any]=payload 
                    results = Attribute.Entity.Query(
                        lookup_key=receiver['key']
                    ).mapping_name()
                    result = results 

            case 'INITIATE':
                Control.metadata.create_all(Transact.engine)
                from module.pretzl.parser import GRAPH 
                result:Dict[List,Any]={}
                with Transact.Session() as session:
                    receiver:Dict[List,Any]=payload 
                    format=Attribute.Entity.Attribute(
                        attribute_index=None, 
                        attribute_source=receiver['graph']['graph_sfid'], 
                        attribute_model='', 
                        attribute_sample='',
                        attribute_trace=receiver['graph']['graph_tracer'],
                        attribute_name=receiver['graph_name'], 
                        attribute_type=receiver['graph_type'], 
                        attribute_data=receiver['graph_data'],
                        attribute_conf=receiver['graph_conf'], 
                        attribute_recc=receiver['graph_recc'], 
                        attribute_attr=receiver['graph_attr'], 
                        entity_event='initiate' 
                    )
                    session.add_all([format])
                    session.commit()

                    #entry table access insert (separate to handler)
                    attributenumber:Integer=format.attribute_index 
                    traceid:uuid.UUID=format.attribute_source.urn.split(':')[2]
                    entry = Attribute.Entity.Entry(
                        entity_name=receiver['graph_name'], 
                        entity_trace=traceid, 
                        entity_label=receiver['graph_attr']['entity_label'],
                        entity_type='attribute', 
                        entity_pack=receiver['graph']
                    )
                    session.add_all([entry])

                    controlid:uuid.UUID=entry.entity_sfid.urn.split(':')[2]
                    attributetrace= Attribute.Entity.Trace(
                        trace_index=None, 
                        entity_key=receiver['graph']['graph_key'], 
                        entity_trace=controlid,
                        entity_event=transact.lower()
                    )
                    session.add_all([attributetrace])
                    session.commit()

                    result={
                        'attribute_id':attributenumber, 
                        'event_logged':receiver, 
                        'entity_sfid':controlid, 
                        'entity_label': entry.entity_label, 
                        'entity_name': format.attribute_name
                    }
                    session.flush()
                    session.close()
                return result 
