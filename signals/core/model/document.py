from enum import Enum
from typing import List, Optional
import uuid
from pydantic import BaseModel as PydanticBM
from dataclasses import dataclass
from core.model.embed import EmbedBase as EmbedModel
import core.model.search as Query

class BModel(PydanticBM):
    class Config:
        arbitrary_types_allowed = True


@dataclass 
class Boundary:
    page_number:int 
    polygon:List[float]

@dataclass
class KeyValueElement:
    content:str 
    bounding_regions:List[Boundary]

@dataclass 
class KeyValuePair:
    key:KeyValueElement
    value:KeyValueElement
    confidence:float

class ReadStrategy(Enum):
     AFR = "AFR"
     ADI = "ADI"
     EDI = "FRM"
     SIMPLE = "Simple"
     LOCAL = "Local"

class SplitStrategy(Enum):
    ROW  = "Row"
    PAGE = "Page"
    FIXED = "Fixed"
    RECURSIVE_AFR = "RecursiveAFR"
    RECURSIVE_LANGCHAIN = "RecursiveLangchain"
    SEMANTIC = "Semantic"


class SearchType(Enum):
    SEMANTIC="SemanticSearch"
    VECTORSEARCH="VectorSearch"


class SearchConfig(BModel):
    DocumentIDs:List[str]
    SearchType:SearchType
    SearchTerm:str
    ResultLimit:int
    IncludeTables:bool 
    embed_model:str 


class Construct(BModel):
    split_strategy : Optional[SplitStrategy] = SplitStrategy.PAGE.value
    embed_model : Optional[EmbedModel] = EmbedModel
    collection_name : Optional[str] = "default"
    chunk_size : Optional[int] = 1000
    chunk_overlap: Optional[int] = 0
    generate_metadata: Optional[bool] = False
    read_strategy : Optional[ReadStrategy] = ReadStrategy.SIMPLE.value


###################################################################
############  CHUNKING INTERFACES FOR VARIABLE INPUTS #############
###################################################################

class Collection:

    @dataclass
    class Metadata:
        coll_model: EmbedModel = None
        coll_chunk_split: SplitStrategy = None
        coll_document_title : str = None 
        coll_timestamp : str = None
        coll_aided_tags : str = None
        coll_pages_total : int = None

class Chunk:

    @dataclass
    class Metadata:
        meta_model : EmbedModel = None
        meta_strategy : SplitStrategy = None
        meta_chunk_number : int = None
        meta_chunk_total : int = None
        meta_aided_tags: str = None
        meta_page_number : int = None
        meta_attr_pairs: List = None



@dataclass 
class CustomChunk:
    chunk_id:str=None
    chunk_timestamp:str=None
    chunk_page_content:str=None
    chunk_embedding:List[float]=None
    chunk_metadata:Chunk.Metadata=None


@dataclass
class Cell:
    content_type : str
    cell_value : str
    col_index : int
    col_span : int 
    row_index : int
    row_span : int 

    def to_dict(self):
        return {
            'content_type' : self.content_type, 
            'cell_value' : self.cell_value, 
            'col_index' : self.col_index, 
            'col_span' : self.col_span, 
            'row_index' : self.row_index, 
            'row_span' : self.row_span
        }


class Document:

    @dataclass
    class Custom:
        doc_id : uuid = None
        doc_title : str = None
        doc_pages : int = None
        doc_tables : str = None
        doc_type : str = None
        doc_created : str = None
        doc_model : str = None
        doc_meta : str = None
        doc_chunks : int = None
        doc_attribute : List[Query.Result.Attribute.KeyPair] = None

        @dataclass
        class Table:
            tab_id : int
            tab_cells : List[Cell]
            tab_columns_num : int
            tab_row_num : int
            tab_header_index : List[int]
            tab_column_index : List[int]
            tab_page_number : int 

        @dataclass
        class Chunk:
            chunk_id : str  = None
            chunk_ts : str = None
            chunk_content : str = None
            chunk_embeds : List[float] = None
            chunk_meta : Chunk.Metadata = None
            chunk_label_id = str = None


@dataclass 
class DocumentParsingResult:
    document_out:Document.Custom
    document_chunks: List[Document.Custom.Chunk]
    document_tables: List[Document.Custom.Table]

@dataclass
class CustomTextResult:
    text_out:str
    text_page_number:str
    text_sort_order:int
    text_match_score:float


@dataclass
class CustomTable:
    cells:List[Cell]
    table_col_count:int
    table_row_count:int 
    header_row_idx:List[int]
    header_col_idx:List[int]
    page_number: int
    table_id:int=None 


@dataclass 
class CustomTableCell:
    cell_content_type:str 
    cell_content_value:str
    cell_column_index:int
    cell_column_span:int 
    cell_row_index:int 
    cell_row_span:int 

    def to_dict(
            self,
    ):
        return {
            'cell_content_type': self.cell_content_type,
            'cell_content_value': self.cell_content_value,
            'cell_column_index': self.cell_column_index,
            'cell_column_span': self.cell_column_span,
            'cell_row_index': self.cell_row_index,
            'cell_row_span': self.cell_row_span
        }


@dataclass
class Span:
    offset:int 
    length:int 

@dataclass
class TextResult:
    text:str
    page:int
    sort:int
    scope:float 

@dataclass
class ParseResult:
    result_document : Document.Custom
    result_chunks : List[Document.Custom.Chunk]
    result_tables : List[Document.Custom.Table]


class DocumentSearchResult(BModel):
    search_results:List[CustomTextResult]=None 
    search_tables:List[CustomTable]=None
    search_keyvals:List[KeyValuePair]=None 


class Stores(Enum):
    HEADER = "langchain_pg_collection"
    CHUNKS = "langchain_pg_embedding"
    TABLES = "extracted_tables"
    ATTRS = "extracted_attributes"
    

    



    

