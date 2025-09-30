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
            

