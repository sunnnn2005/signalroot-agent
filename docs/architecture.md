# SignalRoot Agent Architecture

SignalRoot Agent is a deterministic incident-triage service built to look and behave like a small internal platform engineering tool. It receives service alerts, gathers evidence from operational data sources, ranks likely root causes, and returns a structured incident report.

## Components

- **FastAPI service** exposes health, alert catalog, triage, and dashboard routes.
- **Agent layer** coordinates tool calls, builds evidence, creates hypotheses, and recommends next steps.
- **Tool layer** simulates production integrations for metrics, logs, deploy history, and known incidents.
- **Static dashboard** lets reviewers run triage flows without extra frontend setup.
- **Tests** cover agent reasoning, API contracts, error handling, and dashboard rendering.

## Agent Flow

1. Receive an alert from the alert repository.
2. Query metrics for abnormal service-level signals.
3. Search logs around the alert window.
4. Read recent deploy history for risky changes.
5. Match the current signature against known incidents.
6. Convert all sources into weighted evidence.
7. Rank root-cause hypotheses.
8. Return impact, blast radius, evidence, recommendations, and an agent trace.

## Why It Is Resume-Ready

The project demonstrates API design, production debugging, observability thinking, deterministic agent orchestration, test coverage, and a usable demo surface. It does not depend on paid APIs, so recruiters and interviewers can run it locally.
