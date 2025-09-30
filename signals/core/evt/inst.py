import asyncio, os 
from dotenv import load_dotenv
from typing import Dict, List,Any 
from uuid import uuid4
from datetime import datetime 
from azure.eventhub import EventData 
from azure.eventhub.aio import EventHubProducerClient

class telemetry:

    def __init__(
            self,
    ):
        
        load_dotenv()
        EVENT_HUB_CONNECTION_STRING=os.getenv("EVENT_HUB_CONNECTION_STRING")
        EVENT_HUB_NAME=os.getenv("EVENT_HUB_NAME")


    async def run(
            self, 
            payload:Dict[List,Any]
    ):
        producer=EventHubProducerClient.from_connection_string(
            conn_str=telemetry()().EVENT_HUB_CONNECTION_STRING,
            eventhub_name=telemetry()().EVENT_HUB_NAME
        )
        async with producer:
            event_data_batch=await producer.create_batch()
            event_body={
                'event_id':uuid4(), 
                'event_title':"TEST EVENT",
                'event_desc':'', 
                'event_start':datetime.now(),
                'event_msg':"This is test message", 
                "event_tags":['test','event','message'], 
                "event_state":"active"
           }
        event_data_batch.add(EventData("test_event"))
        await producer.send_batch(event_data_batch)

    asyncio.run(run())