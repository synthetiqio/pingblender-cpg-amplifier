import asyncio, builtins, json, logging, os, ssl, aiohttp
from asyncio import CancelledError
from datetime import datetime, timedelta
from typing import Optional, Any
log=logging.getLogger(__name__)
from module.robot.control import RobotController as RC 
from core.evt.ctrl import EventExceptionController as EC

#AZure based options for integration into EventHub 
from azure.eventhub.aio import EventHubConsumerClient

class Listener:

    class AsyncCallback:
        
        apikey:str
        conn:str 
        queue:Optional[str]
        response:Optional[dict]
        receive_task:Optional[Any]

        username:Optional[str]=None 
        password:Optional[str]=None 
        subscriber_key:Optional[str]=None 

        REQUIRED_PARAMS=['apikey']

        def __init__(
                self, 
                **kwargs
        ):
            for param in self.REQUIRED_PARAMS:
                if param not in kwargs:
                    raise ValueError("Missing required parameters: {param}")
            if "conn" not in kwargs or "queue" not in kwargs:
                raise ValueError("For ASYNC both connection string (conn) and (queue) are required")
            for key, value in kwargs.items():
                builtins.setattr(self, key, value)

            ##protect against empty submission values 
            self.username=kwargs.get("username", None)
            self.password=kwargs.get("password", None)
            self.subscriber_key=kwargs.get("subscriber_key", None)

        async def _listen(
                self,
                correlation_id:str
        ):
            client=EventHubConsumerClient.from_connection_string(
                self.conn, 
                consumer_group="$Default",
                eventhub_name=self.queue
            )
            self.correl:str=correlation_id
            start_time=RC.timestamp()-timedelta(minutes=1)
            self.receive_task=asyncio.create_task(
                client.receive(
                    on_event=self._on_event, 
                    starting_position=start_time, 
                )
            )
            try:
                log.info(f'Starting event listener for req :{correlation_id}')
                await self.receive_task
            except CancelledError:
                pass
            finally:
                await client.close()

        async def _on_event(
                self, 
                partition,
                evt
        ):
            log.debug('Received callback event: {} from the partition with ID:"{}"'.format(
                      evt.body_as_str(encoding='UTF-8'), 
                      partition.partition_id
                      ))
            from module.robot.action.meter import convertTimeISO
            evt_content=evt.body_as_str(encoding='UTF-8')
            evt_dict=json.loads(evt_content)
            ssl_set=ssl.create.default_context(cafile=RC.certPath())
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=ssl_set)
            ) as session:
                url=f'sometimesomasdnuiasd'
                tik=RC.getToken(
                    self.username,
                    self.password,
                    self.subscriber_key
                )
                if tik is None:
                    raise ValueError(f'Failed to get JWT from Charon')
                headers={
                    "Authorization":tik, 
                    "Mimeo-graffiti-subscription":self.apikey
                }
                payload=evt_dict[0]['data']
                payload['timestamp']=convertTimeISO(payload['timestamp'])
                if evt_dict[0]['data']['correlationId'] == self.correl:
                    log.debug(payload)
                    async with session.post(
                        url=url, 
                        headers=headers,
                        json=payload 
                    ) as response:
                        response_text= await response.json()
                        log.debug(f'OpenAI Response: {response_text}')
                        self.response=response_text
                    self.receive_task.cancel()

        async def await_evt_callback(
                self, 
                correlation_id:str
        ):
            try:
                if asyncio.get_event_loop().is_running():
                    await self._listen(correlation_id=correlation_id)
                else:
                    asyncio.run(self._listen(correlation_id=correlation_id))
            except CancelledError:
                pass 
            



            


        