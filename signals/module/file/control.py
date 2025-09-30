import os
from io import BytesIO
from typing import List, Dict, Any
from fastapi import UploadFile, Depends
from sqlalchemy import text, types
from module.pretzl.parser import Read as ReaderService
from module.file.action.File import Load as Store
from module.azure.adi.service.command import DocumentCommand as DocAction
import uuid
from module.file.service.command import (
    FileCommand as FileAction, 
    MatrixCommand as MatrixAction
)
from core.model.document import Construct, DocumentConfig

class Analyze:

    def __init__(
            self, 
            filepath : str
        ):
        self.fileurl = filepath
        from module.file.action.File import Load
        accessdata = Load().DocumentParseCSV(path=self.fileurl)
        return accessdata
    

class Collect:

    def __init__(
            self, 
            metadata
        ):
        self.instruct = metadata 
        self.params = locals()
        self.collection : Dict[List, Any] = {}

    def getFilesList(
            self
        ):
        from module.pgvector.control import Collection as ColCon
        helper = ColCon.Entity.Query(lookup_key=self.instruct)
        result = helper.getFileList(metadata=self.instruct)
        self.collection = result 
        return result


class File:

    class MetadataController:

        def __init__(
                self, 
                meta : Dict[List, Any]
            ):
            #self.e EventController()
            self.startmet : Dict[List, Any] = meta
            self.toplevel : list = ['request', 'keys', 'region', 'input', 'command', 'control']
            self.cleanmet : Dict[List, Any] = {}

        #checked 01222025
        def govern(self):
            for key,value in enumerate(self.startmet):
                if key not in self.toplevel:
                    self.startmet.pop(key)
                self.cleanmet.update({key : value})
            return self.cleanmet



        def cleanDetails(self):
            keypops = ["FileAction", "meta", "file", "files", "runner"]
            for item in keypops:
                if item not in self.startmet['inputs']:
                    self.cleanmet = self.startmet
                else:
                    del self.startmet['inputs'][item]
                    self.cleanmet = self.startmet
            return self.cleanmet
        
            
        def deleteKey(
                self, 
                evals:Dict[List, Any], 
                delkey:str
            ):
            if delkey in evals:
                del delkey
                result = evals
                return result
            else: 
                return evals
            
        def cleanKeys(
                self
            ):
            keypops = ["FileAction", "meta", "file", "files"]
            for item in keypops:
                if item not in self.startmet['inputs']:
                    self.cleanmet = self.startmet
                else:
                    del self.startmet['inputs'][item]
                    self.cleanmet = self.startmet
            return self.cleanmet
        

    class ResponseModel():

        def _init__(
                self, 
                command:str, 
                metadata:Dict[List, Any]
        ):
            #self.e=EventController()
            self.result:Dict[List, Any]= {}
            self.metadata= metadata 
            self.interpreter= metadata['request']
            if metadata['export']:
                self.dataformat= metadata['export']
            self.command= command 


        def runInterpreter(
                self, 
                result
        ):
            meta= self.metadata
            data= result 
            try:
                print('Running Interpreter')
            except:
                print('Something Bad')
            return True
        

        def result (
                self
        ):
            response = self.result
            return response
        

    def __init__(
            self, 
            file:UploadFile, 
            fn:str, 
            construct:Construct= Depends(Construct)
        ):

        #self.e = EventController()
        self.file_content= file
        self.file_name= fn
        self.init_config= construct
        self.file_type= file.content_type
        self.rootdir= os.getcwd()
        self.label= None

    def objectTest(self)->Dict[List, Any]:
        filename : str = self.file_name
        response : Dict[List, Any] = {
            'response' : 'SUCCESS',
            'filename' : filename
        }
        return response 
    

    def setFileLabel(
            self, 
            label:str
        ):
        self.label:str = label
        return self.label
    

    def getFileLabel(
            self,
        ):
        if self.label != None:
            return self.label
        else:
            return self.file_name.split('.')[0]
        

    async def sendToAzureStorage(
            self, 
            file:UploadFile= None, 
            stream:BytesIO= None,
            path:str= None
        ):
        from module.azure.wasb.client import Azure 
        from module.azure.wasb.config import WASB
        from module.azure.wasb.control import BlobController as bc 
        result:Dict[List,Any]={}
        env:Dict[List, Any]= WASB.Default.getEnvVariables()
        if file !=None:
            print("the conditions were met")
            store=Azure().Storing(file=file)
            result= await store.UploadFile()
        return result

    async def fileUpload(
            self
        )->Dict[list, Any]:
        print("[FILE] - Starting file upload for local utility.")
        rs= ReaderService(
            self.file_content,
            self.file_name, 
            self.init_config
        )
        print("[FILE] - Reading instructions for placement.")
        result = await Store.byRoute(
            Store,
            file=self.file_content,
            route=rs.getFileReader(),
            config=self.init_config
        )
        print("[FILE] - File upload action is completed.")
        os.chdir(rs.getOGWorkingDirectory())
        output : str = os.getcwd()
        x : Dict[List, Any] = {'result' : result}
        x.update({'file_trace' : self.init_config})
        x.update({'file_label' : self.getFileLabel()})
        x.update({'reader_set' : rs.getFileReader()})
        #x.update({'columns':rs.getDataColumns()})
        x.update({'reset_dir' : output})
        #x.update({"columns":})
        return x
    
    async def parity(
            self,
    ):
        print("[FILE]: FileUpload - Start")
        self.rs = ReaderService(
            self.file_content, 
            self.file_name,
            self.init_config
        )
        await Store.byRoute(
            Store, 
            file=self.file_content, 
            route=self.rs.getFileReader(),
            config=self.init_config
        )
        return self.file_content
    

    async def blobUpload(
            self,
    ):
        rs = ReaderService(
            file=self.file_content, 
            fn=self.file_name,
            construct=self.init_config
        )
        zed:Dict[List,Any]={}
        from module.azure.wasb.control import BlobController
        result:Dict[List,Any]= await self.sendToAzureStorage(
            file=self.file_content
        )
        print(result)
        b=BlobController(filename=self.file_name)
        c:str= await b.get()
        urls=[c]
        out={
            'action_event':urls
        }
        bn=c.split("/PRETZL/")[1]
        bz=bn.split("?")[0]
        pos=os.getcwd()+f'/PRETZL/{bz}'
        blobname=f'data-in/PRETZL/{bz}'
        zed.update({
            'result':out, 
            'blob':blobname,
            'file_trace': self.init_config,
            'file_label': self.getFileLabel(),
            'reader_set': rs.getFileReader() 
        })
        return zed

    
    async def Blobstore(self):
        from module.azure.wasb.control import BlobController
        rs=ReaderService(
            file=self.file_content, 
            fn=self.file_name,
            construct=self.init_config
        )
        x:Dict[List,Any]={}
        result:Dict[List,Any]=await self.sendToAzureStorage(
            file=self.file_content
        )
        print(result)
        b=BlobController(filename=self.file_name)
        m:str=await b.get()
        urls=[m]
        out={
            'action_event':urls
        }
        bn=m.split('/PRETZL/')[1]
        bz=bn.split('?')[0]
        pos=os.getcw()+f'/PRETZL/{bz}'
        blobname=f'data-in/PRETZL/{bz}'
        x.update({
            "result": out, 
            "blob":blobname, 
            "file_trace":self.init_config(), 
            "file_label":self.getFileLabel(),
            "reader_set":rs.getFileReader()
        })
        return x

    

