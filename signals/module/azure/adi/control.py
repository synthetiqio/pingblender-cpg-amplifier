from module.azure.adi.config import ADI 
from typing import List, Any, Dict
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

#checked 
class ADIController:

    def collectSettings()->Dict[List,Any]:
        return ADI.Default.Settings()
    

#checked
class ADIErrorController:

    def __init__(
            self, 
            case:str=None
    ):
        self.errcase:str=case 
        self.default:Dict[List,Any]=ADI.ERROR_MSG.values


    def Message(self):
        response:Dict[List,Any]={}
        if self.errcase !=None:
            response = self.default.update({'CASE':self.errcase})
        else:
            response=self.default
        return response 
    

class ADIConfigController:

    class Default:


        def __init__(
                self, 
                check:str=None
        ):
            self.defaults:Dict[List,Any]
            self.checkkey:str=check 


        def vars(
                self,
        ):
            from module.azure.adi.config import ADI as Control 
            try:
                response=ADI.Default[self.checkkey].value
            except:
                response=ADI.ERROR_MSG.values()
            return response 
        


class FileController:

    def __init__(
            self
    ):
        from module.file.control import FileController as FileModule 
        self.control['FileController'] = FileModule 
        pass 

    def listFiles(
            self,
    ):
        pass 


class ADIAnalyzer:


    def __init__(
            self, 
            model_id,
            file_url:str=None, 
            file_content=None,
    ):
        self.client = self.getClient()
        self.model_id:str=model_id
        self.file_url:str=file_url
        self.file_content:bytes=file_content

    #checked
    def getClient(
            self
    ):
        return DocumentAnalysisClient(
            endpoint=ADIController.collectSettings()['adi']['endpoint'],
            credential=AzureKeyCredential(ADIController.collectSettings()['adi']['key'])
        )

    #checked
    def analyzeWithFileContent(
        self
    ):
        if not self.file_content:
            raise Exception("File content in binary was not specified")
        poller=self.client.begin_analyze_document(self.model_id, self.file_content)
        output=poller.result()
        self.output = output 
        return output 
    
    #checked
    def analyzeWithFileURL(self):
        if not self.file_url:
            raise Exception("File URL is not specified")
        poller=self.client.begin_analyze_document_from_url(self.model_id, self.file_content)
        output=poller.result()
        self.output = output 
        return output


#checked all 
class ADIClassifier:

    def __init__(
            self, 
            model_id, 
            file_url:str=None, 
            file_content:bytes=None
    ):
        self.client = self.getClient()
        self.model_id:str=model_id
        self.file_url:str=file_url
        self.file_content:bytes=file_content


    def getClient(self):
        return DocumentAnalysisClient(
            endpoint=ADIController.collectSettings()['adi']['endpoint'], 
            credential=AzureKeyCredential(ADIController.collectSettings()['adi']['key'])
        )
    
    def classifyWithFileContent(
            self
    ):
        if not self.file_content:
            raise Exception('File content in Binary not specified')
        poller=self.client.begin_classify_document(
            self.model_id,
            self.file_content
        )
        output=poller.result()
        self.output=output
        return output 
    

    def classifyWithFileURL(self):
        if not self.file_url:
            raise Exception("File URL is not specified ")
        poller=self.client.begin_classify_document_from_url(
            self.model_id, 
            self.file_url
        )
        output=poller.result()
        self.output=output
        return output 
    

    

    