from crewai import Task


def build_classification_task(agent, issues_path: str) -> Task:
    return Task(
        description=(
            f"Load the issues from '{issues_path}' using the Load Issues "
            "tool. For each issue, assign a severity: Critical, High, "
            "Medium, or Low, with a one-sentence justification based on "
            "business impact (financial exposure, customer visibility, "
            "or data integrity risk)."
        ),
        expected_output=(
            "A markdown table: issue_id | category | assigned_severity | "
            "justification."
        ),
        agent=agent,
    )


def build_routing_task(agent, context_tasks) -> Task:
    return Task(
        description=(
            "Using the classified issues, assign each one to the correct "
            "owning team: 'Data Engineering', 'Finance', 'Sales Ops', or "
            "'Data Quality'. Justify each assignment in a few words."
        ),
        expected_output=(
            "A markdown table: issue_id | assigned_severity | routed_team | "
            "routing_reason."
        ),
        agent=agent,
        context=context_tasks,
    )


def build_drafting_task(agent, context_tasks) -> Task:
    return Task(
        description=(
            "For each routed ticket, write a short first-response note "
            "(3-4 sentences) addressed to the owning team, summarizing "
            "the issue and suggesting an immediate next action. Compile "
            "all tickets, sorted by severity (Critical first), into one "
            "markdown document and save it using the Write Triage Tickets "
            "tool to 'output/triaged_tickets.md'."
        ),
        expected_output=(
            "Confirmation the file was written, plus the full triaged "
            "ticket document."
        ),
        agent=agent,
        context=context_tasks,
    )
