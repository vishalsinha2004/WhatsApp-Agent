import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables with override to fix caching issues
load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # Using the model version requested
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    print("❌ ERROR: No API Key found.")
    exit()

# Chat history input
command = '''
[20:30, 12/6/2024] Person1: Can you suggest something I can code while listening?
[20:30, 12/6/2024] Person2: https://www.youtube.com/watch?v=DzmG-4-OASQ
... (rest of your chat history) ...
[20:33, 12/6/2024] Person2: Yeah.
'''

# Prepare the prompt for the model
prompt = (
    "You are a person named Vishal who speaks Hindi and English, is from India. "
    "Analyze the chat history below and respond in a friendly, human-like way as Vishal:\n\n "
    + command
)

# Generate the response
response = model.generate_content(prompt)

# Print the result
print(response.text)