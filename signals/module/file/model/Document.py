import uuid, base64, pandas as pd
from typing import Dict, List, Any 
from enum import Enum 
from pandas import DataFrame 
from sqlalchemy import (
    create_engine, 
    update, select, 
    text, types, Integer, String, 
    UUID as TraceID 
)

from sqlalchemy.dialects.postgresql import JSONB 
from sqlalchemy.orm import (
    DeclarativeBase, 
    Mapped, 
    MappedAsDataclass, 
    mapped_column, 
    sessionmaker
)

from core.config import Env, System as CoreSys
from core.model.request import Matrix as OpModel 
from module.pgvector.config import ORM 

class Control(MappedAsDataclass, DeclarativeBase):
    pass 

class System(CoreSys):

    def __init__(
            self, 
            timezone:str=None,
    ):
        if timezone: 
            self.region=timezone
    
    def get_timestamp(self):
        return CoreSys.Timestamp.getTimeStampeLocal(tmz=self.region)
    
    def get_region_env(self):
        self.region = CoreSys.SYS.getRegionalEnv()
        return self.region 
    


class Document:

    class Manage:

        def __init__(
                self, 
                meta:Dict[List,Any]
        ):
            self.start=meta 
            self.pack=['inputs']

        
        def setPack(
                self, 
                pkg:Dict[List, Any]
        ):
            self.pack=pkg 
            return self.pack 
        
        def getPack(
                self, 
        ):
            return self.pack 
        

        async def moveToWasb(self):
            pass 

        async def updateSource(self):
            try:
                fields:OpModel=self.start['inputs']['body']
                control=Document.Entity.Origin(package=self.start)
                action= await control.updateFieldControls(fields=fields)
                result= control.MapView(id=action['sfid'])
            except:
                result={
                    'result':'FAILURE', 
                    'message':'Failed to update SOURCE fields.'
                }
            return result
        

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
                self.graph = {}



        class Query:

            def __init__(
                    self,
                    lookup_key
            ):
                from module.pgvector.control import Collection as Dox 
                connect= ORM.getConnectionString()
                engine=create_engine(connect)

                self.Session=sessionmaker(bind=engine)
                self.session= self.Session()
                self.lookup=lookup_key 
                self.body:Dict[List,Any]
                self.results={}

    
                self.lu = {
                    'eo':Document.Entity.Entry.entity_sfid,
                    'en':Document.Entity.Entry.entity_name, 
                    'el':Document.Entity.Entry.entity_label, 
                    'es':Document.Entity.Attribute.attr_source,
                    'ml':Document.Entity.Mapping.attr_label
                }

            def View(self):
                from module.file.model.Robot import Robot 
                table=Document.Entity.Mapping
                session=self.Session()
                stt=select(
                    table.field_index,
                    table.field_label,
                    table.field_isai, 
                    table.field_conf,
                    table.field_confinx,
                    table.field_orig,
                    table.field_type,
                    table.field_value
                ) \
                .where(
                    table.field_target == self.lookup
                ).order_by(table.field_index)
                runquery=session.execute(stt)
                rows=runquery.fetchall()
                session.commit()
                session.flush()
                source=[]
                for row in rows:
                    source.append(
                        {
                            'id':row[0],
                            'confidence':row[3],
                            'confidenceIndex':row[4], 
                            'originalHeader':row[5], 
                            'suggestedHeader':row[1],
                            'ai_generated':row[2],
                            'format' :{
                                'value': row[6], 
                                'label': row[6]
                            }
                        }
                    )
                tab2=Document.Entity.Attribute
                se2=self.Session()
                stb=select(
                    tab2.field_index, 
                    tab2.field_conf, 
                    tab2.field_name,
                    tab2.field_recc, 
                    tab2.field_type, 
                    tab2.field_data
                ).where(
                    tab2.field_source==self.lookup
                )
                runquery = se2.execute(stb)
                res=runquery.fetchall()
                se2.commit()
                se2.flush()
                target = []

                for row in res:
                    target.append(
                        {
                            'id':row[0],
                            'confidence':'High',
                            'confidenceIndex':row[1], 
                            'originalHeader':row[2], 
                            'suggestedHeader':row[3],
                            'ai_generated':'False',
                            'format' :{
                                'value': row[4], 
                                'label': row[4]
                            }
                        }
                    )
                    se2.close()
                    response:Dict[List,Any]={}
                    response.update({'sfid':self.lookup})
                    response.update({'targetFields':target})
                    response.update({'sourceFields':source})
                    return response 
                
            def set_spine(
                    self,
            ):
                table = Document.Entity.Attribute
                session=self.Session()
                try:
                    sql=select(
                        table.field_index,
                        table.field_name, 
                        table.field_trace,
                        table.field_conf, 
                        table.field_type,
                        table.field_data,
                        table.field_attr,
                    ).where(
                        table.field_source==self.lookup
                    ).order_by(
                        table.field_index
                    )
                    run_query=session.execute(sql)
                    results=[]
                    rows = run_query.fetchall()
                    for row in rows:
                        results.append(row._asdict())
                    session.commit()
                    session.flush()
                except:
                    results=[]
                    raise SyntaxError("Failed to set Entity Spine for PRETZL")
                    


            def Show(
                    self,
                    samples
                    ):
                from module.pgvector.control import Collection as Coll 
                from module.file.action.Map import Matrix as MD
                from module.file.model.Robot import Robot 
                from module.file.helper import Helper as H 
                table = Document.Entity.Mapping 
                session=self.Session()
                stt=select(
                    table.field_index,
                    table.field_label,
                    table.field_isai, 
                    table.field_conf,
                    table.field_confinx,
                    table.field_orig,
                    table.field_type,
                    table.field_value
                ).where (
                    table.field_target==self.lookup
                ).order_by(
                    table.field_index
                )
                runquery=session.execute(stt)
                rows=runquery.fetchall()
                session.commit()
                session.flush()
                source = []

                samp:DataFrame=pd.DataFrame(samples)
                for row in rows:
                    samplcol = samp.get(row[5]).to_list()
                    source.append({
                        'id': row[0], 
                        'confidence':row[3],
                        'confidenceIndex':row[4],
                        'original_header':row[5],
                        'suggested_header':row[1],
                        'ai_generated':row[2], 
                        'format' : {
                            'value':row[6],
                            'label':row[6],
                        },
                        'sample 1':samplcol[0], 
                        'sample 2':samplcol[1],
                        'sample 3':samplcol[2],
                        'sample 4':samplcol[3]
                    })
                    return source
                
            def Update(
                    self,
                    body:dict 
            ):
                setlist=body['attributes']
                try:
                    n_label=setlist[0]['assigned_header']
                    n_orig=setlist[1]['original_header']
                    n_type=str(setlist[2]['format']['label'])
                    n_value=str(setlist[2]['format']['value'])
                    table=Document.Entity.Mapping 
                    session=self.Session()
                    stmt= (update(table).where(
                        table.field_index==body['id']
                        ).values(
                            field_label=n_label,
                            field_orig=n_orig, 
                            field_type=n_type, 
                            field_value=n_value
                        ))
                    session.execute(stmt)
                    session.commit()
                    session.flush()
                    session.close()
                except:
                    return False 
                #result=self.View()

            def AssignmentUpdate(
                    self, 
                    body:dict
            )->bool:
                from module.file.model.Robot import Robot as R2 
                setlist=body['attributes']
                targ=body['id']
                message:Dict[List,Any]={}
                for item in setlist:
                    session=self.Session()
                    try:
                        target_action= item 
                        origin=Document.Entity.Attribute
                        ctrl=(
                            update(origin).where(
                                origin.field_index==targ
                            ).values(field_type=target_action['format']['label']
                            )
                        )
                        session.execute(ctrl)
                    except:
                        message.update({
                            'result':'FAILURE', 
                            'message':'Target table assignment update failed.'
                        })
                    try: 
                        source_action=item['sourceFields']
                        for field in source_action:
                            sid=field['id']
                            sgs=field['suggested_header']
                            table=Document.Entity.Mapping 
                            exists=bool(session.query(table).filter_by(field))
                            if exists:
                                srcu=(
                                    update(table)
                                    .where(
                                        table.field_index==sid
                                    ).values(
                                        field_label=sgs
                                    )
                                )
                            session.execute(srcu)
                            session.commit()
                        else:
                            message.update({
                                'result':'FAILURE', 
                                'message':'mapping broke down...'
                            })
                    except:
                        message.update({
                            'result':'FAILURE', 
                            'message': 'source table is not able to update the record.'
                        })
                    try:
                        for upds in source_action:
                            sid=upds['id']
                            sgs=upds['suggested_header']
                            robo=R2.Entity.Field
                            srcu=(
                                update(robo).where(
                                    robo.field_index==sid
                                ).values(
                                    field_robot=sgs
                                )
                            )
                        session.execute(srcu)
                        session.commit()
                    except:
                        message.update({
                            'result':'FAILURE', 
                            'message': 'source table is not able to update the record.'
                        })

                session.flush()
                session.close()
                return True

            def getSource(
                    self, 
                    field_idx
            )->uuid:
                table=Document.Entity.Mapping
                session = self.Session()
                stt= select(
                    table.field_index==field_idx
                )
                runquery=session.execute(stt)
                result=runquery.fetchone()
                session.commit()
                session.flush()
                session.close()
                return result
            
            def source_fields(
                    self,
            )->Dict[List,Any]:
                getcheck = self.lookup
                params=locals()
                result: Dict[List,Any]= self._getSource(search=getcheck)
                return result 
            

            def field_assoc(self)->Dict[List,Any]:
                getcheck=self.lookup 
                params=locals()
                result = self._getSourceList(
                    search=getcheck,
                    vector=self.lu['cl']
                )
                return result 
            
            def getReco(
                    self,            
            ):
                result=self._getMapping()
                return result 
            
            def getMapping(
                    self
            ):
                result = self._getMapped()
                return result 
            
            def getIDFromLabel(
                    self, 
                    label
            )->int:
                result = self._getMappedID(
                vector='attribute_label', 
                input=label
                )
                return result 
            
            def getMapFieldId(
                    self,
                    label
            )->int:
                result=self._getSource(
                    search=label
                )
                return result 
            

            def field_label(
                    self, 
                    geturl:bool=False,
            )->Dict[List,Any]:
                getcheck = self.lookup 
                params=locals()
                result= self._getUnit(
                    search=getcheck, 
                    params=params, 
                    vector=self.lu['el']
                )
                return result 
            
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
            
            def entity_sfid(
                    self
            )->Dict[List,Any]:
                getcheck=self.lookup
                params=locals()
                result=self._getFields(
                    search=getcheck, 
                    params=params, 
                    vector=self.lu['eo']
                )
                return result 
            
            def field_name(
                    self,
            )->Dict[List,Any]:
                getcheck=self.lookup 
                params=locals()
                result=self._getUnit(
                    search=getcheck, 
                    params=params, 
                    vector=self.lu['mn']
                )
                return result 
            

            def _getMapped(
                    self,
            ):
                table = Document.Entity.Mapping
                session = self.Session()
                alchemy_sql=select(
                    table.field_index,
                    table.field_label,
                    table.field_orig,
                    table.field_type,
                    table.field_value,
                    table.field_source
                ).where(
                    table.field_target == self.lookup
                )
                run_query=session.execute(alchemy_sql)
                results = run_query.fetchall()
                session.commit()
                session.flush()
                session.close()
                return results



            def _getMappedID(
                    self,
                    vector,
                    input
            ):  
                table=Document.Entity.Mapping 
                session=self.Session()
                alchemy_sql=select(
                    table.field_index
                ).filter(
                    table.field_source == self.lookup, 
                    table.field_label == input
                )
                run_query=session.execute(alchemy_sql)
                result = run_query.fetchone()
                session.commit()
                session.flush()
                session.close()
                return result[0]
            

            def _getMapping(
                    self, 
                    keytype:str='attr_source'
            ):
                table=Document.Entity.Mapping 
                session=self.Session()
                alchemy_sql=select(
                    table.field_index, 
                    table.field_label, 
                    table.field_orig, 
                    table.field_type, 
                    table.field_value, 
                    table.field_target
                ).where(
                    table.field_source == self.lookup  
                )
                run_query = session.execute(alchemy_sql)
                results = run_query.fetchall()
                session.commit()
                session.flush()
                session.close()
                return results 
            

            def _getField(
                    self, 
                    params:Dict[List,Any], 
                    search:str, 
                    vector:str,
            ):
                table=Document.Entity.Field
                session = self.Session()
                alchemy_sql=select(
                    table.field_index, 
                    table.field_type, 
                    table.field_name, 
                    table.field_data, 
                    table.field_conf, 
                    table.field_recc,
                ).where(
                    vector==search 
                )
                run_query=session.execute(alchemy_sql)
                results=run_query.fetchone()._asdict()
                session.commit()
                session.flush()
                self.result = results


            def _getSource(
                    self, 
                    search:str, 
            )->Dict[List,Any]:
                table=Document.Entity.Mapping 
                session=self.Session()
                alchemy=select(
                    table.field_index, 
                    table.field_label,
                    table.field_orig,
                ).where(
                    table.field_target==search
                )
                query=session.execute(alchemy)
                results=query.fetchall()
                session.commit()
                session.flush()
                session.close()
                return results 
            

            def _getFields(
                    self,
                    params:Dict[List,Any], 
                    search:str, 
                    vector:str, 
            )->Dict[List,Any]:
                table=Document.Entity.Attribute
                session=self.Session()
                sql=select(
                    table.field_index, 
                    table.field_type, 
                    table.field_name, 
                    table.field_data, 
                    table.field_conf,
                    table.field_recc,
                ).where(
                    vector==search
                )
                runquery=session.execute(sql)
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
            ):
                table=Document.Entity.Attribute
                session=self.Session()
                sql=select(
                    table.field_index, 
                    table.field_type, 
                    table.field_name, 
                    table.field_data, 
                    table.field_conf,
                    table.field_recc,
                ).where(
                    vector==search
                )
                runquery=session.execute(sql)
                results=runquery.fetchone()
                session.commit()
                session.flush()
                self.result = results
                result:Dict[List,Any]=self.result
                session.close()
                return result        
            

            def _getList(
                    self,
                    search:str, 
                    vector:str,
            ):
                table=Document.Entity.Attribute
                session=self.Session()
                sql=select(
                    table.field_index, 
                    table.field_type, 
                    table.field_name, 
                    table.field_data, 
                    table.field_conf,
                    table.field_recc,
                    table.field_source
                ).where(
                    vector==search
                )
                runquery=session.execute(sql)
                results=runquery.fetchall()
                session.commit()
                session.flush()
                self.result = results
                result:Dict[List,Any]=self.result
                session.close()
                return result
            

            def Ready(
                    self,
            ):
                from module.file.model.Robot import Robot 
                table=Document.Entity.Mapping 
                session=self.Session()
                sql=select(
                    table.field_index, 
                    table.field_label,
                    table.field_type, 
                    table.field_name, 
                    table.field_data, 
                    table.field_conf,
                    table.field_recc,
                ).where(
                    table.mapping_target == self.lookup 
                ).order_by(table.field_index)
                run_query=session.execute(sql)
                rows_out=run_query.fetchall()
                session.commit()
                session.flush()
                source = []
                for rows in rows_out:
                    source.append(
                        {
                            'id':rows[0],
                            'confidence':rows[3], 
                            'confidenceIndex':rows[4],
                            'originalHeader':rows[5],
                            'suggestedHeader':rows[1], 
                            'ai_generated':rows[2], 
                            'format':{
                                'value':rows[6], 
                                'label':rows[6]
                            }
                        }
                    )
                table_2=Document.Entity.Attribute 
                session_2=self.Session()
                sql_2=select(
                    table_2.attr_index,
                    table_2.attr_conf, 
                    table_2.attr_name, 
                    table_2.attr_recc, 
                    table_2.attr_type, 
                    table_2.attr_data
                ).where(
                    table_2.attr_source == self.lookup
                )
                run_query_2=session_2.execute(sql_2)
                result_2=run_query_2.fetchall()
                session_2.commit()
                session_2.flush()
                target=[]
                for rows in result_2:
                    target.append(
                        {
                            'id':rows[0],
                            'confidence':'High', 
                            'confidenceIndex':rows[1],
                            'originalHeader':rows[2],
                            'suggestedHeader':rows[3],
                            'ai_generated': False,
                            'format':{
                                'value':rows[4],
                                'label':rows[4]
                            }
                        }
                    )
                session_2.close()
                response:Dict[List,Any]={}
                response.update({'sfid': self.lookup})
                response.update({'targetFields': target})
                response.update({'sourceFields':source})
                return response 
            

            def _getSourceList(
                    self, 
                    search:str, 
                    vector:str,
                ):
                from module.pgvector.control import Collection
                import json 
                table = Collection.Entity.Entry
                session=self.Session()
                sql=select(
                    table.entity_sfid,
                    table.entity_pack,
                ).where(
                    vector==search
                ).filter(
                    table.entity_type=='transaction'
                ).distinct(
                    table.entity_sfid
                )
                run_query=session.execute(sql)
                result:Dict[List,Any]={}
                for row in run_query.fetchall():
                    serial=str(row[0])
                    rowie=json.dumps(row[1]['result']['action_event'])
                    result.update({serial : rowie})
                results = result 
                session.commit()
                session.flush()
                session.close()
                self.result=results 
                result:Dict[List,Any]= self.result 
                return result

        class Retrieve:
            def __init__(
                    self, 
                    package:Dict[List,Any]
            )->Dict[List,Any]:
                self.package=package 

            async def set_fields(
                    self,
            ):
                result:Dict[List,Any]=Transact.router(
                    transact='RETRIEVE', 
                    payload=self.package,
                )
                return result 
            
        class Create:
            def __init__(
                    self, 
                    package:Dict[List,Any]
            )->Dict[List,Any]:
                self.package=package 

            async def set_fields(
                    self,
            ):
                result:Dict[List,Any]=Transact.router(
                    transact='CREATE', 
                    payload=self.package,
                )
                return result 

            
        class Field:
            def __init__(
                    self, 
                    metadata:Dict[List,Any]
            )->Dict[List,Any]:
                self.m=metadata
    

            class Length:
                def __init__(
                        self,
                        metadata:Dict[list,Any]
                ):
                    self.operators:Dict[List,Any]=metadata['operators']
                def build_formula(
                        self
                ):
                    operation=self.operators
                    return operation 
            """
            TODO: Flagging for redundancy [@Length and @Formula do the same thing.]
            @daniel 092025
            """     

            class Formula:
                def __init__(
                        self,
                        metadata:Dict[List,Any]
                ):
                    self.operators:Dict[List,Any]=metadata['operators']
                def build_formula_str(
                        self,
                ):
                    operation=self.operators
                    return operation 
                
            class Type:
                def __new__(
                        cls,
                        meta:Dict[List,Any]
                ):
                    msg="[FILE : Document Entity] - TYPE created for data field"
                    instance=super().__new__(cls)
                    return instance 
            
