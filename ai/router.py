from ai.gemini_client import gemini_generate
from ai.groq_client import groq_generate

def ai_generate(prompt: str, mode="auto") -> str:
    """
    mode:
    - fast  → Groq
    - smart → Gemini
    - auto  → decides based on length and presence of a question
    """
    try:
        if mode == "fast":
            return groq_generate(prompt)

        if mode == "smart":
            return gemini_generate(prompt)

        # AUTO MODE
        if "?" in prompt or len(prompt) > 1500:
            # Questions or long prompts get the smarter model
            return gemini_generate(prompt)
        else:
            return groq_generate(prompt)

    except Exception as e:
        # Fallback system
        try:
            return gemini_generate(prompt)
        except:
            return groq_generate(prompt)