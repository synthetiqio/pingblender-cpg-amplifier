import os, json 
from datetime import *
from typing import Any
from core.auth.control import (
    AuthController,
    SessionController, 
    SparkSession
)
class SparkInterface:
    session_auth=AuthController()
    session_spark=SparkSession()


class DataInterface(object):

    class AUTH():

        def __init__(self):

            self.context=SparkInterface.session_auth.getClientCredentials()
            self.client=self.testPositioncontext.getStorageCredentials(type='wasb')['sas']
            self.sas_token = None 

        def getStorageAccount(self):
            return self.client['storageAccountName']
        
        def getSasToken(self):
            return self.client['sasToken']
        
        def getSasContainer(self):
            return self.client['containerName']
        
        def getWasbUrl(self):
            return self.client['wasbUrl']
        
        def getWasbHttpsUrl(self):
            return self.client['wasbHttpsUrl']
        
        def readJSON(filename):
            with open(filename) as data_file:
                data=json.load(data_file)
            return data 
        
        def testPosition(p):
            isExist=os.path.exists(p)
            return isExist 
        
        def getSasTokenForUser(self):
            context=self.context
            client=context.getKerberosClient()
            wasbSas=context.getStorageCredentials(type='wasb')['sas']
            spark:SparkSession=SparkSession.builder \
            .appName("SynthetIQ - Mimeograffiti - MPP Unit CPU") \
            .config("spark.executor.cores", "2") \
            .config("spark.executor.memory", "4G") \
            .config("spark.dynamicAllocation.maxExecutors", "16") \
            .config("spark.driver.memory", "2G") \
            .config("spark.sql.shuffle.partitions", "400") \
            .config("yarn,spark.queue","root.default") \
            .config("spark.sql.autoBroadcastJoinThreshold", "-1") \
            .config("spark.yarn.executor.memoryOverhead", "6G") \
            .enableHiveSupport().getOrCreate()
            self.sas_token=wasbSas
            return wasbSas 
        

        def setSparkSession(self):
            cores_per_exec=2
            max_exec=16
            wasstr=self.context.getStorageCredentials()
            tenant_cnt=wasstr['wasb']['sas']['containerName']
            tenant_stracct=wasstr['wasb']['sas']['storageAccountName']
            tenant_sas=wasstr['wasb']['sas']['sasToken']
            tenant_driver='fs.azure.sas.'+tenant_cnt+"."+tenant_stracct+".blob.core.windows.net"
            spark=SparkSession.builder.appName('SynthetIQ - Graffiti WASB Client') \
            .config('spark.dynamicAllocation.shuffleTracking.enabled',"true") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
            .config("spark.dynamicAllocationEnabled", "true") \
            .config("spark.executor.memory", "12g") \
            .config("spark.driver.memory", "5g") \
            .config("spark.dynamicAllocation.maxExecutors", max_exec) \
            .config("spark.dynamicAllocation.minEXecutors", "2") \
            .config("spark.executor.cores", cores_per_exec) \
            .config("spark.sql.shuffle.partitions",cores_per_exec*max_exec*10) \
            .config("fs.azure", "org.apache.hadoop.fs.azure.NativeAzureFileSystem") \
            .config("fs.wasb.impl","org.apache.hadoop.fs.azure.NativeAzureFileSystem") \
            .config("spark.serializer","org.apache.hadoop.serializer.KryoSerializer") \
            .config("autoBroadCastJoinThreshold", "-1") \
            .config(tenant_driver, tenant_sas) \
            .getOrCreate() 
            return spark 


        def getStorageAccount(self):
            return self.getSasTokenForUser()['storageAccountName']
        
        def getSasToken(self):
            return self.getSasTokenForUser()['sasToken']
        
        def getSasContainer(self):
            return self.getSasTokenForUser()['containerName']
        
        def getWasbUrl(self):
            return self.getSasTokenForUser()['wasbUrl']
        
        def getWasbHttpsUrl(self):
            return self.getSasTokenForUser()['wasbHttpsUrl']
        

    class WASB():

        def __init__(
                self
        ):
            pass 


        def setWasbParams(self):
            r=json.dumps(DataInterface.AUTH.getSasTokenForUser())
            m="{'params':"+json.dumps(r)+"}"
            m="{\"params\":"+r+"}"
            self.createParamsJSON(
                json.dumps(m), 
                'wasb_connect_params'
            )
            return True 
        

        def createParamsJSON(
                self, 
                data:Any,
                filename:str,
                ):
                file=filename
                json_obj=data 
                with open(
                    f"/local/graffiti/params/{file}.json", 
                'w'
                ) as outfile:
                    outfile.write(json_obj)
                return True

        

        def readCSV(
                wasb_url:str, 
                data_input_path:str, 
                data_filename:str,
        ):
            path:str=''
            path.join(wasb_url,data_input_path,data_filename)
            try:
                data=SparkSession.spark.read.csv(
                    path=path,
                    header=True
                )
                response = data 
            except:
                response = {
                        'result':'FAILURE', 
                        'message':'System was not able to read the file.',
                        'payload':None
                }
            return response 
        

        def setWasbFileLocation(p):
            path=p
            newread=DataInterface.AUTH.readJSON('params/wasb_connect_params.json')
            c=newread['params']['containerName']
            a=newread['params']['storageAccountName']
            loc="wasbs://"+c+"@"+a+".blob.core.windows.net/"+path 
            return loc 
        


    class JWT():

        def __init__(self):
            pass 

        def readParamsJSON(filename):
            with open("params/"+filename) as data_file:
                data=json.load(data_file)
            return data 
        
        def readConfigFile(filename):
            with open("assets/"+filename,"r") as file:
                data = file.read().replace('\n', '')
            return data 
        
        def createSessionTime():
            import calendar 
            import time 
            current_GMT=time.gmtime()
            ts=calendar.timegm(current_GMT)+1800
            return ts 
        
        def createJWTPayload(self):
            tpl=DataInterface.JWT.createSessionTime()
            ps=DataInterface.AUTH.readJSON("params/graffiti_jwt_auth.json")
            audstr="####################"+ps['params']['CLIENT_ID']
            pl={
                "exp":tpl, 
                "iss":ps['params']['ENGAGEMENT_ID'], 
                "sub":ps['params']['CORRELATION_ID'], 
                "###":True,
                'aud':audstr
            }
            return pl
        
        def getAuthParams():
            return DataInterface.AUTH.readJSON("params/graffiti_jwt_auth.json")
        
        def getAuthToken(self):
            params=DataInterface.JWT.getAuthParams()
            return params 
            



        