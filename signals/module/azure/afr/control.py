from typing import List, Any, Dict 
from azure.ai.formrecognizer import AnalyzeResult
import random, json, string 
from core.model.document import CustomTable, Construct
from fastapi import UploadFile
from module.robot.action.chat import LLMService
from module.azure.afr.model.service import ModelService 
from module.azure.afr.helper import AFRService

from langchain_community.document_loaders import (
    TextLoader, 
    JSONLoader, 
    PyPDFLoader
)
from langchain.chains.llm import LLMChain
from langchain.schema import HumanMessage, SystemMessage
from langchain.docstore.document import Document 
#TODO: STOPPED HERE 1/17
from langchain.prompts.chat import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()
llm = LLMService()

class Utils:

    def convert_to_dict(obj):
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        else:
            return obj
        
    def random_string(length=4):
        return "".join(random.choices(string.ascii_letters+string.digits, k=length))
    

class AFR:

    def __init__(
            self,
            file:UploadFile, 
            meta:Dict[List,Any]
    ):
        self.file = file 
        self.meta:Dict[List,Any]=meta 

    async def loadFile(
            file:UploadFile,
            meta:Construct=Construct 
    ):
        local_service:AFRService=AFRService()
        model_service:ModelService=ModelService()
        temp:AnalyzeResult=await local_service.ParseDocument(
            construct=meta,
            file=file 
            )
        pages:List[Document]=[]
        for page in temp.pages:
            page_content=''
            for line in page.lines:
                page_content+=line.content+"\n"
            key_value_pairs=json.dumps(key_value_pairs, default=Utils.convert_to_dict)
            doc:Document=Document(
                page_content=page_content, 
                page_number=page.page_number, 
                metadata={
                    'width': page.width, 
                    "height":page.height, 
                    "angle":page.angle, 
                    "formulas": page.formulas, 
                    "page_number":page.page_number
                }
            )
            pages.append(doc)
        tables:List[CustomTable]=[]
        for table in temp.tables:
            table_cells= model_service.GetCustomTableCell(cells=table.cells)
            custom_table:CustomTable= model_service.getCustomTable(table, table_cells)
            tables.append(custom_table)
        file_contents={
            "pages":pages, 
            "tables":tables, 
            "key_value_pairs":json.loads(key_value_pairs)
        }
        return file_contents
    

async def FileToDocument(
        file:UploadFile
)->list[Document]:
    file_contents= await file.read()
    doc:Document=Document(page_content=file_contents, metadata={'source':1})
    docs:List[Document]=[]
    docs.append(doc)
    return docs


def loadFileFromPath(
        file_path:str
):
    file_extensions=file_path.split(".")[-1].lower()
    if file_extensions in ["txt", 'md']:
        loader=TextLoader(file_path)
    elif file_extensions== "pdf":
        loader=PyPDFLoader(file_path)
    elif file_extensions=="json":
        loader=JSONLoader(
            file_path=file_path, 
            jq_scema=".[]",
            text_content=False,
        )
    else:
        raise ValueError({f"Unsupported file type: {file_extensions} "})
    return loader.load()

async def LoadFile(file:UploadFile):
    file_ext=file.filename.split(".")[-1].lower()
    print('FILE EXTENSION: ', file_ext)
    if file_ext == '.pdf':
        contents = await file.read()
        return contents
    else:
        return FileToDocument(file)
    
async def LoadAfrFile(
        file:AFRService,
        construct:Construct
)->List[Document]:
    afr_service:AFRService=AFRService()
    model_service:ModelService=ModelService()
    temp:AnalyzeResult= await afr_service.ParseDocument(construct, file)
    pages:List[Document]=[]
    for page in temp.pages:
        page_content=''
        for line in page.lines:
            page_content+=line.content+"\n"
        kvp=json.dumps(temp.key_value_pairs, default=Utils.convert_to_dict)
        doc:Document = Document(
            page_content=page_content, 
            page_number=page.page_number,
            metadata={
                'width':page.width, 
                'height':page.height,
                'angle':page.angle,
                'formulas':page.formulas, 
                'page_number':page.page_number
            },
        )
        pages.append(doc)
    tables:List[CustomTable]=[]
    for table in temp.tables:
        table_cells=model_service.getCustomTable(cells=table.cells)
        custom_table:CustomTable=model_service.getCustomTable(table, table_cells)
        tables.append(custom_table)

    file_contents={
        'pages':pages,
        'tables':tables,
        'key_value_pairs': json.loads(kvp)
    }
    return file_contents



def LLMChainResponse(
        prompt:str, 
        sys_prompt=None, 
        verbose=True,
):
    system_prompt=(
        'You are an expert at classifying and understanding pdf based forms'
    )
    messages=[
        SystemMessage(content=f"{system_prompt}"),
        HumanMessage(content=f'{prompt}')
    ]
    chain_prompt=ChatPromptTemplate.from_messages(messages=messages)
    llmchain = LLMChain(
        llm=llm,
        prompt=chain_prompt,
        verbose=verbose
    )
    return llmchain.run(prompt=chain_prompt)


