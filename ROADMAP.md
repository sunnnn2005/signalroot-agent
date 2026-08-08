# Roadmap

SignalRoot is intentionally small, but it should grow in directions that make the agent loop more useful and more inspectable.

## Near Term

- Add more deterministic incident scenarios.
- Add markdown export for triage reports.
- Improve dashboard accessibility and keyboard navigation.
- Add tests for unknown or low-evidence alerts.
- Document how to add a new tool adapter.

## Medium Term

- Add read-only adapters for Prometheus-style metrics.
- Add read-only adapters for log search systems.
- Add deploy-history adapters for GitHub releases or commit metadata.
- Add a timeline view that shows alerts, deploys, logs, metrics, and known incidents together.
- Add confidence calibration tests for the ranking logic.

## Long Term

- Support incident sessions that track multiple triage reports over time.
- Add configurable weighting rules.
- Add report exports suitable for incident tickets.
- Add a plugin interface for custom organization-specific tools.

## Contribution Notes

Good roadmap issues should stay small enough to review in one pull request. If a feature touches multiple layers, split it into a data/model PR, agent PR, and dashboard PR.
