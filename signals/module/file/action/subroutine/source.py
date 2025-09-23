# signals/rcm/module/file/action/subroutine/source.py
#checked and validated 17 January 2025
import json
from typing import Dict, List, Any 
from module.file.control import (
    Retrieve as R, 
    Map as M, 
    Filter as ET 
)
from module.file.action.File import Load as LP, Manage as MG
from module.file.action.Map import Matrix as MP 
from module.file.model.Field import Field as FP

class Sub:

    def __init__(
            self, 
            metadata
    ):
        self.meta=metadata

    def _getUrls(
            self
    )->list:
        listed:list=[]
        files=MP.Entity.Origin(
            package=self.meta
            ).GetSourceList()
        try:
            for i, row in files:
                print(i)
                uv=row[i]
                uvl=uv['result']['action_event'][0]
                listed.append(str(uvl))
            return listed 
        except:
            raise FileExistsError('[FILE Manager]: System subroutine failed')

    async def set(
            self
    ):
        urlist=self._getUrls()
        print(urlist)
        hold:Dict[List,Any]={}
        print("......[FILE] MATRIX Command: Gathering file data from its local storage location....")
        runner:str = R(metadata=self.meta).Location()
        outcome:Dict[List,Any]=self.meta
        print("......[FILE] MATRIX Command: Read file for initial review assignment of simple types....")
        headings:Dict[List,Any]= await LP().DocumentGetColumns(path=runner)
        documents:Dict[List,Any]= await LP().DocumentParseCSV(path=runner)
        outcome.update({'column_data':headings})
        outcome.update({'document_list': documents})
        tracer=MP.Entity.Origin(package=outcome)
        graph=tracer.CreateGraph()
        result= await tracer.getMatrixControls(map=graph)
        model=FP.Entity.Query(
            lookup_key=result['source_sfid']
        ).setSourceFields(package=result,recomm=graph)
        result.update({'fields':model})
        print("......[FILE] MATRIX Command: RCreate a File Based Mapping of Fields/Values/Types....")
        self.dataobj = result 
        return result 
