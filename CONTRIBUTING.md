# Contributing

Thanks for your interest in SignalRoot Agent.

SignalRoot is meant to stay small, deterministic, and easy to inspect. Contributions should make the incident-triage loop clearer, more realistic, or easier to test.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
```

## Development Workflow

1. Fork the repository.
2. Create a focused branch.
3. Make one small change.
4. Run `python -m pytest`.
5. Open a pull request with a short summary and test plan.

## Pull Requests

Please keep changes focused and include tests for agent logic, API behavior, or dashboard behavior when relevant.

Good contribution areas:

- Add new incident scenarios
- Add new triage tools
- Improve root-cause ranking
- Improve dashboard usability
- Expand tests and documentation

## Good First Issues

Beginner-friendly tasks are labeled `good first issue`. A good first PR should usually touch one of these areas:

- `app/data.py` for a new deterministic scenario
- `tests/` for one new behavior test
- `README.md` or `docs/` for documentation
- `app/dashboard.py` for a small UI improvement

## Design Constraints

- Keep default behavior local-only and deterministic.
- Do not add paid API requirements to the default path.
- Prefer typed Pydantic models over unstructured dictionaries for API contracts.
- Keep tool adapters explicit and testable.
- Avoid large refactors unless they unlock a clear feature.
