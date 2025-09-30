import uuid, datetime, json, base64
from typing import Dict, List, Any
from enum import Enum
from sqlalchemy import (
    create_engine, 
    Index, 
    select, 
    text, 
    types, Integer, String, DateTime, UUID as StoreID, Float, ARRAY
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    DeclarativeBase, 
    Mapped, 
    MappedAsDataclass, 
    mapped_column, sessionmaker
)

from module.pgvector.config import ORM
from core.config import Env, System as CoreSys

class Control(MappedAsDataclass, DeclarativeBase):
    pass

class System(CoreSys):

    def __init__(
            self, 
            timezone:str = None,
    ):
        if timezone:
            self.region = timezone

    def getTimeStamp(self):
        return CoreSys.Timestamp.getTimeStampeLocal(tmz=self.region)
    
    def getRegionEnv(self):
        self.reqhion = CoreSys.SYS.getRegionalEnv()
        return self.region
    
class Process:

    class Entity:


        from sqlalchemy import event
        from sqlalchemy.sql import column
        from sqlalchemy.orm import Session

        class Origin:


            def __init__(
                    self, 
                    package: Dict[List, Any]
                ):
                self.package = package 

        
            class Entry(Env.HasTimestamp, Control):
                __tablename__ = 'process_control'

                entity_sfid: Mapped[uuid.UUID] = mapped_column(
                    types.Uuid, 
                    primary_key=True, 
                    init=False, 
                    server_default=text("gen_random_uuid()")
                )

                entity_name: Mapped[String] = mapped_column(
                    types.String, 
                    nullable=True
                )

                entity_type: Mapped[String] = mapped_column(
                    types.String, 
                    nullable=False
                )

                entity_label: Mapped[String] = mapped_column(
                    types.String, 
                    nullable=True
                )

                entity_trace: Mapped[StoreID] = mapped_column(
                    types.Uuid, 
                    nullable=True
                )

                entity_pack: Mapped[JSONB] = mapped_column(
                    types.JSONB, 
                    nullable=True
                )


            class Trace(Env.HasTimestamp, Env.HasTrace, Control):
                __tablename__='process_trace'

                trace_index: Mapped[Integer] =  mapped_column(
                    types.Integer, 
                    autoincrement=True, 
                    nullable=False, 
                    primary_key=True
                )

                entity_key: Mapped[String] = mapped_column(
                    String(1024), 
                    nullable=False
                )
                
                entity_trace: Mapped[StoreID] = mapped_column(
                    types.Uuid, 
                    nullable=False, 
                    server_default=text("gen_random_uuid()")
                )

                entity_event: Mapped[String] = mapped_column(
                    types.String, 
                    nullable=False
                )


class Transact:


    connect = ORM.getConnectionString()
    engine= create_engine(connect)
    Session = sessionmaker(bind=engine)
    session = Session()


    def makeChecksum(
            inputs: Dict[List, Any]
    )->str:
        code: str = ''
        try: 
            for item in inputs:
                code += str(inputs[item])
            checksum: str = code
            checksum_bytes = checksum.encode("ascii")
            checksum = base64.b64encode(checksum_bytes)
        except UnicodeDecodeError as e:
            checksum = e
        return checksum
    
    def validate(checksum)->bool:
        from sqlalchemy import select 
        getcheck: str = checksum 
        session = Transact.Session()
        stt = select(Process.Entity.Trace.entity_key.like(getcheck))
        result = session.execute(stt)
        session.commit()
        response = result.fetchone()._asdict()
        return True
    

    def router(
            transact: str, 
            payload: Dict[List, Any]
            )->Dict[List, Any]:
        
        match str(transact).upper():

            case 'CREATE': 
                Control.metadata.create_all(Transact.engine)
                with Transact.Session() as session:
                    receiver: Dict[List, Any] = payload
                    open = Process.Entity.Entry(
                        entity_name=payload,
                        entity_trace=payload, 
                        entity_label=payload,
                        entity_type=payload, 
                        entity_pack=payload, 
                    )
                    session.add_all([open])
                    session.commit()
                    controlId: uuid.UUID = open.entity_sfid.urn.split(':')[2]
                    note = Process.Entity.Trace(
                        trace_index=None, 
                        entity_key=payload, 
                        entity_trace=controlId,
                        entity_event=transact.lower()
                    )
                    session.add_all([note])
                    label = open.entity_label
                    session.commit()
                    checkhash: str = note.entity_key
                    result = {
                        'event_logged': payload['event'], 
                        'event_sfid' : controlId,
                        'entity_label': label, 
                        #'trace_hash' : tracer.items()
                    }
                    session.flush()
                    session.close()
                return result
            

            case 'DETAILS':
                Control.metadata.create_all(Transact.engine)
                from module.pretzl.etl import PACK
                result: Dict[List, Any] = {}
                with Transact.Session() as session:
                    receiver: Dict[List, Any] = payload
                    try: 
                        pass
                    except:
                        pass
                return result
            
            case 'STATUS':
                Control.metadata.create_all(Transact.engine)
                from module.pretzl.etl import PACK
                result: Dict[List, Any] = {}
                with Transact.Session() as session:
                    receiver: Dict[List, Any] = payload
                    try: 
                        pass
                    except:
                        pass
                return result
            
            