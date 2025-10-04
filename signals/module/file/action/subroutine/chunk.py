import datetime 
from core.model.document import (
    Chunk, 
    Collection,
    CustomChunk,
    Document,
    CustomTable,
    CustomTableCell, 
)

class ModelService:

    meta_service='' #repl subscription interface.

    def __init__(
            self,
    ):
        return 
    
    def get_extrap_doc(
            self,
            file_name, 
            file_contents,
            file_tables, 
            split_file, 
            embed_model_label
    ):
        result:Document=Document.Custom(
            doc_id=None, 
            doc_title=file_name,
            doc_pages=len(file_contents),
            doc_tables=len(file_tables), 
            doc_type=None, 
            doc_created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            doc_model=embed_model_label.value, 
            doc_meta={},
            doc_chunks=len(split_file),
            doc_attribute=None,
        )
        return result 
    
    

