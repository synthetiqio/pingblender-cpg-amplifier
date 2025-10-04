import os, sys
from typing import Dict, List, Form, Optional, Any
from fastapi import File, Depends, HTTPException
from pydantic import BaseModel 

from langchain.runnables import RunnablePassThrough
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StrOutputParser 

from core.model.document import Construct
from module.pgvector.config import Config 
from jinja2 import Environment, PackageLoader, select_autoescape

class Dialog(BaseModel):
    pass 

    class Questions:

        def __init__(
                self, 
                boundaries:Dict[List, Any], 
                context: str = None, 
                scopes: Dict[list] = None, 
                doc_config: Construct = Depends(Construct)
        ):
            self.boundary : Dict[List, Any] = boundaries
            self.context : str = context 
            self.config : Dict[list] = doc_config
            self.scopes = scopes

            self.persona:str=None 


        async def _getPersona(self):
            return self.persona 

        async def setPersona(
                self,
                description:str,
        )->str:
            self.persona = description.lower()
            return self.persona
        
        async def _setscopes(
                self, 
                scopes
        ):
            pass 

        
        def createActionTemplate(
                self, 
                scopes:Dict[List, Any], 
                task : str = f'Task: Explain the data which was considered in "Context" variable.'
        )->StrOutputParser:
            self.scopes = self._setscopes(scopes)
            if self.persona != None:
                template=f'Do the defined task in the following line separated description of the template: \
                    Persona: {self._getPersona()} \
                    Context : {self.context} \
                    Constraints : {self.scopes} \
                    Task: {task} \
                    '
            return template