################################################################################
        """
        C2 PRETZL 23Controls - Model Layer for Trace [Control 10]
        """
################################################################################

        class Models(Control):
            """@Document.Entity.Models - is a control plane tracing table 
            for the origin, use, and volume of data moving into controls via 
            the Document model set. Any digest of 'document' files will be moved
            through this table and set to trace visibility across the entire
            agentic chain of custody.

            """

            __tablename__='document_models'

            model_index:Mapped[Integer]=mapped_column(
                types.Integer,
                autoincrement=True,
                nullable=False,
                primary_key=True
            )

            model_name:Mapped[String]=mapped_column(
                types.String, 
                nullable=False,
            )
            model_owner:Mapped[String]=mapped_column(
                types.String,
                nullable=False
            )
            model_share:Mapped[bool]=mapped_column(
                types.Boolean, 
                default=False,
            )
            model_type:Mapped[String]=mapped_column(
                types.String, 
                nullable=False, 
                default='Custom'
            )
            model_data:Mapped[JSONB]=mapped_column(
                types.JSON, 
                nullable=True 
            )



        class Entry(Env.HasTimestamp, Control):
            __tablename__='document_control'
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
            entity_type:Mapped[String]=mapped_column(
                String(64),
                nullable=False,
            )
            entity_trace:Mapped[TraceID]=mapped_column(
                types.Uuid, 
                nullable=False,
            )
            entity_pack:Mapped[JSONB]=mapped_column(
                types.JSON,
                nullable=False
            )

        class Trace(Env.HasTimestamp, Control):
            __tablename__='document_trace'
            trace_index:Mapped[uuid.UUID]=mapped_column(
                types.Integer,
                primary_key=True,
                nullable=False,
                autoincrement=True
            )
            entity_key:Mapped[String]=mapped_column(
                String(1024),
                nullable=False
            )
            entity_trace:Mapped[TraceID]=mapped_column(
                types.Uuid, 
                nullable=False,
                server_default=text("gen_random_uuid()")
            )
            entity_event:Mapped[String]=mapped_column(
                types.String,
                nullable=False
            )

        class Attribute(Env.HasTimestamp, Control):
            __tablename__="document_attribute"
            attr_index:Mapped[Integer]=mapped_column(
                types.Integer,
                autoincrement=True,
                primary_key=True,
                nullable=False,
            )
            attr_source:Mapped[TraceID]=mapped_column(
                types.Uuid,
                nullable=False,
            )
            attr_trace:Mapped[String]=mapped_column(
                types.Uuid,
                nullable=False,
            )
            attr_conf:Mapped[String]=mapped_column(
                types.String, 
                nullable=False,
            )
            attr_recc:Mapped[String]=mapped_column(
                types.String, 
                nullable=True
            )
            attr_type:Mapped[String]=mapped_column(
                types.String, 
                nullable=False,
            )
            attr_model:Mapped[String]=mapped_column(
                types.String, 
                nullable=True
            )
            attr_sample:Mapped[JSONB]=mapped_column(
                types.JSON, 
                nullable=True 
            )
            attr_attr:Mapped[JSONB]=mapped_column(
                types.JSON,
                nullable=True,
            )
            attr_name:Mapped[String]=mapped_column(
                nullable=False, 
            )
            attr_data:Mapped[JSONB]=mapped_column(
                types.JSON, 
                nullable=True
            )
            entity_event:Mapped[String]=mapped_column(
                types.String, 
                nullable=False,
            )

        class Mapping(Env.HasTimestamp, Control):
            __tablename__="document_mapping"
            mapping_index:Mapped[Integer]=mapped_column(
                types.Integer, 
                autoincrement=True,
                nullable=False,
                primary_key=True
            )
            mapping_label:Mapped[String]=mapped_column(
                types.String, 
                nullable=False
            )
            mapping_target:Mapped[TraceID]=mapped_column(
                types.Uuid, 
                nullable=False,
            )
            mapping_confinx:Mapped[Integer]=mapped_column(
                types.Integer,
                nullable=False,
            )
            mapping_conf:Mapped[String]=mapped_column(
                types.String,
                nullable=False
            )
            mapping_source:Mapped[String]=mapped_column(
                types.Uuid, 
                nullable=False,
            )
            mapping_type:Mapped[String]=mapped_column(
                types.String, 
                nullable=False,
            )
            mapping_value:Mapped[String]=mapped_column(
                types.String, 
                nullable=False,
            )
            mapping_orig:Mapped[String]=mapped_column(
                types.String, 
                nullable=True, 
            )
            mapping_isai:Mapped[bool]=mapped_column(
                types.Boolean, 
                nullable=False,
                default=False,
            )

        class Update:

            def __new__(
                    cls,
                    meta:Dict[List,Any]
            ):
                msg="FILE - Document : Entity UPDATE object created to instruct"
                instance=super().__new__(cls)
                return instance
            

