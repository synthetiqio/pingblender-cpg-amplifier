
#   Graffiti - by Mimeograph SynthetIQ
 
#   NOTICE OF LICENSE
 
#   This source file is subject to the Academic Free License (AFL 3.0)
#   If you did not receive a copy of the license and are unable to
#   obtain it through the world-wide-web, please send an email
#   to license@mimeograffiti.com so we can send you a copy immediately.
 
#   DISCLAIMER
 
#   Do not edit or add to this file if you wish to upgrade Graffiti to newer
#   versions in the future. If you wish to customize Graffiti for your
#   needs please refer to https://mimeographffiti.com for more information.
 
#  @folder      module.core.cron
#  @package     Graffiti Root Manager Agents
#  @copyright   Copyright (c) 2024-2025 Mimeograph Holdings. (https://mimeographffiti.com)
#  @license     Academic Free License (AFL 3.0)
import json, os, logging, sys
from core.cron.etc.config import (
    CRON as CronConfig, 
    system as Cronsys,
    module as Cronmod,
)
class ConfigControl:

    def __init__(self):
        self.config = CronConfig() 

class ObserverControl:

    class Config:

        def __init__(self):
            self.config = CronConfig()

        def get(
                self,
                subj
        ):
            pass
            
        def _get_node(
                self,   
                nodename:str,
        ):
            sys:json=Cronmod.settings
            data=json.loads(sys)
            modkey=nodename.split('/')
            self._op_node=data[modkey[0].lower()][modkey[1].lower()]
            return self._op_node

        def getNode(
            self,
            nodename:str
        ):
            return self._get_node(nodename)