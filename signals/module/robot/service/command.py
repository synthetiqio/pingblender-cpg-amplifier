from enum import Enum 
from typing import Dict, List, Any, Optional 
from fastapi import UploadFile 

from module.file.config import FILE as ConfigControl 
from langchain_core.documents import Document 

class ServiceCommand:

    def __init__(
            self,
            comm:str, 
            file:UploadFile, 
            meta:Dict[List,Any], 
            name:str, 
            spot:str,
    ):
        
        self.comm = comm 
        self.name=name 
        self.file:UploadFile=file 
        self.meta:Dict[List,Any]=meta 

        if file != None:
            self.name=file.filename
        self.name=name or "ROBOT Module ServiceCommand Unit"
        self.spot=str=spot

    def _getCommand(self)->str:
        command = self.command
        return command 
    

    async def Action(
            self, 
            metadata:Dict[List,Any]=None
    )->Dict[List,Any]:
        data:Dict[List,Any]={}
        response:Dict[List,Any]={}
        if self.file != None:
            file = self.file 
        print(metadata)
        self.meta=metadata 
        casestr=self._getCommand()
        configs=self.meta 

        try:
            match str(casestr).upper():
                case 'UPLOAD':
                    from module.file.control import FileController as U 
                    from module.pgvector.control import Collection as R 
                    runner=U(file=self.file, fn=self.file.filename, construct=configs)
                    outcome:Dict[List,Any]= await runner.Upload()
                    outcome.update({
                        'headers':{
                            'genesis': self.file.filename,
                            'bytes': self.file.size
                        }
                    })
                    tracer=R.Entity.Receive(package=outcome)
                    result= await tracer.getCollectionControls(
                        print(f'[ROBOT]: ServiceCommand Upload - Initializing')
                    )
                    response=result 

                case 'REVIEW':
                    from module.file.control import Retrieve as RE
                    from module.file.action.File import Load as FL 
                    from langchain_core.documents import Document 
                    runner:str=RE(metadata=self.meta).Location()
                    print("[ROBOT] - Step 1/3 - REVIEW Commnd : Receiving URL for Controlled Asset")
                    documents:List[Document]= await FL().DocumentParseCSV(path=runner)
                    headings:Dict[List,Any]= await FL().DocumentGetColumns(path=runner)
                    print("[ROBOT] - Step 2/3 - REVIEW Command : Loading Data from Controlled Resource")
                    response.update({
                        'data_columns': headings, 
                        'document_list': documents,
                    })


                case 'LIST':
                    from module.file.control import FileController as OP 
                    from module.pgvector.control import Collection as Col 
                    instance=Col().Entity.Query(lookup_key=self.file.filename).byFilename()
                    self.file.filename=instance 
                    runner=OP(file=None, fn=self.file.filename, construct=self.meta).ResponseModel()
                    response=runner 

                case 'DETAILS':
                    from module.file.control import Retrieve as x 
                    runner: Dict[List,Any]=x(metadata=self.meta).Details()
                    print("[ROBOT] - State: Receiving - DETAILS Command")
                    response=runner 

                case 'GETLOC':
                    from module.file.control import Retrieve as LOCLO
                    runner:str=LOCLO(metadata=self.meta).Location()
                    print("[ROBOT] - State: GET GETLOC Command - Retieving File PATH")
                    #entry:Dict[List,Any]= runner.get("Entry")
                    u:Dict[List,Any]=({
                        'url':runner 
                    })
                    response=u 

                case 'COLLECT':
                    from module.file.control import CollectController as ColCon 
                    runner:Dict[List,Any]={}
                    results=ColCon(metadata=self.meta).getFilesList()
                    if len(results) > 0:
                        for key,value in enumerate(results):
                            runner.update({key:value})
                        response=runner 
                    else:
                        response={
                            '[ROBOT] - State: Empty Result COLLECT Command'
                        }

                case 'DELETE':
                    from module.file.control import FileController as FilCon
                    runner=FilCon(file=self.file, fn=self.file.filename)
                    outcome:Dict[List, Any]= await FilCon.fileDelete(data, configs)
                    response=outcome 

                case 'ANALYZE':
                    from module.file.control import AnalyzeController as AnaCon
                    from module.file.control import Retrieve as RetCon
                    subj=RetCon(metadata=self.meta).Location()['metdata']['url']
                    runner=AnaCon(filepath=subj)
                    outcome:Dict[List, Any]= await AnaCon.fileAnalyze()
                    response = outcome 

                case 'EMBED':
                    from module.file.control import FileController as Emb 
                    runner=Emb(file=self.file, fn=self.file.filename)
                    outcome:Dict[List, Any]= await Emb.fileEmbed(data, configs)
                    response=outcome

                case 'MANAGE':
                    from module.file.control import FileController as M 
                    runner=M(file=self.file, fn=self.file.filename)
                    outcome:Dict[List,Any]= await M.fileManage(data, configs)
                    response=outcome 
                
                case '_':
                    response={
                            'result':'FAILURE', 
                            'message': 'No valid action command was provided.'
                    }

        except ValueError:
            response=ConfigControl.ERROR_MSG
        self.response=response 
        return response
    

    class ACTION(Enum):
        REVIEW:Dict[List,Any]=ConfigControl.PLAN.ProducePlan()
        UPLOAD:Dict[List,Any]=ConfigControl.PLAN.CollectOp()
        DELETE:Dict[List,Any]=ConfigControl.PLAN.Cleanup()
        ANALYZE:Dict[List,Any]=ConfigControl.PLAN.BuildReport()
        EMBED:Dict[List,Any]=ConfigControl.PLAN.CollectRun()
        MANAGE:Dict[List,Any]=ConfigControl.PLAN.CollectActions()



