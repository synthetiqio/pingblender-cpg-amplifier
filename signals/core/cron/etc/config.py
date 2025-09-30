
#   Graffiti - by Mimeograph SynthetIQ
 
#   NOTICE OF LICENSE
 
#   This source file is subject to the Academic Free License (AFL 3.0)
#   If you did not receive a copy of the license and are unable to
#   obtain it through the world-wide-web, please send an email
#   to license@mimeograffiti.com so we can send you a copy immediately.
 
#   DISCLAIMER
 
#   Do not edit or add to this file if you wish to upgrade Graffiti to newer
#   versions in the future. If you wish to customize Graffiti for your
#   needs please refer to https://mimeograffiti.com for more information.
 
#  @folder      module.core.cron
#  @package     Graffiti Root Manager Agents
#  @copyright   Copyright (c) 2024-2025 Mimeograph Holdings. (https://mimeograffiti.com)
#  @license     Academic Free License (AFL 3.0)
import json 
import os
from typing import Dict, List, Any
import logging 
log = logging.getHandlerNames(__name__)

class CRON:

    ERROR_MSG:Dict[List, Any]={
        'result' : 'Failure', 
        'message' : f'[{__name__}] : Service failure - Configuration Level [Root]',
        'payload': None
    }

    class Timestamp:

        def getTimestampLocal(
                tmz : str = 'America/New_York'
        )->str:
            from datetime import datetime
            from pytz import timezone
            fmt = '%Y-%m-%dT%H:%M:%S'
            c = timezone(tmz)
            loc_dt = datetime.now(c)
            fd = loc_dt.strftime(fmt)
            return fd


        def getDaystampLocal(
                tmz : str = 'America/New_York'
        )->str:
            from datetime import datetime
            from pytz import timezone
            fmt = '%Y-%m-%d'
            c = timezone(tmz)
            loc_dt = datetime.now(c)
            fd = loc_dt.strftime(fmt)
            return fd

class system:

    settings:json={

    }

class module:
    settings:json={
       'version':'1.0.0', 
       'name':'Graffiti_Cronjobs', 
       'global' :{
           'resources': {
               'module': {
                    'core': {
                        'cron': {
                            'cronjob_schedule':'module.core.cron.operate'
                            }
                        }
                    }
           },
           'model': {
               'cron': [
                   {
                       'class':'Task', 
                       'controlled_entities': [
                           'Process',
                           'Schedule'
                        ], 
                        'control_interface': {
                            'dependency':'sqlalchemy.orm'
                        }
                   },
                   {
                       'class':'Transact', 
                       'controlled_actions':['create','process','processing','failed','queue','cancel']
                    }
               ]
           }
       }, 
       'crontab':
            {
                'events' : {
                    'default': {
                        'observe': {
                            'class': 'Observe', 
                            'control_method':{
                                'method':'dispatch'

                            }, 
                            'control_events':['pending','running','success','missed','error','idle'],
                        }
                    }
                }, 
                'jobs':[
                    {#default healthcheck on cron scheduler.
                        'task_key':'every_15_minutes_during_business_hours', 
                        'schedule': {
                            'cycle' :{
                                'cron_expression': '*/15 9-12,14-17 * Nov-Dec,Jan-Feb Mon-Fri -8'
                                }, 
                        }, 
                        'action' : {
                            'run': [
                                {
                                    'model':'cron.model.observe', 
                                    'mode':'Test'
                                }
                            ]
                        }
                    },
                ]
            }, 
        'default':
        {
            'system':
            {
                'cron': [
                    {
                    'schedule_generate_every':15
                    },
                    {
                    'schedule_ahead_for':20
                    }, 
                    {
                    'schedule_lifetime':15
                    },
                    {
                    'history_cleanup_every':10
                    },
                    {
                    'history_success_lifetime':60
                    }, 
                    {
                    'history_failure_lifetime':600
                    }
                ]
            }
        },
        'administration':{
            'translate' :{
                'module':{
                    'core':{
                        'cron':{
                            'files': {
                                'default':{
                                    'Graffiti_Cronjobs.csv'
                                }
                            }
                        }
                    }
                }
            }
        }
       
       }