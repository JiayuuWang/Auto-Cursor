from openai import OpenAI
from dotenv import load_dotenv
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