class MatrixCommand:

    def __init__(
            self, 
            comm:str, 
            graph:str,
            meta:Dict[List,Any]
    ):
        self.comm=comm
        self.meta:Dict[List,Any]=meta 
        self.name='[MATRIX] - System Input Controll Assist'


        self.filename:str=None
        self.label:str=None
        self.collection_name:str=None 
        self.target_schema:str=None 
        self.list:List[any]=None 


    def _getCommand(self)->str:
        command = self.comm 
        return command 
    
    async def Action(
            self, 
            metadata:Dict[List,Any]=None, 
            data:List[Document]=None, 
    )->Dict[List,Any]:
        self.meta=metadata
        self.data:Dict[List,Any]
        response:Dict[List,Any]={}
        casestr=self._getCommand()
        self.meta.update({"Action": casestr})
        configs=self.meta 

        try:
            match str(casestr).upper():
                case 'CREATE':
                    from module.file.control import Retrieve as R, MapController as M
                    from module.file.action.File import Load as B
                    from module.file.action.Map import Matrix as X 
                    from module.file.model.Field import Field as F  
                    hold:Dict[List,Any]={}
                    
                    print('[MATRIX] State: Gathering file data from local location')
                    runner:str=R(metadata=self.meta).Location()
                    outcome:Dict[List,Any]=self.meta 
                    
                    print("[MATRIX] State: Read file for initial review. CREATE Command.")
                    headings:Dict[List,Any]= await B().DocumentGetColumns(path=runner)
                    documents:list= await B().DocumentParseCSV()
                    outcome.update({
                        'column_data': headings, 
                        'document_list':documents
                    })
                    
                    print('[MATRIX] CREATE Command - generates metdata representation of qualities.')
                    tracer=X.Entity.Origin(package=outcome)
                    graph=tracer.CreateGraph()

                    print('[MATRIX] CREATE Command - State: Graph Succeeded')
                    result= await tracer.getMatrixControls(map=graph)

                    print('[MATRIX] INITIATE Command - Started binding result')
                    model= F.Entity.Query(lookup_key=result['source_sfid']).pullTargetFields(
                        package=result
                    )

                    print('[MATRIX] CREATE Command - State: Created a file based on mapping.')
                    result.update({'fields':model})
                    response=result 

                case 'CHAT':
                    from module.file.control import Retrieve as Re
                    from module.file.action.Chat import Chat as Ch 
                    runner=Re(metadata=self.meta).Location()
                    hold:Dict[List,Any]={}
                    result=''
                    result = Ch(
                        targetFile=runner['target'], 
                        inputDataFile=runner['source']
                    ).getRobotRecommendation()
                    response = result 

                case 'STORE':
                    from module.file.control import Retreive as ReR 
                    from module.file.action.File import Load as FE 
                    from module.file.action.Map import Matrix as M 
                    hold:Dict[List,Any]={}
                    runner:str=ReR(metadata=self.meta).Location()
                    headings:Dict[List,Any]= await FE().DocumentGetColumns(path=runner)
                    hold.update({
                        'data_columns':headings,
                    })
                    hold['result'] = await M.Entity.Create(package=response).setFields()
                    response=hold 

                case 'DETAILS':
                    from module.file.control import Retrieve as XM, FileController as FED
                    runner:Dict[List,Any]=XM(metadata=self.meta).Schema()
                    print('[MATRIX] DETAILS Command - State: Columns and response headings.')
                    response=runner 


                case 'LIST':
                    from module.file.control import MapController as MLM
                    from module.file.action.Map import Matrix as FME 
                    settings=MLM(file=self.file, fn=self.file.filename, constructs=configs)
                    outcome:Dict[List,Any]= await settings.listFields()
                    tracer=FME.Entity.Receive(package=outcome)
                    result= await tracer.getMatrixControlls()
                    print('[MATRIX] LIST Command - State: Review and modify data types and field mappings')
                    response=result 
                
                case _:
                    response = {
                            'result':'FAILURE', 
                            'message': 'No valid MatrixCommand action was provided for run.'
                    }
        except ValueError:
            response = ConfigControl.ERROR_MSG

        self.response=response 
        return response 






        




        
