from typing import Any, List, Optional, Sequence, Tuple, Union 
from core.auth.control import MeterController
from module.robot.service.openai.chat import AzureChatOpenAI
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.agents.openai_functions_multi_agent.base import OpenAIMultiFunctionsAgent
from langchain.callbacks.base import BaseCallbackManager
from langchain.agents import BaseSingleActionAgent
from langchain.prompts.chat import(BaseMessagePromptTemplate)
from langchain.schema.language_model import BaseLanguageModel
from langchain.tools.base import BaseTool 
from langchain.schema.messages import (SystemMessage)
from langchain.pydantic_v1 import root_validator

class FunctionsAgent(OpenAIFunctionsAgent):

    @root_validator
    def validate_llm(
        cls, 
        values:dict
    )->dict:
        services = MeterController.OpenAILLM.get_chat
        if not isinstance(values['llm'], services):
            raise ValueError("Only supported with ChatOpenAI models")
        return values 
    
    @classmethod 
    def root_tool(
        cls, 
        llm:BaseLanguageModel, 
        tools:Sequence[BaseTool], 
        cb_mgr:Optional[BaseCallbackManager],
        extra_prompt_msg:Optional[List[BaseMessagePromptTemplate]],
        sys_msg:Optional[SystemMessage]=SystemMessage(
            content="You are a capable and competent AI assistant"
        ),
        **kwargs:Any,
    )->BaseSingleActionAgent:
        if not isinstance(llm, AzureChatOpenAI):
            raise ValueError("Unfortunately that model is not currently supported")
        prompt = cls.create_prompt(
            extra_prompt_messages=extra_prompt_msg,
            system_message=sys_msg
        )
        return cls(
            llm=llm, 
            prompt=prompt,
            tools=tools,
            callback_manager=cb_mgr,
            **kwargs,
        )



class MultiFunctionsAgent(OpenAIMultiFunctionsAgent):

    @root_validator
    def validate_llm(
        cls, 
        values:dict
    )->dict:
        if not isinstance(values['llm'], AzureChatOpenAI):
            raise ValueError("Only supported with ChatOpenAI models")
        return values 