#############################  END CTRL 10 #####################################            

class Transact:

    connect=ORM.getConnectionString()
    engine=create_engine(connect)
    Session=sessionmaker(bind=engine)
    session = Session()

################################################################################

    """
    @23Controls - CTRL 11 - Entity Transaction Serial Validation.
    """
################################################################################

    def issue_checksum(
        file_headers:Dict[List,Any]
    ):
        """
        @issue_checksum provides transaction serial authentic trace in record.
        """
        try: 
            code:str=''
            for item in file_headers:
                code+= str(file_headers[item])
            check_str:str=code
            check_bytes=check_str.encode('ascii')
            checksum = base64.b64encode(check_bytes)
            return checksum 
        except:
            raise EncodingWarning("CHECKSUM ERR [ENCODE] - Check file permiit")
        
    def validate(
            checksum
        )->bool:
        session = Transact.Session()
        sql=select(
            Document.Entity.Trace
            ).where(
            Document.Entity.Trace.entity_key.like(checksum)
            )
        run_query = session.execute(sql)
        session.commit()
        response=run_query.fetchone()._asdict()
        print(response)
        return True 
        ###TODO: Function needs to be mapped to the tables better.

############################### END CTRL 11 ####################################


################################################################################
    """
    23Controls : CTRL 12 - Entity Based Tranasaction Router & Feature Mgmt
    """
