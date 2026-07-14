import os
import json
from crewai.tools import tool
from src.schema import Issue


@tool("Load Issues")
def load_issues(file_path: str) -> str:
    """
    Loads issues from a JSON file matching the shared Issue schema and
    returns them as a formatted list for triage. Use this first to see
    what needs to be classified and routed.
    """
    if not os.path.exists(file_path):
        return f"ERROR: File not found at {file_path}"

    issues = Issue.load_from_file(file_path)
    lines = [issue.to_prompt_line() for issue in issues]
    return f"Loaded {len(issues)} issues:\n" + "\n".join(lines)


@tool("Write Triage Tickets")
def write_triage_tickets(content: str, output_path: str = "output/triaged_tickets.md") -> str:
    """
    Writes the final triaged ticket list (with severity, routing team, and
    a drafted first response for each) to a markdown file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Triaged tickets written to {output_path}"
