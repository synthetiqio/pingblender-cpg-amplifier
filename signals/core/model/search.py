
from enum import Enum
from typing import List, Optional
import datetime, json, uuid
from pydantic import BaseModel as PydanticBM
from dataclasses import dataclass

class BModel(PydanticBM):
    class Config:
        arbitrary_types_allowed = True

class Search:
    type : str
    scope : json 
    boundary : json

    ##these likely need to be moved to a better place.
    @dataclass
    class Type(Enum):
        SEMANTIC = "SemanticSearch"
        VECTOR = "VectorSearch"

    @dataclass
    class Boundary:
        page_total: int
        page_range : json
        page_limit : int

        @dataclass
        class Region:
            page_number : int
            polygon_cord : List[float]
        
        @dataclass
        class Span:
            offset: int
            length: int
            height: int


class Identity:
    check_id : uuid
    check_label : str
    check_type : str
    check_photo : list[float]
    check_code : str
    check_content : json
    check_issue : str
    check_authority : str

@dataclass
class KVElement:
    content: str
    regions: List[Search.Boundary.Region]

@dataclass
class Result:

    @dataclass
    class Attribute:

        @dataclass
        class KeyPair:
            key: KVElement
            value: KVElement
            confidence : float

    @dataclass
    class Title:
        text : str
        style : json
        position : str
        has_table : bool = False



    @dataclass
    class Sheet:
        name : str 
        data_columns: int
        data_type: str
        data_label : str
        data_form: bool
        score : float

        @dataclass
        class Row:
            type : str
            label : str
            value : str
            index : int
            final : int
            col_index : int = None
            col_span : int = None

        @dataclass
        class Cell:
            type : str
            value : str
            index : int
            span : int
            row_index : int
            row_span : int

    @dataclass
    class Table:
        text : str 
        pagenumber : str
        sort: int
        score : float

        class Cell:
            type : str
            value : str
            index : int
            span : int
            row_index : int
            row_span : int

class Vectors(BModel):
    sfids : list[str]
    type : Search.Type
    input_term : str
    limit_rows : int
    incl_tab : bool
    embed_model : str


class Results(BModel):
    results : List = None
    tables : List[Result.Table] = None
    sheets : List[Result.Sheet] = None
    rows : List[Result.Sheet.Row] = None
    titles : List[Result.Title] = None
    attributes : List[Result.Attribute] = None
    identities : List[Identity] = None

    class Table:
        text : str 
        pagenumber : str
        sort: int
        score : float