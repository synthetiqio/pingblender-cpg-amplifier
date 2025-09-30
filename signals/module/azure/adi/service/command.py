import logging, json, os, asyncio, io
from typing import Dict, List, Any
from module.pgvector.control import Collection
from module.azure.adi.control import ADIController as ADIC, ADIConfigController
from module.azure.adi.config import ADI as Config
from module.file.edge.client import ApiClient
from module.file.edge.file_api import FileApi
from module.file.edge.configuration import Configuration
from langchain_core.documents import Document

class ADICommand:


    def __init__(
            self, 
            comm:str, 
            graph:str, 
            meta:Dict[List, Any]

    ):
        self.comm=comm
        self.meta=graph
        self.name='[AZURE - ADI]: Service Request - ACTIVE'

        self.filename:str= None
        self.label:str= None
        self.collection_name:str= None
        self.target_schema:str= None
        self.list:str= None



    def _getCommand(
            self
    )->str:
        return str(self.comm)
    

    async def Action(
            self, 
            metadata:Dict[List, Any]= None, 
            data:List[Document]= None
    )->Dict[List, Any]:
        self.meta= metadata
        self.data:Dict[List,Any]= data
        response:Dict[List,Any]={}


        '''
        ADI Command Unit - This is the command center for all ADI related tasks.
        It will take in a command and execute the appropriate action based 
        on the command. the is the C2 Pattern (Command & Control) for ADI.
        '''
        casestr= self._getCommand()
        self.meta.update({'Action':casestr})
        configs=self.meta

        try:
            match str(casestr).upper():

                case 'READ':
                    from module.file.control import (
                        Retrieve as R, 
                        Map as M
                    )
                    from module.file.action.File import Load as B
                    hold:Dict[List,Any]
                    runner:str= R(metadata-self.meta).Location()
                    outcome: Dict[List,Any]=self.meta
                    headings:Dict[List,Any]=await B().DocumentGetColumns(path=runner)
                    documents:Dict[List,Any]=await B().DocumentParseCSV(path=runner)
                    outcome.update({'column_data':headings})
                    outcome.update({'document_list':documents})
                    print('[AZURE | ADI]: READ - Generates meatadata representation of the file qualities.')
                    print('[AZURE | ADI]: command = READ -> Storing headings/sample of document.')
                    tracer= R.Entity.Origin(package=outcome)
                    graph=tracer.CreateGraph()
                    result= await tracer.getMatrixControls(map=graph)
                    print("[AZURE | ADI]: ADI Command -> Create a file based on the mapping")
                    response=result

                
                case 'LIST':
                    from module.file.control import Retrieve as R, Map as M
                    from module.file.action.File import Load as B
                    print("[AZURE | ADI]: LIST - generates a list of the files in defined storage.")
                    hold:Dict[List,Any]={}
                    runner:str=R(metadata=self.meta).Location()
                    outcome:Dict[List,Any]=self.meta
                    print('[AZURE | ADI]: ADI Command -> produce list for service')
                    response=outcome

                case 'LOAD':
                    from module.file.control import Retrieve as R
                    from module.file.action.File import Load as F
                    from module.file.action.Map import Matrix as M

                    print('[AZURE | ADI]: LOAD - Promotes controlled data for use.')
                    hold:Dict[List,Any]={}
                    runner:str=R(metadata=self.meta).Location()
                    headings:Dict[List,Any]= await F().DocumentGetColumns(path=runner)
                    hold.update({'data_columns': headings})
                    hold['result']= await M.Entity.Create(package=response).setFields()
                    response=hold


                case 'STORE':
                    from module.file.control import Retrieve as R
                    from module.file.action.File import Load as F
                    from module.file.action.Map import Matrix as M
                    hold:Dict[List, Any]={}
                    runner:str=R(metadata=self.meta).Location()
                    headings:Dict[List,Any]=await F().DocumentGetColumns(path=runner)
                    hold.update({'data_columns':headings})
                    hold['result']=await M().Entity.Create(package=response).setFields()
                    response=hold

                case 'DETAILS':
                    from module.file.control import Retrieve as X
                    runner:Dict[List,Any]=X(metadata=self.meta).Schema()
                    print('[AZURE | ADI]: DETAILS - provides detailed view and schema review of raw file.')
                    response=runner

                case _:
                    response = {
                            'result' : 'Failure', 
                            'message' : 'The system default case was triggered and has no further info.', 
                            'payload': None
                    }
        except ValueError:
            response = ADIConfigController.Default(check=None)
        self.response=response
        return response 
    



