from dotenv import load_dotenv
load_dotenv()
from agents import set_default_openai_api
import os
set_default_openai_api(os.getenv("OPENAI_API_KEY"))