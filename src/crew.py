from crewai import Crew, Process
from src.agents import (
    build_classifier_agent,
    build_router_agent,
    build_response_drafter_agent,
)
from src.tasks import (
    build_classification_task,
    build_routing_task,
    build_drafting_task,
)


def run_triage(issues_path: str) -> str:
    classifier = build_classifier_agent()
    router = build_router_agent()
    drafter = build_response_drafter_agent()

    classification_task = build_classification_task(classifier, issues_path)
    routing_task = build_routing_task(router, context_tasks=[classification_task])
    drafting_task = build_drafting_task(drafter, context_tasks=[classification_task, routing_task])

    crew = Crew(
        agents=[classifier, router, drafter],
        tasks=[classification_task, routing_task, drafting_task],
        process=Process.sequential,
        verbose=True,
    )

    return crew.kickoff()
