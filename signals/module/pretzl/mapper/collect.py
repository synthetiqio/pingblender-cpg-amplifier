from module.pretzl.control import PRETZL as Locus
from concurrent.futures import ThreadPoolExecutor
import json, uuid, os, re, pandas as pd, numpy as np
from ast import literal_eval
from dotenv import load_dotenv


class ReadyAgent:

    class Vector:
        pass 

    class Ops():

        def __init__(
                self
        ):
            pass 


        class Collection:

            def __init__(self):
                pass 

            def setName(self, name:str, scid:str=None)->bool:
                 pass



        class Read:
            pass 

            class CSV:
                
                def __init__(
                        self, 
                        file_name:str=None,
                        file_data:any=None, 
                        file_path:str=None, 
                        file_sepp:str=None
                ):
                    
                    self.subj=file_name
                    
                async def read(self, filename):
                    return pd.read_csv(filename)
                



