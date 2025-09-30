import os, sys
from typing import Dict, List, Form, Optional, Any
from fastapi import File, Depends, HTTPException
from langchain.runnables import RunnablePassThrough
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StrOutputParser 

from module.pgvector.config import Config 
from jinja2 import Environment, PackageLoader, select_autoescape

from core.model.document import Construct

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

    
    def createActionTemplate(
            self, 
            scopes:Dict[List, Any], 
            task : str = 'Task: Explain the data which was considered.'
    ):
        
        template=f'Do the defined task in the following line separated description of the template: \
            Context : {self.context} \
            Constraints : {scopes} \
            Task: {task} \
            '
        return template