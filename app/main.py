from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from app.agent import SignalRootAgent
from app.dashboard import render_dashboard
from app.models import Alert, TriageReport
from app.tools import AlertRepository

app = FastAPI(title="SignalRoot Agent", version="1.0.0")
alerts = AlertRepository()
agent = SignalRootAgent()


@app.get("/health")
def health():
    return {"status": "ok", "service": "signalroot-agent"}


@app.get("/alerts", response_model=list[Alert])
def list_alerts():
    return alerts.list_alerts()


@app.get("/alerts/{alert_id}", response_model=Alert)
def get_alert(alert_id: str):
    alert = alerts.get_alert(alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@app.post("/alerts/{alert_id}/triage", response_model=TriageReport)
def triage_alert(alert_id: str):
    alert = alerts.get_alert(alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return agent.triage(alert)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return render_dashboard()
