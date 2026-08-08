# Spec: SignalRoot Agent

## Objective
Build an engineering incident triage agent that simulates a large-company internal SRE platform. The system accepts service alerts, calls tools for metrics, logs, deployment history, and known incidents, then generates an evidence-based triage report with likely root cause, impact, confidence, and next steps.

Target users are backend, infrastructure, SRE, and AI engineering internship interviewers reviewing whether this project demonstrates agent workflows beyond a generic chatbot.

## Tech Stack
- Python 3.12
- FastAPI
- Pydantic
- pytest
- In-memory deterministic demo data for alerts, metrics, logs, deploys, and prior incidents
- Optional future LLM provider boundary, but default behavior must run without paid APIs

## Commands
- Create venv: `python3.12 -m venv .venv && source .venv/bin/activate`
- Install: `pip install -r requirements.txt -r requirements-dev.txt`
- Run API: `uvicorn app.main:app --reload`
- Test: `python -m pytest`
- Docker: `docker build -t signalroot-agent . && docker run -p 8001:8000 signalroot-agent`

## Project Structure
- `app/main.py`: FastAPI entrypoint and routes
- `app/models.py`: API contracts and typed report schemas
- `app/data.py`: deterministic incident scenarios and telemetry
- `app/tools.py`: metric, log, deploy, and incident lookup tools
- `app/agent.py`: multi-step triage orchestration
- `app/dashboard.py`: static engineer-facing dashboard
- `tests/`: unit and API tests
- `docs/`: architecture and usage documentation

## Code Style
Use explicit, typed Python functions with small tool boundaries:

```python
def collect_evidence(alert: Alert) -> EvidenceBundle:
    metrics = metrics_tool.query(alert.service)
    logs = logs_tool.search(alert.service, alert.started_at)
    deploys = deploy_tool.recent(alert.service, alert.started_at)
    return EvidenceBundle(metrics=metrics, logs=logs, deploys=deploys)
```

## Testing Strategy
- Unit tests for root-cause hypothesis generation and evidence scoring.
- API tests for alert listing, triage report creation, health, and dashboard rendering.
- Tests must run without network, secrets, Docker, or external services.

## Boundaries
- Always: keep demo data deterministic, validate API inputs, run tests before claiming done.
- Ask first: adding paid LLM dependencies, external telemetry services, or authentication.
- Never: commit secrets, require paid APIs for default demo, make unsupported production claims.

## Success Criteria
- A user can run the API locally and open `/dashboard`.
- At least three incident scenarios produce distinct triage reports.
- Reports include evidence, likely root cause, confidence, blast radius, and next steps.
- Tests pass in CI and locally.
- README clearly explains large-company internship relevance and resume bullets.
