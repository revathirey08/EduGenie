from gemini_client import generate_text
from utils import validate_user_text


def answer_question(question: str) -> str:
    """
    Answer an educational question.
    """

    question = validate_user_text(question)

    prompt = f"""
You are EduGenie, an AI educational assistant.

Answer the student's question accurately and clearly.

Student question:
{question}

Instructions:
1. Give a direct answer first.
2. Explain the concept in simple language.
3. Use an example when useful.
4. Avoid unnecessary complexity.
5. If the question is academic, structure the answer clearly.
6. If you are uncertain about a fact, say so instead of inventing information.

Return only the educational answer.
"""

    return generate_text(
        prompt,
        temperature=0.3,
        max_output_tokens=1500
    )