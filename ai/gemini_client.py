import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

def gemini_generate(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip()
