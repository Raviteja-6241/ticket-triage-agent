import os
from crewai import Agent, LLM
from src.tools import load_issues, write_triage_tickets

llm = LLM(
    model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
    temperature=0.2,
)


def build_classifier_agent() -> Agent:
    return Agent(
        role="Ticket Classifier",
        goal="Load raw issues and assign each one a severity level "
             "(Critical, High, Medium, Low) based on business impact, "
             "not just the upstream hint.",
        backstory=(
            "You are an experienced support operations lead. You've seen "
            "enough incidents to know that a 'high' hint from an upstream "
            "system doesn't always mean business-critical, and vice versa. "
            "You reason about actual impact: financial exposure, customer "
            "visibility, and data integrity risk."
        ),
        tools=[load_issues],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def build_router_agent() -> Agent:
    return Agent(
        role="Ticket Router",
        goal="Assign each classified issue to the correct owning team: "
             "'Data Engineering' (pipeline/ETL issues), 'Finance' (pricing "
             "anomalies), 'Sales Ops' (duplicate/customer-facing order "
             "issues), or 'Data Quality' (general missing/invalid data).",
        backstory=(
            "You are an operations coordinator who knows exactly which "
            "team owns which category of problem, and you never let a "
            "ticket sit unrouted."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def build_response_drafter_agent() -> Agent:
    return Agent(
        role="First-Response Drafter",
        goal="Write a short, professional first-response note for each "
             "ticket that could be sent to the responsible team, "
             "summarizing the issue and suggesting an immediate next "
             "action.",
        backstory=(
            "You are a business systems analyst who writes clear, concise "
            "communications that get busy engineers and analysts to act "
            "quickly without needing to re-read the raw data."
        ),
        tools=[write_triage_tickets],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
