#/signals/module/pretzl/parser - core package parser
import os, json, csv, aiofiles, aiofiles, openpyxl, pandas as pd
import datetime, calendar, time, logging, json, asyncio

from io import BytesIO
from pytz import timezone
from pandas import DataFrame, ExcelFile
from fastapi import UploadFile, File, Depends
from fastapi.encoders import jsonable_encoder 
from typing import List, Optional, Any, Dict
from langchain.docstore.document import Document

from core.model.document import Construct
from module.azure.afr.service.command import AFR 
from module.robot.expert.agent.proc.meta import MetadataService 



class Extract:

    def __init__(
            self, 
            fname : str
        ):
        self.filename:str= fname 

    async def extractSheetsToCSV(
            self, 
            xls: BytesIO
        ):
        fn : str = self.filename.split(".")[0]
        print('[PRETZL] : [FILEMANAGER] - \
              EXTRACTING : XLSX to SHEETS - running')
        try:
            xl = pd.ExcelFile(xls)
            ls = xl.sheet_names
            for sheet in ls:
                print(f"DOCAI PRETZL : [FILEMANAGER] - \
                    EXTRACTING {sheet} sheet in {fn} file")
                df = pd.read_excel(xls, sheet_name = sheet)
                df.to_csv(f'{fn}_{sheet}.csv')
            return True
        except FileNotFoundError:
            return False

    async def headings(
            self, 
            filedata : UploadFile
        ):
        return 
    

    async def labels(
            self, 
            filedata: UploadFile
        ):
        return 




