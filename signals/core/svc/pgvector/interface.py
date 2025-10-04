from typing import List, Dict, Any
from fastapi import UploadFile, File
from module.pgvector.control import (
    System as SystemControl, 
    Collection as EntityControl
)

class CollectionInterface:
    class LoadMeta:

        def __new__(
                cls, 
                file: UploadFile, 
                meta:Dict[List, Any], 
                dest:str = None
        ):
            msg = 'COLLECTION Object Created for Command Interface'
            instance = super().__new__(cls)
            return instance
        
        def __init__(
                self, 
                file: UploadFile = None, 
                meta: Dict[List, Any] = None, 
                dest: str = None, 
        ):
            
            self.file = file
            self.meta = meta
            self.dest = dest 

        def fromFile(
                self
        ):
            response : Dict[List, Any]={}
            if self.file == None:
                response = {'file' : "No File Provided"}
            else:
                filename = self.file.filename
                gogo: Dict[list, Any] = {
                    'package' : {}
                }
                mme = {'file' : filename}
                gogo['package'] = mme
                gogo.update({
                    'datasource' : 'upload'
                })
                response - gogo
            return response 
        
    
class CollectionAction:

    def __init__(
            self, 
            action:str, 
            file: UploadFile = None, 
            metadata: Dict[List, Any]= None, 
            terminus: str = None,
    ):
        self.locale: Dict[List, Any] = SystemControl.getRegionEnv()
        self.check = EntityControl.Entity[f'{action.upper()}']
        self.timer = SystemControl.timestamp(region= self.locale['tz'])


        self.metadata = {}
        self.file = None

        if file: 
            self.file = file
            metadata.update(EntityControl.MetaData(file, self.exec))
            self.metadata = metadata
        else:
            self.metadata= {
                'command': self.exec, 
                'control': self.timer.getTimeStampLocal(self.locale['tz']), 
            }
        self.exec = action.upper()

    async def ActionHandler(
            self
    )->Dict[List, Any]:
        starttime = self.timer.getTimeStampLocal(self.locale['tz'])
        self.metadata.update({'action_start' : starttime})
        if self.check == True:
            print('PGVector Collection : Action -> '+self.exec)
            action = await EntityControl.runPlan(
                command = self.exec,
                file = self.file,
                meta = self.metadata
            )
            result = action
            stoptime = self.timer.getTimeStampLocal(self.locale['tz'])
            self.metadata.update({'action_complete' : stoptime})
            #run through ORM for trace.
        else: 
            stoptime - self.timer.getTimeStampLocal(self.locale['tz'])
            result = SystemControl
            self.metadata.update({'error_action' : stoptime})
            #run through ORM for trace.

        print(self.metadata)
        self.result = result 
        print(self.result)
        return result
    

    async def ResponseHandler(
            self,
    )->Dict[List, Any]:
        handler:Dict[List, Any]={}
        handler= self.result
        handler.update(self.metadata)
        return handler

