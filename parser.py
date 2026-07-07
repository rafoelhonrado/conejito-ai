"""
parser.py
"""

import json
from datetime import date, timedelta
from typing import Annotated

from pydantic import TypeAdapter, Field

from llm import chat
from prompts import SYSTEM_PROMPT, build_user_prompt
from schemas import FinanceAction


FinanceActionAdapter = TypeAdapter(
    Annotated[
        FinanceAction,
        Field(discriminator="action")
    ]
)


def extract_json(text: str) -> dict:
    if not text:
        raise ValueError("Empty model response")

    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(f"No JSON object found:\n{text}")

    return json.loads(text[start:end + 1])


def parse_user_message(user_message: str):
    today = date.today()
    yesterday = today - timedelta(days=1)

    # IMPORTANT: do not use .format() because SYSTEM_PROMPT contains JSON braces
    system_prompt = (
        SYSTEM_PROMPT
        .replace("{today}", today.isoformat())
        .replace("{yesterday}", yesterday.isoformat())
    )

    user_prompt = build_user_prompt(user_message)

    raw_output = chat(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=512
    )

    print("\nMODEL OUTPUT")
    print(raw_output)

    data = extract_json(raw_output)

    if data.get("action") == "clarify":
        return data

    return FinanceActionAdapter.validate_python(data)
