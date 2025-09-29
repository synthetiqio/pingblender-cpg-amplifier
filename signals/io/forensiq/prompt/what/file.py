from openai import OpenAI
client = OpenAI()

"""
class: File_Prompt (init) - Handles loading and processing of prompt files \
    for Forensiq. Supports different scopes (e.g., 'what', 'how', 'why') to \
    customize the prompt context. Prepares a response for a handoff to a ready \
    state for the next processing agent. 

Attributes:
    oai_schema (str): Path to the OpenAI schema JSON file.

Methods:
    __init__(self, scope: str): Initializes the File_Prompt with a given scope
    get_output_text(self): Returns the processed output text from the prompt.
"""
class File_Prompt:

    def __init__(self, scope: str):
        self.oai_schema = "signals/io/forensiq/prompt/.json"
        response = client.responses.create(
            prompt={self.oai_schema[scope]}
        )
        self.output_text = response.output_text
        
    def get_output_text(self):
        return self.output_text
