"""Small, provider-neutral domain models.

These models intentionally distinguish raw answers from interpretations.
"""
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Literal


@dataclass(frozen=True)
class Option:
    id: str
    label: str


@dataclass(frozen=True)
class Question:
    id: str
    domain: str
    dimension: str
    prompt: str
    response_type: Literal["single_choice", "free_text"]
    options: tuple[Option, ...] = ()
    rationale: str = ""

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.domain.strip() or not self.dimension.strip():
            raise ValueError("Question id, domain, and dimension must be non-empty.")
        if self.response_type == "single_choice" and len(self.options) < 2:
            raise ValueError("Single-choice questions require at least two options.")
        if self.response_type == "free_text" and self.options:
            raise ValueError("Free-text questions must not define options.")
        option_ids = [option.id for option in self.options]
        if len(option_ids) != len(set(option_ids)):
            raise ValueError(f"Question {self.id!r} has duplicate option ids.")


@dataclass(frozen=True)
class Answer:
    user_id: str
    question_id: str
    answered_at: datetime
    choice_id: str | None = None
    free_text: str | None = None

    def __post_init__(self) -> None:
        if bool(self.choice_id) == bool(self.free_text):
            raise ValueError("Provide exactly one of choice_id or free_text.")


@dataclass(frozen=True)
class Evidence:
    answer_id: str
    question_id: str
    summary: str


@dataclass(frozen=True)
class Hypothesis:
    id: str
    statement: str
    domain: str
    confidence: Literal["low", "medium", "high"]
    supporting_evidence: tuple[Evidence, ...] = ()
    counter_evidence: tuple[Evidence, ...] = ()
    open_questions: tuple[str, ...] = ()
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class HumanProfile:
    user_id: str
    hypotheses: list[Hypothesis] = field(default_factory=list)
    last_updated: datetime | None = None
    version: int = 1


@dataclass(frozen=True)
class DailyAssessment:
    assessment_date: date
    questions: tuple[Question, ...]

    def __post_init__(self) -> None:
        if len(self.questions) != 5:
            raise ValueError("A daily assessment must contain exactly five questions.")
        ids = [question.id for question in self.questions]
        if len(ids) != len(set(ids)):
            raise ValueError("A daily assessment cannot repeat a question.")
