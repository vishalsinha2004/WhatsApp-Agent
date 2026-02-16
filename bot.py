import pyautogui
import time
import pyperclip
import os
from dotenv import load_dotenv
from ai.router import ai_generate

# Disable failsafe for high-res screens (optional)
pyautogui.FAILSAFE = False

# Load environment variables (just to check API keys, though router handles them)
load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env")
    exit()

print(f"📡 Gemini API Key loaded (ends with ...{api_key[-5:]})")

# -------------------------------
# CONFIGURATION – adjust these coordinates to your screen!
# You can find them using the helper script Main.py
# -------------------------------
SELECT_START_X, SELECT_START_Y = 1003, 237      # Top‑left corner of the chat area
SELECT_END_X, SELECT_END_Y = 2187, 1258         # Bottom‑right corner
MESSAGE_BOX_X, MESSAGE_BOX_Y = 1808, 1328       # Where to click to type
# ------------------------------------------------

# Global variable to track the last message we replied to
last_message_text = ""

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------

def get_recent_history(chat_log, max_lines=8):
    """Return the last `max_lines` messages from the copied chat."""
    lines = chat_log.strip().split('\n')
    if not lines:
        return ""
    recent = lines[-max_lines:]
    return '\n'.join(recent)

def get_last_message_details(chat_log):
    """
    Parses WhatsApp chat log to get the sender and the message.
    Format: [HH:MM, DD/MM/YYYY] Sender: Message
    """
    try:
        lines = chat_log.strip().split('\n')
        if not lines:
            return None, None
        last_line = lines[-1]
        if "] " in last_line and ": " in last_line:
            part_after_time = last_line.split("] ", 1)[1]
            sender, message = part_after_time.split(": ", 1)
            return sender.strip(), message.strip()
    except Exception:
        pass
    return None, None

def generate_vishal_response(chat_history):
    """
    Builds an improved prompt with persona, few‑shot examples,
    and instructs to reply naturally.
    """
    try:
        # Use only the most recent messages to keep prompt focused
        recent = get_recent_history(chat_history, max_lines=8)

        prompt = f"""
You are Vishal, a 25‑year‑old from Mumbai who speaks casual Hinglish (mix of Hindi and English).
You are friendly, witty, and use common Indian expressions like "yaar", "accha", "bhai", "kya chal raha hai?".
You sometimes add emojis (😂, 👍, 😎) but don't overdo it.

Here are a few examples of how Vishal talks:

Friend: "Kal party kahan hai?"
Vishal: "Bhai, same place, 8 baje milte hain 👍"

Friend: "Can you help me with the project?"
Vishal: "Haan yaar, bata kya chahiye?"

Friend: "What's up?"
Vishal: "Bas mast, tu bata?"

Now here is the recent WhatsApp conversation (oldest to newest):
{recent}

Reply to the **last message** naturally, as if you're chatting with a friend.
- Keep it short and engaging.
- Match the language of the other person (if they use Hindi, reply in Hinglish; if English, reply in English).
- Do not include any labels, quotes, or explanations—just your message.
"""
        return ai_generate(prompt, mode="auto")

    except Exception as e:
        print(f"❌ AI generation error: {e}")
        return None

def send_whatsapp_message(message, max_retries=3):
    """
    Safely sends a WhatsApp message with verification and fallback typing.
    """
    for attempt in range(1, max_retries + 1):
        try:
            # Copy message to clipboard
            pyperclip.copy(message)
            time.sleep(0.2)

            # Verify clipboard content
            if pyperclip.paste().strip() != message.strip():
                raise ValueError("Clipboard copy failed")

            # Click on the message box
            pyautogui.click(MESSAGE_BOX_X, MESSAGE_BOX_Y)
            time.sleep(0.3)

            # Paste
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)

            # Send
            pyautogui.press('enter')

            print(f"✅ Message sent successfully (attempt {attempt})")
            return True

        except Exception as e:
            print(f"⚠️ Send attempt {attempt} failed: {e}")
            time.sleep(0.5)

    # Fallback: type message manually
    print("🧯 Fallback: typing message manually...")
    pyautogui.click(MESSAGE_BOX_X, MESSAGE_BOX_Y)
    time.sleep(0.3)
    pyautogui.typewrite(message, interval=0.02)
    pyautogui.press('enter')
    return False

# -------------------------------
# MAIN LOOP
# -------------------------------

print("🚀 Bot starting in 3 seconds... Switch to WhatsApp Web and ensure the chat is visible.")
time.sleep(3)

while True:
    try:
        # Step 1: Select and copy the chat area
        pyautogui.moveTo(SELECT_START_X, SELECT_START_Y)
        pyautogui.dragTo(SELECT_END_X, SELECT_END_Y, duration=1.0, button='left')
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)
        pyautogui.click(SELECT_START_X, SELECT_START_Y)  # Deselect

        full_chat = pyperclip.paste()
        sender, message = get_last_message_details(full_chat)

        # Step 2: Decide if we should reply
        if message and sender != "Vishal" and message != last_message_text:
            print(f"📩 New message from {sender}: {message}")

            reply = generate_vishal_response(full_chat)

            # Safety check – if reply is empty or too short, use a default
            if not reply or len(reply.strip()) < 2:
                reply = "Haha, got it! 😄"

            print(f"📤 Reply: {reply}")

            # Step 3: Send the reply
            send_whatsapp_message(reply)

            last_message_text = message  # Avoid re‑sending to the same message

        else:
            print("⏳ Waiting for new messages from others...")

    except Exception as e:
        print(f"⚠️ System error: {e}")

    time.sleep(10)  # Check every 10 seconds