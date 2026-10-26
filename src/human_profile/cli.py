"""Small CLI to preview the five-question daily assessment."""
import argparse
from datetime import date

from .assessment import select_daily_questions
from .question_bank import load_questions


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview a daily psychology-oriented assessment.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    daily = subparsers.add_parser("daily", help="Select today's five questions")
    daily.add_argument("--date", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()

    if args.command == "daily":
        questions = select_daily_questions(load_questions(), args.date)
        print(f"Daily assessment — {args.date.isoformat()} (5 questions)\n")
        for index, question in enumerate(questions, start=1):
            print(f"{index}. [{question.domain} / {question.dimension}] {question.prompt}")
            for option in question.options:
                print(f"   {option.id}) {option.label}")
            if question.response_type == "free_text":
                print("   (free-text response)")
            print()


if __name__ == "__main__":
    main()