################################################################################
    def router(
        transact:str,
        payload:Dict[List,Any]
    )->Dict[List,Any]:
        """router - this is the logical control point for the model based 
        transactions in teh backend Collection Controls. These assure there is
        non-duplication of uploads, and begin the system level trace of all 
        files through the system. 
        """
        match str(transact).upper():

            case 'RETRIEVE':
                """
                RETRIEVE: Ingest data from CREATE to build a filedata set:
                - Writes to PG Database about the file metadata and trace 
                - Allows for labeling of file reference in abstraction. 
                - Returns a payload for use by the services 
                - Includes information about the current file locations.
                """
                Control.metadata.create_all(Transact.engine)
                with Transact.Session() as session:
                    try:
                        receiver:Dict[List,Any]=payload 
                        results=Document.Entity.Query(
                            lookup_key=receiver['key']
                        ).mapping_name()
                        result = results 
                    except:
                        response = {
                            'result':'FAILURE',
                            'msg': f'Failure in '.__class__
                        }
                        raise SyntaxError(response)
                return result  
            

            case 'UPDATE':
                from module.file.model.Robot import Robot
                receiver:Dict[List,Any]=payload
                for result in payload['update']:
                    try:
                        action=Document.Entity.Query(
                            lookup_key=payload['sfid']
                        ).Update(body=result)
                    except:
                        response={
                           'result':'FAILURE',
                            'msg': f'Failure in '.__class__
                        }
                        raise SyntaxError(response)
                output=Document.Entity.Query(lookup_key=payload['sfid']).View
                return output
            

            case 'GENMATRIX':
                Control.metadata.create_all(Transact.engine)
                result:Dict[List,Any]={}
                with Transact.Session() as session:
                    receiver: Dict[List,Any]=payload 
                    try:
                        behold=Document.Entity.Mapping(
                            field_index=None,
                            field_label=receiver['field_label'], 
                            field_target=receiver['field_target'], 
                            field_source=receiver['field_source'], 
                            field_isai=receiver['field_isai'], 
                            field_confinx=receiver['field_confinx'], 
                            field_conf=receiver['field_conf'], 
                            field_type=receiver['field_type'], 
                            field_value=receiver['field_value'], 
                            field_orig=receiver['field_orig']
                          )
                        session.add_all(behold)
                        session.commit()
                    except:
                          response={
                            'result':'FAILURE',
                            'msg': 'ECL - Document failed at '.__class__
                          }
                    session.flush()
                    session.close()
                return result 


            case 'INITIATE':
                """
                ORIGINATE: Gathering cusory inpu about the data which is being
                digested provides a landing strip of columns and input to create
                for the data whic his received by the system and interpreted.
                """
                Control.metadata.create_all(Transact.engine)
                from module.pretzl.parser import GRAPH
                from module.file.action.subroutine.type import Format as FMT
                initiate_result:Dict[List,Any]={}
                
                with Transact.Session() as session:
                    init_receiver:Dict[List,Any]=payload
                    settype=FMT.Eval(input=receiver['graph_data']).getType()
                    init_format=Document.Entity.Attribute(
                        attr_index=None, 
                        attr_source=init_receiver['graph']['graph_sfid'], 
                        attr_model='',
                        attr_sample='',
                        attr_trace=init_receiver['graph']['graph_tracer'], 
                        attr_name=init_receiver['graph_name'], 
                        attr_type=settype,
                        attr_data=init_receiver['graph_data'], 
                        attr_recc=init_receiver['graph_recc'],
                        attr_attr=init_receiver['graph_attr'], 
                        entity_event='initiate'
                    )
                    session.add_all([init_format])
                    session.commit()
                    attr_number:Integer=init_format.attr_index
                    trace_id:uuid.UUID=init_format.attr_source.urn.split(':')[2]

                    attribute_entry=Document.Entity.Entry(
                        entity_name=receiver['graph_name'], 
                        entity_trace=trace_id,
                        entity_label=receiver['graph_attr']['entity_label'], 
                        entity_type='field', 
                        entity_pack=receiver['graph']
                    )
                    session.add_all([attribute_entry])
                    session.commit()

                    control_id:uuid.UUID=attribute_entry.entity_sfid.urn.split(':')[2]
                    attr_trace = Document.Entity.Trace(
                        trace_index=None, 
                        entity_key=receiver['graph']['graph_key'], 
                        entity_trace=control_id,
                        entity_event=transact.lower()
                    )
                    session.add_all([attr_trace])
                    session.commit()

                    result = {
                        'attr_id': attr_number,
                        'event_logged': receiver, 
                        'entity_sfid': control_id,
                        'entity_label': attribute_entry.entity_label,
                        'entity_name': attribute_entry.entity_name,
                    }
                    session.flush()
                    session.close()
                return result 

