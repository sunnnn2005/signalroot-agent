from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class Severity(str, Enum):
    low = "LOW"
    medium = "MEDIUM"
    high = "HIGH"
    critical = "CRITICAL"


class Alert(BaseModel):
    id: str
    service: str
    title: str
    severity: Severity
    started_at: datetime
    signal: Literal["latency", "errors", "saturation", "traffic"]
    description: str


class MetricPoint(BaseModel):
    name: str
    value: float
    unit: str
    status: Literal["normal", "warning", "critical"]
    detail: str


class LogEvent(BaseModel):
    timestamp: datetime
    service: str
    level: Literal["INFO", "WARN", "ERROR"]
    message: str
    trace_id: str


class DeployEvent(BaseModel):
    timestamp: datetime
    service: str
    version: str
    author: str
    summary: str
    risk: Literal["low", "medium", "high"]


class KnownIncident(BaseModel):
    id: str
    service: str
    title: str
    root_cause: str
    signature: list[str]
    resolution: str


class EvidenceItem(BaseModel):
    source: Literal["metrics", "logs", "deploys", "known_incidents"]
    summary: str
    weight: float = Field(ge=0, le=1)


class RootCauseHypothesis(BaseModel):
    cause: str
    confidence: float = Field(ge=0, le=1)
    reasoning: str
    supporting_evidence: list[str]


class TriageReport(BaseModel):
    alert: Alert
    impact: str
    blast_radius: list[str]
    evidence: list[EvidenceItem]
    likely_root_cause: RootCauseHypothesis
    alternative_hypotheses: list[RootCauseHypothesis]
    recommended_next_steps: list[str]
    generated_at: datetime
    agent_trace: list[str]


class TriageRequest(BaseModel):
    alert_id: str
