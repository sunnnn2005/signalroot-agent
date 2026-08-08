# Security

SignalRoot is local-first and deterministic by default. It does not require secrets, production credentials, paid APIs, or external telemetry systems.

## Supported Use

The default project is safe to run locally because it only reads bundled scenario data.

## Reporting Issues

If you find a security issue, please open a GitHub issue with enough detail to reproduce it. Do not include secrets, private telemetry, or production data in the report.

## Integration Guidelines

Future integrations should follow these rules:

- read-only by default
- no secrets committed to the repository
- no production remediation commands in the default path
- clear failure behavior when credentials or external services are unavailable
- tests that run without network access

## Out of Scope

SignalRoot is not a production incident automation system. It does not claim to safely execute remediations, rollbacks, or paging workflows.
