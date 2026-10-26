"""Deterministic daily question selection."""
from datetime import date
from collections import defaultdict

from .models import DailyAssessment, Question

# Aim for five distinct domains in each assessment. Date-based rotation makes
# the daily set reproducible without asking an LLM to choose questions.
DOMAIN_ORDER = (
    "decision_making",
    "emotional_regulation",
    "motivation",
    "social_behavior",
    "behavioral_patterns",
    "self_perception",
    "relationships",
    "ambiguity_tolerance",
)


def select_daily_questions(
    questions: list[Question],
    assessment_date: date,
    answered_question_ids: set[str] | None = None,
) -> tuple[Question, ...]:
    """Select five questions, preferring unseen questions and broad coverage.

    Reproducible for a given date and answer history. If the user has answered
    the entire bank, questions may recur; repetition is not treated as failure.
    """
    if len(questions) < 5:
        raise ValueError("At least five bank questions are required.")
    answered = answered_question_ids or set()
    by_domain: dict[str, list[Question]] = defaultdict(list)
    for question in questions:
        by_domain[question.domain].append(question)

    domain_order = list(DOMAIN_ORDER)
    # Rotate the starting domain so the first slot is not always the same.
    offset = assessment_date.toordinal() % len(domain_order)
    domain_order = domain_order[offset:] + domain_order[:offset]
    selected: list[Question] = []
    used_domains: set[str] = set()

    for domain in domain_order:
        candidates = by_domain.get(domain, [])
        candidates = sorted(candidates, key=lambda q: (q.id in answered, q.id))
        candidate = next((q for q in candidates if q.id not in {s.id for s in selected}), None)
        if candidate is not None:
            selected.append(candidate)
            used_domains.add(domain)
        if len(selected) == 5:
            break

    # Support custom domains and small banks with fewer than five configured domains.
    remaining = sorted(questions, key=lambda q: (q.id in answered, q.domain, q.id))
    for question in remaining:
        if len(selected) == 5:
            break
        if question.id not in {item.id for item in selected}:
            selected.append(question)

    if len(selected) != 5:
        raise ValueError("Could not select five unique questions.")
    return DailyAssessment(assessment_date, tuple(selected)).questions
