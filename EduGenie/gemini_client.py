from functools import lru_cache

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    """
    Create and cache the Gemini client.
    """

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


def generate_text(
    prompt: str,
    temperature: float = 0.4,
    max_output_tokens: int = 2048,
) -> str:
    """
    Generate normal text using Gemini.
    """

    client = get_client()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()


def generate_json(
    prompt: str,
    response_schema,
    temperature: float = 0.3,
    max_output_tokens: int = 4096,
):
    """
    Generate structured JSON using a Pydantic schema.
    """

    client = get_client()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            response_mime_type="application/json",
            response_schema=response_schema,
        ),
    )

    parsed = getattr(response, "parsed", None)

    if parsed is not None:
        return parsed

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError(
            "Gemini returned an empty JSON response."
        )

    return response_schema.model_validate_json(text)