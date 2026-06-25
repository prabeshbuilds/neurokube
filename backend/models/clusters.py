from pydantic import BaseModel


class ClusterInfo(BaseModel):
    name: str
    cluster: str
    server: str
    namespace: str
    is_current: bool


class ClusterListResponse(BaseModel):
    status: str
    clusters: list[ClusterInfo]
    error: str | None = None
