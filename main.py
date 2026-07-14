"""
Ticket Triage Agent
--------------------
Part of the Business Ops Agent Suite. Consumes issues emitted by the
Multi-Agent Data Pipeline (or any agent following ISSUE_SCHEMA.md) and
classifies, routes, and drafts first-response tickets for them.

Run with:
    python main.py
"""

from dotenv import load_dotenv
from src.crew import run_triage

load_dotenv()

ISSUES_PATH = "data/issues.json"


def main():
    print(f"Starting triage on: {ISSUES_PATH}\n{'=' * 50}")
    result = run_triage(ISSUES_PATH)
    print("\n" + "=" * 50)
    print("TRIAGE COMPLETE")
    print("=" * 50)
    print(result)


if __name__ == "__main__":
    main()
