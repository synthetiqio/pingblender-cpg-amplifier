from openai import OpenAI 
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
client.embeddings.create(
    model="text-embedding-ada-002",
    input="The quick brown fox jumped over the lazy dog",
    encoding_format="float"
)