class Read:
    """
    PRETZL/Parser - CLASS:(@Read) -- Functions (Preparatory I/O Controls)
    File reading and preprocessing to acquire data from the structure 
    and present traceable options to the developer for services which 
    are routed through controllers to the file management location.
    """

    def __init__(
            self, 
            file:UploadFile, 
            fn:str, 
            construct:Construct= Depends(Construct)
        ):
        self.file_content = file
        self.file_name = fn
        self.init_config = construct
        self.file_type = file.content_type
        self.rootdir = os.getcwd()

    #######################################################################
    ###############FILE READER INTERFACE CONTROL UNITS ####################
    #######################################################################


    def _getFileTimestamp(self, tmz: str)->str:
        """
        private @_getFileTimestamp() - class instance.
        """
        c = timezone(tmz)
        loc_dt = datetime.datetime.now(c). \
            strrftime("%Y-%m-%dT%H:%M:%S.%f+00:00")
        return loc_dt

    def _setFileName(self,path:str)->str:
        n1=path.split('/')
        n2=len(n1)-1
        n3=n1[n2].split('.')
        n4=n3[0]
        filename=n4
        #self.file_name=filename 
        return filename 



        """
        ReaderService Cursory Utilities: private functions.
        _readCSVFile 
        _getFileHeaders
        _getDataFrame
        """

    def _readCSVFile(self)->object:
        file = open(self.file_content)
        csvf = csv.reader(file)
        return csvf
    
    def _getFileHeaders(self)->list:
        header = []
        header = next(self.file_content)
        return header 
    
    def _getDataFrame(self)->DataFrame:
        data = pd.read_csv(self.file_content)
        df = pd.DataFrame(data)
        return df
    

    def _getContentType(
            self, 
            cap : Optional[str] = None
        ):
        if cap:
            self.type = cap.split('/')[1]
        else:
            cap = self.file_content.content_type
            self.type = cap.split('/')[1]
        return self.type


    def _getFileExtension(
            self, 
            cap : Optional[str] = None
            ):
            if cap != None:
                extension = cap.split('.')[1]
            else:
                extension = self.file_content.filename
            self.type = extension.split('.')[1]
            return self.type


    def _getFileNameStr(
            self, 
        )->str:
        cap = self.file_name
        self.filestring = cap.split('.')[0]
        return self.filestring
    
    def _osParamsJSON(self)->json:
        with open (f'params/{self.file_name}') as data_file:
            data = json.load(data_file)
        return data
    
    def _readJSON(self)->json:
        with open( self.file_name ) as data_file:
            data = json.load(data_file)
        return data
    
    def _createPlanJSON(
            self,
            data : json, 
            jf : str 
        )->bool:
        filename = jf
        json_object = data
        with open(
            os.getcwd()+f'params/{filename}/.json', 'w') as outfile:
            outfile.write(json_object)
        return True

    def getOGWorkingDirectory(self):
        return self.rootdir
    
    def getFileReader(
            self
        )->dict:
        ft = self.file_type.split('/')[1]
        from module.pretzl.model.reader import Router as R
        pointer : dict = R.get(ft)
        return pointer
    
    def _getFileTags(
            self,
            ttags : Optional[list[str]] = None
        )->dict[str]:
        """
        LLM Microprompt for the labeling of elements visible in the 
        embedding polygons and vectors. 

        TODO: Replace this initial logic for target file subject and scope.
        """
        lot = {
            'TitleOnPage' : 'Use this tag eif there is a Title \
            or Titles on the page being analyzed',
            'RowOnPage' : 'Use this tag if there is a row exhibited \
                on the page being analyzed',
            'TableOnPage' : 'Use this tag if there is a table on the \
                page being analyzed', 
            'IdentityOnPage' : 'Use this tag if the personal \
                information of a biological human or mammal is listed on the page'
        }
        if ttags:
            lot.update(ttags)
        return lot
    
    #checked
    def _getFileAttributes(
            self, 
            filters: Optional[list] = []

        )->DataFrame:
        df = pd.DataFrame(
                data= self.file_content
            )
        drop_columns = List[filters]
        df_cleaned = df.drop(*drop_columns)
        df_cleaned.limit(1).toPandas().head(1)
        return df_cleaned
    
    def _getCloudConfig(
            self, 
            ch:str
    )->tuple:
        pivot=ch
        c:tuple
        c['subscription']='Microsfot Azure'
        return c
        
    

    def createSessionTime(
            self, 
            o : Optional[int]
        )->int:
        cGMT= time.gmtime()
        t= calendar.timegm(cGMT)+o
        return 
    


    #checked - updated - 01212025 dws
    def getHelpWithMetadata(
            self, 
            pack,
    ):
        from module.file.action.splitters.page import PageSplitter
        from core.model.document import DocumentParsingResult as DPR
        meta_service = MetadataService()
        splitter:PageSplitter=PageSplitter()
        split_file:DPR = splitter.split(self.init_config, pack)
        self.metadata:list= meta_service.GenerateMetadataForDocument(
            documents=split_file
        ).split(', ')
        return split_file 
   


    def getRobotMetadata(
            self, 
            pack
        )->List:
        from core.model.document import ParseResult
        from module.robot.prompt.meta import Human
        robo = Human()
        sp = PART.Splitter(
            command=self.init_config, 
            pages=pack
            )
        sf : ParseResult = sp.Split()
        self.metadata = robo.metaForDocument(docs=sf)
        return sf



    async def getHeadersCollection(
            self, 
            f: DataFrame, 
            fn : str 
    )->tuple:
        cf = self.init_config
        t = self._getContentType()
        c = self._getCloudConfig(cf)
        collect = self._getFileHeaders(self, f)
        return collect
    

    async def getDataColumns(
            self, 
            path : str = None
    )->Dict:
        response : Dict[List, Any] = {}
        if path != None:
            dataframe : DataFrame = pd.read_csv(path)
        else :
            dataframe : DataFrame = pd.read_csv(self.file_content.file)
        response = dataframe.dtypes.to_dict()
        return response
    
    #checked - added - 01212025 - dws
    async def getRowValues(
            self,
            path:str=None, 
            row:int=None,
    ):
        specific = 1
        if row != None:
            specific= 1+row 
        response:Dict[List,Any]={}
        if path != None:
            dataframe:DataFrame=pd.read_csv(path)
        else:
            dataframe:DataFrame=pd.read_csv(self.file_content.file)
        response=dataframe.iloc[specific].to_dict()
        return response 
    
    #checked - updated - 01212025 - dws
    async def getDataPackaged(
            self, 
            file : UploadFile, 
            fn : str, 
            dc : Optional[Dict[list, Any]]
    )->List[Document]:
        
        from core.model.document import Document as DocU, DocumentParsingResult
        from module.azure.afr.control import LoadAfrFile
        CT = DocU.Custom.Table
        self.filename = fn
        if dc:
            self.init_config = dc 
        route = self.getFileReader()
        print(route)
                #simplified reader breakdowns.
        reader = await LoadAfrFile(file, self.init_config)

        #ignores cases without tables, skips the variable inclusion.
        tablelist : List[DocU.Custom.Table] = reader['tables']
        pages : List[Document] = reader['pages']
        split : List[Document] = self.getRobotMetadata(pack=pages)
        
        self.parsing_unit : List[Document] = pages
        self.parsing_tables = tablelist
        self.parsing_chunks = split
        print("[PRETZL] - Reader service creating a packaged data file.")
        return self.parsing_unit


    async def getFileContent(self)->list:
        o = []
        for chunk in self.parsing_chunks:
            o.append(chunk)
        return o


    async def getDataSample(self)->list:
        start : list = self.getFileContent()
        return start[0]
    

    async def getLLMLabels(self)->list:
        p = self.metadata
        return p
    

    async def buildServicePlan(
            self,
            plan : Dict[list, Any]
    )->Dict:
        result : Dict[list, Any]
        x = {
            'name' : self._getFileNameStr(),
            'time' : self._getFileTimestamp(),
            'type' : self._getContentType(),
            'route' : self.getFileReader(),
            'sowd' : self.rootdir
        }
        plan.update(x)
        result = plan
        await self._storeEmbeddings()
        return result

