import uuid 
from typing import Dict, List, Any
from sqlalchemy import (
    create_engine, update,
    select, text, 
    types, Integer, 
    UUID as StoreID, 
    String, UniqueConstraint
)

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    DeclarativeBase, 
    Mapped, 
    MappedAsDataclass, 
    mapped_column, 
    sessionmaker
)

from core.model.request import Assign as OpModel
from module.core.config import Env, System as CoreSys
from module.pgvector.config import ORM 


class Control(MappedAsDataclass, DeclarativeBase):
    pass

class System(CoreSys):

    def __init__(
            self,
            timezone:str=None
    ):
        if timezone:
            self.region=timezone 

    def getTimeStamp(self):
        return CoreSys.Timestamp.getTimeStampeLocal(tmz=self.region)
    
    def getRegionEnv(self):
        self.region = CoreSys.SYS.getRegionalEnv()
        return self.region
    

class Schema:



    class Manage:
        def __init__(
                self, 
                meta:Dict[List,Any]
        ):
           self.start = meta 

        async def updateSource(self):
            fields:OpModel=self.start['inputs']['body']
            action= await Schema.Entity.Origin(
                package=self.start
                ).updateFieldControls(
                    fields=fields
                )
            return action 
        

    class Entity:

        from sqlalchemy import event
        from sqlalchemy.sql import column 
        from sqlalchemy.orm import Session 

        class Origin:

            def __init__(
                    self,
                    package:Dict[List,Any]
            ):
                self.pack=package

            def bind(
                    self,
                    sub:dict=None
            )->Dict[List,Any]:
                self.start=self.pack
                self.sfid=self.pack['inputs']['sfid']

                import pandas as pd
                from module.file.model.Field import Field as FO
                changeto=FO.Entity.Query(lookup_key=self.sfid)
                curstate=FO.Entity.Origin(package=self.start)
                assigned=curstate.MapView(id=self.sfid)

                assigned['target']=str(self.sfid)
                try:
                    assigned['source']=str(changeto.getSource(field_idx=assigned['sourceFields'][0]['id'])[0])
                    assigned['sourceFields']=curstate.MapView(id=self.sfid)['sourceFields']
                except:
                    assigned['source']=None 
                    assigned['sourceFields']={}
                schema= Schema.Entity()
                holding=schema.Prepare(
                    package=self.start
                ).holdFields(
                    set=assigned
                )
                if len(sub) >=1:
                    for item in sub:
                        schema.Update(package=self.start).editFields(set=item)
                targets=schema.Query(lookup_key=self.sfid).getTargetFields()
                a:list=[]
                for item in targets:
                    b={
                        'id': item[0], 
                        'confidence':item[2], 
                        'confidenceIndex':item[3], 
                        'originalHeader':item[4], 
                        'suggestedHeader':item[5], 
                        'ai_generated':item[6],
                        'format':{
                            'value': item[7], 
                            'label': item[7]
                        },
                        'sourceFields':{
                            'id':item[9],
                            'suggested_header':item[10]
                        }
                    }
                    a.append(b)
                assign:Dict[List,Any]={}
                assign.update({'target_control':assigned['target']})
                assign.update({'target_fields': a})
                assign.update({'source_assignments':assigned['source']})
                assign.update({'source_mapping':assigned['sourceFields']})
                return assign 
            

            def receiveFieldControls(
                    self, 
                    fields:Dict[List,Any]=None
            )->Dict[List,Any]:
                self.graph=self.GetGraff()
                self.fields=self.graph['graph']
                if fields != None:
                    self.graph=fields['graph']
                stack=[]
                del self.pack['graph_origin']['event_logged']
                for index, (key, value) in enumerate(
                    self.pack['graph_meta'].items()
                ):
                    datafield=self.pack['graph_data']['page_content'].split("\n")[index].split(": ")[1]
                    self.graph['graph_name']=key
                    self.graph['graph_conf']=self.pack['graph_conf']
                    self.graph['graph_recc']=self.pack['graph_recc']
                    self.graph['graph_type']=value
                    self.graph['graph_data']=datafield 
                    self.graph['graph_attr']=self.pack 

                    result:Dict[List,Any]=Transact.router(
                        transact="INITIATE", 
                        payload=self.graph
                    )
                    stack.append(result)
                return stack 
            
            async def setFieldControls(
                self, 
                fields:Dict[List,Any]=None
            )->Dict[List,Any]:
                if fields !=None:
                    self.graph=fields
                result:Dict[List,Any]=Transact.router(
                    transact="ACCEPT", 
                    payload=self.graph 
                )
                return result 
            

            async def lockFieldControls(
                    self, 
                    fields:Dict[List,Any]=None
            )->Dict[List,Any]:
                if fields !=None:
                    self.graph=fields
                result:Dict[List,Any]=Transact.router(
                    transact="AFFIRM", 
                    payload=self.graph
                )
                return result 
            


        class Query:

            def __init__(
                    self,
                    lookup_key
            ):
                connect=ORM.getConnectionString()
                engine=create_engine(connect)

                self.Session=sessionmaker(bind=engine)
                self.session = self.Session()
                self.lookup = lookup_key
                self.body:Dict[List,Any]={}
                self.result={}

                self.lu={
                    'eo': Schema.Entity.Entry.entity_sfid,
                    'en': Schema.Entity.Entry.entity_name,
                    'el': Schema.Entity.Entry.entity_label,
                    'es': Schema.Entity.Assignment.assign_source,
                    'et': Schema.Entity.Assignment.assign_target,
                }

            def graph_sfid(
                    self,
            )->Dict[List,Any]:
                getcheck=self.lookup
                par=locals()
                result = self._getFields(
                    search=getcheck,
                    params=par,
                    vector=self.lu['go']

                )
                return result 
            
            def getTargetFields(
                    self,
                    params:dict=None
            ):
                table=Schema.Entity.Template
                session=self.Session()
                tfs=select(
                    table.holder_id, 
                    table.holder_target, 
                    table.holder_conf, 
                    table.holder_confidx,
                    table.holder_ogheader, 
                    table.holder_subheader,
                    table.holder_ai, 
                    table.holder_format, 
                    table.source_sfid,
                    table.source_fieldid,
                    table.source_subheader, 
                    table.schema_assigned
                ) \
                .where(
                    table.holder_target==self.lookup
                )
                query = session.execute(tfs)
                results=query.fetchall()
                session.commit()
                session.flush()
                self.result=results
                result:Dict[List,Any]=self.result 
                session.close()
                return result 
            

            
            def _getAssignments(
                    self,
                    params:Dict[List,Any], 
                    search:str,
                    vector:str
            )->Dict[List,Any]:
                table=Schema.Entity.Assignment 
                session=self.Session()
                stt=select(
                    table.field_index,
                    table.field_type,
                    table.field_name, 
                    table.field_data, 
                    table.field_conf,
                    table.field_recc,
                ) \
                .where(
                    vector == search 
                )
                runquery= session.execute(stt)
                results=runquery.fetchall()
                session.commit()
                session.flush()
                self.result=results 
                result:Dict[List,Any]=self.result 
                session.close()
                return result 
            

            def _getUnit(
                    self, 
                    params:Dict[List,Any], 
                    search:str, 
                    vector:str
            ):
                table=Schema.Entity.Assignment 
                session= self.Session()
                stt=select(
                    table.field_index,
                    table.field_type, 
                    table.field_name,
                    table.field_data,
                    table.field_conf, 
                    table.field_recc
                ) \
                .where(
                    vector==search
                )
                runquery= session.execute(stt)
                results=runquery.fetchone()
                session.commit()
                session.flush()
                self.result=results 
                result:Dict[List,Any]=self.result 
                session.close()
                #worth noting: package:Dict[List,Any]=self.result['t']
                return result 
            
            def _getSourceList(
                    self, 
                    search:str, 
                    vector:str
            ):
                from module.pgvector.control import Collection 
                import json 
                table= Collection.Entity.Entry 
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
                runquery= session.execute(stt)
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
                outcome:Dict[List,Any]=self.result 
                return outcome 
            
        class Retrieve:

            def __init__(
                    self, 
                    package:Dict[List,Any]
            )->Dict[List,Any]:
                self.package = package

            async def getFields(
                    self
            ):
                result:Dict[List,Any]=Transact.router(
                    transact="RETRIEVE", 
                    payload=self.package 
                )
                return result 
            

        class Create:


            def __init__(
                    self,
                    package:Dict[List,Any]
            )->Dict[List,Any]:
                self.package=package 

            async def setFields(
                    self,
            ):
                result:Dict[List,Any]=Transact.router(
                    transact="CREATE",
                    payload=self.package
                )
                return result 
            

        class Prepare:

            def __init__(
                    self,
                    package:Dict[List,Any]
            )->Dict[List,Any]:
                self.package=package                
            def holdFields(
                    self, 
                    set:Dict[List,Any]

            ):
                self.package.update({'matrix':set})
                try:
                    result:Dict[List,Any]=Transact.router(
                        transact="HOLDASSIGN", 
                        payload=self.package
                    )
                except:
                    result = {
                            'result':'FAILURE',
                            'message':'The ASSIGNMENT task could not be executed.'
                        }
                    raise Exception("The Assignment hold could not be executed")
                return result 
            
        class Update:

            def __init__(
                    self, 
                    package:Dict[List,Any]
            )->Dict[List,Any]:
                self.package=package 

            def editFields(
                    self,
                    set:Dict[List,Any]
            ):
                self.package.update({'matrix':set})
                try:
                    result:Dict[List,Any]=Transact.router(
                        transact="EDIT", 
                        payload=self.package
                    )
                except:
                    result = {
                            'result':'FAILURE',
                            'message':'The ASSIGNMENT task could not be executed.'
                    }
                    raise Exception("The Assignment hold could not be executed")
                return result 
            

            


        class Entry(Env.HasTimestamp, Control):
            __tablename__="assign_control"

            entity_sfid:Mapped[uuid.UUID]=mapped_column(
                types.Uuid,
                primary_key=True,
                init=False,
                server_default=text("gen_random_uuid()")
            )
            entity_name:Mapped[String]=mapped_column(
                types.String, 
                nullable=True 
            )
            entity_label:Mapped[String]=mapped_column(
                types.String,
                nullable=True 
            )
            # entity_attr:Mapped[ARRAY]=mapped_column(
            #     types.ARRAY(JSONB),
            #     nullable=False
            # )
            entity_type:Mapped[String]=mapped_column(
                String(64),
                nullable=False
            )
            entity_trace:Mapped[StoreID]=mapped_column(
                types.Uuid,
                nullable=False
            )
            entity_pack:Mapped[JSONB]=mapped_column(
                types.JSON, 
                nullable=True 
            )

    
        class Trace(Env.HasTimestamp, Env.HasTrace, Control):
            __tablename__ = 'assign_trace'

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

        class Template(Env.HasTimestamp,Control):
            __tablename__="assign_template"
            holder_inex:Mapped[Integer]=mapped_column(
                types.Integer, 
                autoincrement=True,
                nullable=False,
                primary_key=True
            )
            holder_id:Mapped[Integer]=mapped_column(
                types.Integer,
                nullable=False
            )
            holder_target:Mapped[StoreID]=mapped_column(
                types.Uuid,
                nullable=False
            )
            holder_conf:Mapped[str]=mapped_column(
                types.String,
                nullable=False 
            )
            holder_confidx:Mapped[Integer]=mapped_column(
                types.Integer,
                nullable=False 
            )
            holder_ogheader:Mapped[str]=mapped_column(
                types.String, 
                nullable=True

            )
            holder_subheader:Mapped[str]=mapped_column(
                types.String,
                nullable=True
            )
            holder_ai:Mapped[bool]=mapped_column(
                types.Boolean, 
                nullable=False
            )
            holder_format:Mapped[str]=mapped_column(
                types.String, 
                nullable=False 
            )
            source_sfid:Mapped[StoreID]=mapped_column(
                types.UUID, 
                nullable=False 
            )
            source_fieldid:Mapped[Integer]=mapped_column(
                types.Integer, 
                nullable=True 
            )
            source_subheader:Mapped[str]=mapped_column(
                types.String,
                nullable=True 
            )
            schema_assigned:Mapped[bool]=mapped_column(
                types.Boolean,
                nullable=True, 
                default=False 
            )

        class Assignment(Env.HasTimestamp, Env.HasTrace, Control):
            __tablename__="assignment_values"
            assign_index:Mapped[Integer]=mapped_column(
                types.Integer,
                autoincrement=True,
                nullable=False,
                primary_key=True
            )
            assign_target:Mapped[StoreID]=mapped_column(
                types.Uuid,
                nullable=False
            )
            assign_source:Mapped[String]=mapped_column(
                types.Uuid, 
                nullable=False 
            )
            assign_field:Mapped[String]=mapped_column(
                types.String,
                nullable=False 
            )
            assign_trace:Mapped[String]=mapped_column(
                types.Uuid, 
                nullable=True
            )
            assign_type:Mapped[String]=mapped_column(
                types.String, 
                nullable=False 
            )
            assign_model:Mapped[String]=mapped_column(
                types.String, 
                nullable=True
            )

            assign_collection:Mapped[String]=mapped_column(
                types.String, 
                nullable=True 
            )
            assign_data:Mapped[JSONB]=mapped_column(
                types.JSON, 
                nullable=True 
            )
            entity_event:Mapped[String]=mapped_column(
                types.String, 
                nullable=False 
            )


