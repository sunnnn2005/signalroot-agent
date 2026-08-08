from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "signalroot-agent"}


def test_alert_catalog():
    response = client.get("/alerts")

    assert response.status_code == 200
    alerts = response.json()
    assert len(alerts) == 3
    assert {alert["id"] for alert in alerts} >= {"alert_checkout_latency", "alert_recommendation_errors"}


def test_triage_endpoint_returns_report():
    response = client.post("/alerts/alert_checkout_latency/triage")

    assert response.status_code == 200
    payload = response.json()
    assert payload["alert"]["service"] == "checkout-api"
    assert "database" in payload["likely_root_cause"]["cause"].lower()
    assert payload["evidence"]


def test_missing_alert_returns_404():
    response = client.post("/alerts/missing/triage")

    assert response.status_code == 404
    assert response.json()["detail"] == "Alert not found"


def test_dashboard_renders():
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert "SignalRoot Agent" in response.text
    assert "/alerts" in response.text
