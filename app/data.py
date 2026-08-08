from datetime import datetime, timezone

from app.models import Alert, DeployEvent, KnownIncident, LogEvent, MetricPoint, Severity


ALERTS = [
    Alert(
        id="alert_checkout_latency",
        service="checkout-api",
        title="checkout-api p95 latency above 900ms",
        severity=Severity.high,
        started_at=datetime(2026, 8, 8, 8, 15, tzinfo=timezone.utc),
        signal="latency",
        description="p95 latency stayed above the 900ms paging threshold for 10 minutes.",
    ),
    Alert(
        id="alert_recommendation_errors",
        service="recommendation-api",
        title="recommendation-api 5xx error rate spike",
        severity=Severity.critical,
        started_at=datetime(2026, 8, 8, 9, 5, tzinfo=timezone.utc),
        signal="errors",
        description="5xx rate crossed 8 percent after a model feature rollout.",
    ),
    Alert(
        id="alert_payments_saturation",
        service="payments-worker",
        title="payments-worker queue saturation",
        severity=Severity.medium,
        started_at=datetime(2026, 8, 8, 10, 30, tzinfo=timezone.utc),
        signal="saturation",
        description="Payment queue depth is growing faster than worker drain rate.",
    ),
]


METRICS = {
    "checkout-api": [
        MetricPoint(name="p95_latency_ms", value=1240, unit="ms", status="critical", detail="Baseline is 280ms."),
        MetricPoint(name="error_rate", value=1.8, unit="percent", status="warning", detail="Small increase, not primary signal."),
        MetricPoint(name="db_query_p95_ms", value=940, unit="ms", status="critical", detail="Database query latency rose before API latency."),
        MetricPoint(name="request_rate", value=1320, unit="rpm", status="normal", detail="Traffic is within normal weekday band."),
    ],
    "recommendation-api": [
        MetricPoint(name="error_rate", value=9.4, unit="percent", status="critical", detail="Errors began after feature rollout."),
        MetricPoint(name="p95_latency_ms", value=410, unit="ms", status="warning", detail="Latency rose with retries."),
        MetricPoint(name="model_timeout_rate", value=7.9, unit="percent", status="critical", detail="Timeouts concentrated on vector feature fetch."),
        MetricPoint(name="request_rate", value=880, unit="rpm", status="normal", detail="Traffic is not elevated."),
    ],
    "payments-worker": [
        MetricPoint(name="queue_depth", value=18400, unit="jobs", status="critical", detail="Normal queue depth is below 3000."),
        MetricPoint(name="worker_cpu", value=91, unit="percent", status="critical", detail="Workers are CPU saturated."),
        MetricPoint(name="job_error_rate", value=0.4, unit="percent", status="normal", detail="Jobs are slow, not failing."),
        MetricPoint(name="drain_rate", value=420, unit="jobs/min", status="warning", detail="Drain rate is below ingest rate."),
    ],
}


LOGS = [
    LogEvent(timestamp=datetime(2026, 8, 8, 8, 16, tzinfo=timezone.utc), service="checkout-api", level="ERROR", message="database timeout while reserving inventory", trace_id="trc_chk_001"),
    LogEvent(timestamp=datetime(2026, 8, 8, 8, 17, tzinfo=timezone.utc), service="checkout-api", level="WARN", message="retrying inventory reservation after 800ms", trace_id="trc_chk_002"),
    LogEvent(timestamp=datetime(2026, 8, 8, 8, 20, tzinfo=timezone.utc), service="checkout-api", level="ERROR", message="connection pool wait exceeded 500ms", trace_id="trc_chk_003"),
    LogEvent(timestamp=datetime(2026, 8, 8, 9, 6, tzinfo=timezone.utc), service="recommendation-api", level="ERROR", message="vector feature lookup timed out", trace_id="trc_rec_001"),
    LogEvent(timestamp=datetime(2026, 8, 8, 9, 7, tzinfo=timezone.utc), service="recommendation-api", level="ERROR", message="fallback ranker failed after feature timeout", trace_id="trc_rec_002"),
    LogEvent(timestamp=datetime(2026, 8, 8, 10, 31, tzinfo=timezone.utc), service="payments-worker", level="WARN", message="worker batch processing exceeded target duration", trace_id="trc_pay_001"),
    LogEvent(timestamp=datetime(2026, 8, 8, 10, 34, tzinfo=timezone.utc), service="payments-worker", level="WARN", message="queue backlog above autoscale threshold", trace_id="trc_pay_002"),
]


DEPLOYS = [
    DeployEvent(timestamp=datetime(2026, 8, 8, 7, 58, tzinfo=timezone.utc), service="checkout-api", version="v1.14.2", author="inventory-platform", summary="Changed inventory reservation query path.", risk="high"),
    DeployEvent(timestamp=datetime(2026, 8, 8, 9, 0, tzinfo=timezone.utc), service="recommendation-api", version="v2.8.0", author="ml-platform", summary="Enabled vector feature fetch for 25 percent of traffic.", risk="high"),
    DeployEvent(timestamp=datetime(2026, 8, 8, 8, 50, tzinfo=timezone.utc), service="payments-worker", version="v1.7.4", author="payments", summary="Adjusted batch size from 100 to 500.", risk="medium"),
]


KNOWN_INCIDENTS = [
    KnownIncident(
        id="inc_1042",
        service="checkout-api",
        title="Inventory database pool exhaustion",
        root_cause="inventory query regression exhausted database connections",
        signature=["database timeout", "connection pool", "db_query_p95_ms"],
        resolution="rollback query path and reduce pool wait timeout",
    ),
    KnownIncident(
        id="inc_1188",
        service="recommendation-api",
        title="Vector feature store timeout",
        root_cause="feature store timeout caused recommendation fallback failures",
        signature=["vector feature", "model_timeout_rate", "fallback ranker"],
        resolution="disable vector feature flag and replay failed requests",
    ),
    KnownIncident(
        id="inc_1215",
        service="payments-worker",
        title="Batch size CPU saturation",
        root_cause="large worker batch size saturated CPU and slowed queue drain",
        signature=["queue backlog", "worker_cpu", "batch processing"],
        resolution="revert batch size and scale workers temporarily",
    ),
]
