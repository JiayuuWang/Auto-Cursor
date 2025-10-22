from openai import OpenAI
from dotenv import load_dotenv
from google import genai
load_dotenv()
import os

openrouter_client = OpenAI(
  base_url=os.getenv("OPENROUTER_API_BASE"),
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

closeai_client = OpenAI(
  base_url=os.getenv("OPENAI_API_BASE"),
  api_key=os.getenv("OPENAI_API_KEY"),
)

gemini_client = genai.Client(vertexai=True,http_options={"base_url": os.getenv("GEMINI_API_BASE")},api_key=os.getenv("OPENAI_API_KEY"))