from __future__ import annotations 
from functools import cached_property

from .conduit import CollectTransact, CollectResult
from .table import VectorCollectTable 
from ..config import Config 
from core.model.document import Construct

from sqlalchemy import and_, or_, select, delete, String, text 
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession
)
from sqlalchemy.orm import Mapped, mapped_column, declared_attr

class Settings:
    from enum import Enum 
    class conf(Enum):
        CFG = Config(
            doc_state='start', 
            doc_config=Construct
        )


from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, List, Optional, Type, AsyncIterator
from pgvector.sqlalchemy import Vector 
from sqlalchemy.ext.declarative import AbstractConcreteBase
from module.pgvector.model.base import Base 

class CollectionPoint(BaseModel):
    id:str 
    embedding:List[float]=[]
    metadata:Dict[str, Any]={}


class CollectionPointResult(BaseModel):
    payload:CollectionPoint
    score:float 


class CollectionTable(AbstractConcreteBase, Base):
    __abstract__=True
    id:Mapped[str]= mapped_column(
        "id", 
        String, 
        autoincrement=False, 
        nullable=False, 
        unique=True, 
        primary_key=True
    )
    
    @declared_attr
    def embedding(cls)->Mapped[List[float]]:
        return mapped_column(
            "embedding", 
            Vector(),
            nullable=False,
        )
    
    metadata:Mapped[Dict[str,Any]]=mapped_column(
        'metadata', 
        JSONB,
        server_default=text("'{}'::jsonb"), 
        nullable=False
    )


    @classmethod
    async def readAll(
        cls, 
        session:AsyncSession, 
        include_medatdata:bool, 
    ):
        stmt=select(cls)
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row 

    @classmethod
    async def readByID(
        cls,
        session:AsyncSession,
        point_id:str,
        include_metadata:bool=False,
    ):
        stmt=select(cls).where(cls.id==point_id)
        return await session.scalar(stmt.order_by(cls.id))
    
    @classmethod
    async def create(
        cls, 
        session:AsyncSession,
        id:str, 
        embedding:List[float], 
        metadata:Dict[str,Any]
    ):
        collection=cls(
            id=id, 
            embedding=embedding, 
            metadata=metadata
        )
        session.add(collection)
        await session.commit()
        await session.flush()

    
    @classmethod
    async def update(
        cls, 
        session:AsyncSession, 
        id:str,
        embedding:List[float],
        metadata:Dict[str,Any]
    ): 
        stmt=select(cls).where(cls.id==id)
        result= await session.execute(stmt)
        collection = result.scalar_one_or_none()
        if collection:
            collection.embedding = embedding 
            collection.metadata = metadata 
            await session.commit()

    @classmethod
    async def delete(
        cls, 
        session:AsyncSession,
        id:str
    ):
        stmt=delete(cls).where(cls.id == id)
        await session.execute(stmt)
        await session.commit()



class VectorCollect(BaseModel):

    name:str 
    dimensions:int 
    sessionmaker: async_sessionmaker[AsyncSession]=Field(..., exclude=True)
    doc_config=ConfigDict(arbitrary_types_allowed=True)


    async def getSettings(
            self, 
            result:Dict[list, Any]=None
    ):
        self.doc_config
        self.result=result

        def __init__(
                self, 
                doc_state:str='modified', 
                doc_config:Construct=Config.variable
        )->Dict:
            self=self 
            new_state=doc_state
            new_config=doc_config
            doc_config = Config.Custom 

            o=Config(
                doc_state="check", 
                doc_config=doc_config
            )
            o.evaluate(new_state, new_config)
            o.current_state
            result=o
            super().__init__(result=result)
            return result 
        

    async def _buildFilters(
            self, 
            column:Mapped[Dict[str,Any]], 
            filters:Dict[str, Any]
    ):
        k, v=list(filters.items())[-1]
        if k == '$and':
            return and_(
                *[self._buildFilters(
                    column, 
                    filter
                ) for filter in v]
            )
        elif k == '$or':
            return or_(*[
                self._buildFilters(
                    column, 
                    filter
                ) for filter in v
            ])



    def buildTable(
            self
    )->Type[VectorCollectTable]:
        class AbstractTable(VectorCollectTable):
            __tablename__=self.name
            __dimensions__=self.dimensions
            __mapper_args__={
                'polymorphic_identity':self.name, 
                "concrete":True
            }
            __table_args__={
                'extend_existing':True 
            }
            try:
                def embedding(cls)->Mapped[List[float]]:
                    return mapped_column(
                        'embedding', 
                        Vector(self.dimensions), 
                        nullable=False 
                    )
            except:
                raise Exception 
        return AbstractTable


    async def create(self)->None:
        pass 


    def keyCheck(error):
        return 'Duplicate Key' in error

    def table(self)->Type[VectorCollectTable]:
        return self.buildTable()
    


    async def readById(
            self, 
            cls, 
            session:AsyncSession, 
            pointer:str, 
            include_metadata:bool=False
    ):
        sel = select(cls).where(cls.id == pointer)
        return await session.scalar(sel.order_by(cls.id))
    


    async def get(
            self, 
            id:str, 
    )->CollectTransact:
        async with self.sessionmaker() as session:
            result = await self.table.readById(session=session, pointer=id)
            if result is None:
                raise ("Collection not found")
            return CollectTransact(
                id=result.id,
                embedding=result.embedding, 
                metadata=result.metadatas
            )
        
    async def query(
            self, 
            query:List[float],
            limit:int=10,
            filter:Optional[Dict[str,Any]]=None,
    )->List[CollectResult]:
        if self.table is None:
            return []
        q=select(self.table).order_by(self.table.embedding.cosine_distance(q))
        q=q.column(1-self.table.embedding.cosine_distance(q)).label('cosine_similarity')
        if filter is not None:
            filter_exp= self._buildFilters(
                self.table.metadatas, 
                filter
            )
            q=q.filter(filter_exp)
        q=q.limit(limit)
        async with self.sessionmaker() as session:
            query_execution= await session.execute(q)
            results = query_execution.all()
        return [
            CollectResult(
                payload=CollectTransact(
                    id=result[0].id, 
                    embedding=result[0].embedding,
                    metadata=result[0].metadatas
                ), 
                score=result[1],
            ) for result in results
        ]
    
    async def insert(
            self, 
            id:str, 
            embedding:List[float], 
            metadata:Dict[str, Any]={}
    )->None:
        async with self.sessionmaker() as session:
            await self.table.create(
                session=session,
                id=id, 
                embedding=embedding, 
                metadata=metadata
            )

    async def update(
            self, 
            id:str, 
            embedding:List[float],
            metadata:Dict[str,Any]={}
    )->None:
        async with self.sessionmaker() as session:
            await self.table.update(
                session=session,
                id=id, 
                embedding=embedding, 
                metadata=metadata
            )

    async def upsert(
            self, 
            id:str,
            embedding:List[float],
            metadata:Dict[str,Any]={}
    )->None:
        try:
            await self.insert(
                id, 
                embedding,
                metadata
            )
        except Exception as err:
            if self.keyCheck(err.args[0]):
                await self.update(
                    id, 
                    embedding, 
                    metadata 
                )
            else:
                raise err 