#########################################################
##############   Vector Interface for Embeddings ########
#########################################################

    async def getEmbeddings(self)->list:
        from module.pgvector.action.embed import Entity as Body
        from module.pgvector.connect import Client, Interface
        collection = []
        for index,split in enumerate(self.parsing_chunks):
            print("Processing Chunk: ", index+1, "/", len(self.parsing_chunks))
            collection.append(Body.Embed.embed_chunk(split))
        return collection 
    

    async def _storeEmbeddings(self)->bool:
        from langchain_core.embeddings import Embeddings
        from module.pgvector.connect import (
            Client,
            Interface
        )
        vc = Interface(
            documents = self.parsing_unit, 
            metadatas=self.metadata, 
            collection_name=self.file_name, 
            configs=self.init_config
        )
        print(Embeddings)
        embeddings : list = await self.getEmbeddings()
        await vc.setEmbeddings(embeddings=embeddings)
        db = vc.loadEmbeddingsFromDocument()
        return db

    async def runPlan(
            self,
            plan: Dict[List, Any]
        ):
        data = plan
        return data


##partitioning dependencies.
from core.model.document import Construct, SplitStrategy
class PART:

    class Splitter:

        def __init__(
                self,
                command : Construct, 
                pages : List[Document]
            ):
            self.comm = command
            self.pack : List[Document] = pages
            
        def Split(
                self,
                cfg : Construct = None
            ):
            parse = PRETZL
            if cfg != None:
                route : SplitStrategy = cfg.split_strategy
            else:
                route : SplitStrategy = self.comm.split_strategy
            try:
                result = PRETZL.Action(
                            classname='part.split',
                            action=route,
                            units=self.pack,
                            chips=Construct.chunk_size,
                            lattice=Construct.chunk_overlap
                        )
                return result
            except:
                raise ValueError("Could not match valid ACTION for Split")

#checked 
class GRAPH:

    def __init_(
            self, 
            pack:Dict[List, Any]= None, 
            format:str= None
    ):
        self.params = locals()
        self.result = Dict[List, Any] = {}
        self.fields = Dict[List, Any] = {}

    def setVar(
            self, 
            param:str, 
            value:Any
        ):
        self.params.update({
            param:value
        })
        return self.params
    
    def response(self):
        getresult = self.result
        return getresult
    