class Interface:
    class MetadataController:
        def __init__(
                self
            ):
            return
    class Manager:
        def __init__(
                self,
                comm:str, 
                meta:Dict[List, Any], 
                file:UploadFile= None,
                path:str= None, 
                name:str= None, 
                pack:Dict[List, Any]= None, 
                furl:str= None
            ):
            self.comm = comm 
            self.metadata = meta
            if file != None:
                self.buffer = file
            if name != None:
                self.filename = name 

        def Handler(
                self
            ):
            command : str = self.comm
            return command.upper()
        

        def getAllFilesStore(
                self
            ):
            #TODO: fix what the contractor blew up.
            action = Store()
            result = action.getDirectoryListing()
            return result 
        

        def getFilePackageUnits(
                self
            ):
            from module.file.action.File import Load
            action = Load()
            f : str = self.filename.split('.')[0]
            result = action.getCollectedAssets(filename=f)
            return result 
        

    async def service_test(
            file:UploadFile, 
            construct:Construct= Depends(Construct)
        )->Dict:
        rs= ReaderService(file, file.filename, construct)
        asset:Dict[list]= await rs.getDataPackaged(
            file, 
            file.filename, 
            construct
        )
        plan:Dict[list]
        plan={
            "headers" : [file.content_type, file.filename, file.size],
            "package" : asset,
            "chunks" : await rs.getFileContent(), 
            "labels" : await rs.getLLMLabels(), 
            "assets" : await rs.getEmbeddings()
        }
        action= await rs.buildServicePlan(plan, file)
        tracer = await rs.runPlan(action)
        return tracer
        
    
