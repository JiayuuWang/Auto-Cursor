from openai import OpenAI
from dotenv import load_dotenv
from google import genai
load_dotenv()
import os
if os.getenv("OPENROUTER_API_KEY") and os.getenv("OPENROUTER_API_BASE"):
  openrouter_client = OpenAI(
    base_url=os.getenv("OPENROUTER_API_BASE"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    )
else:
  openrouter_client = None

if os.getenv("OPENROUTER_API_KEY") and not os.getenv("OPENROUTER_API_BASE"):
  openrouter_client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY")
  )
else:
  openrouter_client = None

if os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_BASE"):
  closeai_client = OpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
  )
else:
  closeai_client = None

if os.getenv("OPENAI_API_KEY") and not os.getenv("OPENAI_API_BASE"):
  closeai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
  )
else:
  closeai_client = None

if os.getenv("GEMINI_API_KEY") and os.getenv("GEMINI_API_BASE"):
  gemini_client = genai.Client(vertexai=True,http_options={"base_url": os.getenv("GEMINI_API_BASE")},api_key=os.getenv("GEMINI_API_KEY"))
else:
  gemini_client = None


if os.getenv("GEMINI_API_KEY") and not os.getenv("GEMINI_API_BASE"):
  gemini_client = genai.Client(vertexai=True,api_key=os.getenv("GEMINI_API_KEY"))
else:
  gemini_client = None