#checked all - updates - 01212025 - dws
class PACK: 

    def __init__(
            self, 
            box : Dict[Any, Any] = None
        ): 
        if box != None:
            self.receiver= box
            self.source:str= box['package']['file']
            self.coll:str= box['package']['target_collection']
            self.select:Dict[List, Any]= box['inputs']
        else:
            self.receiver = {}
        self.queue = box['process_queue']
        self.subject : Dict[List, Any]  = {}
        self.fileurl : str = self.source 
        self.runner : BytesIO = None


    def _establishMetadata(
            self
        )->Dict[List, Any]:
        m : Dict[List, Any] = self.source['metadata']
        return m
    
    #checked - updated - 01212025 dws 
    def setCollectionName(
            self, 
            update:str,
        )->str:
        self.coll = update 
        result=self.coll
        return result 
    
    #checked - updated - 012212025 - dws
    def _getCollectionName(
            self,
    ):
        return self.coll 
    
    #checked - updated - 01212025 - dws
    def setSelections(
            self, 
            settings: Dict[List, Any] = None
    )->Dict[List, Any]:
        config : Dict[List, Any]  = {}
        if self.select != 'empty':
            config = self.select
        else:
            config = Construct
        return config

    #checked - updated - 01212025 - dws
    def collectDataForDocuments(
            self
    ):
        program = self.source.split('.')[0]
        approach = self.receiver['metadata']['details']['reader_set']
        databody = list[Document]
        match str(approach['datareader']).upper():


            case "AFR":
                databody = None
                if approach['dataformat'] == "PDF_PARSABLE":
                    from module.azure.afr.service.command import AFR as AZLOD
                    loader = AZLOD.Parse(file_path=self.fileurl)
                docs = loader

            #checked - added - 01212025 - dws
            case "DOCINTEL":
                databody = None
                if approach['dataformat'] == 'PDF_PARSABLE':
                    from langchain_community.document_loaders.pdf import OnlinePDFLoader
                    from module.azure.adi.control import ADIController as DIL
                    loader= DIL(file_path=self.fileurl)

                elif approach['dataformat'] == "EXCEL_10":
                    from langchain_community.document_loaders.excel import UnstructuredExcelLoader as LocalLoader 
                    loader= LocalLoader(file_path=self.fileurl, mode='single')

            #checked - updated - 01212025 - dws
            case "LANGCHAIN":
                databody = None

                if approach['dataformat'] == "CSV_TXT":
                    from langchain_community.document_loaders.csv_loader import CSVLoader
                    loader = CSVLoader(file_path=self.fileurl)
                elif approach['dataformat'] == "EXCEL_10":
                    from langchain_community.document_loaders.csv_loader import UnstructuredCSVLoader as LocalLoader
                    loader = LocalLoader(file_path=self.fileurl, mode="single")
                docs = loader.load()

            case "UNSTRUCTURED":
                databody = None
                from langchain_community.document_loaders import UnstructuredFileLoader as UFL
                loader = UFL(file_path=self.fileurl, mode='elements')

        databody.append(docs)
        return databody

    #checked - updated - modified - 01212025 - dws
    def set(self)->Dict[List, Any] :
        package : Dict[List, Any] = {}
        package.update (
            {
                'shaper' : self._establishMetadata(),
                'name' : self.setCollectionName(),
                'body' : self.collectDataForDocuments(),
                'selections' : self.setSelections(),
        })
        return package

