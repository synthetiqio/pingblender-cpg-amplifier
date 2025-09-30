from pathlib import Path
from openai import OpenAI
import os 
from dotenv import load_dotenv
load_dotenv()

ai_client=OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
speech_file_path = Path(__file__).parent / "speech.mp3"
response = ai_client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="There is very little I can say which will help make you feel better about the fact that the deadlines for the projects \
    which you're working on are not satisfying. If you can hold out a little longer, I do believe that the commercial impact of the  !\
    episodic technology will provide you with a view into the future that you can be an active particpant.",
)
response.write_to_file()