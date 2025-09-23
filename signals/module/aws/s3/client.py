import boto3, os
from typing import Dict, List, Any 
from module.aws.config import AWS as ClientConfig 
from dotenv import load_dotenv
load_dotenv()

AWS:Dict[List,Any]={}
AWS=ClientConfig.Route.Default['S3'].value
# AWS['bucket_stream']=ClientConfig.Route.Default().S3.get('bucket_stream')
# AWS['secret']=ClientConfig.Route.Default().S3.get('secret')
# AWS['access']=ClientConfig.Route.Default().S3.get('access')

class Transit:

    def __init__(
            self,
    ):
        self.client = boto3.client(
            's3',
            aws_access_key_id=AWS.get('access_key'),
            aws_secret_access_key=AWS.get('secret_key'), 
            verify=False #TODO:obviously cannot keep this in production.
        )

        self.resource = boto3.resource(
            's3',
            aws_access_key_id=AWS.get('access_key'),
            aws_secret_access_key=AWS.get('secret_key'), 
            verify=False
        )

    def client_action(self):
        return self.client 

    
    def getBucketName(self, isPipeline:bool=False)->str:
        if isPipeline == True:
            self.bucket_name = AWS.get('stream_name')
        else:
            self.bucket_name=AWS.get('bucket_name')
        return self.bucket_name 
    

    def resource_action(
            self,
        ):
        return self.resource 
    

    def getS3Bucket(self):
        resource_hold=self.getResource()
        self.bucket_conduit=resource_hold.Bucket(self.getBucketName)
        return self.bucket_conduit 
    