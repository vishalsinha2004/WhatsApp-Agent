import google.generativeai as genai

# Configure your Gemini API key
genai.configure(api_key="AIzaSyD0MJpiETfLw9nPkxdCEXlZn3i_usJ91Kw")

# Instantiate the model
model = genai.GenerativeModel('gemini-2.0-flash')

# Chat history input
command = '''
[20:30, 12/6/2024] Person1: Can you suggest something I can code while listening?
[20:30, 12/6/2024] Person2: https://www.youtube.com/watch?v=DzmG-4-OASQ
[20:30, 12/6/2024] Person2: This one.
[20:30, 12/6/2024] Person2: https://www.youtube.com/watch?v=DzmG-4-OASQ
[20:31, 12/6/2024] Person1: This is in Hindi.
[20:31, 12/6/2024] Person1: Send me some English songs.
[20:31, 12/6/2024] Person1: But wait—
[20:31, 12/6/2024] Person1: This song is amazing.
[20:31, 12/6/2024] Person1: So I’ll stick to it.
[20:31, 12/6/2024] Person1: Still, send me some English songs too.
[20:31, 12/6/2024] Person2: Hold on.
[20:31, 12/6/2024] Person1: I know what you're about to send. 😂😂
[20:32, 12/6/2024] Person2: https://www.youtube.com/watch?v=ar-3chBG4NU
This one is a Hindi-English mix, but it’s great.
[20:33, 12/6/2024] Person1: Okay okay.
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