class Action:

    class MetadataController:
        def __init__(self):
            pass 


    def MetaData(
            file : UploadFile, 
            comm : str
        ):
        from module.pretzl.parser import PRETZL, Read
        a:Dict[List, Any]
        a={
            "headers" : {
                "content_type" : file.content_type, 
                "filename" : file.filename
            }
        }
        return a
    

    def runPlan(
            command : str, 
            file = UploadFile, 
            meta = Dict[List, Any]
        )->Dict[List,Any]:
        meta.update({
            'command' : str(command)
            })
        fa = FileAction(
            comm=command, 
            file=file, 
            meta=meta
        )
        response : Dict[List, Any] = fa.Action(metadata=meta)
        return response

    def runQuery(
            command:str, 
            meta:Dict[List,Any]
    )->Dict[List,Any]:
        meta.update({'command':str(command)})
        fa = FileAction(comm=command, meta=meta)
        response:Dict[List,Any]=fa.Action(metadata=meta)
        return response

#checked - added - 01222025
class Filter:
    #TODO: consolidate methods logic and naming for outcomes on search and filter

    class Search:

        def __init__(
                self, 
                unk_ids:list=None,
        ): 
            
            self.added = unk_ids 
            self.hotkeys=['Unnamed_', 'Unknown:']

        def collect(
                self,
                dictobj:dict
        ):
            result:dict={}
            for search_key in self.hotkeys:
                reqs=[{key:val} for key,val in dictobj.items() if search_key in key]
                result.update({search_key:reqs})
            return result 
        
        def filter(
                self,
                dictobj:dict
        ):
            result:dict={}
            for search_key in self.hotkeys:
                res=[{key:val} for key, val in dictobj.items() if search_key in key]
                result.update({search_key:res})
            return result

class Map: 

    def __init__(self):
        self.params = locals()


    async def createGraph(
            self, 
            metadata : Dict[List, Any] = None
        ):
        from module.pretzl.etl.mapping import MatrixService as MapService
        from module.file.action.Map import Matrix as MapAttr
        reader = MapService.Map(
            filename = self.params['filename'],
            graph=self.params['format'], 
            metadata=self.params['metadata']
        )
        print("[MAP] LIST : MapControl : Create Graph - START")
        result = await MapAttr.Entity.Create(
            package=reader
        ).getFields()
        x : Dict[List, Any] = {'result' : result}
        x.update({'map_trace' : self.params['metadata']['configs']})
        return x
    

    async def listFields(
            self
        )->Dict[list, Any]:
        print("MAP LIST : MapCOntrol : List Fields - START")
        from module.pretzl.etl.mapping import MatrixService as MapService
        from module.file.action.Map import Matrix as MapAttr
        reader = MapService.Map(
            filename = self.params['filename'],
            graph=self.params['format'], 
            metadata=self.params['metadata']
        )
        result = await MapAttr.Entity.Receive(
            package=reader['mappings']['entity_sfid']
        ).getFields()
        x : Dict[List, Any] = {'result' : result}
        x.update({'map_trace' : self.params['metadata']['configs']})
        return x


class Document:

    def __init__(
            self
    ):
        pass 

    def runPlan(
            command:str, 
            params:Dict[List,Any]
    )->Dict[List,Any]:
        from module.azure.adi.service.command import DocumentCommand
        params.update({
            'command':str(command)
        })
        ma = DocumentCommand(
            comm=command, 
            graph=params 
        )
        response:Dict[List, Any]=ma.Action(graph=params)
        return response 

class Matrix:

    class MetadataController: 
        def __init__(
                self, 
                metadata:Dict[List,Any]
                ):
            self.meta = metadata
            pass 

        def getAttr(
                self
        ):
            from core.model.request import Matrix 
            if 'attr' in self.meta['inputs'].keys():
                subject:Matrix=self.meta['inputs']['attr']
                self.meta['inputs']['sfid']=subject.sfid
                self.meta['inputs']['body']=subject.data 
                self.meta['inputs']['type']='schema'
                self.meta['inputs']['label']=None 
                del self.meta['inputs']['attr']
                print('After Processing: {}'.format(self.meta))
                return self.meta['inputs']
            else:
                return self.meta['inputs']

    def MetaData():
        m : Dict[List, Any] = {}
        return m
    
    def runPlan(
            command:str, 
            graph:Dict[List, Any], 
            meta:Dict[List, Any]
    )->Dict[List, Any]:
        meta.update({'command': str(command)})
        ma = MatrixAction(comm=command, graph=graph, meta=meta)
        response : Dict[List, Any] = ma.Action(metadata=meta)
        return response 



