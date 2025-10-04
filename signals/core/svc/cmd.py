import logging, asyncio, io, json 
from typing import Dict, List, Any

class BatchCommand: 

    """BatchCommand - the comman dunit for handling and routing transformation on the
    source data based on mapped instructeions and TaskTemplates.
    """

    def __init__(
            self, 
            comm: str, 
            graph : Dict[List, Any]
    ):
        self.comm = comm 
        self.name='[CORE]: Command Service - Batch C2 Interface'
        self.meta:Dict[List, Any] = graph
        self.filename:str= None 
        self.label:str= None
        self.type:str= None
        self.searchphrase:Any= None
        self.collection_name:str= None
        self.target_schema:str= None
        self.list:str= None

    def _getCommand(self):
        command = self.comm
        return command 
        
    async def Action(self, graph)->Dict[List, Any]:
        from core.control import ConfigController as Config
        self.meta = graph
        response : Dict[List, Any] = {}
        casestr = self._getCommand()

        try:
            match str(casestr).upper():
                case 'EXTRACT':
                    
                    try:
                        from module.file.control import View
                        from starlette.datastructures import UploadFile
                        from module.pgvector.control import Collection
                        from module.azure.wasb.client import Azure 
                        from module.azure.wasb.control import (
                            AzureController, 
                            BlobController, 
                            ClientController
                        )
                        from fastapi import BackgroundTasks
                        payload = self.meta['queue']
                        headers = self.meta['headers']
                        background_task = self.meta['background_task']
                        blob_location = 'adi-parsed-staging'

                        def prepareEventForWorkflow(metadata):
                            response = {
                                'correlation_id':headers.get("correlation-id"), 
                                'engagement_id':headers.get('engagement-id'),
                                'client_id':headers.get('client-id'),
                                'activity_id':metadata.get('activity_id'), 
                                'batch_id':metadata.get('batch_id'),
                                'status':metadata.get('status'), 
                                'data_source':[
                                    {   "key":"sourcefile_id",
                                        "value":metadata['sourceFileID'].get('id')
                                        },
                                    {
                                        "key":"extracted_field_id",
                                        "value":metadata['extractedFieldID'].get('id')
                                    }, 
                                    {
                                        "key":"confidencescore",
                                        "value":metadata.get("confidencescore")
                                    }
                                    ]
                            }
                            return response 
                        

                        async def proc_doc(
                                sfid, 
                                file_path:str
                        ):
                            status, confidence, json_fileid = '', '', ''
                            try:
                                from module.azure.adi.model.generic import DocIntelParse
                                await Collection.Entity.Process(
                                    package={
                                        'headers':{
                                            'sfid':sfid
                                        }}
                                    ).setStatusAsProcessing()
                                logging.info('{}.{}'.format(sfid,file_path))
                                parsed_docs=DocIntelParse().parse_docs(sfid=sfid, file_path=file_path)
                                parsed_doc_file=io.BytesIO(json.dumps(parsed_docs).encode('utf-8'))
                                upload_file=UploadFile(filename=f'{blob_location}/{sfid}.json', file=parsed_doc_file)
                                await AzureController(metadata={'file':upload_file}).FileToBlobStorage()
                                json_fileid=sfid
                                await Collection.Entity.Process(
                                    package={
                                        'headers':{
                                            'sfid':sfid
                                        }
                                    }
                                ).setStatusAsProcessed()
                                status='Extracted'
                                confidence='High'
                            except Exception:
                                import traceback
                                status='FAILED'
                                confidence='Low'
                                await Collection.Entity.Process(
                                    package={
                                        'headers':{
                                            'sfid':sfid
                                        }
                                    }
                                ).setStatusAsFailed()
                                print(traceback.print_exc())
                            finally:
                                metadata = {
                                    'activity_id':payload['activity_id'], 
                                    'batch_id':payload['batch_id'], 
                                    'status':status, 
                                    'confidencescore':confidence,
                                    'sourcefield_id':{'id':sfid}, 
                                    'extracted_file_id':{'id':json_fileid}
                                }
                                response = prepareEventForWorkflow(metadata=metadata)
                                logging.info("File Processed: {}".format(response))


                        async def proc_all_docs(
                                    sfids,
                                    concurrent_tasks=3
                        ):
                            
                            semaphore=asyncio.Semaphore(concurrent_tasks)
                            async def sem_proc_doc(sfid,filepath):
                                async with semaphore:
                                    await proc_doc(sfid,filepath)

                            tasks= [sem_proc_doc(sfid=sfid, filepath=filepaths['sourcefile_id']) for sourcefile_id, sfid in sfids.items()]
                            await asyncio.gather(*tasks)

                        await Collection.Entity.Process(package={'headers':payload}).setStatusAsBatchReceive()
                        batch_details=View.Document(params=payload['batchId']).getLatestRecordsForBatchID()
                        sfids={str(batch_detail['entity_trace']):str(batch_detail['entity_sfid']) for batch_detail in batch_details}
                        filepaths={
                            datasource['sourcefile_id']:Azure.Manage().downloadUrlUsingBlobUrl(blob_url=datasource['filepath']) for datasource in payload['datasource']     
                        }
                        background_task.add_task(proc_all_docs,sfids)
                        result={
                            'status':'Graffiti created task to process {} documents'.format(len(sfids))
                        }
                        response - result 
                    except Exception as err:
                        import traceback
                        traceback.print_exc(err)
                        result={
                                'result':'FAILURE', 
                                'message':'Extract method failed in the command unit.',
                                'payload': f'additional details:{err}'
                        }
                    response = result 
                case _:
                    result={
                                'result':'FAILURE', 
                                'message':'Extract method failed in the command unit.',
                                'payload': f'additional details:{err}'
                    }
                    response=result 
        except ValueError as vem:
            response=Config.ErrorMSG(msg=vem)
            raise ValueError(response)
        

        self.response=response 
        return response 
        


                            