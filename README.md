# AI Human Profile

An AI life coach that builds an evolving, evidence-based understanding of a person through **five psychology-oriented questions each day**.

The product's core loop is:

1. Select a balanced set of five questions from a curated bank.
2. Record the user's answers as observations, without interpreting them as diagnoses.
3. Ask an LLM to propose cautious profile hypotheses grounded in those observations.
4. Store hypotheses separately from answers, including evidence, confidence, and contradictions.
5. Revise the profile as new evidence arrives and let the user correct it.

## Principles

- **Evidence before labels:** a single answer is not a personality verdict.
- **Separate facts from hypotheses:** original answers remain intact when interpretations change.
- **Uncertainty is first-class:** hypotheses include confidence and counter-evidence.
- **Deterministic control flow:** question selection and validation are application logic, not LLM decisions.
- **Psychology-informed, not diagnostic:** the sample bank is exploratory and is not a validated psychometric instrument.

## Quick start

Requires Python 3.11+; runtime has no third-party dependencies.

```bash
python -m unittest discover -s tests -v
python -m human_profile.cli daily --date 2026-10-25
```

To select questions from the bank in code:

```python
from datetime import date
from human_profile.question_bank import load_questions
from human_profile.assessment import select_daily_questions

questions = load_questions()
today = select_daily_questions(questions, date.today(), answered_question_ids=set())
for question in today:
    print(question.id, question.prompt)
```

## Project structure

- `src/human_profile/models.py` — typed domain models for questions, answers, observations, and hypotheses.
- `src/human_profile/question_bank.py` — loads and validates the curated JSON bank.
- `src/human_profile/assessment.py` — deterministic daily selection with domain coverage and repeat avoidance.
- `src/human_profile/profile.py` — profile update rules that preserve evidence and uncertainty.
- `src/human_profile/prompts/profile_analysis.md` — LLM analysis contract; provider integration is intentionally separate.
- `data/questions.json` — starter bank of psychology-oriented scenario questions.
- `tests/` — standard-library unit tests.

## Current scope

This is a domain-focused foundation, not a deployed web app or a validated assessment. It deliberately keeps LLM-provider wiring, authentication, database persistence, and UI out of the first increment. The data models and prompt contract establish boundaries before those integrations are added.

## Next milestones

1. Add a persistence adapter and answer submission API.
2. Add an LLM provider adapter with structured-output validation and retries.
3. Evaluate question quality, coverage, bias, and profile consistency with consented test data.
4. Build the daily answering and profile-review UI.
