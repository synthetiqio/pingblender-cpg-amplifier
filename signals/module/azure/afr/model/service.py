from core.model.document import (
    Chunk, 
    CustomTable,
    CustomTableCell,
    CustomChunk,
    Collection,
    Document, 
    Cell,
    Construct
)
from module.robot.expert.agent.proc.meta import MetadataService
from core.control import Config
from typing import Any 

class ModelService:

    meta_service: MetadataService=MetadataService()

    def __init__(
            self,
    ):
        return 
    
    def GetCustomDocument(
            self,
            filename:str,
            file_contents:Any, 
            file_tables, 
            split_file, 
            embed_model_select
    ):
        return Document.Custom(
            doc_id=None, 
            doc_title=filename, 
            doc_pages=len(file_contents),
            doc_tables=len(file_tables),
            doc_type=None,
            doc_created=Config.Timestamp.getTimestampLocal(), 
            doc_model=embed_model_select.value,
            doc_meta={},
            doc_chunks=len(split_file),
            doc_attribute=None
        )


    def GetDocumentMetaData(
            self, 
            document: Document.Custom,
            construct: Construct, 
            split_file
    ):
       return Collection.Metadata (
           coll_model=document.doc_model,
           coll_pages_total=document.doc_pages,
           coll_document_title=document.doc_title,
           coll_timestamp=document.doc_created,
           coll_chunk_split=construct.split_strategy.value, 
           coll_aided_tags=(
               self.meta_service.GenerateMetadataForDocument(documents=split_file)
               if construct.generate_metadata== True
               else None 
           ),   
       )


    def GetChunkMetadata(
            self,
            index, 
            split, 
            construct:Construct, 
            document:Document.Custom
    ):
        ai_tags=self.meta_service.GetMetadataForPage(split)
        chunk_metadata = Chunk.Metadata(
            meta_model= construct.embed_model.value, 
            meta_strategy=construct.split_strategy.value,
            meta_chunk_number=index+1,
            meta_chunk_total=document.doc_chunks,
            meta_aided_tags=ai_tags
        )
        return chunk_metadata
    
    def GetCustomChunk(
            self,
            page_content, 
            chunk_embedding, 
            chunk_metadata
    ):
        return CustomChunk(
            chunk_id=None,
            chunk_timestamp=Config.Timestamp.getTimestampLocal(),
            chunk_page_content=page_content, 
            chunk_metadata=chunk_metadata,
            chunk_embedding=chunk_embedding,

        )
    

    def GetCustomTableCell(
            self, 
            cells,
    ):
        table_cells=[]
        for cell in cells:
            custom_cell:CustomTableCell = CustomTableCell(
                    cell_content_type=cell.kind,
                    cell_content_value=cell.content, 
                    cell_column_index=cell.column_index,
                    cell_column_span=cell.column_span, 
                    cell_row_index=cell.row_index, 
                    cell_row_span=cell.row_span,
            )
            table_cells.append(custom_cell)
        return table_cells
        
        
    def getCustomTable(
            self, 
            table, 
            table_cells,
    ):
        return CustomTable(
            table_cells=table_cells, 
            table_col_count=table.column_count,
            table_row_count=table.row_count, 
            header_row_idx=[],
            header_col_idx=[], 
            page_number=table.bounding_regions[0].page_number,
        )