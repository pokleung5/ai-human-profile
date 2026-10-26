"""Conservative profile-update helpers.

The LLM is expected to propose hypotheses; this module validates basic safety
invariants and keeps raw answers outside the profile interpretation layer.
"""
from datetime import datetime, timezone
from .models import HumanProfile, Hypothesis


def replace_hypotheses(
    profile: HumanProfile,
    proposed: list[Hypothesis],
    *,
    minimum_supporting_evidence: int = 2,
) -> HumanProfile:
    """Apply a proposed profile snapshot while downgrading weakly supported claims.

    This is a deliberately small baseline, not a substitute for a full review
    policy. A hypothesis supported by fewer than two distinct answers cannot
    be marked high confidence.
    """
    normalized: list[Hypothesis] = []
    for hypothesis in proposed:
        evidence_ids = {e.answer_id for e in hypothesis.supporting_evidence}
        confidence = hypothesis.confidence
        if len(evidence_ids) < minimum_supporting_evidence and confidence == "high":
            confidence = "low"
        normalized.append(Hypothesis(
            id=hypothesis.id,
            statement=hypothesis.statement,
            domain=hypothesis.domain,
            confidence=confidence,
            supporting_evidence=hypothesis.supporting_evidence,
            counter_evidence=hypothesis.counter_evidence,
            open_questions=hypothesis.open_questions,
            updated_at=hypothesis.updated_at,
        ))
    profile.hypotheses = normalized
    profile.last_updated = datetime.now(timezone.utc)
    profile.version += 1
    return profile
