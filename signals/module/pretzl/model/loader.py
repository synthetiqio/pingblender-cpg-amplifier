from pydantic import BaseModel
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import (
    PyPDFLoader, 
    DirectoryLoader, 
    CSVLoader, 
    Docx2txtLoader, 
    TextLoader, 
    UnstructuredExcelLoader,
    UnstructuredHTMLLoader, 
    UnstructuredPowerPointLoader, 
    UnstructuredMarkdownLoader, 
    JSONLoader
)

class Type(BaseModel):
    pass

    mappings = {
        '*.txt' : TextLoader,
        '*.pdf' : PyPDFLoader, 
        '*.csv' : CSVLoader, 
        '*.docx' : Docx2txtLoader, 
        '*.xlss' : UnstructuredExcelLoader, 
        '*.xlsx' : UnstructuredExcelLoader, 
        '*.html' : UnstructuredHTMLLoader, 
        '*.pptx' : UnstructuredPowerPointLoader, 
        '*.ppt' : UnstructuredPowerPointLoader, 
        '*.md' : UnstructuredMarkdownLoader, 
        '*.json' : JSONLoader
                }