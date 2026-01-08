from ai.gemini_client import gemini_generate
from ai.groq_client import groq_generate

def ai_generate(prompt: str, mode="auto") -> str:
    """
    mode:
    - fast  → Groq
    - smart → Gemini
    - auto  → decides automatically
    """

    try:
        if mode == "fast":
            return groq_generate(prompt)

        if mode == "smart":
            return gemini_generate(prompt)

        # AUTO MODE
        if len(prompt) > 1500:
            return gemini_generate(prompt)  # better reasoning
        else:
            return groq_generate(prompt)    # faster

    except Exception as e:
        # 🔁 Fallback system
        try:
            return gemini_generate(prompt)
        except:
            return groq_generate(prompt)
