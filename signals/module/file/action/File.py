import os
from uuid import uuid4
from fastapi import UploadFile, File, Depends
from typing import Dict, List, Any, Optional
from core.model.document import Construct
from module.pretzl.parser import PRETZL as ParseControl
from langchain.docstore.document import Document


class Manage:

    class Source:

        def __init__(
                self,
                target:uuid4=None, 
                list:list[uuid4,uuid4]=None
        ):
            self.sources_in=list 
            self.sources_map=target 

        def getAffiliate(
                self
        ):
            pass 

class Load:



    def __init__(
            self, 
            file: UploadFile = File(...), 
            route : Dict[list, Any] = None, 
            config : Construct = Depends(Construct)
        ):
        
        self.file = file
        self.config = config
        self.route = route 


    async def byRoute(
            
            self, 
            file: UploadFile,
            route : Dict[list, Any] = None, 
            config : Construct = Depends(Construct)
        ):
        from core.config import Env as E
        
        self.route = route
        self.file = file
        self.config = config
        self.sep = E.Dock.FS.value

        parser = ParseControl(
            file, 
            check=self.route['dataformat'], 
            construct=config
        )

        self.store = await parser.setStorePath(path="PRETZL")
        file_route = route
        reader = file_route['datareader']
        filepath:str=str(os.getcwd()+self.sep+self.file.filename)
        if reader == 'AFR':
            storefile = await parser.loadPathAssets(file)
        elif reader == 'Mimeograph':
            storefile = await parser.loadPathAssets(file)
        elif reader == 'EDI':
            storefile = await parser.loadPathAssets(file)
            await parser.push_edi_embeddings(path=filepath)
        elif reader == 'DocIntel':
            storefile = await parser.loadPathAssets(file)
        elif reader == 'TextLoader':
            storefile = await parser.loadPathAssets(file)
            await parser.get_columns(path=filepath)
        elif reader == 'PRETZL':
            storefile  = await parser.loadPathAssets(file)
        else:
            storefile  = await parser.loadPathAssets(file)

        response : Dict[List, Any] = await self.listQueue(
            self, 
            filename=self.file.filename, 
            path=self.store, 
            check=file_route['dataformat'], 
            config=config
        )
        result : Dict[List, Any] = {}
        result.update({
            'action_event' : [filepath]
            }
        )
        return result
    

    async def byRouteBlob(
            self, 
            file:UploadFile, 
            route:Dict[list, Any]=None, 
            config:Construct=Depends(Construct)
    ):
        from core.config import Env as E 
        self.route = route 
        self.file=file 
        self.config=config 
        self.sep=E.Dock.FS.value 

        parser=ParseControl(
            file, 
            check=self.route['dataformat'], 
            construct=config 
        )
        from module.azure.wasb.client import Azure
        from module.azure.wasb.control import BlobController
        await Azure.Storing(
            file=self.file
            ).UploadFile()
        router = await BlobController(
            filename=self.file.filename
            ).get()
        print(router)
        self.store = await parser.setStorePath(path="PRETZL")
        file_route=route 
        reader=file_route['datareader']
        filepath:str= str(f'{os.getcwd()}{self.sep}{self.file.filename}')
        if reader == 'AFR':
            storefile= await parser.loadPathAssets(file)
        elif reader == 'Mimeograph':
            storefile = await parser.loadPathAssets(file)
        elif reader == 'EDI':
            storefile = await parser.loadPathAssets(file)
        elif reader == 'DocIntel':
            storefile= await parser.loadPathAssets(file)
        elif reader == "TextLoader":
            storefile= await parser.loadPathAssets(file)
            if file_route['dataformat'] in [
                'CSV_TEXT',
                'EXCEL_10',
                'EXCEL_9',
                'TAB_TEXT'
                ]:
                columns:Dict= await parser.getColumns(path=filepath)
            else:
                pass ##load this up with modular conditionals.
        elif reader == "PRETZL":
            file_results = await parser.loadPathAssets(file)
        else:
            file_results = await parser.loadPathAssets(file)
        response:Dict[List,Any]= await self.listQueue(
            self, 
            filename=self.file.filename,
            path=self.store, 
            check=file_route['dataformat'], 
            config=config  
        )
        result={}
        result.update({
            'action_event': response
        })
        return result 
            



    async def getCollectedAssets(
            self
        ):
        
        f = self.file.filename.split('.')[0]
        route = self.store
        os.chdir(route)
        parser = ParseControl(
            file=None, 
            check=None, 
            construct=None
        )
        result : Dict[list] = await parser.getFilesList(filter=f)
        return result
    

    async def computePath(
            self, 
            filename : str = None, 
            fileid : uuid4 = None
        ):
        path : str = ''
        localfile = f'{self.store}{filename}'
        return path
    

    async def convertPathToDocument(
            self, 
            filepath:str=None, 
    )->list[Document]:
        import pandas as pd 
        contents =open(file=self.computePath())
        doc:Document= Document(
            page_content=contents, 
            metadata={'source': 1}
        )
        docs:List[Document]=[]
        docs.append(doc)
        return docs 
    

    async def convertFileToDocument(
            file:UploadFile
    )->list[Document]:
        contents= await file.read(size=file.size)
        doc: Document= Document(
            page_content=contents,
            metadata={'source': 1}
        )
        docs:List[Document]=[]
        docs.append(doc)
        return docs 
    

    async def DocumentXlsColumns(
            self, 
            path
    )->dict:
        from module.pretzl.reader.standard_xls import Xls 
        docbits= Xls().DataColumns(path=path).frame_to_dict()
        return docbits 
    

    async def DocumentParsePDF(
            self
    )->Dict[List,Any]:
        from module.pretzl.reader.standard_pdf import Pdf as Read 
        doctabs= Read().Tables.frame_to_dict()
        content= Read().Content.get_docuemnt_content()
        docimg= Read().Images.get_document_images()
        response={
            'document_pages': content, 
            'document_tables': doctabs, 
            'document_images': docimg
        }
        return response 
    

    async def DocumentGetColumns(
            self, 
            path
     ):
        from module.pretzl.reader.standard_csv import Csv 
        hurl = self._getLocalPath(path=path)
        docbits=Csv().DataColumns(path=hurl).frame_to_dict()
        return docbits 
    

    async def DocumentParseXLS(
        self, 
        path
    ):
        from module.pretzl.reader.standard_xls import GetDocuments as XL
        docbits= XL(fileurl=self._getLocalPath(path))
        response:List[Document]=docbits.firstState()
        return response 

    
    async def DocumentParseCSV(
            self, 
            path
        )->List[Document]:
        from module.pretzl.reader.standard_csv import GetDocuments
        docbits = GetDocuments(fileurl=path)
        response : List[Document] = docbits.firstState()
        return response

    
    def _getLocalPath(
            self, 
            path
    )->str:
        blob_url=path 
        file=blob_url.split('/PRETZL')[1]
        path=file.split('?')[0]
        pup=str(os.getcwd())
        return f'{pup}/PRETZL{path}'
    

    def _getBlobPath(
            self, 
            path
    )->str:
        blob_url=path 
        blob=blob_url.split('?')[0]
        name=blob.spliit('data-in/')[1]
        path=f'data-in/{name}'
        return path 
    

    async def BlobCSV(
            self, 
            blobpath
    )->List[Document]:
        path=self._getBlobPath(blobpath)
        from module.pretzl.reader.azure.storage.wasb import GetDocuments 
        docbits = GetDocuments(blob_name=path)
        response:List[Document]= await docbits.firstState()
        return response 
    

    async def BlobData(
            self, 
            blobpath
    ):
        path= self._getBlobPath(blobpath)
        from module.pretzl.reader.azure.storage.wasb import GetDocuments 
        docbits = await GetDocuments(blob_name=path).getFirstFrame()
        return docbits 
    

    async def listQueue(
            self, 
            file : UploadFile = None, 
            filter : str = None, 
            check : str = None, 
            path : str = None, 
            filename : str = None, 
            config : Optional[Construct] = None
    )->Dict[list,Any]:
        catch = locals()
        if filename != None:
            body = None
            filter = filename.split('.')[0]
            parser = ParseControl(
                file=body, 
                check=check, 
                construct=config
            )
            result : Dict[List, Any] = await parser.getFilesList(file=filter)

        if file != None:
            body = catch['file']
            filter = file.filename.split('.')[1]
            parser = ParseControl(
                file=body, 
                check=check, 
                construct=config
            )
            result : Dict[List, Any] = await parser.getFilesList(filter=filter)
        return result