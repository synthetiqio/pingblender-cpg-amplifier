import os 
from enum import Enum
from typing import Any, Dict, List


"""Storage Mapping and Routing Configurations for Signals Systems."""
class STORAGE:


    """ ROUTES in core ETL path for storage and data mapping across the 
    controls plane.
    """
    class ROUTES(Enum):
        DATA_IN : str = 'data-in'
        DATA_OUT : str = 'data-out'
        SYS_LOGS : str = 'logs'
        TMP_DATA : str = 'tmp'
        ARCHIVE : str = 'archive'
        METADATA : str = 'meta'
        ERROR_CODE : dict = {'message' : 'Storage Routing Control Failure. \
                              Check Configuration Settings'}
    

        """ Get all defined routes for cloud storage system
        Returns:
            Dict: Dictionary of pre-defined routes for channeling through
            controls. 
        """
        def getRoutes()->Dict:
            rte : Dict = {}
            try: 
                rte = {
                    'ingest' : STORAGE.ROUTES.DATA_IN.value, 
                    'product' : STORAGE.ROUTES.DATA_OUT.value,
                    'tmp' : STORAGE.ROUTES.TMP_DATA.value, 
                    'arch' : STORAGE.ROUTES.ARCHIVE.value, 
                    'meta' : STORAGE.ROUTES.METADATA.value
                }
            except:
                rte = {
                    'error_code' : STORAGE.ROUTES.ERROR_CODE.values
                }
            return rte
        

    """ Default configuration for Azure WASB Storage. 
    These are environment variables that should be set in the deployment 
    development environment. This will conform to Azurite and Azure Cloud
    storage accounts. This can be overridden by AWS S3 or GCP Storage when
    the account is configured for commercial license. 
    """
    class Default(Enum):
        ACCOUNT_URL : str = os.environ.get('AZURE_STORAGE_URL')
        ACCESS_KEY : str = os.environ.get('AZURE STORAGE_ACCESS_KEY')
        ACCOUNT_NAME : str = os.environ.get('AZURE_STORAGE_ACCOUNT')
        ACCOUNT_CONTAINER : str = os.environ.get('AZURE_STORAGE_ACCOUNT_CONTAINER')
        ERROR_CODE : str = "A configuration variable is NOT SET"
        FILE_INGEST : str = 'data-in'
        FILE_OUTPUT : str = 'data-out'


        def getEnvVariables()->Dict:
            env : Dict = {}
            try:
                env = {
                    'url' : STORAGE.Default.ACCOUNT_URL.value, 
                    'name' : STORAGE.Default.ACCOUNT_NAME.value, 
                    'access_key' : STORAGE.Default.ACCESS_KEY.value, 
                    'container' : STORAGE.Default.ACCOUNT_CONTAINER.value, 
                    'ingest' : STORAGE.Default.FILE_INGEST.value
                }
            except: 
                env = {
                    'error_code' : STORAGE.Default.ERROR_CODE.value
                }
            return env