class View:
    class Document:

        def __init__(
                self,
                params
        ):
            self.params = params
            self.result = None

        def getFileName(self)->str:
            from module.pgvector.control import Collection as Coll
            try:
                file_details= Coll.Entity.Query(
                    lookup_key=self.params['subject']
                    ).filename()
                return file_details
            except:
                raise KeyError('key [sfid] - did not return a result from lookup')
            

        def getLocation(self)->Dict[List,Any]:
            from module.pgvector.control import Collection as Coll
            try:
                file_details= Coll.Entity.Query(
                    lookup_key=self.params['subject']
                    ).bySfid()
                return file_details
            except:
                raise KeyError('key [sfid] - did not return from lookup')
            
        def getPDFDirectory(
                self
        )->List:
            from module.pgvector.control import Collection as Coll
            from uuid import UUID
            files= Coll.Entity.Query(
                lookup_key=f'.pdf'
                ).getReadablesList()
            pdfs = []
            try:
                for i in enumerate(files):
                    item= {}
                    print(i)
                    setsfid:str= str(i[1][0])
                    item.update({'sfid': f'{setsfid}'})
                    item.update({'filename':f'{i[1][1]}'})
                    locstr= i[1][3]['result']['action_event'][0]
                    item.update({'fileloc': f'{locstr}'})
                    pdfs.append(item)
                return pdfs
            except:
                raise FileNotFoundError('No PDFs found in the directory')
            

        def getLatestRecordsForBatchID(self):
            from module.pgvector.control import Collection 
            batch_details= Collection.Entity.Query(
                lookup_key=self.params.lower()
                ).entity_labels()
            latest_batch_records = []
            latest_timestamp= 0
            for batch_detail in batch_details:
                if batch_detail['timestamp'].timestamp() > latest_timestamp:
                    latest_timestamp = batch_detail['timestamp'].timestamp()
            for batch_detail in batch_details:
                if batch_detail['timestamp'].timestamp() == latest_timestamp:
                    latest_batch_records.append(batch_detail)
            return latest_batch_records
        
        def getEntityDetailsByID(self):
            from module.pgvector.control import Collection
            try:
                field_details = Collection.Entity.Query(
                    lookup_key=self.params['subject']
                    ).entity_sfid()
                return field_details
            except:
                raise KeyError('Key SFID was not found in the controls units.')
            
        def getLatestProcessedRecordsById(self):
            from module.pgvector.control import Collection 
            batch_details = Collection.Entity.Query(
                lookup_key=self.params
                ).process_record()
            return batch_details 
        

        def getPDFDiectory_hold(
                self, 
                filter:str='.pdf'
        ):
            from dotenv import load_dotenv
            from module.pgvector.control import Collection as Coll
            load_dotenv()
            lookup_name= Coll.Entity()
            if os.environ.get("DOCKERIZED")== 'true':
                fss="/"
            else:
                fss="\\"
            import glob
            position= os.getcwd()
            try:
                path= os.chdir(f'{position}{fss}PRETZL{fss}PDF_PARSABLE{fss}')
            except:
                path=position

            try:
                files = os.listdir(path)
                pdfs = []
                for file in files:
                    p= os.getcwd()
                    item={}
                    if file.endswith(filter):
                        filename= lookup_name.Query(lookup_key=file).entity_name()
                        item.update({'sfid': filename['entity_sfid']})
                        item.update({'filename': file})
                        locstr = f'{p}{fss}{file}'
                        item.update({'fileloc': locstr})
                        pdfs.append(item)
                os.chdir(position)
                return pdfs 
            except:
                raise FileNotFoundError('NO PDFs found in the directory')
            
        def list(self):
            from module.azure.adi.control import FileController as FS
            action = FS()
            result= action.listFiles()
            return result 
            

    class MapState:

        def __init__(
                self, 
                meta:Dict[List, Any]
        ):
            self.actor=meta
            self.sfid=meta['inputs']['sfid']

        async def get(
                self
        )->Dict[List,Any]:
            from module.file.model.Field import Fields as FM
            result:Dict[List,Any]=FM.Entity.Origin(
                package=self.actor
            ).MapView(id=self.sfid)
            return result 
        
        async def getOrigin(
                self, 
                incl
        )->Dict[List,Any]:
            from module.file.model.Field import Field as FS
            try:
                result=FS.Entity.Query(
                    lookup_key=self.sfid
                ).Show(samples=incl)
                return result 
            except:
                raise KeyError('SFID not found.')
            

