import logging 
log=logging()
class EventExceptionController(Exception):
    with Exception as err:
        response = {
                'result': 'EVT Control Exception', 
                'message': 'An issue prevents the EVT from passing', 
                'payload': f'Exception.Failure : {err}'
        }
        log.debug(response)
        raise response
    
