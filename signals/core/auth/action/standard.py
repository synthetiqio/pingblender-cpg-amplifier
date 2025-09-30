import base64, requests, os, json
from typing import Dict, List, Any, Optional
from core.auth.config import BADGE as Config 

class MeterAuth:

    def __init__(
            self, 

    ):
        self.version = Config.Default.VERSION.value
        self.baseurl= Config.Default.ENDPOINT.value
        self.service= Config.Default.SERVICE.value 

        self.token=''

    def getServiceEndpoint(
            self,
            subscription:str, 
            model:str
    ):
        self.service= subscription
        embed:str
        uri:list=[
            str(self.baseurl), 
            str(model)+"/",
            str(self.service), 
            '?api-version='+str(self.version)
        ]
        embed=''.join(uri)
        return embed 
    

    def _getServicePrincipal(
            self,
    ):
        return Config.Default.USER.value
    

    def _getServicePassword(
            self,
    ):
        return Config.Default.PASS.value 
    

    def _getKey(
            self
    )->str:
        self.creds=self._generateCredentials()
        return self.creds 
    

    def _generateCredentials(
            self,
    ):
        i=[]
        i.append(str(self._getServicePrincipal()))
        i.append(str(self._getServicePassword()))
        c=':'.join(i)
        cbytes=c.encode('utf-8')
        credential=base64.b64decode(cbytes).decode('utf-8')
        return credential
    
    def authenticate(
            self,
    )->Dict[List,Any]:
        url=Config.Default.AUTHURL.value
        response=requests.post(
            url=url, 
            data={},
            headers={
                'Mimeo-graffiti-subscription':self._getKey(), 
                'Authorization':'Basic '+self._generateCredentials(),

            }, 
        )
        result:Dict[List,Any]
        if response.status_code != 200:
            raise ValueError('Login failed')
        try:
            self.token=response.headers['Authorization']
        except KeyError:
            result={
                    'result':'FAILURE',
                    'status_code': response.status_code,
                    'message':'Authorization header not found in the response', 
                    'payload':None 

                }
        if self.token !='':
            result={
                    'result':'SUCCESS', 
                    'status_code': response.status_code, 
                    'auth_token': self.token, 
                    'payload': self.token 

                }
        return result 