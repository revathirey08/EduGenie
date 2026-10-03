from gemini_client import generate_text
from utils import validate_user_text


def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    days_per_week: int = 5,
    hours_per_day: float = 1.0,
) -> str:
    """
    Generate a personalized learning roadmap.
    """

    topic = validate_user_text(topic)
    level = validate_user_text(level)

    prompt = f"""
You are EduGenie, a personalized learning mentor.

Create a structured learning roadmap for:

Topic:
{topic}

Student level:
{level}

Study schedule:
{days_per_week} days per week
{hours_per_day} hours per day

Create a practical roadmap from the student's current level toward advanced understanding.

Include:

1. Learning goal
2. Prerequisites
3. Beginner stage
4. Intermediate stage
5. Advanced stage
6. Weekly study plan
7. Practice activities
8. Mini-project ideas
9. Revision strategy
10. Interview or assessment preparation
11. Recommended types of resources

For resources, recommend resource TYPES or well-known learning platforms/books/videos where appropriate.
Do not invent URLs.

Keep the roadmap realistic for the available study schedule.
"""

    return generate_text(
        prompt,
        temperature=0.5,
        max_output_tokens=3500
    )