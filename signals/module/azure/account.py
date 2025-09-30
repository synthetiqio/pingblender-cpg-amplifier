import logging
log=logging()
from enum import Enum 
from pydantic import BaseModel
from typing import Dict,List,Any,Optional
from load_dotenv import load_dotenv
load_dotenv()

class AzureCloud:

    def __init__(self):
        pass 


    class Storage:


        class Wasb:


            def __init__(self):
                pass 