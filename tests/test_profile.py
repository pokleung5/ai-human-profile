import unittest

from human_profile.models import Evidence, HumanProfile, Hypothesis
from human_profile.profile import replace_hypotheses


class ProfileTests(unittest.TestCase):
    def test_high_confidence_with_one_answer_is_downgraded(self):
        hypothesis = Hypothesis(
            id="h1",
            statement="The user prefers planning.",
            domain="decision_making",
            confidence="high",
            supporting_evidence=(Evidence("a1", "q1", "Chose to plan ahead"),),
        )
        profile = replace_hypotheses(HumanProfile("user-1"), [hypothesis])
        self.assertEqual(profile.hypotheses[0].confidence, "low")
        self.assertEqual(profile.version, 2)

    def test_repeated_independent_evidence_can_retain_high_confidence(self):
        hypothesis = Hypothesis(
            id="h1",
            statement="The user often prefers planning.",
            domain="decision_making",
            confidence="high",
            supporting_evidence=(
                Evidence("a1", "q1", "Plans before acting"),
                Evidence("a2", "q2", "Prefers a clear plan"),
            ),
        )
        profile = replace_hypotheses(HumanProfile("user-1"), [hypothesis])
        self.assertEqual(profile.hypotheses[0].confidence, "high")


if __name__ == "__main__":
    unittest.main()
