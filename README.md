# SignalRoot Agent

[![test](https://github.com/sunnnn2005/signalroot-agent/actions/workflows/test.yml/badge.svg)](https://github.com/sunnnn2005/signalroot-agent/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

SignalRoot is a small, deterministic incident-triage agent. It takes a service alert, calls a set of operational tools, ranks the evidence it finds, and returns a structured root-cause report.

The project is intentionally local-first. It does not call paid APIs or external observability vendors by default. The goal is to make the agent loop inspectable: every tool call, evidence item, hypothesis, and recommendation is visible in the response.

![SignalRoot Agent dashboard](docs/assets/signalroot-dashboard.png)

## The Model

SignalRoot is built around four simple objects:

- **Alert**: the incident entry point, including service, signal, severity, and start time.
- **Tool**: a deterministic source of operational context, such as metrics, logs, deploy history, or known incidents.
- **Evidence**: a weighted observation produced by a tool.
- **TriageReport**: the final report containing impact, blast radius, likely root cause, alternatives, next steps, and an agent trace.

The agent does not hide its reasoning behind a paragraph of generated text. It builds a report from typed objects, which makes the behavior easier to test and easier to replace with real integrations later.

## How It Works

1. Load the alert.
2. Query service metrics.
3. Search logs around the alert window.
4. Read recent deploy history.
5. Match against known incident signatures.
6. Convert all signals into weighted evidence.
7. Rank root-cause hypotheses.
8. Return a report with the supporting trace.

The current scenarios cover checkout latency, recommendation errors, and payment queue saturation. They are deterministic so tests can assert the actual behavior instead of only checking that the API returns a response.

## Why This Exists

Most incident demos stop at dashboards and alerts. SignalRoot explores the next step: turning observability signals into an operator-facing triage loop that is structured enough to test.

This is not meant to replace an SRE. It is a compact reference implementation for the agent pattern behind internal incident tools:

```text
alert -> tools -> evidence -> hypothesis -> action plan
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload
```

Open:

- Dashboard: `http://127.0.0.1:8000/dashboard`
- API docs: `http://127.0.0.1:8000/docs`

Run a triage request:

```bash
curl -X POST http://127.0.0.1:8000/alerts/alert_checkout_latency/triage
```

## API Surface

```text
GET  /health
GET  /alerts
GET  /alerts/{alert_id}
POST /alerts/{alert_id}/triage
GET  /dashboard
```

## Development

```bash
python -m pytest
```

Docker:

```bash
docker build -t signalroot-agent .
docker run --rm -p 8000:8000 signalroot-agent
```

## Contributing

Contributions are welcome. Good starter tasks are labeled [`good first issue`](https://github.com/sunnnn2005/signalroot-agent/labels/good%20first%20issue), and broader tasks are labeled [`help wanted`](https://github.com/sunnnn2005/signalroot-agent/labels/help%20wanted).

Useful first contributions:

- Add one deterministic incident scenario
- Add one test for an edge case
- Improve dashboard accessibility
- Improve documentation or examples
- Add an export format for reports

See [CONTRIBUTING.md](CONTRIBUTING.md) and [ROADMAP.md](ROADMAP.md) before opening a pull request.

## Repository Layout

```text
app/
  agent.py       Agent loop and root-cause ranking
  data.py        Local incident scenarios
  dashboard.py   Demo UI
  main.py        FastAPI routes
  models.py      Typed contracts
  tools.py       Operational tool adapters
docs/
  architecture.md
  spec.md
tests/
  test_agent.py
  test_api.py
```

## Safety and Scope

SignalRoot runs on local deterministic data. It does not connect to production systems, execute remediation commands, or send notifications. If real observability backends are added later, they should be implemented as explicit tool adapters with tests and read-only defaults.

## Roadmap

See [ROADMAP.md](ROADMAP.md) and the open issues for planned work.

## License

MIT
