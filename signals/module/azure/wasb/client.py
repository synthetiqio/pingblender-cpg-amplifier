import os, datetime
from azure.core.credentials import AzureSasCredential as ASC
from azure.storage.blob.aio import BlobServiceClient as BSC, BlobClient as BC

from module.azure.wasb.config import WASB
from module.pretzl.parser import PRETZL, PORTL

from fastapi import UploadFile, File
from typing import Dict, Any, List
from uuid import uuid4
from io import BytesIO

class Azure:

    ENV:Dict[List, Any]= WASB.Default.getEnvVariables()

    try:
        account_url:str= ENV['url']
        account_name = ENV['name']
        account_key = ENV['access_key']
        account_container = ENV['container']
        account_landing = ENV['ingest']
        sas_url = f'{account_url}{account_container}'
        loc:str=None
    except:
        raise ValueError("Azure Environment Variables are not set")

    # def __init__(
    #         self,
    #         env : Dict[List, Any] = WASB.Default.getEnvVariables(), 
    #         file : UploadFile = File(...)
    #     ):
    #     if file:
    #         self.file = file
    #     else: 
    #         self.file = None


    #     self.account_url = env["url"]
    #     self.account_name = env['name']
    #     self.account_key = env['access_key']
    #     self.account_container = env['container']
    #     self.account_landing = env['ingest']

    #     self.sas_token = self._createServicesSAS()
    #     self.account_credential = ASC(signature=self.sas_token)

    #     self.blobSasUrl = self.account_url + self.account_container

    #     self.service_client : BSC = BSC(
    #         account_url = self.blobSasUrl, 
    #         credential=self.account_credential
    #     )

    #     self.blob_client : BC = BC(
    #         container_name=self.account_container, 
    #         account_url = self.blobSasUrl, 
    #         credential = self.account_credential, 
    #         blob_name = file.filename
    #     )


    def createServiceSAS()->str:
        from azure.storage.blob import (
            ContainerSasPermissions as CSP, 
            generate_container_sas
        )
        key : str = Azure.account_key
        start_time = datetime.datetime.now(datetime.timezone.utc)
        expiry_time = start_time+datetime.timedelta(hours=2)
        try:
            sas_token = generate_container_sas(
                account_name = Azure.account_name,
                container_name = Azure.account_container, 
                account_key = key, 
                permission = CSP(
                    read=True, 
                    write=True, 
                    delete=True, 
                    list=True
                ), 
                expiry=expiry_time, 
                start=start_time
            )
        except:
            raise ValueError("Azure Storage SAS Token was not received")   
        return sas_token
    
    def createBlobSAS(
            bloburl:str
    ):
        from azure.storage.blob import BlobSasPermissions, generate_blob_sas
        start_time=datetime.datetime.now()
        expiry_time=start_time+datetime.timedelta(hours=12) #configurable
        sas_token=generate_blob_sas(
            account_name=Azure.account_name, 
            container_name=Azure.account_container,
            blob_name=bloburl,
            account_key=Azure.account_key, 
            permission=BlobSasPermissions(
                read=True, 
                create=True, 
                add=True,
                write=True, 
                tag=True
            ),
            expiry=expiry_time, 
            start=start_time
        )
        return sas_token
    

    class Utils:

        def __init__(
                self, 
                blobname:str,
                container:str=None,
        ):
            self.name=blobname
            self.client=None
            if container==None:
                self.container=Azure.account_container

        def getContainer(self):
            return self.container
        
        def getServiceClient(self):
            try: 
                self.client= BSC(
                    account_url= Azure.account_url, 
                    credential=ASC(signature=Azure.createServiceSAS())
                )
                return self.client
            except:
                raise ValueError('ServiceClient was not created from Azure.Utils')
            
        def getBlobClient(self):
            try:
                self.client= BC(
                    account_url=Azure.account_url, 
                    container_name=Azure.account_container,
                    blob_name=self.name,
                    credential=ASC(signature=Azure.createServiceSAS()),
                )
                return self.client
            except:
                raise ValueError("BlobClient was not created from Azure.Utils")
            
        
    class Container:

        def __init__(
                self,
                name:str, 
                permit:Dict[List, Any]=None
        ):
            self.container_name=name
            self.service:BSC=BSC(
                account_url=Azure.account_url,
                credential=ASC(
                    signature=ASC(signature=Azure.createServiceSAS())
                )
            )

        def create(
                self
        )->bool:
            try:
                self.service.create_container(
                    self.container_name
                )
                return True
            except:
                return False
                
    class Manage:

        def __init__(
                self, 
                ctrl:str=None,
                batch_id:str=None,
                collection_id:str=None,
                owner_id:str=None,
                wasbloc:str=None
        ):
            self.load:BytesIO=None
            self.barrier:str=None

            self.subj:uuid4=ctrl if ctrl is not None else None
            self.batch:uuid4=batch_id if batch_id is not None else None
            self.owner:str=owner_id if owner_id is not None else None
            self.coll:str=collection_id if collection_id is not None else None
            self.qualblobaddr=wasbloc if wasbloc is not None else None

            self.service:BSC=BSC(
                account_url=Azure.account_url, 
                credential=ASC(signature=Azure.createServiceSAS())
            )

            self.container=self.service.get_container_client(
                Azure.account_container
            )


        def _getClient(self):
            client=BC(
                container_name=Azure.account_container, 
                account_url=Azure.account_url,
                credential=ASC(signature=Azure.createServiceSAS()), 
                blob_name=self.qualblobaddr
            )
            self.client= client
            return self.client
        

        def _generateTraceID(str=None)->str:
            return str(uuid4())
        

        def _buildBlobPath(
                self, 
                fn:str=None,
        )->str:
            filename:str=None
            if fn !=None & self.filename==None:
                filename=fn
            elif self.filename != None & fn == None:
                filename= self.filename
            else:
                filename= str(uuid4())
            return Azure.account_landing+'/'+filename+'.json'
        

        async def getBlobFile(
                self, 
                file_name:str=None, 
                file_type:str=None      
        ):
            filename = f'{self.subj}.{file_type}'
            self.qualblobaddr=Azure.account_landing+'/'+filename
            c=self._getClient()
            async with c:
                blob_data= await c.download_blob()
                data= await blob_data.readall()
            return data 
        

        async def getBlobFileData(
                self, 
                blobname
        ):
            self.qualblobaddr=blobname
            c=self._getClient()
            async with c:
                blob_data= await c.download_blob()
                data = await blob_data.readall()
            return data

        def getService(self):
            return self.service
        
        def getContainer(self):
            return self.container
        
        def upload(
                self, 
                src:str,
                dst:str
        ):
            if(os.path.isdir(src)):
                self.uploadFolder(
                    src, 
                    dst
                )
            else:
                self.uploadFile(
                    src, 
                    dst
                )

        def uploadFile(
                self, 
                src:str,
                dst:str
        ):
            client=self._getClient()
            print(f'[STORAGE][Azure WASB] State: Uploading {src} to {dst}')
            try:
                with open(src, 'rb') as data:
                    client.upload_blob(
                        name=dst, 
                        data=data, 
                        overwrite=True
                    )
                client.close()
            except:
                raise Exception("The Moving.uploadFile function failed")
            

        def uploadFolder(
                self, 
                src:str, 
                dst:str,
        ):
            prefix= '' if dst == '' else dst + '/'
            prefix += os.path.basename(src) + '/'
            try:
                for root, dirs, files in os.walk(src):
                    for name in files:
                        dir_part= os.path.relpath(
                            root, 
                            src
                        )
                        dir_part= '' if dir_part == '.' else dir_part + '/'
                        file_path= os.path.join(
                            root, 
                            name
                        )
                        blob_path= prefix+dir_part+name
                        self.uploadFile(
                            src=file_path, 
                            dst=blob_path
                        )
            except:
                raise Exception("Blob storage functionality failed in Azure")
            

        def downloadURL(
                self,
                url:str
        ):
            u=f'{Azure.sas_url/{url}}'
            self.qualblobaddr=u 
            c=Azure().createBlobSAS(bloburl=url)
            if c:
                return f'{u}?{c}'
            else:
                return f'{u}'+'NO_SAS_AVAILABLE'
        
        def downloadUrlUsingBlobUrl(self, blob_url):
            from urllib.parse import urlparse
            parsed_url= urlparse(blob_url)
            path= parsed_url.path
            if path.startswith('/'):
                path=path[1:]
            parts=path.split('/', 2)
            blob_path=parts[2]
            sas_details= Azure().createBlobSAS(bloburl=blob_path)
            if sas_details:
                return f'{blob_url}?{sas_details}'
            else:
                return f'{blob_url}'+ 'NO_SAS_AVAILABLE'
    
        def download(
                self, 
                src:str,
                dst:str
        ):
            if not dst:
                raise Exception('a Destination (dst) must be provided')
            try:
                blobs= self.listFiles(
                    src,
                    recursive=True
                )
            except:
                raise Exception("ListFiles Function has failed.")
            if blobs:
                if not src == '' and not src.endswith('/'):
                    src+= '/'
                if not dst.endswith('/'):
                    dst += '/'
                dst += os.path.basename(os.path.normpath(src))+'/'
                blobs= [src+blob for blob in blobs]
                for blob in blobs:
                    bdst= dst+os.path.relpath(
                        path=blob, 
                        start=src
                    )
                    try:
                        self.downloadFile(
                            src=blob,
                            dst=bdst
                        )
                    except:
                        raise Exception('Azure WASB Download Function failed.')
            else:
                self.downloadFile(src, dst)

        def downloadFile(
                self,
                src: str,
                dst: str,
        ):
            if dst.endswith('.'):
                dst+='/'
            bdst=dst+os.path.basename(src) if dst.endswith('/') else dst
            print(f'Downloading {src} to {bdst}')
            os.makedirs(
                name=os.path.dirname(bdst ),
                exist_ok=True
            )
            bc= self.container.get_blob_client(blob=src)
            with open(bdst, 'wb') as file:
                data= bc.download_blob()
                file.write(data.readall())



        def listFiles(
                        self, 
                        path: str, 
                        recursive=False,
        )->list:
            if not path == '' and not path.endswith('/'):
                path += '/'
                blob_iter= self.container.list_blobs(
                    name_starts_with=path
                )
                files=[]
                for blob in blob_iter:
                    rdir= os.path.relpath(
                        path=blob.name,
                        start=path
                    )
                    if rdir != '_SUCCESS' and (
                        not '/' in rdir or recursive
                    ):
                        files.append(rdir)
                return files 
            
        def listFilePath(
                self, 
                path:str, 
                recursive=False,
        ):
            tr=Azure.account_landing
            if not path == '' and not path.endswith('/'):
                path += '/'
            blob_iter = self.container.list_blobs(name_starts_with=path)
            paths=[]
            for blob in blob_iter:
                relative_path = os.path.relpath(blob.name, path)
                if relative_path != '_SUCCESS' and (
                    not '/' in relative_path or recursive
                ):
                    paths.append(
                        tr+blob.name
                    )
            return paths 
        

        def listDirs(
                self, 
                path:str, 
                recursive=False
        ):
            if not path == '' and not path.endswith('/'):
                path += '/'
            blob_iter= self.container.list_blobs(
                name_starts_with=path
            )
            dirs=[]
            for blob in blob_iter:
                rdir= os.path.dirname(
                    os.path.relpath(
                        path=blob.name, 
                        start=path
                    )
                )
                if rdir and (recursive or not '/' in rdir) and not rdir in dirs:
                    dirs.append(rdir)
            return dirs
        

        def remove(
                self, 
                path:str
        ):
            blobs = self.listFiles(
                path=path,
                recursive=True
            )
            if not blobs:
                return "Blob doesn't exist on this path"
            elif len(blobs) == 1 and blobs[0] == 'placeholder.txt':
                return 'Only the placeholder file exists in folder.'
            if not path== '' and not path.endswith('/'):
                path += '/'
            blobs= [path+blob for blob in blobs if blob != 'placeholder.txt']
            print('Deleting the following files: ')
            print("\n".join(blobs))
            self.client.delete_blob(*blobs)

        def removeDir(
                self, 
                path:str
        ):
            blobs = self.listFiles(
                path=path, 
                recursive=True 
            )
            if not blobs:
                return "The blob doesn't exist in this path"
            elif len(blobs)==1 and blobs[0]=='placeholder.txt':
                return "Only the placeholder file exists in the folder"
            if not path=='' and not path.endswith('/'):
                path+='/'
            blobs=[path+blob for blob in blobs if blob != 'placeholder.txt']
            print("Deleting the following files")
            print('\n'.join(*blobs))
            self.client.delete_blob(*blobs)



        
        class List:
            def items(
                    self
            )->list:
                op = []
                try:
                    bl= Azure.Manage().getContainer().list_blobs()
                    for blb in bl:
                        op.append(blb)
                    return op
                except:
                    return op 
            
        async def exists(
                self, 
                path:str
        )->bool:
            blob_iter = self.container.list_blobs()
            async for blob in blob_iter:
                if blob.name.endswith(path):
                    return True
            return False


    class Moving:

        def __init__(
                self, 
                package: Dict[List, Any]=None,
        ):
            self.singleton= package
            self.ac = ASC(
                signature=Azure.createServiceSAS()
            )
            if self.start != None & 'path' in self.start['inputs']:
                Azure.loc= self.singleton['inputs']['path']
                self.stream= PORTL.Binary(
                    path=Azure.loc, 
                ).getBinaryStream()

            self.blobcservice:BSC= BSC(
                account_url=Azure.account_url, 
                credential=self.ac
            )


        def _createBlob(
                self, 
                path
        )->BytesIO:
            try: 
                stream= PORTL.Binary(path=path).getBinaryStream()
                return stream
            except:
                raise ValueError("Blob was not created from MOVING")
    
        def _repositionBlob(
                self, 
                blob: BytesIO
        )->Dict[List, Any]:
            pass

        def setBlobPosition(
                self, 
                current:str, 
                target:str,
        ):
            pass

        async def fromPath(
                self
        )->Dict[List,Any]:
            from io import BytesIO
            from module.pretzl.parser import PORTL
            treat = PORTL.Binary(path=Azure.loc)
            blob: BytesIO = await treat.getBinaryStream()
            fn= blob.name 
            try:
                lbc:BC=self.bc(
                    container_name=Azure.account_container, 
                    account_url=Azure.sas_url, 
                    credential=self.ac,
                    blob_name=fn
                )
            except:
                raise ValueError('BlobClient was not created')
            
            check = await lbc.exists()
            if(check== False):
                await lbc.upload_blob(
                    data=blob, 
                    blob_type='BlockBlob', 
                    metadata={
                        'test': fn
                    }
                )
                await lbc.close()
                result={
                        'result': 'SUCCESS', 
                        'message': f'[STORAGE] (WASB)- {fn} uploaded', 
                        'file_url': f'{Azure.account_url}{Azure.account_container}/{Azure.account_landing}/{fn}'
                }
            else:
                result={
                        'result': 'FAILRE', 
                        'message': f'[STORAGE] A file with that name exists in the storage location', 
                        'file_url': f'{Azure.account_url}{Azure.account_container}/{Azure.account_landing}/{fn}'
                }
            return result 
        

    class Storing:

        def __init__(
                self, 
                file, 
                meta:Dict[List, Any]= None
            ):
            if file:
                self.file:bytes=file
                self.meta=meta['inputs'] if meta else None
                self.metafile:UploadFile = self.meta['file'] if self.meta else self.file 

            from module.azure.wasb.control import BlobController 
            self.set_blob: str= BlobController(filename=self.metafile.filename).setWasbPath()
            self.ac = ASC(signature=Azure.createServiceSAS())
            self.service_client:BSC= BSC(
                account_url=Azure.account_url, 
                credential=self.ac 
            )
            self.blob_client:BC = BC(
                container_name=Azure.account_container, 
                account_url=Azure.account_url,
                credential=self.ac, 
                blob_name=self.set_blob
            )


        def _getClient(
                self
        ):
            client=BC(
                container_name=Azure.account_container, 
                account_url=Azure.account_url, 
                credential=ASC(signature=Azure.createServiceSAS()), 
                blob_name=self.set_blob
            )
            self.client = client
            return self.client 
        
        
        async def getBlobClient(
                self
        )->BSC:
            wasb: BSC = self.service_client
            return wasb 
        
        async def UploadFile(
                self, 
                overwrite=True
        )->Dict[List,Any]:
            from io import BytesIO
            from core.model.document import Construct
            result:Dict[str, Any]= {}
            blob= BytesIO(self.metafile.file.read())
            blob_client = self.blob_client
            await blob_client.upload_blob(
                data=blob, 
                overwrite=overwrite, 
                blob_type='BlockBlob', 
                metadata={
                    'test': self.metafile.filename
                }
            )
            await blob_client.close()
            result = {
                        'result': 'SUCCESS', 
                        'message': f'[STORAGE] (WASB)- {self.metafile.filename} is uploaded to {Azure.account_landing}',
                        'file_url': f'{Azure.account_url}{Azure.account_container}/{Azure.account_landing}/{self.metafile.filename}'
                    }
            return result 
        
        async def _getAccessKey(self)->str:
            return str(Azure.account_key)
        

        async def getAccountName(
                self
        )->str:
            return str(Azure.account_name)
            