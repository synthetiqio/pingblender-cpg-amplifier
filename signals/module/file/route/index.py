from fastapi import (
    File, 
    UploadFile, 
    APIRouter, 
    Form, 
    HTTPException, 
    status, 
    Header
)
#from module.file.control import AuthController
from fastapi.param_functions import Annotated 
from typing import Dict, List, Any 
import json, logging 

file_module=APIRouter()
@file_module.get(
    path="/{command}/{sfid}", 
    tags=['File Entity Actions'], 
    status_code=status.HTTP_200_OK,
    summary="ENDPOINT: return_filedata - command (str): [DETAILS, HEADINGS, GETLOC, UPDATE]", 
    description="SFID extended file search for details and fields, tables or positions of data \
        files within system controls",
    responses={
        200: {"description": "OK"}, 
        401:{"description": "Unauthorized - Failed to Authenticate with GIF"}, 
        422:{"description":"Malformed Input (Check Types, Variables & Values)"}
    }
)
@file_module.get(
    path="/{command}", 
    tags=['File Entity Actions'], 
    status_code=status.HTTP_200_OK,
    summary="ENDPOING: return_filedata - command (str): [DETAILS, HEADINGS, GETLOC, UPDATE]", 
    description="SFID extended file search for details and fields, tables or positions of data \
        files within system controls",
    responses={
        200: {"description": "OK"}, 
        401:{"description": "Unauthorized - Failed to Authenticate with GIF"}, 
        422:{"description":"Malformed Input (Check Types, Variables & Values)"}
    }
)
async def return_filedata(
    command:str,
    sfid:str=None,
    collection_name:str=None, 
    wasburl:list=None, 
    label:Annotated[str,Form()]=None, 
    name:Annotated[str,Form()]=None,
    type:Annotated[str,Form()]='source',
    mimeo_graffiti_subscription:Annotated[str|None, Header()]=None,
    authorization:Annotated[str|None, Header()]=None 
):
    # ch= await AuthController(auth_token=authorization).validate()
    # if ch['status_code']==401:
    #     raise HTTPException(
    #         status_code=401,
    #         detail=ch
    #     )
    body=locals()
    reqs:Dict[List,Any]={}
    reqs.update({
        'subject':sfid,
        'command':command,
        'inputs':body
    })
    try:
        from core.svc.file.interface import FileAction
        action=FileAction(databody=reqs)
        await action.ActionHandler()
        result:Dict[List,Any]=await action.ResponseHandler()
        result.update({
            'authority': authorization
        })
        return result 
    except ValueError as ve:
        logging.error(f'ERROR: GET FILE {ve}')
        raise HTTPException(
            status_code=500, 
            detail={
                    'result':'FAILURE',
                    'message': str(ve),
                    'payload':None 
            }
        )
    except Exception as e:
        logging.error(f'Unexpected error: {e}', exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    


@file_module.post(
    path="/{command}", 
    tags=['File Entity Controls'], 
    status_code=status.HTTP_200_OK,
    summary="ENDPOINT: return_filedata - command (str): [DETAILS, HEADINGS, GETLOC, UPDATE]", 
    description="SFID extended file search for details and fields, tables or positions of data \
        files within system controls",
    responses={
        200: {"description": "OK"}, 
        401:{"description": "Unauthorized - Failed to Authenticate with GIF"}, 
        422:{"description":"Malformed Input (Check Types, Variables & Values)"}
    }
)
async def file_action(
    command:str,
    file:UploadFile=None,
    data:Dict=None,
    collection_name:str=None, 
    wasburl:list=None, 
    label:Annotated[str,Form()]=None, 
    metadata:Dict[List,Any]=None,
    dest:Annotated[str,Form()]=None,
    type:Annotated[str,Form()]='source',
    mimeo_graffiti_subscription:Annotated[str|None, Header()]=None,
    authorization:Annotated[str|None, Header()]=None 
)->Dict:
    from core.svc.file.interface import FileAction
    #ch= await AuthController(auth_token=authorization).validate()
    # if ch['status_code']==401:
    #     raise HTTPException(
    #         status_code=401,
    #         detail=ch
    #     )
    meta:Dict[List,Any]={}
    try:
        meta.update({'inputs':locals()})
        action=FileAction(
            action=command, 
            file=file, 
            metadata=meta
            )
        runner= await action.ActionHandler()
        result= await action.ResponseHandler()
        return result 
    
    except ValueError as ve:
        logging.error(f'ERROR: GET FILE {ve}')
        raise HTTPException(
            status_code=500, 
            detail={
                    'result':'FAILURE',
                    'message': str(ve),
                    'payload':None 
            }
        )
    except Exception as e:
        logging.error(f'Unexpected error: {e}', exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    


@file_module.post(
    path="s/{command}", 
    tags=['File Entity Controls'], 
    status_code=status.HTTP_200_OK,
    summary="ENDPOINT: return_filedata - command (str): [DETAILS, HEADINGS, GETLOC, UPDATE]", 
    description="SFID extended file search for details and fields, tables or positions of data \
        files within system controls",
    responses={
        200: {"description": "OK"}, 
        401:{"description": "Unauthorized - Failed to Authenticate with GIF"}, 
        422:{"description":"Malformed Input (Check Types, Variables & Values)"}
    }
)
async def files_action(
    command:str,
    files:List[UploadFile],
    collection_name:str=None, 
    wasburl:list=None, 
    label:Annotated[str,Form()]=None, 
    name:str=None,
    metadata:Dict[List,Any]=None,
    sfid:Annotated[str,Form()]=None,
    type:Annotated[str,Form()]='source',
    mimeo_graffiti_subscription:Annotated[str|None, Header()]=None,
    authorization:Annotated[str|None, Header()]=None 
)->Dict:
    # ch= await AuthController(auth_token=authorization).validate()
    # if ch['status_code']==401:
    #     raise HTTPException(
    #         status_code=401,
    #         detail=ch
    #     )
    try:
        multifile_response:Dict[List,Any]={}
        meta:Dict[List,Any]={}
        for file in files:
            meta=locals()
            result= await file_action(
                command=command,
                file=file, 
                metadata=meta,
                label=meta['label']
            )
            multifile_response.update({
                #'authority': authorization,
                'unit_key:'+result['metadata']['details']['entity_sfid']:result
                })
        del meta
        return multifile_response    
    except ValueError as ve:
        logging.error(f'ERROR: GET FILE {ve}')
        raise HTTPException(
            status_code=500, 
            detail={
                    'result':'FAILURE',
                    'message': str(ve),
                    'payload':None 
            }
        )
    except Exception as e:
        logging.error(f'Unexpected error: {e}', exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )