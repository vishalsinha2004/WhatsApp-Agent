import pyautogui
import time
import pyperclip
import google.generativeai as genai

# Configure Gemini with your API key
genai.configure(api_key="")

# Define function to check last sender
def is_last_message_from_sender(chat_log, sender_name=""):
    messages = chat_log.strip().split("/2024] ")[-1]
    return sender_name in messages

# Step 1: Click on Chrome
pyautogui.click(1639, 1412)
time.sleep(1)

while True:
    time.sleep(5)

    # Step 2: Select the chat content
    pyautogui.moveTo(972, 202)
    pyautogui.dragTo(1639, 1412, duration=2.0, button='left')

    # Step 3: Copy text to clipboard
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(2)
    pyautogui.click(1994, 281)

    # Step 4: Get chat history
    chat_history = pyperclip.paste()

    print(chat_history)
    print(is_last_message_from_sender(chat_history))



    if is_last_message_from_sender(chat_history):
        # Step 5: Prepare prompt for Gemini
        prompt = f"""

I am a person named Vishal who speaks Hindi and English, is from India.
Analyze the chat history below and respond in a friendly, human-like way as Vishal: 


{chat_history}
"""

        # Step 6: Use Gemini to generate response
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)


        # Step 7: Copy and send the response
        pyperclip.copy(response.text)

        pyautogui.click(1808, 1328)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')

