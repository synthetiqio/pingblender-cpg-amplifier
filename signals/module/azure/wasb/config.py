import os
from enum import Enum
from typing import Dict, List, Any
import core.config as CoreConfig
from dotenv import load_dotenv
load_dotenv()

class WASB:

    #root error message for the module. build on based on details of Exceptions.
    ERROR_MSG:Dict[List,Any]={
            'result':'FAILURE', 
            'message': '[WASB] - Storage option is not configured properly', 
            'payload': None 
    }

    #WASB current service feature actions.
    class Action(Enum):
        STORE:bool=True
        LIST:bool=True 
        ACTION_1:bool=True 
        DOWNLOAD:bool=True
        VIEWFILE:bool=True 


    class Ext:

        def ErrorMSG():
            return CoreConfig.Env.ERROR_MSG
        
        def Env():
            return CoreConfig.Env 
        
        def Sys():
            return CoreConfig.System


    class Default(Enum):
        ACCOUNT_URL:str= os.getenv("AZURE_STORAGE_URL")
        ACCESS_KEY:str= os.getenv("AZURE_STORAGE_ACCESS_KEY")
        ACCOUNT_NAME:str= os.getenv("AZURE_STORAGE_ACCOUNT")
        ACCOUNT_CONTAINER:str= os.getenv("AZURE_STORAGE_ACCOUNT_CONTAINER")
        ERROR_CODE:str= "A configuration variable is NOT SET"
        FILE_INGEST:str= 'data-in'
        FILE_OUTPUT:str= 'data-out'

        def getEnvVariables()->Dict:
            env : Dict = {}
            try:
                env = {
                    'url' : WASB.Default.ACCOUNT_URL.value,
                    'name' : WASB.Default.ACCOUNT_NAME.value, 
                    'access_key' : WASB.Default.ACCESS_KEY.value, 
                    'container' : WASB.Default.ACCOUNT_CONTAINER.value, 
                    'ingest' : WASB.Default.FILE_INGEST.value
                }
            except: 
                env = {
                    'error_code' : WASB.Default.ERROR_CODE.value
                }
            return env

    class ROUTES(Enum):
        DATA_IN : str = 'data-in'
        DATA_OUT : str = 'data-out'
        SYS_LOGS : str = 'logs'
        TMP_DATA : str = 'tmp'
        ARCHIVE : str = 'archive'
        METADATA : str = 'meta'
        ERROR_CODE : dict = {
                'result':'FAILURE', 
                'message': '[WASB]: Routing failure in core config controller.',
                'payload': None 
        }


        def getRoutes()->Dict:
            rte : Dict
            try: 
                rte = {
                    'ingest' : WASB.ROUTES.DATA_IN.value, 
                    'product' : WASB.ROUTES.DATA_OUT.value,
                    'tmp' : WASB.ROUTES.TMP_DATA.value, 
                    'arch' : WASB.ROUTES.ARCHIVE.value, 
                    'meta' : WASB.ROUTES.METADATA.value

                }
            except:
                rte = {
                    'error_code' : WASB.ROUTES.ERROR_CODE.values
                }
            return rte