from gemini_client import generate_text
from utils import validate_user_text


def explain_concept(topic: str) -> str:
    """
    Explain a difficult concept in beginner-friendly language.
    """

    topic = validate_user_text(topic)

    prompt = f"""
You are EduGenie, a patient educational teacher.

Explain the following concept to a beginner:

{topic}

Follow this structure:

1. Simple definition
2. Why it is important
3. How it works
4. Real-world example
5. Simple example
6. Key points to remember

Rules:
- Use simple English.
- Avoid unnecessary technical words.
- If you use a technical word, explain it.
- Keep the explanation suitable for students.
- Do not assume advanced knowledge.
"""

    return generate_text(
        prompt,
        temperature=0.4,
        max_output_tokens=1800
    )