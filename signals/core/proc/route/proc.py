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
    path="/{command}/{prid}", 
    tags=["CORE: Utilities"], 
    status_code=status.HTTP_200_OK, 
    description="Process State | Endpoint: actions affailiated with getting intermediates", 
    summary="ENDPOINT: process_query - Command Interface", 
    responses={
        200: {"description":"OK"}, 
        401:{"description": "Unauthorized - Failed to Authenticate with SSO"}, 
        422:{"description": "Malformed Input (check types and values)"},         
    }
)
@module.post(
    path="/{command}", 
    tags=["CORE: Utilities"], 
    status_code=status.HTTP_200_OK, 
    description="Process State | Endpoint: actions affailiated with getting intermediates", 
    summary="ENDPOINT: process_query  -command (str): [QUEUE]", 
    responses={
        200: {"description":"OK"}, 
        401:{"description": "Unauthorized - Failed to Authenticate with SSO"}, 
        422:{"description": "Malformed Input (check types and values)"},         
    }
)
async def process_inquiry(
    command:str,
    prid:Optional[str]=None,
    batch_id:Optional[str]=None, 
    data:dict=None, 
    authorization:Annotated[str|None, Header()]=None,
    mimeo_graffiti_subscription:Annotated[str|None, Header()]=None, 
    background_tasks:BackgroundTasks=None
):
    from core.svc.process.interface import ProcessAction as ThisAction
    from core.model.request import ProcManage as RequestModel
    try:
        body:RequestModel=data 
        reqs:Dict[List,Any]={}
        reqs.update({
            'subject':prid,
            'command':command,
            'inputs':body,
            'authority':authorization,
            'background_task':background_tasks
        })
        action=ThisAction(reqs)
        await action.ActoinHandler()
        response = await action.ResponseHandler()
        return response 
    except ValueError as ve:
        logging.error(f'ERROR: Document - {ve}')
        raise HTTPException(
            status_code=500,
            res={ 
                'result':"FAILURE", 
                'message':f'CLASS: {__name__} created an error',
                'payload':f'Error Details: {ve}'
            }
        )
    except Exception as e:
        logging.error(f'Unexpected Error: {e}', exc_info=True)
        raise HTTPException(status_code=500,detail=str(e))