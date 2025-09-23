import logging
import boto3
from botocore.exceptions import ClientError
from typing import Dict, List, Any 

#AMAZON Interface Controls and IAM - [ROOT]
AWS:Dict[List,Any]={}
AWS['bucket_name']="pingblender-local-supply"
AWS['bucket_stream']="pingblender-proc-pipeline"
AWS['secret']=""
AWS['access']=""

s3_client = boto3.client(
        region='us-east-1',
        aws_access_key_id=AWS['access'],
        aws_secret_access_key=AWS['secret']   
)

def create_bucket(
        bucket_name, 
        region='us-east-1',
        aws_access_key_id=AWS['access'],
        aws_secret_access_key=AWS['secret']
        
    ):
    try:
        if region is None:
            s3_client.create_bucket(
                Bucket=bucket_name
            )
        else:
            location = {
                'LocationConstraint': region
            }
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration=location
            )
    except ClientError as e:
        logging.error(e)
        return False
    return True

def list()->dict:
    s3 = s3_client
    response = s3.list_buckets()
    bucket_list={}
    for bucket in response['Buckets']:
        bucket_list.update({bucket["Name"]:bucket})
    return bucket_list