class Transact:

    connect=ORM.getConnectionString()
    engine=create_engine(connect)
    Session=sessionmaker(bind=engine)
    session=Session()

    def router(
            transact:str, 
            payload:Dict[List,Any]
    )->Dict[List,Any]:
        match str(transact).upper():

            case 'RETRIEVE':
                Control.metadata.create_all(Transact.enginer)
                with Transact.Session() as Session:
                    try:
                        receiver:Dict[List,Any]=payload
                        results=Schema.Entity.Query(
                            lookup_key=receiver['key']
                        ).graph_sfid()
                        result = results 
                    except Exception as err:
                        result={
                                'result': 'FAILURE',
                                'message': 'this schema could not be retrieved.', 
                                'payload': f'Final Code: {err}'
                            }
                return result 
            
            case 'UPDATE': 
                from module.file.model.Robot import Robot 
                Control.metadata.create_all(Transact.engine)
                with Transact.Session() as session:
                    receiver:Dict[List,Any]=payload
                    for record in payload['update']:
                        results=Schema.Entity.Query(
                            lookup_key=payload['sfid']
                        ).Update(body=record)
                        result=results
                        setout=Robot.Entity.Query(
                            lookup_key=payload['sfid']
                        ).Update(body=record)
                        setout 
                return result 
            

            case 'GENMATRIX':
                Control.metadata.create_all(Transact.engine)
                result:Dict[List,Any]={}
            
                with Transact.Session() as session:
                    receiver:Dict[List,Any]=payload 
                    establish=Schema.Entity.Assignment(
                        field_index=None,
                        field_label=receiver['field_label'],
                        field_targe=receiver['field_target'], 
                        field_source=receiver['field_source'], 
                        field_isai=receiver['field_isai'], 
                        field_confinx=receiver['field_confinx'], 
                        field_conf=receiver['field_conf'], 
                        field_type=receiver['field_type'], 
                        field_value=receiver['field_value'], 
                        field_orig=receiver['field_orig']
                    )
                    session.add_all([establish])
                    session.commit()
                    session.flush()
                    session.close()

                return result 
            

            case 'INITIATE': 

                Control.metadata.create_all(Transact.Engine)
                from module.pretzl.etl import GRAPH 
                from module.file.action.subroutine.type import format as FMT 
                result: Dict[List,Any]={}
                with Transact.Session() as session:

                    receiver:Dict[List,Any]=payload
                    settype=FMT.Eval(input=receiver['graph_data']).getType()
                    format=Schema.Entity.Assignment(
                        field_index=None, 
                        field_source=receiver['graph']['graph_sfid'], 
                        field_model='', 
                        field_sample='',
                        field_trace=receiver['graph']['graph_tracer'], 
                        field_name=receiver['graph_name'], 
                        field_type=settype,
                        field_data=receiver['graph_data'],
                        field_conf=receiver['graph_conf'], 
                        field_recc=receiver['graph_recc'], 
                        field_attr=receiver['graph_attr'],
                        entity_event='initiate'

                    )
                    session.add_all([format])
                    session.commit()

                    fieldnumber:Integer=format.assign_index
                    traceid:uuid.UUID=format.assign_source.urn.split(':')[2]

                    fieldentry= Schema.Entity.Entry(
                        entity_name=receiver['graph_name'], 
                        entity_trace=traceid, 
                        #entity_attr=receiver['result'],
                        entity_label=receiver['graph_attr']['entity_label'], 
                        entity_type='field', 
                        entity_pack=receiver['graph']
                    )
                    session.add_all([fieldentry])
                    session.commit()

                    controlid:uuid.UUID=fieldentry.entity_sfid.urn.split(':')[2]
                    fieldtrace= Schema.Entity.Trace(
                        trace_index=None,
                        entity_key=receiver['graph']['graph_key'], 
                        entity_trace=controlid,
                        entity_event=transact.lower()
                    )
                    session.add_all([fieldtrace])
                    session.commit()


                    result = {
                        'field_id':fieldnumber, 
                        'event_logged':receiver, 
                        'entity_sfid':controlid,
                        'entity_label':fieldentry.entity_label, 
                        'entity_name':format.assign_name,
                        #'event_trace':tracer.items()
                    }

                    session.flush()
                    session.close()
                return result 
            

            case 'HOLDASSIGN':
                Control.metadata.create_all(Transact.engine)
                result:Dict[List,Any]=payload
                try:
                    with Transact.Session() as session:
                        mapping=result['matrix']
                        target=mapping['target']
                        source=mapping['source']
                        for item in mapping['targetFields']:
                            holder= Schema.Entity.Template(
                                holder_index=None, 
                                holder_id=item['id'], 
                                holder_target=target, 
                                holder_conf=item['confidence'],
                                holder_confidx=item['confidenceIndex'], 
                                holder_ogheader=item['originalHeader'], 
                                holder_subheader=item['suggestedHeader'],
                                holder_ai=item['ai_generated'], 
                                holder_format=item['format']['value'], 
                                source_sfid=source,
                                source_fieldid=item['sourceFields']['id'], 
                                source_subheader=item['sourceFields']['suggested_header']
                            )
                            session.add_all([holder])
                        session.commit()
                        session.flush()
                except:
                    result={
                            'result': 'FAILURE', 
                            'message': 'The Assignment Transaction could not execute for ORM Holding', 
                            'payload': None
                    }
                session.close()
                return True
            

            case 'EDIT':
                session = Transact.Session()
                workset=payload 
                message:Dict[List,Any]={}
                if len(workset['matrix']['id']) >= 1:
                    print('EDITING TEMPLATE')
                    id=workset['matrix']['id']
                    attr=workset['matrix']['attributes']
                    try:
                        origin= Schema.Entity.Template
                        ctrl= (
                            update(origin)
                            .where(
                                origin.holder_id==id 
                            )
                            .values(
                                holder_format=attr[0]['format']['label'], 
                                source_fieldid= attr[0]['sourceFields'][0]['id'], 
                                source_subheader= attr[0]['sourceFields'][0]['sugggested_header']
                            )
                        )
                        session.execute(ctrl)
                        session.commit()
                        session.flush()
                    except Exception as err:
                        message.update({
                            'details' : {
                                'result': 'FAILURE', 
                                'message':' The EDIT update could not be executed.', 
                                'payload': f'Additional Error Details: {err}'


                            }
                        })
                        session.close()
                        raise Exception("The assignment edit could not be executed")
                session.close()
                return True 