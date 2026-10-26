import unittest
from datetime import date

from human_profile.assessment import select_daily_questions
from human_profile.question_bank import load_questions


class DailyAssessmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions = load_questions()

    def test_selects_exactly_five_unique_questions(self):
        selected = select_daily_questions(self.questions, date(2026, 10, 25))
        self.assertEqual(len(selected), 5)
        self.assertEqual(len({question.id for question in selected}), 5)

    def test_selection_is_reproducible(self):
        first = select_daily_questions(self.questions, date(2026, 10, 25))
        second = select_daily_questions(self.questions, date(2026, 10, 25))
        self.assertEqual([q.id for q in first], [q.id for q in second])

    def test_prefers_unanswered_questions(self):
        selected = select_daily_questions(
            self.questions,
            date(2026, 10, 25),
            answered_question_ids={q.id for q in self.questions[:10]},
        )
        self.assertTrue(all(q.id not in {item.id for item in self.questions[:10]} for q in selected))

    def test_daily_domains_are_broad_when_bank_allows(self):
        selected = select_daily_questions(self.questions, date(2026, 10, 25))
        self.assertEqual(len({q.domain for q in selected}), 5)


if __name__ == "__main__":
    unittest.main()
