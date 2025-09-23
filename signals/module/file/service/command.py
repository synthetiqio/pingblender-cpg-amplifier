import os
from enum import Enum 
from typing import Dict, List, Any
from fastapi import UploadFile

from module.file.config import FILE as ConfigController
from langchain_core.documents import Document 

class FileCommand:

    def __init__(
                self, 
                comm : str, 
                file : UploadFile, 
                meta : Dict[List, Any], 
                name : str = None, 
                spot : str = None
            ):
            self.comm = comm 
            self.name : str = __name__
            self.file : UploadFile = file
            self.meta : Dict[List, Any] = meta

            self.response:Dict[List,Any]


    def _getCommand(self)->str:
          command = self.comm
          return command 
    


    async def Action(
                self, 
                metadata : Dict[List, Any] = None
            )->Dict[List,Any]:

            data : Dict[List, Any] = {}
            response : Dict[List, Any] = {}
            
            if self.file != None:
                from module.file.control import File as RML
                file = self.file 
                self.file.filename=str(file.filename).replace(' ', '_')

            print(metadata)
            self.meta = metadata 
            casestr = self._getCommand()
            configs = self.meta 


            try:
                  match str(casestr).upper():
                        
                        case 'UPLOAD':
                              outcome:Dict[List,Any]={}
                              from module.file.control import File as FLO
                              from module.pgvector.control import Collection as R
                              
                              outcome = await FLO(
                                    file=self.file, 
                                    fn = self.file.filename, 
                                    construct=configs
                              ).fileUpload()
                              print("[FILE] - Controller Accessed.")
                              outcome.update({'headers':
                                              { 
                                                    'genesis' : self.file.filename,
                                                    'bytes' : self.file.size
                                              }})
                              
                              tracer = R.Entity.Receive(package=outcome)
                              result = await tracer.getCollectionControls()
                              print("[FILE] : UPLOAD Command : Ingest and file trace for functions.")
                              response = result 

                        case 'BUPLOAD':
                              from module.file.control import File as FileControl
                              from module.pgvector.control import Collection 
                              from module.file.action.subroutine.local import Put
                              outcome= await FileControl(
                                    file=self.file, 
                                    fn=self.file.filename, 
                                    construct=configs 
                              ).Blobstore()
                              outcome.update({
                                    'headers': {
                                          'genesis':self.filename, 
                                          'bytes':self.file.size
                                    }
                              })
                              tracer=Collection.Entity.Receive(package=outcome)
                              result = await tracer.getCollectionControls()
                              await Put(blob_name=result['event_logged']['blob']).load()
                              print("[FILE] - UPLOAD Command : Ingest file and trace for DS function.")
                              response = result 


                        case 'REVIEW':
                              from module.file.control import Retrieve as RL
                              from module.file.action.File import Load as FL
                              from langchain_core.documents import Document
                              runner : str = RL(metadata=self.meta).Location()
                              print('STEP 1/3')
                              documents : List[Document] = await FL().DocumentParseCSV(path=runner)
                              headings : Dict[List, Any] = await FL().DocumentGetColumns(path=runner)
                              print('STEP 2/3')
                              response.update({'data_columns': headings})
                              response.update({'document_list' : documents})


                        case 'LIST':
                              from module.file.control import File as OP
                              from module.pgvector.control import Collection as Col
                              instance = Col().Entity.Query(lookup_key=self.file.filename).byFilename()
                              self.file.filename = instance
                              runner = OP(file=None, fn=self.file.filename, metadata=self.meta).ResponseModel()
                              response = runner

                    
                        case 'DETAILS':
                              from module.file.control import Retrieve as X
                              runner : Dict[List, Any] = X(metadata=self.meta).Details()
                              print('FILE DETAILS Command : Receiving package state and metadata about file.')
                              response = runner 


                        case 'GETLOC':
                              from module.file.control import Retrieve as L
                              runner : str = L(metadata=self.meta).Location()
                              print('FILE GETLOC Command : receiving URL for Controlled Data Asset')
                              u : Dict[List, Any] = ({'url' : runner})
                              response = u
                              

                        case 'COLLECT':
                              from module.file.control import Collect as C
                              runner : Dict[List, Any] = {}
                              results = C(metadta=self.meta).getFilesList()
                              if len(results) > 0:
                                  for key, value in enumerate(results):
                                      runner.update({key : value})
                                  response = runner
                              else:
                                  response = {
                                          "FILE LIST  : No Files in collection"
                                    }

                            
                        case 'DELETE':
                              from module.file.control import FileControl
                              runner = FileControl(file=self.file, fn=self.file.filename)
                              outcome : Dict[List, Any] = await FileControl.de
                              response = outcome
                              
                        case 'ANALYZE':
                              from module.file.control import (
                                    Analyze as A, 
                                    Retrieve as U
                              )
                              subject = U(metadata=self.meta).Location()['metadata']['details']['url']
                              runner = A(filepath=subject)
                              outcome : Dict[List, Any] = await A.Analyze()
                              response = outcome 

                        case 'EMBED':
                              from module.file.control import File as E
                              runner = E(file=self.file, fn=self.file.filename)
                              outcome : Dict[List, Any] = await E.Embed(data, configs)
                              response = outcome

                        case 'MANAGE':
                              from module.file.control import FileControl as M
                              runner = M(file=self.file, fn=self.file.filename)
                              outcome : Dict[List, Any] = await M.Manage(data, configs)
                              response = outcome
                        case  _:
                              response = {
                                    'result' : 'Failure', 
                                    'details' : 'No valid ACTION was provided'
                              }
            except ValueError:
                  response = ConfigController.ERROR_MSG.values
            self.response = response 
            return response 
    

    class ACTION(Enum):
          REVIEW : Dict[List, Any] = ConfigController.PLAN.ProducePlan()
          UPLOAD : Dict[List, Any] = ConfigController.PLAN.CollectOp()
          DELETE : Dict[List, Any] = ConfigController.PLAN.Cleanup()
          ANALYZE : Dict[List, Any] = ConfigController.PLAN.BuildReport()
          EMBED :Dict[List, Any] = ConfigController.PLAN.CollectRun()
          MANAGE : Dict[List, Any] = ConfigController.PLAN.CollectActions()



