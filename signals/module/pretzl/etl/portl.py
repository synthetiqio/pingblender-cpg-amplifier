import aiofiles, json, pandas as pd
from fastapi import UploadFile
from io import BytesIO

class Binary:

    def __init__(
            self, 
            path:str = None, 
            sfid:str = None, 
            file:UploadFile = None
    ):
        self.file: UploadFile= None 
        self.file_binary:BytesIO= None 

        self.path = path
        if file != None & sfid == None:
            self.file = self._convertToStandard(file)
        if path !=None & sfid == None & file== None:
            self.file = self._convertToStandard(open(path, 'rw'))
        if sfid != None & path == None & file == None:
            self.file = self._convertToStandard(self.getBinaryStream())


    def _readFile(self):
        return self.file.read()
    
    def _writeFile(self, data):
        self.file.write(data)
        return True
    
    def _closeFile(self):
        self.file.close()
        return True 
    

    def _convertToStandard(
            self, 
            file: UploadFile
    )->UploadFile:
        self.file = file 
        return self.file 
    
    def _getFileName(self):
        return self.path.split('.')[0]
    
    def _getFileExtension(self):
        return self.path.split('.')[1]
    
    def convertToDataFrame(self):
        return pd.read_csv(self.path)
    
    def convertToJSON(self):
        return json.load(self.path)
    
    async def getBinaryStream(
            self
    )->BytesIO:
        from module.pgvector.control import Collection as CO 
        if self.sfid != None & self.path == None:
            op = CO.Entity.Query(lookup_key=self.sfid).bySfid()
        try:
            if self.sfid != None & self.path == None:
                op = CO.Entity.Query(lookup_key=self.sfid).bySfid()
                async with aiofiles.open(
                    op, 
                    'wb', 
                ) as out:
                    content= await out.read()
                    ex:BytesIO = BytesIO(content)

        except:
            ex = print("[PRETZL | PORTL]: ERROR - No BINARY conversion was possible")
        self.file_binary = ex 
        return self.file_binary