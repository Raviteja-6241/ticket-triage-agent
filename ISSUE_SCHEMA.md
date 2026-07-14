# Issue Schema — Shared Contract

This is the data contract that lets independent agents in the **Business Ops
Agent Suite** hand work off to each other without being tightly coupled.

Any upstream agent (e.g. the [Multi-Agent Data Pipeline](https://github.com/YOUR_USERNAME/multi-agent-data-pipeline)'s
Validator Agent) that produces a list of issues should emit them in this
shape. Any downstream agent (like this Triage Agent) only needs to know this
schema — not the internals of whichever agent produced it.

## `issue` object

```json
{
  "issue_id": "string, unique, e.g. 'DQ-1006'",
  "source": "string, which system/agent raised it, e.g. 'data-pipeline-validator'",
  "category": "string, e.g. 'missing_value' | 'negative_quantity' | 'duplicate' | 'pricing_anomaly'",
  "description": "string, human-readable description of the issue",
  "affected_records": ["array of strings, e.g. order_ids or row references"],
  "raised_at": "ISO 8601 timestamp",
  "raw_severity_hint": "optional string, upstream agent's rough guess: 'low' | 'medium' | 'high'"
}
```

## Example file: `issues.json`

```json
[
  {
    "issue_id": "DQ-1003",
    "source": "data-pipeline-validator",
    "category": "missing_value",
    "description": "Order 1003 is missing a quantity value.",
    "affected_records": ["1003"],
    "raised_at": "2026-06-02T10:00:00Z",
    "raw_severity_hint": "medium"
  },
  {
    "issue_id": "DQ-1006",
    "source": "data-pipeline-validator",
    "category": "negative_quantity",
    "description": "Order 1006 has a negative quantity (-3), possibly a return.",
    "affected_records": ["1006"],
    "raised_at": "2026-06-05T10:00:00Z",
    "raw_severity_hint": "high"
  }
]
```

## How to connect the two repos

In `multi-agent-data-pipeline`, add a small tool alongside `write_report_file`
that serializes the Validator Agent's findings into this schema and writes
`output/issues.json`. That file becomes the direct input to this repo's
`data/issues.json` (or feed it via API/shared storage in a real deployment).

This repo does **not** need to know anything about CSVs, sales data, or the
Extractor/Summarizer agents from Project 1 — it only needs a file that
matches this schema. That's the point: agents compose like functions with a
typed interface, not a monolithic script.
