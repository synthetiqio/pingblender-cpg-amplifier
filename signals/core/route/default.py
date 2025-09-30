from fastapi import File, UploadFile, APIRouter, Form, status, HTTPException, Body, responses, BackgroundTasks
from typing import Dict, List, Any, Annotated, Optional 
import json, logging 

router = APIRouter()
@router.get(
    path='/healthcheck', 
    responses={
        200: {'description': "OK"}, 
        401: {'description': "Unauthorized - Failed Authentication"}, 
        422: {'description': "Malformed Input (Check Types & Values)"}
    }
)
async def health_check(
):
    return {
        'result' : 'Success - the router is operating as intended.'
    }