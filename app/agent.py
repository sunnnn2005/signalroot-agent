from datetime import datetime, timezone

from app.models import Alert, EvidenceItem, RootCauseHypothesis, TriageReport
from app.tools import DeployHistoryTool, KnownIncidentTool, LogSearchTool, MetricsTool


class SignalRootAgent:
    def __init__(
        self,
        metrics_tool: MetricsTool | None = None,
        log_tool: LogSearchTool | None = None,
        deploy_tool: DeployHistoryTool | None = None,
        incident_tool: KnownIncidentTool | None = None,
    ) -> None:
        self.metrics_tool = metrics_tool or MetricsTool()
        self.log_tool = log_tool or LogSearchTool()
        self.deploy_tool = deploy_tool or DeployHistoryTool()
        self.incident_tool = incident_tool or KnownIncidentTool()

    def triage(self, alert: Alert) -> TriageReport:
        trace = [f"received alert {alert.id} for {alert.service}"]

        metrics = self.metrics_tool.query(alert.service)
        trace.append(f"called {self.metrics_tool.name}: {len(metrics)} metrics")

        logs = self.log_tool.search(alert)
        trace.append(f"called {self.log_tool.name}: {len(logs)} log events")

        deploys = self.deploy_tool.recent(alert)
        trace.append(f"called {self.deploy_tool.name}: {len(deploys)} deploy events")

        known_incidents = self.incident_tool.match(alert, logs, metrics)
        trace.append(f"called {self.incident_tool.name}: {len(known_incidents)} known incidents")

        evidence = self._build_evidence(metrics, logs, deploys, known_incidents)
        likely, alternatives = self._hypothesize(alert, evidence)

        return TriageReport(
            alert=alert,
            impact=self._impact(alert),
            blast_radius=self._blast_radius(alert.service),
            evidence=evidence,
            likely_root_cause=likely,
            alternative_hypotheses=alternatives,
            recommended_next_steps=self._next_steps(likely.cause, alert.service),
            generated_at=datetime.now(timezone.utc),
            agent_trace=trace,
        )

    def _build_evidence(self, metrics, logs, deploys, known_incidents) -> list[EvidenceItem]:
        evidence: list[EvidenceItem] = []

        for metric in metrics:
            if metric.status != "normal":
                weight = 0.9 if metric.status == "critical" else 0.55
                evidence.append(EvidenceItem(source="metrics", summary=f"{metric.name}={metric.value}{metric.unit}: {metric.detail}", weight=weight))

        for log in logs:
            if log.level in {"ERROR", "WARN"}:
                weight = 0.8 if log.level == "ERROR" else 0.45
                evidence.append(EvidenceItem(source="logs", summary=f"{log.level} {log.message} ({log.trace_id})", weight=weight))

        for deploy in deploys:
            weight = {"low": 0.25, "medium": 0.55, "high": 0.85}[deploy.risk]
            evidence.append(EvidenceItem(source="deploys", summary=f"{deploy.version} by {deploy.author}: {deploy.summary}", weight=weight))

        for incident in known_incidents:
            evidence.append(EvidenceItem(source="known_incidents", summary=f"{incident.id}: {incident.title}, prior root cause: {incident.root_cause}", weight=0.8))

        return sorted(evidence, key=lambda item: item.weight, reverse=True)

    def _hypothesize(self, alert: Alert, evidence: list[EvidenceItem]) -> tuple[RootCauseHypothesis, list[RootCauseHypothesis]]:
        text = " ".join(item.summary.lower() for item in evidence)
        candidates: list[RootCauseHypothesis] = []

        if "database" in text or "connection pool" in text or "db_query" in text:
            candidates.append(self._hypothesis("database query regression or pool saturation", 0.9, evidence))
        if "vector feature" in text or "feature store" in text or "model_timeout" in text:
            candidates.append(self._hypothesis("ML feature store timeout after feature rollout", 0.9, evidence))
        if "queue" in text or "worker_cpu" in text or "batch" in text:
            candidates.append(self._hypothesis("worker saturation from batch size or ingest/drain imbalance", 0.86, evidence))
        if "traffic" in text or alert.signal == "traffic":
            candidates.append(self._hypothesis("traffic spike exceeded service capacity", 0.55, evidence))

        if not candidates:
            candidates.append(self._hypothesis("unknown service regression requiring manual investigation", 0.35, evidence))

        candidates.sort(key=lambda item: item.confidence, reverse=True)
        return candidates[0], candidates[1:3]

    def _hypothesis(self, cause: str, confidence: float, evidence: list[EvidenceItem]) -> RootCauseHypothesis:
        supporting = [item.summary for item in evidence[:4]]
        return RootCauseHypothesis(
            cause=cause,
            confidence=confidence,
            reasoning=f"The strongest evidence points to {cause}. The agent correlated high-weight metrics, logs, deploys, and prior incidents.",
            supporting_evidence=supporting,
        )

    def _impact(self, alert: Alert) -> str:
        if alert.severity.value in {"CRITICAL", "HIGH"}:
            return f"{alert.service} is likely affecting user-facing reliability for the alerted path."
        return f"{alert.service} has degraded operational health but limited confirmed user impact."

    def _blast_radius(self, service: str) -> list[str]:
        mapping = {
            "checkout-api": ["checkout flow", "inventory reservation", "order creation"],
            "recommendation-api": ["home feed ranking", "product recommendations", "personalization fallback"],
            "payments-worker": ["payment capture delay", "settlement queue", "merchant payout freshness"],
        }
        return mapping.get(service, [service])

    def _next_steps(self, cause: str, service: str) -> list[str]:
        if "database" in cause:
            return [
                "Compare database query plans before and after the latest deploy.",
                "Temporarily rollback the inventory reservation query path.",
                "Increase connection pool visibility and page database owner if pool wait stays high.",
            ]
        if "feature store" in cause:
            return [
                "Disable the vector feature flag for the affected traffic slice.",
                "Check feature store timeout and retry dashboards.",
                "Replay failed recommendation requests after fallback stabilizes.",
            ]
        if "worker saturation" in cause:
            return [
                "Revert recent worker batch-size change.",
                "Scale workers until drain rate exceeds ingest rate.",
                "Add a guardrail alert for queue growth rate, not only absolute depth.",
            ]
        return [
            f"Open an incident channel for {service}.",
            "Assign owners for metrics, logs, deploy review, and customer impact.",
            "Collect five fresh traces before deciding rollback or mitigation.",
        ]
