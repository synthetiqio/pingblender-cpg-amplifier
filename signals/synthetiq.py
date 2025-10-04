
import os, json, logging, requests
from typing import Dict, List, Any
logging.basicConfig(level=logging.INFO)
from core.ctrl.cors import EnvironmentController as EC
from core.model.request import Matrix,DocManage,ChatManage,AzureManage
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi import (
    FastAPI, UploadFile,
    Request, Depends, File, 
    Form, responses, HTTPException, 
    status, APIRouter
)

cors_list=EC.get().urls()
#high level configurations.
api_path=os.getenv("API_PATH", "/v1/api").rstrip('/')
bet : str = os.getenv("APP_ROUTE")
app = FastAPI(
    root_path=api_path,
    summary="SynthetIQ Signals"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_list,
    allow_methods=["*"], 
    allow_headers=["*"],
    )


#root service level endpoints for SynthetIQ Signals Graffiti AI Amplifier.
@app.get(path="/")
async def live_check():
    return json.dump({
            'response': 'OK', 
            'msg': 'Pingblender on SynthetIQ Signals'
    })

#File Services Routes
from module.file.route.index import file_module as file_svc
app.include_router(file_svc,prefix='ctrl/0')