class DocumentCommand:

    def __init__(
            self,
            comm:str, 
            graph:Dict[List, Any]
    ):
        self.comm = comm
        self.meta:Dict[List,Any]=graph
        self.name="DOCUMENT Command Unit - ACTIVE"
        #self.response:Dict[List,Any]= Config.Mapping.ResponseModel

        #searchable response parameters
        self.filename:str=None
        self.label:str=None
        self.type:str=None
        self.searchphrase:str=None
        self.collection_name:str=None
        self.target_schema:str=None
        self.list:str=None


    def _getCommand(
            self
    )->str:
        return str(self.comm)


    async def Action(
            self, 
            graph
    )->Dict[List,Any]:
        self.meta=graph
        response:Dict[List,Any]={}
        casestr= self._getCommand()
        self.meta.update({'Action':casestr})
        configs=self.meta
        try:
            match str(casestr).upper():
                case 'PROCESS':
                    from module.file.control import View
                    from starlette.datastructures import UploadFile
                    from module.azure.wasb.client import Azure
                    from module.azure.wasb.control import (
                        AzureController, 
                        BlobController, 
                        DeeplinkController as DLink
                    )
                    from fastapi import BackgroundTasks
                    payload=graph['inputs']
                    sfids=payload['sfids']
                    blob_location=DLink(metadata=self.meta).path()

                    async def process_document(sfid, file_path):
                        from module.azure.adi.model.generic import DocIntelParse
                        from module.pgvector.control import Collection
                        await Collection.Entity.Process(
                            package={'headers': {'sfid': sfid}}
                        ).setStatusAsProcessing()
                        parsed_docs=DocIntelParse().parse_docs(
                            sfid=sfid, 
                            file_path=file_path
                        )
                        parsed_doc_file=io.BytesIO(json.dumps(parsed_docs).encode('uft-8'))
                        upload_file=UploadFile(
                            filename=f"{blob_location}/{sfid}.json",
                            file=parsed_doc_file
                        )
                        await AzureController(
                            metadata={'file':upload_file}).FileToBlobStorage()
                        await Collection.Entity.Process(
                            package={'headers': {'sfid':sfid}}
                        ).setStatusAsProcessed()

                    async def process_all_documents(
                        sfids, 
                        concurrent_tasks=3
                        ):
                        semaphore=asyncio.Semaphore(concurrent_tasks)

                        async def sem_process_document(sfid):
                            async with semaphore:
                                file_path = View().Document(
                                    params={
                                        'subject': sfid
                                    }
                                ).getLocation()
                                tasks=[sem_process_document(sfid) for sfid in sfids]
                                await asyncio.gather(*tasks)
                        
                    background_task=graph['background_task']
                    background_task.add_task(process_all_documents, sfids)
                    result={
                        'status':'[AZURE | ADI] : TASK Initiated - created to process {} documents'.format(len(sfids))
                    }
                    response=result


                case 'LIST':
                    from module.file.control import View
                    try:
                        from module.azure.wasb.control import DeeplinkController as DLink
                        from module.azure.wasb.client import Azure
                        payload=graph['inputs']
                        if 'batch_id' in payload:
                            batch_details=View.Document(params=payload['batch_id']).getLatestRecordsForBatchID()
                            sfid_traces={str(batch_detail['entity_sfid']): str(batch_detail['entity_trace']) for batch_detail in batch_details}
                            sfid=list(sfid=sfid_traces.keys())
                        else:
                            if 'sfids' not in payload:
                                #captures singular sfid for file associations with mapping.
                                payload.update({'sfids':[graph['subject']]})
                                sfids=payload['sfids']
                                sfid_traces={}
                        document_status= {}
                        for sfid in sfids:
                            overall_fields_confidence_levels = {
                                'Low': 0, 
                                'Medium':0, 
                                'High':0
                            }
                            all_confidence_levels={'Low','Medium','High'}
                            overall_confidence_label_by = 'AI'
                            overall_confidence_label='High'
                            entity_details=View().Document(params={'subject':sfid}).getEntityDetailsByID()
                            process_details=View().Document(params=sfid).getLatestProcessedRecordsById()
                            if process_details:
                                headers={
                                    'client_id': entity_details['entity_pack']['headers']['clientId'], 
                                    'engagement_id':entity_details['entity_pack']['headers']['engagementId'], 
                                    'correlation_id':entity_details['entity_pack']['headers']['correlationId'], 
                                    'subscription_key':entity_details['entity_pack']['headers']['Mimeo-graffiti-subscription'],
                                    'authorization':self.meta['authority']
                                }
                                configuration=Configuration()
                                configuration.api_key['mimeo-graffiti-subscription'] = headers.get('subscription_key')
                                configuration.api_key['Authorization'] = headers.get("authorization")
                                openapiclient = ApiClient(
                                    configration=configuration
                                )
                                file_download_response=FileApi(
                                    api_client=openapiclient
                                ).get_file_download_id(
                                    id=str(process_details['process_id']), 
                                    x_client_id=headers.get('client_id'), 
                                    x_engagement_id=headers.get('engagement_id'), 
                                    x_correlation_id=headers.get('correlation_id'), 
                                    _preload_content=False
                                )
                                blob_data=file_download_response.data
                                parsed_docs=json.loads(blob_data)

                                for doc in parsed_docs[sfid]:
                                    fields_confidence_levels=doc['parsed_document']['documents']['fields_confidence_levels']
                                    overall_fields_confidence_levels['Low']+=fields_confidence_levels['Low']
                                    overall_fields_confidence_levels['Medium']+=fields_confidence_levels['Medium']
                                    overall_fields_confidence_levels['High']+=fields_confidence_levels['High']
                                    if doc['parsed_document']['documents']['confidence_level_by']=='User': overall_confidence_label_by = 'User'
                                    doc_confidence_label=doc['parsed_document']['documents']['confidence_label']
                                    if all_confidence_levels.index(doc_confidence_label) < all_confidence_levels.index(overall_confidence_label):
                                        overall_confidence_label=doc_confidence_label

                            trace_details=Collection.Entity.Query(lookup_key=sfid).entity_trace()
                            filename=Collection.Entity.Query(lookup_key=sfid).filename()
                            latest_status, latest_timestamp = '',0
                            for trace_detail in trace_details:
                                if trace_detail['timestamp'].timestamp() > latest_timestamp:
                                    latest_status=trace_detail['entity_event']
                                    latest_timestamp=trace_detail['timestamp'].timestamp()

                            document_status[sfid]= {
                                'file_name': filename['entity_name'], 
                                'status': latest_status, 
                                'timestamp': int(latest_timestamp), 
                                'fields_confidence_levels':overall_fields_confidence_levels,
                                'batch_id': payload.get('batch_id', ''),
                                'file_id': sfid_traces[sfid] if payload.get('batch_id') else '',
                                'confidence_label_by': overall_confidence_label_by, 
                                'confidence_label': overall_confidence_label
                            }
                        response=document_status
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        result= {
                                'result':'FAILURE', 
                                'message': 'No valid document ACTION was provided',
                                'payload':f'Error details: {e}'
                            }
                        response=result
                        raise Exception(Config.ERROR_MSG)
                    
                case 'VIEW':
                    import requests, base64
                    from urllib.parse import urlparse
                    from module.file.control import View
                    batch_id=self.meta['inputs']['batch_id']
                    sourceFileId=self.meta['inputs']['file_id']
                    batch_details=View.Document(params=batch_id).getLatestRecordsForBatchID()
                    sfid=[str(batch_detail['entity_sfid']) for batch_detail in batch_details if
                          str(batch_detail['entity_trace']) == sourceFileId][0]
                    entity_details=View.Document(params={'subject': sfid}).getEntityDetailsByID()
                    headers= {
                        'client_id': entity_details['entity_pack']['headers']['clientId'], 
                        'engagement_id':entity_details['entity_pack']['headers']['engagementId'], 
                        'correlation_id':entity_details['entity_pack']['headers']['correlationId'], 
                        'subscription_key':entity_details['entity_pack']['headers']['Mimeo-graffiti-subscrption'],
                        'authorization':self.meta['authority']
                    }
                    configuration=Configuration()
                    configuration.api_key['mimeo-graffiti-subscription'] = headers.get('subscription_key')
                    configuration.api_key['Authorization'] = headers.get("authorization")
                    openapiclient = ApiClient(
                        configration=configuration
                    )
                    file_download_response=FileApi(
                        api_client=openapiclient
                    ).get_file_download_id(
                        id=str(process_details['process_id']), 
                        x_client_id=headers.get('client_id'), 
                        x_engagement_id=headers.get('engagement_id'), 
                        x_correlation_id=headers.get('correlation_id'), 
                        _preload_content=False
                    )
                    file_content_binary= file_download_response.data
                    file_path_resp=FileApi(
                        api_client=openapiclient
                    ).get_file_path_id(
                        id=sourceFileId, 
                        x_client_id=headers.get('client_id'), 
                        x_engagement_id=headers.get('engagement_id'), 
                        x_correlation_id=headers.get('correlation_id')
                    )
                    file_content=base64.b64encode(file_content_binary).decode('utf-8')
                    _, file_extension = os.path.splitext(file_path_resp.file_name)
                    result={
                        'file_content': file_content, 
                        'file_extension': file_extension, 
                        'file_name': file_path_resp.file_name, 
                        'file_path': file_path_resp.file_path
                    }
                    response=result


                case 'LOAD':
                    from starlette.datastructures import UploadFile
                    from module.file.control import View
                    from module.azure.adi.model.generic import DocIntelParse
                    from module.azure.wasb.control import AzureController, BlobController as DLink
                    from module.azure.wasb.client import Azure 

                    try:
                        batch_id=self.meta['inputs']['batch_id']
                        sourceFileId=self.meta['inputs']['file_id']
                        batch_details=View.Document(params=batch_id).getLatestRecordsForBatchID()
                        sfid=[str(batch_detail['entity_sfid']) for batch_detail in batch_details if
                            str(batch_detail['entity_trace']) == sourceFileId][0]
                        entity_details=View.Document(params={'subject': sfid}).getEntityDetailsByID()
                        process_details=View().Document(params=sfid).getLatestProcessRecordsById()
                        headers= {
                            'client_id': entity_details['entity_pack']['headers']['clientId'], 
                            'engagement_id':entity_details['entity_pack']['headers']['engagementId'], 
                            'correlation_id':entity_details['entity_pack']['headers']['correlationId'], 
                            'subscription_key':entity_details['entity_pack']['headers']['Mimeo-graffiti-subscrption'],
                            'authorization':self.meta['authority']
                        }
                        configuration=Configuration()
                        configuration.api_key['mimeo-graffiti-subscription'] = headers.get('subscription_key')
                        configuration.api_key['Authorization'] = headers.get("authorization")
                        openapiclient = ApiClient(
                            configration=configuration
                        )
                        logging.info('Downloadling from EDGE File Manager: {}'.format(str(process_details['process_id'])))
                        file_download_response=FileApi(
                            api_client=openapiclient
                        ).get_file_download_id(
                            id=str(process_details['process_id']), 
                            x_client_id=headers.get('client_id'), 
                            x_engagement_id=headers.get('engagement_id'), 
                            x_correlation_id=headers.get('correlation_id'), 
                            _preload_content=False
                        )
                        blob_data=file_download_response.data
                        parsed_docs=json.loads(blob_data)
                        response=parsed_docs
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        result= {
                                'result':'FAILURE', 
                                'message': 'No valid document ACTION was provided'
                            }
                        response=result
                        raise Exception(Config.ERROR_MSG)

                case 'CHAT':
                    from module.azure.adi.model.generic import DocIntelAgent
                    from module.azure.wasb.control import DeeplinkController as DLink
                    from module.azure.wasb.client import Azure 
                    from module.file.edge.file_api import FileApi
                    from module.file.edge.client import ApiClient
                    from module.file.edge.configuration import Configuration
                    try:
                        payload=graph['inputs']
                        query_type=payload['data']['query_type']
                        # batch_id=self.meta['inputs']['batch_id']
                        # sourceFileId=self.meta['inputs']['file_id']
                        # batch_details=View.Document(params=batch_id).getLatestRecordsForBatchID()
                        sfid=[str(batch_detail['entity_sfid']) for batch_detail in batch_details if
                            str(batch_detail['entity_trace']) == sourceFileId][0]
                        entity_details=View.Document(params={'subject': sfid}).getEntityDetailsByID()
                        process_details=View().Document(params=sfid).getLatestProcessRecordsById()
                        headers= {
                            'client_id': entity_details['entity_pack']['headers']['clientId'], 
                            'engagement_id':entity_details['entity_pack']['headers']['engagementId'], 
                            'correlation_id':entity_details['entity_pack']['headers']['correlationId'], 
                            'subscription_key':entity_details['entity_pack']['headers']['Mimeo-graffiti-subscrption'],
                            'authorization':self.meta['authority']
                        }
                        configuration=Configuration()
                        configuration.api_key['mimeo-graffiti-subscription'] = headers.get('subscription_key')
                        configuration.api_key['Authorization'] = headers.get("authorization")
                        openapiclient = ApiClient(
                            configration=configuration
                        )
                        logging.info('Downloadling from EDGE File Manager: {}'.format(str(process_details['process_id'])))
                        file_download_response=FileApi(
                            api_client=openapiclient
                        ).get_file_download_id(
                            id=str(process_details['process_id']), 
                            x_client_id=headers.get('client_id'), 
                            x_engagement_id=headers.get('engagement_id'), 
                            x_correlation_id=headers.get('correlation_id'), 
                            _preload_content=False
                        )
                        blob_data=file_download_response.data
                        #blob_location = DLink(metadata=self.meta).path()
                        #data= await Azure.Manage(ctrl=f'{blob_location}/{sfid}).getBlobFile()
                        parsed_docs= json.loads(blob_data)
                        if query_type.lower().strip() == 'summary':
                            output = DocIntelAgent().get_summary_output(
                                parsed_docs=parsed_docs, 
                                summary_for='chat'
                            )
                        else:
                            query= payload['data']['query']
                            output= DocIntelAgent().get_chat_output(
                                parsed_docs=parsed_docs, 
                                query=query
                            )
                        response= output
                    
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        result= {
                                'result':'FAILURE', 
                                'message': 'No valid document ACTION was provided'
                            }
                        response=result
                        raise Exception(Config.ERROR_MSG)
                        


                case 'EDIT':
                    from module.azure.wasb.client import Azure 
                    from starlette.datastructures import UploadFile
                    from module.azure.wasb.control import AzureController 
                    from collections import defaultdict
                    try:
                        payload=graph['inputs']
                        headers=self.meta.get('headers', {})
                        sfid=graph['subject']
                        edits=payload['data']
                        #blob_location=dynamic_file
                        blob_location='parsed-json'
                        data= await Azure.Manage(ctrl='f{blob_location}/{sfid}').getBlobFile()
                        data= json.load(data)
                        success_edits=defaultdict(list)
                        for edit in edits:
                            fields=edit['field_id'].split(':')
                            if len(fields) > 1:
                                edit= {
                                    'field_id': int(fields[0]), 
                                    'sub_field_id': int(fields[1]), 
                                    'value': edit['value']
                                }
                            else:
                                edit= {
                                    'field_id': int(fields[0]),  
                                    'value': edit['value']
                                }
                            success=False
                            for page in data[sfid]:
                                for field in page['parsed_document']['documents']['fields']:
                                    if 'field_id' in field and 'content' in field and 'sub_field_id' not in edit:
                                        if isinstance(field['value'], str):
                                            field['value']= edit['value']
                                            field['content']= edit['value']
                                            success=True
                                        elif isinstance(field['value'], dict):
                                            field['value'][edit['sub_field']]= edit['value']
                                            success=True
                                    elif 'data' in field:
                                        for row in field['data']:
                                            for cell in row:
                                                if 'field_id' in cell and cell['field_id']== edit['sub_field_id']:
                                                    if 'value' in cell and 'content' in cell:
                                                        if isinstance(cell['value'], str):
                                                            cell['value']= edit['value']
                                                            cell['content']= edit['value']
                                                            success=True
                                    continue
                            if success:
                                success_edits['Success'].append(edit['field_id'])
                            else:
                                success_edits['Fail'].append(edit['field_id'])
                        parsed_doc_file= io.BytesIO(json.dumps(data).encode('utf-8'))
                        upload_file= UploadFile(filename=f"{blob_location}/{sfid}.json", file=parsed_doc_file)
                        await AzureController(metadata={'file': upload_file}).FileToBlobStorage(overwrite=True)


                        def prepareEventWorkflow(metadata):
                            response={
                                'correlation_id': headers.get('correlation_id'), 
                                'engagement_id': headers.get('engagement_id'), 
                                'client_id': headers.get('client_id'), 
                                'batch_id': headers.get('batch_id'), 
                                'status': metadata.get('status'), 
                                'dataSource': [
                                    {
                                        'key': 'sourceFieldId', 
                                        'value': metadata['sourceFieldId'].get('id')
                                    }, 
                                    {
                                        'key': 'extractedFileId',
                                        'value': metadata['extractedFileId'].get('id')
                                    }
                                ]

                            }
                            return response
                        json_fileid= sfid
                        metadata= {
                            'status': 'Fixed' if success_edits else 'Skipped', 
                            'sourceFileId': {
                                'id': sfid
                            }, 
                            'extractedFileId': {
                                'id': json_fileid
                            }
                        }
                        evt_response= prepareEventWorkflow(metadata=metadata)
                        result= {'result': success_edits}
                        response=result
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        result= {
                                'result':'FAILURE', 
                                'message': 'No valid document ACTION was provided'
                            }
                        response=result

                case 'STORE':
                    try:
                        result= {
                                'result':'Success', 
                                'message': 'Method is approved for use in this service'
                        }
                    except:
                        result= {
                                'result':'FAILURE', 
                                'message': 'Method is NOT approved for use in this service'
                        }
                        response=result
                case _:
                    result= {
                            'result':'FAILURE', 
                            'message': 'No valid document ACTION was provided'
                    }
                    response=result

        except ValueError:
            response= Config.ERROR_MSG
            raise ValueError(Config.ERROR_MSG)
        
        self.response = response
        return response


            
        








    
                    