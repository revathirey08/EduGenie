import pytest

from utils import (
    clean_json_block,
    parse_json_safely,
    validate_user_text,
)


def test_clean_json_block():

    value = """```json
    {"name": "EduGenie"}
    ```"""

    result = clean_json_block(value)

    assert result == '{"name": "EduGenie"}'


def test_parse_json_safely():

    value = """```json
    {
        "name": "EduGenie",
        "version": "1.0"
    }
    ```"""

    result = parse_json_safely(value)

    assert result["name"] == "EduGenie"

    assert result["version"] == "1.0"


def test_validate_user_text():

    result = validate_user_text(
        "  Python Programming  "
    )

    assert result == "Python Programming"


def test_validate_empty_text():

    with pytest.raises(ValueError):

        validate_user_text("")


def test_validate_spaces():

    with pytest.raises(ValueError):

        validate_user_text("     ")