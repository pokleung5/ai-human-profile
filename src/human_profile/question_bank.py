"""Question bank loading and structural validation."""
import json
from pathlib import Path
from typing import Iterable

from .models import Option, Question

DEFAULT_BANK_PATH = Path(__file__).resolve().parents[2] / "data" / "questions.json"


def load_questions(path: Path = DEFAULT_BANK_PATH) -> list[Question]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Question bank root must be a JSON array.")
    questions = [question_from_dict(item) for item in payload]
    validate_bank(questions)
    return questions


def question_from_dict(item: dict) -> Question:
    options = tuple(Option(id=option["id"], label=option["label"])
                    for option in item.get("options", []))
    return Question(
        id=item["id"],
        domain=item["domain"],
        dimension=item["dimension"],
        prompt=item["prompt"],
        response_type=item["response_type"],
        options=options,
        rationale=item.get("rationale", ""),
    )


def validate_bank(questions: Iterable[Question]) -> None:
    items = list(questions)
    if len(items) < 5:
        raise ValueError("Question bank must contain at least five questions.")
    ids = [question.id for question in items]
    if len(ids) != len(set(ids)):
        raise ValueError("Question ids must be unique.")
    domains = {question.domain for question in items}
    if len(domains) < 5:
        raise ValueError("Question bank must cover at least five domains.")