class MatrixCommand: 
      
      def __init__(
                  self, 
                  comm : str, 
                  graph : str, 
                  meta : Dict[List, Any]
            ):

            self.comm = comm
            self.meta : Dict[List, Any] = meta
            self.name = 'Mapping : Get Request'

            self.filename : str = None
            self.label : str = None
            self.collection_name : str = None
            self.target_schema : str = None
            self.list : str = None

      def _sweep(self)->bool:
            import glob 
            patt="PRETZL/*"
            dirs=glob.glob(patt)
            for dir in dirs:
                  if os.path.isdir(dir):
                        try:
                              os.rmdir(dir)
                              print(f'Deleted Directory: {dir}')
                              return True 
                        except OSError as e:
                              print(f'Error deleting {dir} : {e}')

      def _tearDown(self):
            if os.path.exists(self.tmpfile):
                  os.unlink(self.tmpfile)
            os.rmdir(self.tmpdir)


      def _getCommand(self)->str:
            command = self.comm
            return command 
    

      async def Action(
                  self, 
                  metadata : Dict[List, Any] = None, 
                  data : List[Document] = None
            )->Dict[List, Any]:

            self.meta = metadata 
            self.data : Dict[List, Any] = data 
            casestr = self._getCommand()
            self.meta.update({'Action' : casestr})
            configs = self.meta
            try:
                match str(casestr).upper():
                      

                  case 'GENERATE':
                        from module.file.action.subroutine.target import Sub as T
                        from module.file.action.subroutine.source import Sub as S
                        await T(metadata=self.meta).set()
                        await S(metadata=self.meta).set()

                  case 'CREATE':
                        import json
                        from module.file.control import RetrievalController as R, MapController as M
                        from module.file.action.File import Load as B
                        from module.file.action.Map import Matrix as X
                        from module.file.model.Field import Field as F
                        from module.file.action.Chat import Chat as CC
                        from module.file.model.Robot import Robot as Ro 
                        from module.file.helper import Helper as H 


                        hold : Dict[List, Any] = {}

                        print('FILE MATRIX Command : Gathering file info from local storage')
                        runner : str = R(metadata=self.meta).Location()
                        outcome : Dict[List, Any] = self.meta 

                        print('FILE MATRIX Command = Read file for Initial review/assignment of types')
                        headings : Dict[List, Any] = await B().DocumentGetColumns(path=runner)
                        documents : list = await B().DocumentParseCSV(path=runner)
                        outcome.update({'column_data' : headings})
                        outcome.update({'document_list' : documents})

                        print('MATRIX : CREATE - generates a metadata representation of file qualities')
                        tracer = X.Entity.Origin(package=outcome)
                        graph = tracer.CreateGraph()

                        print("CHAT ENGAGED in files analysis from source tied to target input model")
                        lister = X.Entity.Origin(package=self.meta).GetSourceSamples()
                        for row in enumerate(lister):
                              r = row
                        sources = r[1][1]
                        robot = CC(
                              meta=self.meta, 
                              targetFile = runner, 
                              inputDataFile = sources['result']['action_event'][0]
                        ).getBotsRecommendation()
                        graph.update({'robot_reads' : robot})
                        print('MATRIX Command = CREATE -> Graph Succeeded')
                        result = await tracer.getMatrixControls(map=graph)

                        print("FIELD Command = INITIATE -> Started")
                        model = F.Entity.Query(
                              lookup_key=result['source_sfid']
                        ).pullTargetFields(package=result, recomm=graph)

                        print("FILE MATRIX Command : Create a file based on mappings of Fields/Types")
                        result.update({'fields' : model})
                        response = result 

                  case 'CHAT': 
                        from module.file.control import RetrievalController as Re 
                        from module.file.action.Chat import Chat as Ch
                        from module.file.action.Map import Matrix as Mx
                        target  = Re(metadata=self.meta).Location()
                        lister = Mx().Entity.Origin(package=self.meta).GetSourceSamples()
                        for row in enumerate(lister):
                              r = row 

                        sources = r[1][1]
                        result = Ch(
                              meta=self.meta,
                              targetFile = target, 
                              inputDataFile = sources['result']['action_event'][0]
                        ).getBotRecommendation()
                        response = result

                  case 'DOCIMG':
                        from module.file.control import RetrievalController as I
                        from module.pretzl.parser import PRETZL as PR 
                        from module.azure.adi.model.receipt import ADIReceipt as A
                        target = I(metadata=self.meta).Location()
                        result = await A(url=target).analyzeReceipt()
                        response = result 


                  case 'STORE':
                        from module.file.control import RetrievalController as R
                        from module.file.action.File import Load as F
                        from module.file.action.Map import Matrix as M
                        hold : Dict[List, Any] = {}
                        runner : str = R(metadata=self.meta).Location()
                        headings : Dict[List, Any] = await F().DocumentGetColumns(path=runner)
                        hold.update({'data_columns' : headings})
                        hold['result'] = await M.Entity.Create(package=response).setFields()
                        response = hold

                  case 'DETAILS':
                        pass

                  case 'LIST':
                        from module.file.control import MapController as M
                        from module.file.action.Map import Matrix as F
                        settings = M(file=self.file, fn=self.file.filename, construct=configs)
                        outcome : Dict[List, Any] = await settings.listFields()
                        tracer = F.Entity.Receive(package=outcome)
                        result = await tracer.getMatrixControls()
                        print("FILE MATRIX COMMAND : Review and modify the data type sand field maps.")
                        response = result 

                  case _:
                        response = {
                              'result' : 'Failure', 
                              'details' : 'No valid Matrix MAPPING ACTION was provided'
                        }
            
            except ValueError:
                response = ConfigController.ERROR_MSG.values
            self.response = response 
            return response 
    

    


        


    