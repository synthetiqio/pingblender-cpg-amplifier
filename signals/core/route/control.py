from core.svc.cmd import BatchCommand as EntityAction 
from core.route.config import API as Config 
from typing import Dict,List,Any 
from module.pretzl.parser import Read as ReaderService 
from fastapi.openapi.utils import get_openapi

from module.azure.adi.config import ADI as ADIConfig
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential


class APIUnit:

    def __init__(
            self,
    ):
        pass 


    def runPlan(
            command:str, 
            params:Dict[List,Any]
    )->Dict[List,Any]:
        params.update({
            'command':str(command)
        })
        ma = EntityAction(
            comm=command, 
            graph=params 
        )
        response:Dict[List,Any]=ma.Action(graph=params)
        return response 
    

class ActionController:

    def __init__(
            self,
    ):
        pass 


    def runPlan(
            command:str, 
            params:Dict[List,Any]
    )->Dict[List,Any]:
        params.update({
            'command':str(command)
        })
        ma = EntityAction(
            comm=command, 
            graph=params 
        )
        response:Dict[List,Any]=ma.Action(graph=params)
        return response 


class ADIAnalyzer:

    def __init__(
            self, 
            model_id, 
            file_url:str=None,
            file_content=None,
    ):
        self.client=self.getClient()
        self.model_id:str=model_id
        self.file_url:str=file_url
        self.file_content:bytes=file_content

    def getClient(self):
        return DocumentAnalysisClient(
            endpoint=ADIController.collectSettings()['adi']['endpoint'],
            credential=AzureKeyCredential(ADIController.collectSettings()['adi']['key'])
        )


    def analyzeFileContent(self):
        if not self.file_content:
            raise ValueError("File content is required for analysis.")
        poller=self.client.begin_analyze_document(
            model_id=self.model_id, 
            document=self.file_content
        )
        result=poller.result()
        self.output=result.to_dict()
        return result
        
    def analyzeFileURL(self):
        if not self.file_url:
            raise ValueError("File URL is required for analysis.")
        poller=self.client.begin_analyze_document_from_url(
            model_id=self.model_id, 
            document_url=self.file_url
        )
        result=poller.result()
        self.output=result.to_dict()
        return result

class ADIClassifier:

    def __init__(
            self, 
            model_id, 
            file_url:str=None,
            file_content=None,
    ):
        self.client=self.getClient()
        self.model_id:str=model_id
        self.file_url:str=file_url
        self.file_content:bytes=file_content

    def getClient(self):
        return DocumentAnalysisClient(
            endpoint=ADIController.collectSettings()['adi']['endpoint'],
            credential=AzureKeyCredential(ADIController.collectSettings()['adi']['key'])
        )
    
    def classifyFileContent(self):
        if not self.file_content:
            raise ValueError("File content is required for classification.")
        poller=self.client.begin_classify_document(
            model_id=self.model_id, 
            document=self.file_content
        )
        result=poller.result()
        self.output=result
        return result
    
    def classifyFileURL(self):
        if not self.file_url:
            raise ValueError("File URL is required for classification.")
        poller=self.client.begin_classify_document_from_url(
            model_id=self.model_id, 
            document_url=self.file_url
        )
        result=poller.result()
        self.output=result
        return result

class ADIController:

    def collectSettings()->Dict[List,Any]:
        adi=ADIConfig()
        settings:Dict[List,Any]=adi.Default.Settings()
        return settings

class ADIErrorController:

    def __init__(
            self, 
            case:str=None
    ):
        self.errcase:str=case 
        self.default:Dict[List,Any]= ADIConfig.ERROR_MSG.values()

    
    '''
    Message mapping for ADI Service errors.[created by AI - double check it]
    '''
    def Message(self):
        msg:str=self.errcase 
        if msg=='AUTH':
            self.default['message']='[ADI SERVICE] - Authentication Error'
        elif msg=='KEY':
            self.default['message']='[ADI SERVICE] - API Key Error'
        elif msg=='ENDPOINT':
            self.default['message']='[ADI SERVICE] - Endpoint Error'
        elif msg=='LIMIT':
            self.default['message']='[ADI SERVICE] - Rate Limit Exceeded'
        elif msg=='TIMEOUT':
            self.default['message']='[ADI SERVICE] - Request Timeout'
        elif msg=='SERVICE':
            self.default['message']='[ADI SERVICE] - Service Unavailable'
        else:
            self.default['message']='[ADI SERVICE] - Unknown Error'
        return self.default

class ADIConfigController:

    class Default:

        def __init__(
                self,
                check:str=None
        ):
            self.defaults:Dict[List,Any] 
            self.checkkey:str=check

        def vars(self):
            from module.azure.adi.config import ADI as Control 
            try:
                response = Control.Default[self.checkkey].value
            except:
                response = Control.ERROR_MSG.values()
            return response
            

class DocumentController:

    def custom_openapi()->Dict[str,Any]:
        openapi_schema=get_openapi(
                title="Mimeograph Graffiti: GenAI Agents, Assistants and Controls", 
                version="1.0.0", 
                summary="""
                System controls and scalable architecture supporting ingest, 
                classification and executive function for sensitive and regulated 
                data sources. The system supports control of files, sheets, fields
                graphs, ERD, and variable models from diverse LLM/ChatGPT units
                via commercial subscription. 
                """,
                description="""
                Backend data services to handle multi-format data input and workflow
                management for complex AI Assisted data transformation and control
                """,
        )
        openapi_schema["info"]["x-logo"]={
                "url":"https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
        }
        return openapi_schema

class ConfigController:

    def __init__(
            self,
            cfg:str=None,
            evt:str=None,
            proc:str=None,
            state:str=None
    ):
        self.error:Dict[List,Any]=Config.ERROR_MSG

    def Region(self):
        return Config.Ext.Sys().SYS.getRegionalEnv()
    
    def Filesep(self):
        return Config.Ext.Env().Dock.FS
    
    def Timestamp(self):
        return Config.Ext.Sys().Timestamp 
    
    def ErrorMSG(
            self,
            msg:str=None,
    ):
        try:
            self.error['payload']=msg
            return self.error
        except ErrorResponse as e:
            raise e 
        

    def checkAction(
            self, 
            action=str 
    ):
        try:
            check = Config.Action[action.upper()].value
        except ValueError as e:
            msg=f'Action {action} not found in configuration'
            self.error['payload']=msg
            check=self.error 
        return check 
    

class ErrorResponse:

    def __init__(
            self,
            err:str
    ):
        self.err=err 
        #self.e = Evt()

    def __str__(self):
        errobj={
                    'result':'FAILURE',
                    'message':f'Routing has encountered an error', 
                    'payload':None
        }
        return errobj

class FileController:

    def __init__(
            self,
    ):
        from module.file.control import FileController as FileModule 
        self.control['FileController']=FileModule()
        pass 

    def listFiles(
            self, 
    ):
        pass 