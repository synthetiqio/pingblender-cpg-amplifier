from fastapi import (
    APIRouter,
    status,
    HTTPException, 
    Header,
    BackgroundTasks
)
from fastapi.param_functions import Annotated 
from typing import Dict, List, Optional, Any
import json, logging 
from core.model.request import DocManage

module=APIRouter()

@module.post(
    path="/{command}/{ohid}", 
    tags=["CORE: ADI Commands"], 
    status_code=status.HTTP_200_OK, 
    description="Document Entity Endpoint: actions affiliated with file for ingest", 
    summary="ENDPOINT: Azure Document Intelligence - Command Interface", 
    responses={
        200: {"description":"OK"}, 
        401:{"description": "Unauthorized - Failed to Authenticate with SSO"}, 
        422:{"description": "Malformed Input (check types and values)"},         
    }
)
@module.post(
    path="/{command}", 
    tags=["CORE: ADI Commands"], 
    status_code=status.HTTP_200_OK, 
    description="Document Entity Endpoint: actions affiliated with file for ingest", 
    summary="ENDPOINT: Azure Document Intelligence - Command Interface", 
    responses={
        200: {"description":"OK"}, 
        401:{"description": "Unauthorized - Failed to Authenticate with SSO"}, 
        422:{"description": "Malformed Input (check types and values)"},         
    }
)
async def document_action(
    command:str,
    sfid:Optional[str]=None,
    batch_id:Optional[str]=None, 
    data:dict=None, 
    authorization:Annotated[str|None, Header()]=None,
    mimeo_graffiti_subscription:Annotated[str|None, Header()]=None, 
    background_tasks:BackgroundTasks=None
):
    from core.svc.document.interface import Action as DocAction
    try:
        body:DocManage=data 
        reqs:Dict[List,Any]={}
        reqs.update({
            'subject':sfid,
            'command':command,
            'inputs':body,
            'authority':authorization,
            'background_task':background_tasks
        })
        action=DocAction(reqs)
        await action.ActionHandler()
        response = await action.ResponseHandler()
        return response 
    except ValueError as ve:
        logging.error(f'ERROR: Document - {ve}')
        raise HTTPException(
            status_code=500,
            res={ 
                'result':"FAILURE", 
                'message':str(ve),
                'payload':None 
            }
        )
    except Exception as e:
        logging.error(f'Unexpected Error: {e}', exc_info=True)
        raise HTTPException(status_code=500,detail=str(e))