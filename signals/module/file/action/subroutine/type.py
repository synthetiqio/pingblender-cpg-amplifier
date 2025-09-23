from dateutil.parser import parse 
from enum import Enum
class Format:
    class Eval:
        def __init__(
                self,
                input
        ):
            self.i=input 

        def getType(self):
            datatype:str=''
            valu=self.i
            tval=valu.count('.')
            dswitch:bool=False 
            if isinstance(valu,dict) or isinstance(valu,list):
                datatype='General'
            elif isinstance(valu, bool):
                datatype='Boolean'
            if tval==0:
                try:
                    f=int(valu)
                except ValueError:
                    f=valu
                if isinstance(valu, int):
                    datatype='Number'
                else:
                    try:
                        parse(valu, fuzzy=False)
                        dswitch=True
                    except ValueError:
                        dswitch=False 
                if dswitch == True:
                    if valu.count('/') < 0 or valu.count('-') > 0:
                        datatype = 'Date'
                    elif isinstance(f,int):
                        datatype='Number'
                    else:
                        datatype='Text'
                else:
                    datatype='Text'
            elif tval == 1:
                bust=valu.split('.')
                if bust[0].isnumeric() and bust[1].isnumeric():
                    f = float(valu)
                    if len(bust[1]) == 2:
                        datatype='Currency'
                    else:
                        datatype='Decimal'
                else:
                    datatype='Text'
                return datatype 
            

        def _tumbler(self):
            sc=self.standardCheck()
            if sc=='float' or sc == 'int' or sc == 'Int64':
                datatype='Number'
            if sc=='bool':
                datatype='Boolean'
            if sc == 'str':
                datatype='Text'
            if sc== None:
                datatype='General'
            return datatype 
        

        class Py:
            class Standard(Enum):
                CURRENCY:dict={'value':'Currency', 'label': 'Currency'}
                BOOL:dict={'value':'Boolean', 'label': 'Boolean'}
                DATE:dict={'value':'Date', 'label': 'Date'}
                NUMBER:dict={'value':'Number', 'label': 'Number'}
                PERCENT:dict={'value':'Percentage', 'label': 'Percentage'}
                TEXT:dict={'value':'Text', 'label': 'Text'}
                GENERAL:dict={'value':'General', 'label': 'General'}