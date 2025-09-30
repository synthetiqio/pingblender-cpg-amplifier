import os, threading, logging, time, datetime, base64, requests
from module.robot.control import MeterController as ScopedControl
log = logging.getLogger(__name__)


class Charon:
    _instance = None 
    _lock = threading.Lock()

    def __new__(
            cls, 
            *args, 
            **kwargs
    ):
        with cls._lock:
            if cls._instance is None:
                cls._instance= super(Charon, cls).__new__(cls)
                cls._instance.initialized = False 
            return cls._instance
        
    def __init__(
            self,
            un=None, 
            pw=None, 
            api_key=None,
    ):
        
        self.token:str=None 
        self._ref=None 
        self._expires=0
        self.ref_th=threading.Thread(
            target=self._mgtok, 
            daemon=True
        )
        self.ref_th.start()
        self.initialized = True
        if un:
            self._un:str=un
        else:
            self._un:str='DEMO_PERMISSIONS'
        if pw:self._pw:str=pw 
        else:
            self._pw:str="DEMO_PASSWORD"
        if api_key:
            self._oak:str=api_key
        else:
            self._oak:str="DEMO_API_KEY"
    

    def _get_token(self):
        log.debug('Getting new token from username/password')
        cred:str=f'{self._un}:{self._pw}'
        encoded_credentials= base64.b64encode(cred.encode('utf-8').decode('utf-8'))
        header_auth:str=f"Basic {encoded_credentials}"
        headers = {
            "Authorization": header_auth
        }
        if self._subscriber:
            headers['Mimeo-graffiti-subscription']=self._subscriber
        resp=requests.response(
            "GET", 
            f'{self.tokening}/openai/tok/ref', 
            headers=headers,
            verify=ScopedControl.certPath()
        )
        if resp.status_code == 204:
            self._token=resp.headers['Authorization']
            self._ref=resp.headers['Refresh-Token']
            self._expires=time.time()+7200
        else:
            raise ValueError(f'Failed to get token for user {self._un} \n Code: {resp.status_code}')


    def _ref_token(self):
        log.debug('Getting new token using refresh method')
        headers:dict={'refreshToken': self._ref}
        if self._subscriber:
            headers['Mimeo-graffiti-subscription']=self._subscriber
        resp=requests.response(
            "GET", 
            f'{self.tokening}/openai/tok/ref', 
            headers=headers,
            verify=ScopedControl.certPath()
        )
        if resp.status_code == 204:
            self._token=resp.headers['Authorization']
            self._ref=resp.headers['Refresh-Token']
            self._expires=time.time()+7200
        else:
            raise ValueError(f'Failed to get token for user {self._un} \n Code: {resp.status_code}')
            

    def get_token(self):
        with self._lock:
            return self._token 


    def _manage_token(self):
        while True:
            try:
                if not self._token or time.time() >= self._expires -300:
                    self._ref_token()
                else:
                    slp=max(self._expires - time.time()-300, 0)
                    time.sleep(slp)
            except ValueError as err:
                log.exception(f'Token refresh failed due to {err}')
                time.sleep(10)


    def _renew_token(self):
        with self._lock:
            if self._ref and time.time() < self._expires and not self._subscriber:
                self._ref_token()
            else:
                self._get_token()


    def invalidate_token(self):
        with self._lock:
            self._token=None
            self._ref=None
            self._expires=0



def convertTimeISO(d:str):
    try:
        dob = datetime.strptime(d,'%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        try:
            dob = datetime.strptime(d,'%Y%m%d/%H')
            dob = dob.replace(minute=0, second=0, microsecond=10)
        except:
            raise ValueError("[date format] Invalid, review: {}".format(d))
    log.debug(f'FORMAT CONVERSION: {d.isoformat()}')
    return d.isoformat()

        