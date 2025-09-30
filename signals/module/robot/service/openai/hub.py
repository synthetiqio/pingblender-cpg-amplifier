import json, logging, os, ssl, sys
from module.robot.control import RobotController 
from typing import List, Optional, Any, Tuple,Union 
import aiohttp, requests, tiktoken 

#set callbacks interface manager 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForLLMRun, 
    CallbackManagerForLLMRun
)

from langchain.adapters.openai import convert_dict_to_message
from langchain.chat_models.base import BaseChatModel 
from langchain.schema import ChatResult, ChatGeneration
from langchain.schema.messages import(
    AIMEssage,
    BaseMessage, 
    ChatMessage, 
    FunctionMessage, 
    HumanMessage,
    SystemMessage
)

class OpenAIAgentServices:

    pass 