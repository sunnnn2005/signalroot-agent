# Architecture

SignalRoot is a local-first incident-triage agent. It is organized as a small runtime loop: receive an alert, call read-only tools, convert observations into weighted evidence, rank hypotheses, and return a typed report.

The default implementation uses deterministic local data. That keeps the system inspectable, testable, and safe to run without credentials.

## Runtime Loop

```text
Alert
  -> MetricsTool
  -> LogSearchTool
  -> DeployHistoryTool
  -> KnownIncidentTool
  -> EvidenceItem[]
  -> RootCauseHypothesis[]
  -> TriageReport
```

The agent is deliberately not implemented as a single free-form prompt. Each step has an explicit typed boundary so behavior can be tested and replaced incrementally.

## Components

### API Layer

`app/main.py` exposes the FastAPI surface:

- health checks
- alert catalog
- individual alert lookup
- triage report generation
- dashboard rendering

The API returns Pydantic models rather than ad hoc dictionaries.

### Model Layer

`app/models.py` defines the contracts used across the runtime:

- `Alert`
- `MetricPoint`
- `LogEvent`
- `DeployEvent`
- `KnownIncident`
- `EvidenceItem`
- `RootCauseHypothesis`
- `TriageReport`

These models are the public shape of the system.

### Tool Layer

`app/tools.py` contains read-only adapters over local scenario data. The current tools simulate:

- metrics lookup
- log search
- deploy history
- known incident matching

Future production integrations should be added as new adapters with the same read-only default.

### Agent Layer

`app/agent.py` coordinates the tool calls and builds the final report. Its responsibilities are:

- call tools in a predictable order
- convert raw observations into weighted evidence
- rank root-cause hypotheses
- generate next-step recommendations
- include an `agent_trace` for inspection

### Dashboard Layer

`app/dashboard.py` provides a zero-build demo UI. It is intentionally simple so the backend remains the source of truth.

## Extension Points

Good extension points:

- add deterministic incident scenarios in `app/data.py`
- add read-only tool adapters in `app/tools.py`
- add hypothesis rules in `app/agent.py`
- add report export helpers
- add API tests for new behavior

Avoid mixing these layers in one large change. A good PR should usually update one scenario, one tool, one report behavior, or one dashboard interaction.

## Operational Boundaries

SignalRoot does not:

- connect to production systems by default
- execute remediation commands
- send alerts or notifications
- require paid APIs
- require secrets

Any future integration with real telemetry systems should preserve read-only defaults and include tests for failure behavior.

## Test Strategy

The tests verify both the agent loop and the API contract:

- known scenarios produce expected root-cause categories
- evidence is sorted by weight
- missing alerts return 404
- the dashboard renders
- the API returns typed reports

The project should remain runnable with:

```bash
python -m pytest
```
