from datetime import timedelta

from app.data import ALERTS, DEPLOYS, KNOWN_INCIDENTS, LOGS, METRICS
from app.models import Alert, DeployEvent, KnownIncident, LogEvent, MetricPoint


class AlertRepository:
    def list_alerts(self) -> list[Alert]:
        return ALERTS

    def get_alert(self, alert_id: str) -> Alert | None:
        return next((alert for alert in ALERTS if alert.id == alert_id), None)


class MetricsTool:
    name = "metrics.lookup"

    def query(self, service: str) -> list[MetricPoint]:
        return METRICS.get(service, [])


class LogSearchTool:
    name = "logs.search"

    def search(self, alert: Alert) -> list[LogEvent]:
        start = alert.started_at - timedelta(minutes=5)
        end = alert.started_at + timedelta(minutes=30)
        return [
            event
            for event in LOGS
            if event.service == alert.service and start <= event.timestamp <= end
        ]


class DeployHistoryTool:
    name = "deploys.recent"

    def recent(self, alert: Alert) -> list[DeployEvent]:
        start = alert.started_at - timedelta(minutes=60)
        return [
            deploy
            for deploy in DEPLOYS
            if deploy.service == alert.service and start <= deploy.timestamp <= alert.started_at
        ]


class KnownIncidentTool:
    name = "incidents.match"

    def match(self, alert: Alert, logs: list[LogEvent], metrics: list[MetricPoint]) -> list[KnownIncident]:
        haystack = " ".join(
            [alert.title, alert.description]
            + [log.message for log in logs]
            + [metric.name for metric in metrics]
        ).lower()

        matches = []
        for incident in KNOWN_INCIDENTS:
            if incident.service != alert.service:
                continue
            if any(token.lower() in haystack for token in incident.signature):
                matches.append(incident)
        return matches
