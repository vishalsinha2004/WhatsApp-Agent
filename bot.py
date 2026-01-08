import pyautogui
import time
import pyperclip
import google.generativeai as genai
import os
from dotenv import load_dotenv
from ai.router import ai_generate

# Disable failsafe for high-res screens
pyautogui.FAILSAFE = False 

# --- 1. DIAGNOSTICS & SETUP ---
# Use override=True to ensure the new key is always loaded
load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # Using the model version requested
    # Note: If you get a 'model not found' error, change this to 'gemini-2.0-flash'
    model = genai.GenerativeModel('gemini-2.5-flash')
    print(f"📡 Using API Key ending in: ...{api_key[-5:]}")
else:
    print("❌ ERROR: No API Key found in .env! Please add GEMINI_API_KEY=your_key")
    exit()

# Global variable to track the last message we replied to
last_message_text = ""

# --- 2. CORE FUNCTIONS ---

def get_last_message_details(chat_log):
    """
    Parses WhatsApp chat log to get the sender and the message.
    Format: [HH:MM, DD/MM/YYYY] Sender: Message
    """
    try:
        lines = chat_log.strip().split('\n')
        if not lines: return None, None
        
        last_line = lines[-1]
        if "] " in last_line and ": " in last_line:
            part_after_time = last_line.split("] ", 1)[1]
            sender, message = part_after_time.split(": ", 1)
            return sender.strip(), message.strip()
    except Exception:
        pass
    return None, None


def generate_vishal_response(chat_history):
    try:
        prompt = f"""
        You are Vishal, a friendly person from India who speaks Hinglish.

        INSTRUCTIONS:
        1. Reply ONLY to the last message
        2. Human, casual tone
        3. Output ONLY the message

        CHAT HISTORY:
        {chat_history}
        """

        return ai_generate(prompt, mode="auto")

    except Exception as e:
        print(f"❌ AI Error: {e}")
        return None
def send_whatsapp_message(message, max_retries=3):
    """
    Safely sends a WhatsApp message with verification and fallback.
    """

    for attempt in range(1, max_retries + 1):
        try:
            # Copy message to clipboard
            pyperclip.copy(message)
            time.sleep(0.2)

            # Verify clipboard
            if pyperclip.paste().strip() != message.strip():
                raise ValueError("Clipboard copy failed")

            # Focus message box
            pyautogui.click(1808, 1328)
            time.sleep(0.3)

            # Paste
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)

            # Final send
            pyautogui.press('enter')

            print(f"✅ Message sent successfully (attempt {attempt})")
            return True

        except Exception as e:
            print(f"⚠️ Send attempt {attempt} failed: {e}")
            time.sleep(0.5)

    # 🔁 Fallback: type message manually
    print("🧯 Fallback: typing message manually...")
    pyautogui.click(1808, 1328)
    time.sleep(0.3)
    pyautogui.typewrite(message, interval=0.02)
    pyautogui.press('enter')

    return False


# --- 3. MAIN LOOP ---

print("🚀 Bot starting in 3 seconds... Switch to WhatsApp Web.")
time.sleep(3)



while True:
    try:
        # Step A: Select and copy the chat area using coordinates from Main.py
        pyautogui.moveTo(1003, 237) 
        pyautogui.dragTo(2187, 1258, duration=1.0, button='left') 
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)
        pyautogui.click(1003, 237) # Click to deselect

        full_chat = pyperclip.paste()
        sender, message = get_last_message_details(full_chat)

        # Step B: Logic to decide if we should reply
        if message and sender != "Vishal" and message != last_message_text:
            print(f"📩 New message from {sender}: {message}")
            
            reply = generate_vishal_response(full_chat)
            
            if reply:
                print(f"📤 Proper Response: {reply}")
                
                # Step C: Send the reply
                send_whatsapp_message(reply)

                
                last_message_text = message 
        else:
            print("⏳ Waiting for new messages from others...")

    except Exception as e:
        print(f"⚠️ System Error: {e}")

    time.sleep(10)