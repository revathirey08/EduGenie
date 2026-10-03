from gemini_client import generate_text
from utils import validate_user_text


def summarize_text(text: str) -> str:
    """
    Summarize educational content.
    """

    text = validate_user_text(text)

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational text.

TEXT:
{text}

Requirements:
1. Keep the important information.
2. Remove repetition.
3. Use simple English.
4. Do not introduce facts that are not in the source text.
5. Make the result useful for quick revision.
6. Use headings or bullet points when helpful.

Return only the summary.
"""

    return generate_text(
        prompt,
        temperature=0.2,
        max_output_tokens=2000
    )