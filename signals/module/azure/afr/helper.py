import os 
from azure.core.credentials import AzureKeyCredential 
from azure.ai.formrecognizer import DocumentAnalysisClient, AnalyzeResult 
from fastapi import UploadFile 
from core.model.document import Construct 

class AFRService:

    afr_endpoint=os.environ['AFR_ENDPOINT']
    afr_apikey=os.environ['AFR_APIKEY']

    def __init__(self):
        return 
    

    async def ParseDocument(
            self, 
            construct:Construct, 
            file:UploadFile, 
            filepath:str=None 
    ):
        dac= DocumentAnalysisClient(
            endpoint=self.afr_endpoint,
            credential=AzureKeyCredential(self.afr_apikey)
        )
        poller= None 
        print("File is done processing in AFR")
        if file:
            file_contents= await file.read()
            poller=dac.begin_analyze_document(
                'prebuilt-document',
                document=file_contents, 
                connection_verify=False
            )
        if filepath:
            with open(filepath, "rb") as file:
                poller=dac.begin_analyze_document(
                    'prebuild-document', 
                    document=file, 
                    connection_verify=False 
                )
        if poller is not None:
            result: AnalyzeResult = poller.result()
            return result 
        


    def get_key_value_pair(kv_pair):
        print('Found: Key->Value Pairs')
        if kv_pair.key:
            print(
                "Key '{}' found within '{}' bounding regions".format(
                kv_pair.key.content, 
                kv_pair.key.bounding_regions,
                ))
        if kv_pair.value:
            print(
                "Value '{}' found within '{}' bounding regions\n".format(
                    kv_pair.value.content,
                    kv_pair.value.bounding_regions,
                )
            )


    def get_table_cells(
            table_idx, 
            table,
    ):
        print(
            "Table # {} has {} rows and {} columns".format(
                table_idx, 
                table.row_count, 
                table.column_count
            )
        )
        for region in table.bounding_regions:
            print(
                "Table # {} loction on page: {} is {}".format(
                    table_idx, 
                    region.page_number,
                    region.polygon,
                )
            )