class Retrieve:

    def __init__(
            self, 
            metadata:Dict[List,Any], 
            sfid:uuid=None
    ):
        self.m = metadata 
        self.original_cwd = os.getcwd()
        self.uid = sfid or None 

    def getCurrentUrl(
            self,
    ):
        from module.pgvector.control import Collection as Coll
        file_details= Coll.Entity.Query(lookup_key=self.uid).bySfid()
        return file_details


    def _getLocation(
            self, 
            sfid
    )->str:
        from module.pgvector.control import Collection as Coll
        file_details= Coll.Entity.Query(lookup_key=sfid).bySfid()
        return file_details 
    

    def KeyLocations(
        self
    )->list:
        try:
            sfid:list= self.m['inputs']['metadata']['source_sfids']
            lister=[]
            for item in sfid:
                operator:Dict[List,Any]= self._getLocation(sfid=item)
                lister.append(operator)
            return lister
        except:
            raise KeyError('SFID not found in db trace search.')
        
    def Location(
            self, 
            filename:str = None,
    )->str:
        result:str= ""
        operator:Dict[List,Any]=self.Details()
        if 'entity_pack' in operator and 'result' in operator['entity_pack']:
            drill: str= operator['entity_pack']['result']
            if isinstance(drill, dict) and 'action_event' in drill:
                if isinstance(drill['action_event'], list) and drill['action_event']:
                    result = drill['action_event'][0]
                else:
                    raise ValueError('ACTION EVENT is empty or is not configured as a list')
            else:
                raise KeyError('ACTION EVENT key is missing from params.')
        else:
            raise KeyError('ENTITY PACK or RESULT key is missing in operator.')
        return result 
    

    def Schema(self)->Dict[List, Any]:
        result:Dict[List, Any] = {}
        self.m['inputs']=Matrix.MetadataController(
            metadata=self.m['inputs']).getAttr()
        from module.file.action.Map import Matrix as Map
        if self.m['inputs']['label'] is not None:
            con:str= self.m['inputs']['label']
            r= Map.Entity.Query(lookup_key=con)
            result= r.mapping_label()
        if self.m['inputs']['sfid'] is not None:
            con: types.UUID= self.m['inputs']['sfid']
            r= Map.Entity.Query(lookup_key=con)
            result= r.graph_sfid()     
        if self.m['inputs']['name'] is not None:
            con:types.String= self.m['inputs']['name']
            r= Map.Entity.Query(lookup_key=con)
            result= r.mapping_name()    
        return result  
    

    def Url(
            self,
            ctrl:str=None
    ):
        handle:str=ctrl or self.m['inputs'].get('sfid') or self.m['inputs'].get('subject')
        result:Dict[List,Any]={}
        try:
            result.update({
                'sfid': handle,
                'data' : [
                    { 
                        'url': self._getLocation(sfid=handle)
                    }
                ]
            })
            return result 
        except:
            raise KeyError('SFID not found.')
        
    def Details(self)->Dict[List,Any]:
        result:Dict[List,Any]={}
        from module.pgvector.control import Collection as Coll
        if self.m['inputs']['sfid'] != None:
            con: types.UUID= self.m['inputs']['sfid']
            r= Coll.Entity.Query(
                lookup_key=con
                )
            result= r.entity_sfid()  
        if self.m['inputs']['label'] != None:
            r= Coll.Entity.Query(
                lookup_key=self.m['inputs']['label']
                )
            result= r.entity_label()        
        else: 
            pass    
        if self.m['inputs']['name'] is not None:
            con:types.String= self.m['inputs']['name']
            r= Coll.Entity.Query(lookup_key=con)
            result= r.entity_name()    
        return result  

            
    def Documents(self):
        body:Dict[List,Any]=self.Details()
        print(self.Location())
        os.chdir(self.original_cwd)
        return body 
    


class Schema:
    class Bindings:


        def __init__(
                self,
                meta
        )->Dict[List,Any]:
            self.meta=meta
            self.look=meta['inputs']['sfid']
            self.body=meta['inputs']['body']

        def set(self)->Dict[List,Any]:
            from module.file.model.Schema import Schema as FS
            g = FS.Entity.Origin(package=self.meta)
            result=g.bind(sub=self.body)
            return result 
        
        def delete(
                self
        )->Dict[List,Any]:
            from module.file.model.Schema import Schema as FD
            x = FD.Manage(meta=self.meta).delete()
            return x 
        




