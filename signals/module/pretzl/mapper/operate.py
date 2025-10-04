import pandas as pd 
from langchain.prompts import ChatPromptTemplate
from module.robot.action.common import OpenAILLMChat
from module.pretzl.control import PRETZL as ModController 
from pydantic import BaseModel

class Structure():
    pass 

    class LargeLanguage:

        class History(BaseModel):
            pass


        class Model:

            def __init__(self):
                pass 

            class Options:
                pass 


class Engine():

    def __init__(
            self, 
            src_input:str, 
            set_target:str,
    ):
        self.params:dict={}
        self.s = src_input
        self.t = set_target

    def read_datafile(
            self, 
            fn
    ):
        return pd.read_csv(fn)
    
    def get_response(
            self, 
            sys_prompt, 
            use_prompt, 
            response_format
    ):
        robot={}
        template=ChatPromptTemplate.from_messages([
            ("system", sys_prompt), 
            ("human", f"{use_prompt}")
        ])
        if response_format == 'json': 
            response = robot['outcome']