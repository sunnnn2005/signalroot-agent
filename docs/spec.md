# Specification

SignalRoot is a deterministic incident-triage agent for local experimentation with agentic reliability workflows.

## Purpose

The system turns operational signals into a structured triage report. It is designed for inspection rather than automation theater: tool calls are explicit, evidence is typed, and the report can be tested.

## Non-Goals

- No production remediation.
- No automatic rollback.
- No required LLM provider.
- No required external observability vendor.
- No hidden network calls in the default path.

## Functional Requirements

- List available alerts.
- Return an individual alert by id.
- Generate a triage report for a known alert.
- Include impact, blast radius, evidence, likely root cause, alternatives, recommendations, timestamp, and trace.
- Return a clear 404 for unknown alerts.
- Render a browser dashboard with the same backend data.

## Runtime Contracts

### Alert

An alert is the entry point for the runtime. It includes service, severity, signal type, start time, and description.

### EvidenceItem

Evidence is a weighted observation from a tool. It must identify its source and explain the observation in a stable summary string.

### RootCauseHypothesis

A hypothesis contains a cause, confidence score, reasoning, and supporting evidence.

### TriageReport

The report is the final output. It should be useful both as JSON and as a source for future markdown/text exports.

## Tool Contracts

Current tools are deterministic local adapters:

- `MetricsTool`
- `LogSearchTool`
- `DeployHistoryTool`
- `KnownIncidentTool`

Future tools should follow the same pattern:

- read-only by default
- explicit inputs
- typed outputs
- no hidden mutation
- tested failure behavior

## Commands

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload
python -m pytest
```

Docker:

```bash
docker build -t signalroot-agent .
docker run --rm -p 8000:8000 signalroot-agent
```

## Quality Bar

- Tests must pass locally and in CI.
- New scenarios should be deterministic.
- New report fields should be represented as typed Pydantic models.
- New tools should not require secrets in the default path.
- Documentation should describe behavior without overstating production readiness.
