from app.agent import SignalRootAgent
from app.tools import AlertRepository


def triage(alert_id: str):
    alert = AlertRepository().get_alert(alert_id)
    assert alert is not None
    return SignalRootAgent().triage(alert)


def test_checkout_alert_points_to_database_regression():
    report = triage("alert_checkout_latency")

    assert "database" in report.likely_root_cause.cause.lower()
    assert report.likely_root_cause.confidence >= 0.85
    assert "checkout flow" in report.blast_radius
    assert any(item.source == "known_incidents" for item in report.evidence)
    assert any("metrics" in step for step in report.agent_trace)


def test_recommendation_alert_points_to_feature_store_timeout():
    report = triage("alert_recommendation_errors")

    assert "feature store" in report.likely_root_cause.cause.lower()
    assert any("vector feature" in item.summary.lower() for item in report.evidence)
    assert "Disable the vector feature flag for the affected traffic slice." in report.recommended_next_steps


def test_payments_alert_points_to_worker_saturation():
    report = triage("alert_payments_saturation")

    assert "worker saturation" in report.likely_root_cause.cause.lower()
    assert any("queue" in item.summary.lower() for item in report.evidence)
    assert any("Scale workers" in step for step in report.recommended_next_steps)


def test_evidence_is_ranked_by_weight():
    report = triage("alert_checkout_latency")
    weights = [item.weight for item in report.evidence]

    assert weights == sorted(weights, reverse=True)