#checked - added - 01212025 - dws
class PORTL:


    class Edi:

        def __init__(
                self, 
                event:str, 
                context:Dict[List,Any]
        ):
            self.event_state=0
            self.event=event 
            
            self.file_context=context or None 
            self.file_content=context['subj'] or None 

        def location(self):
            from module.file.control import Retrieve
            if 'sfid' in self.context:
                local=self.context['sfid']
                meta:Dict[List,Any]={
                    'inputs' :{
                        'sfid':local
                    }
                }
                store:str=Retrieve(metadata=meta,sfid=local).getCurrentUrl()
                print(store)
            self.store_url=store 
            return store

        def process(self):
            match self.evt.upper():
                case "PARSE|EDI|XML":
                    from openai import OpenAI
                    from langchain_core.embeddings import Embeddings
                    client=OpenAI(
                        api_key=os.getenv("OPENAI_WR")

                    )
                    filen:str= self.location()
                    xmldoc:str= filen.replace(".DAT", ".xml")
                    document:str=''
                    import pyx12.x12file, pyx12.x12n_document
                    import pyx12.x12xml_simple, pyx12.params
                    import xmltodict
                    with open(xmldoc, 'w') as xmlio:
                        pyx12.x12n_document.x12n_document(
                            param=pyx12.params.params(),
                            src_file=str(filen),
                            fd_997=None,
                            fd_html=None,
                            fd_xmldoc=xmlio
                        )
                    jsondoc:str=xmldoc.replace(".xml",".json")
                    print(f"Converting XML to JSON for Embeddings: {xmldoc} -> {jsondoc}")
                    with open(xmldoc, 'r') as xio, open(jsondoc, 'w') as jio:
                        json.dump(
                            xmltodict.parse(xio.read()),
                            jio
                        )
                        embed= client.embeddings.create(
                            model='text-embedding-3-large', 
                            encoding_format=float,
                            input=jio
                        )
                    return embed 

        def wrapper(self):
            outcome=self.attempt()
            lambda_standard={
                "Records": [
                    {
                    "eventVersion": "2.0",
                    "eventSource": "aws:s3",
                    "awsRegion": "us-east-1",
                    "eventTime": "1970-01-01T00:00:00.000Z",
                    "eventName": self.context,
                    "userIdentity": {
                        "principalId": "EXAMPLE"
                    },
                    "requestParameters": {
                        "sourceIPAddress": "127.0.0.1"
                    },
                    "responseElements": {
                        "x-amz-request-id": "EXAMPLE123456789",
                        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
                    },
                    "s3": {
                        "s3SchemaVersion": "1.0",
                        "configurationId": "testConfigRule",
                        "bucket": {
                        "name": "example-bucket",
                        "ownerIdentity": {
                            "principalId": "EXAMPLE"
                        },
                        "arn": "arn:aws:s3:::example-bucket"
                        },
                        "object": {
                        "key": "test_key",
                        "sequencer": "0A1B2C3D4E5F678901"
                        }
                    }
                    }
                ], 
                "Result":{
                    outcome
                }
                }  
            return lambda_standard

        async def jump(self)->Dict[List,Any]:
            out:Dict[List,Any]={
                'result': 'SUCCESS', 
                'message': f'The {self.evt} object worked',
                'details':self.wrapper()
            }
            return out



    class Binary:

        def __init__(
                self, 
                path:str = None, 
                sfid:str = None, 
                file:UploadFile = None
        ):
            self.file: UploadFile= None 
            self.file_binary:BytesIO= None 

            self.path = path
            if file != None and sfid == None:
                self.file = self._convertToStandard(file)
            if path !=None and sfid == None and file== None:
                self.file = self._convertToStandard(open(path, 'w+'))
            if sfid != None and path == None and file == None:
                self.file = self._convertToStandard(self.getBinaryStream())

        def _readFile(self):
            return self.file.read()
        
        def _writeFile(self, data):
            self.file.write(data)
            return True
        
        def _closeFile(self):
            self.file.close()
            return True 

        def _convertToStandard(
                self, 
                file: UploadFile
        )->UploadFile:
            self.file = file 
            return self.file 
        
        def _getFileName(self):
            return self.path.split('.')[0]
        
        def _getFileExtension(self):
            return self.path.split('.')[1]
        
        def convertToDataFrame(self):
            return pd.read_csv(self.path)
        
        def convertToJSON(self):
            return json.load(self.path)
        
        async def getBinaryStream(
                self
        )->BytesIO:
            from module.pgvector.control import Collection as CO 
            if self.sfid != None & self.path == None:
                op = CO.Entity.Query(lookup_key=self.sfid).bySfid()
            try:
                if self.sfid != None & self.path == None:
                    op = CO.Entity.Query(lookup_key=self.sfid).bySfid()
                    async with aiofiles.open(
                        op, 
                        'wb', 
                    ) as out:
                        content= await out.read()
                        ex:BytesIO = BytesIO(content)

            except:
                ex = print("[PRETZL | PORTL]: ERROR - No BINARY conversion was possible")
            self.file_binary = ex 
            return self.file_binary


