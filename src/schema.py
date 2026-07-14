"""
Typed representation of the shared Issue schema (see ISSUE_SCHEMA.md).

Keeping this as a small, dependency-free module means other agents in the
suite can import just this file if they want type-safe access to the
contract, without pulling in this whole project.
"""

from dataclasses import dataclass, field
from typing import List, Optional
import json


@dataclass
class Issue:
    issue_id: str
    source: str
    category: str
    description: str
    affected_records: List[str] = field(default_factory=list)
    raised_at: str = ""
    raw_severity_hint: Optional[str] = None

    @staticmethod
    def load_from_file(path: str) -> List["Issue"]:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [Issue(**item) for item in raw]

    def to_prompt_line(self) -> str:
        """Compact single-line representation used when feeding issues to an LLM."""
        records = ", ".join(self.affected_records)
        return (
            f"[{self.issue_id}] category={self.category} "
            f"records=({records}) hint={self.raw_severity_hint} :: {self.description}"
        )
