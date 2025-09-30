from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient, AnalyzeResult
from fastapi import UploadFile, File 
from typing import List, Optional, Any, Dict 
from io import BytesIO 

class KeyHandler:
    from module.azure.afr.config import AFR 
    AFR_END=AFR.Default.AFR_ENDPOINT
    AFR_KEY=AFR.Default.AFR_API_KEY

class DataBody:

    def fromFile(
            file:UploadFile
    )->BytesIO:
        try:
            content:BytesIO=file.read()
            return content
        except: 
            raise FileNotFoundError 
        
    def fromPath(
            file_path:str
    )->BytesIO:
        content:BytesIO
        try: 
            with open(file=file_path, mode='rb') as filedata:
                content = filedata 
            return content 
        except:
            raise FileNotFoundError
        

class AFR:

    class Parse:

        def __init__(
                self,
                file:UploadFile=None, 
                file_path:str=None,
                model:str='prebuilt-document'
        ):
            if file != None:
                self.subj:BytesIO=DataBody.fromFile(file=file)
            elif file_path != None:
                self.subj:BytesIO=DataBody.fromPath(file_path=file_path)
            self.model = model 

        def analyze(
                self,
        )->AnalyzeResult:
            client = DocumentAnalysisClient(
                endpoint=KeyHandler.AFR_END,
                credential=AzureKeyCredential(KeyHandler.AFR_KEY)
            )
            try:
                body = client.begin_analyze_document(
                    model_id=self.model,
                    document=self.subj
                )
                result:AnalyzeResult=body.result()
            except Exception:
                result= "There is no AFR.Parse Error Message"
            return result 