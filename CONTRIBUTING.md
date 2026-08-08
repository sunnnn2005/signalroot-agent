# Contributing

Thanks for your interest in SignalRoot Agent.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
```

## Pull Requests

Please keep changes focused and include tests for agent logic, API behavior, or dashboard behavior when relevant.

Good contribution areas:

- Add new incident scenarios
- Add new triage tools
- Improve root-cause ranking
- Improve dashboard usability
- Expand tests and documentation
