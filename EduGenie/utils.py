import json
import re
from typing import Any


def clean_json_block(text: str) -> str:
    """
    Remove Markdown code fences from JSON responses.
    """

    if not text:
        return ""

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


def parse_json_safely(text: str) -> Any:
    """
    Parse JSON safely after removing Markdown fences.
    """

    cleaned = clean_json_block(text)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON returned by AI: {exc}"
        ) from exc


def validate_user_text(text: str) -> str:
    """
    Basic validation and cleanup.
    """

    if not text:
        raise ValueError("Input cannot be empty.")

    cleaned = text.strip()

    if not cleaned:
        raise ValueError("Input cannot contain only spaces.")

    return cleaned