from gemini_client import generate_json
from models import QuizResponse
from utils import validate_user_text


def generate_quiz(text: str) -> QuizResponse:
    """
    Generate exactly three MCQs with four options each.
    """

    text = validate_user_text(text)

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly 3 multiple-choice questions from the provided educational text.

SOURCE TEXT:
{text}

Requirements:

- Generate exactly 3 questions.
- Every question must have exactly 4 options.
- There must be exactly one correct answer.
- The correct answer must exactly match one of the four options.
- Questions must be based only on the provided text.
- Create plausible incorrect options.
- Include a short explanation for every answer.
- Make the questions suitable for student learning.
- Do not create trick questions.

Return the result according to the requested structured schema.
"""

    result = generate_json(
        prompt,
        QuizResponse,
        temperature=0.3,
        max_output_tokens=3000
    )

    return result