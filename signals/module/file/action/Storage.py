from fastapi import UploadFile, File
from typing import Dict, List, Any


class AzureStore:

    async def upload(
            file : UploadFile = File(...)
    ):
        from module.azure.wasb.client import AzureStorage
        from module.azure.wasb.config import WASB as Store

        env : Dict[List, Any] = Store.Default.getEnvVariables()
        store = AzureStorage(env=env, file=file)
        result = await store.uploadBlob()

        return result