class PRETZL: 

    #checked
    def __init__(
            self, 
            file:UploadFile= File(...), 
            check:str= None, 
            construct:Construct= Depends(Construct)
        ):
        self.owkd= os.getcwd()
        self.file= file 
        self.plan= check
        self.config= construct
        self.dockerized= self._dockedOS()

    #checked
    async def _createDirectory(
            self, 
            path : str
    )->bool:
        fs : Dict[list]  = self._dockedOS()
        st = os.getcwd()
        runner = os.path.join(st, path)
        try:
            if not os.path.exists(runner):
                os.makedirs(runner)
            os.chdir(runner)
            print(f'Currently working out of: {os.getcwd()}')
        except Exception as err:
            return False 
        return True
    
    def _serialize_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4
            )

    #checked
    def _dockedOS(
            self
        )->Dict[List, Any]:
        docker:Dict[list]
        fss:str 
        if os.environ.get("DOCKERIZED")== 'true':
            fss = "/"
        else:
            fss = "\\"
        docker = {
            'ENV': os.environ.get("DOCKERIZED"), 
            "UNX": fss, 
            "OWD": self.owkd
        }
        return docker 
    
    #checked
    async def get_columns(
        self, 
        path : str
    )->Dict[List, Any]:
        response = Dict[List, Any] = {}
        try:
            dataframe : DataFrame = pd.read_csv(path)
            response.update({
                "fileschema" : dataframe.dtypes.to_dict()
                })
            return response
        except:
            raise Exception

    #checked
    async def push_edi_embeddings(
        self, 
        path : str
    ):
        """
        @getColumns expects a simple dict for a response to render correctly. 
        This will be drawn from the file and converted into a dataframe, which
        should expose gaps in the headings if the file is malformed.
        """
        try:
            import jq
            from langchain_community.document_loaders import JSONLoader
            from module.robot.control import SynthController as ServiceInterface
            result = pd.read_csv(path).to_json(index='episodiq_id')
            ai_client=ServiceInterface().open_api()
            client_settings=ServiceInterface().get_settings()

            print(os.getcwd())
            atomic_subject=self.config['sfid'] or self.config['subj']
            with open(f'./EDI/{atomic_subject}/structured.json', 'w+') as sauce:
                sauce.write(result)
                sauce.close()
            print(pd.read_json(f'./EDI/{atomic_subject}/structured.json'))
            print("ENND OF WORK")
            loaddata=JSONLoader(
                file_path='structured.json', 
                jq_schema=".[]",
                text_content=False,
            )
            loaded = loaddata.load()
            for item in loaded:
                vari = str(item.__str__)
                embed = ai_client.embeddings.create(
                    input=vari, 
                    model=client_settings.embed_model,
                    user=client_settings.embed_user
                )
                with open(f'./edi/{atomic_subject}/embeddings.txt', 'w+') as f:
                    f.write(str(embed))
                vari=''
            f.close()
            print("[EPISODIQ] - Claims Embeddings Generated.")

        except Exception as e:
            raise e 
    
    #checked
    async def convertToDataFrame(
            self, 
            file : UploadFile
    )->DataFrame:
        df = pd.read_csv(file.file)
        file.file.close()
        return {"filename" : file.filename}
    

    #checked - added:01212025 - dws
    async def getWasbPath(
            self,
    ):
        from module.azure.wasb.control import BlobController, ClientController
        B=BlobController(self.file.filename)
        return B.setWasbPath()


    #checked - updated:01212025 - dws
    async def setStorePath(
            self, 
            path : str = "eval"
    )->str:
        fs:Dict[List, Any]= self._dockedOS()
        in_file= self.file
        self.filename= in_file.filename
        filetype:str= self.plan 
        pathbuild= [path, filetype, self.filename]
        #filepath = os.getcwd()+fs["UNX"].join)(pathbuild)
        if await self._createDirectory(path):
            if await self._createDirectory(filetype):
                self.storepath = os.getcwd()
        return self.storepath 
    

    #checked
    async def getStorePath(
            self, 
            filename : str 
    )->str:
        from module.pgvector.control import Collection
        c = Collection.Entity.Query(lookup_key=filename).byFilename()
        return c
    

    #checked
    async def loadPathAssets(
            self, 
            file: UploadFile = File(...)
    )->str:
        in_file = file
        filetype = self.plan
        rebase = os.getcwd()
        
        async with aiofiles.open(self.filename, 'wb') as out:
            content = await in_file.read()
            ex = Extract(fname = self.filename)
            if filetype == "EXCEL_10":
                await ex.extractSheetsToCSV(BytesIO(content))
            await out.write(content)
            await out.flush()
            print(os.listdir(self.storepath))
        os.chdir('../../')
        print(os.getcwd())
        return self.storepath
    


    #checked
    async def getBinaryStream(
            self
    )->BytesIO:
        file = self.file
        try:
            async with aiofiles.open(
                file.filename, 
                'wb'
            ) as out:
                content = await file.read()
                ex : BytesIO = BytesIO(content)
        except:
            ex = print("AUTOETL : ERROR - No BINARY Conversion was possible.")
        self.file_binary = ex
        return self.file_binary
    

    #checked - added - 01212025 - dws
    async def listPDFFiles(
        self, 
        reader,
    ):
        fs=self._dockedOS()
        if reader==None:
            path=os.getcwd()
        else:
            path=reader
        files = os.listdir(path)
        pdfs=[]
        for file in files:
            if file.endswith(".pdf"):
                pdfs.append(file)
        return pdfs 

    #checked - updated - 01212025 - dws
    async def getFilesList(
            self, 
            store : str = '', 
            filter : str = '', 
            file : str = ''
    )->Dict[list, Any]:
        import glob
        from dotenv import load_dotenv
        load_dotenv()
        path = ''
        stat = self._dockedOS()
        filesep=os.path.sep
        if store != None:
            path = store
        else: 
            path = os.getcwd()
        result : Dict[list]
        if filter != '':
            result = glob.glob(f'{path}{filesep}{file}*.{filter}')
        elif file != '':
            result = glob.glob(f'{path}{filesep}{file}*')
        else:
            result = glob.glob(f'{path}{filesep}*')
        return result
        
        
        