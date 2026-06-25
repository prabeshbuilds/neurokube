from pydantic import BaseModel, Field

from models.diagnosis import Diagnosis


class ProblematicPod(BaseModel):
    name: str
    namespace: str
    status: str
    reason: str | None = None
    container: str | None = None


class PodsInvestigation(BaseModel):
    healthy: bool
    problematic_pods: list[ProblematicPod] = Field(default_factory=list)
    error: str | None = None


class LogEntry(BaseModel):
    pod: str
    namespace: str
    container: str | None = None
    lines: list[str] = Field(default_factory=list)
    note: str | None = None


class LogsInvestigation(BaseModel):
    collected: int = 0
    entries: list[LogEntry] = Field(default_factory=list)


class EventFinding(BaseModel):
    reason: str
    type: str
    message: str
    namespace: str
    resource: str
    count: int = 1
    last_seen: str | None = None


class EventsInvestigation(BaseModel):
    summary: str
    total_findings: int = 0
    findings: list[EventFinding] = Field(default_factory=list)
    error: str | None = None


class DeploymentCondition(BaseModel):
    type: str
    status: str | None = None
    reason: str | None = None
    message: str | None = None


class ProblematicDeployment(BaseModel):
    name: str
    namespace: str
    desired_replicas: int
    available_replicas: int
    ready_replicas: int
    unavailable_replicas: int
    issues: list[str]
    conditions: list[DeploymentCondition] = Field(default_factory=list)


class DeploymentsInvestigation(BaseModel):
    healthy: bool
    total_deployments: int = 0
    problematic_deployments: list[ProblematicDeployment] = Field(default_factory=list)
    error: str | None = None


class NetworkFinding(BaseModel):
    service: str
    namespace: str
    type: str
    issue: str
    message: str
    selector: dict[str, str] = Field(default_factory=dict)
    selector_match: dict | None = None


class NetworkInvestigation(BaseModel):
    healthy: bool
    total_services: int = 0
    findings: list[NetworkFinding] = Field(default_factory=list)
    error: str | None = None


class InvestigationPayload(BaseModel):
    pods: PodsInvestigation
    logs: LogsInvestigation
    events: EventsInvestigation
    deployments: DeploymentsInvestigation
    network: NetworkInvestigation


class InvestigateRequest(BaseModel):
    investigation_id: str
    cluster_context: str


class InvestigateResponse(BaseModel):
    status: str
    investigation: InvestigationPayload
    diagnosis: Diagnosis
    cluster_healthy: bool = False
    cluster_context: str = ""
