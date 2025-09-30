from azure.core.credentials import AzureKeyCredential 
from azure.ai.formrecognizer import DocumentAnalysisClient
from module.azure.adi.control import ADIController 
from typing import Dict, List, Any 

class ADIReceipt:

    def __init__(
            self,
            url:str
    ):
        self.url = url 

        self.error:Dict[List,Any]={
                    'result': 'ERROR', 
                    'message': 'ADIController failed in ADI Models', 
                    'payload': None
        }

        self.client = DocumentAnalysisClient(
            endpoint=ADIController.collectSettings()['adi']['endpoint'], 
            credential=AzureKeyCredential(ADIController.collectSettings()['adi']['key'])
        )


    
    async def analyzeReceipt(
            self
    ):
        try:
            poller=self.client.begin_analyze_document_from_url(
                model_id='prebuilt-invoice', 
                document_url=self.url
            )
            receipts=poller.result()
            self.receipt = receipts 
            return receipts
        except:
            raise BufferError


    async def analyzeInvoice(
            self,
    ):
        try:
            poller=self.client.begin_analyze_document_from_url(
                model_id='prebuilt-invoice', 
                document_url=self.url
                )
            invoice=poller.result 
            self.receipt=invoice 
            return invoice 
        except:
            raise BufferError
        

        
