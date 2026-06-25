import json
from datetime import datetime, timezone

from kubernetes.kubectl_executor import KubectlExecutor, KubectlResult

UNHEALTHY_WAITING_REASONS = {
    "CrashLoopBackOff",
    "ImagePullBackOff",
    "ErrImagePull",
    "Error",
    "ContainerCreating",
}

UNHEALTHY_TERMINATED_REASONS = {"OOMKilled", "Error"}
UNHEALTHY_PHASES = {"Pending", "Failed", "Unknown"}
STUCK_CONTAINER_CREATING_SECONDS = 120


class PodInspector:
    """Inspects pod status and detects unhealthy workloads."""

    def __init__(self, executor: KubectlExecutor) -> None:
        self.executor = executor

    def inspect(self) -> dict:
        result = self.executor.run("get", "pods", "-A", "-o", "json")
        if not result.success:
            return {
                "healthy": False,
                "error": result.stderr.strip() or "Failed to fetch pods",
                "problematic_pods": [],
            }

        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            return {
                "healthy": False,
                "error": "Failed to parse pod data",
                "problematic_pods": [],
            }

        problematic_pods = []
        for item in data.get("items", []):
            issue = self._detect_pod_issue(item)
            if issue:
                problematic_pods.append(issue)

        return {
            "healthy": len(problematic_pods) == 0,
            "problematic_pods": problematic_pods,
        }

    def _detect_pod_issue(self, pod: dict) -> dict | None:
        metadata = pod.get("metadata", {})
        name = metadata.get("name", "unknown")
        namespace = metadata.get("namespace", "default")
        phase = pod.get("status", {}).get("phase", "Unknown")
        creation_ts = metadata.get("creationTimestamp")
        pod_age_seconds = self._pod_age_seconds(creation_ts)

        if phase in UNHEALTHY_PHASES:
            return {
                "name": name,
                "namespace": namespace,
                "status": phase,
                "reason": f"Pod phase is {phase}",
            }

        for container in pod.get("status", {}).get("containerStatuses") or []:
            issue = self._inspect_container_status(
                name, namespace, container, pod_age_seconds
            )
            if issue:
                return issue

        for container in pod.get("status", {}).get("initContainerStatuses") or []:
            issue = self._inspect_container_status(
                name, namespace, container, pod_age_seconds, init=True
            )
            if issue:
                return issue

        return None

    def _inspect_container_status(
        self,
        pod_name: str,
        namespace: str,
        container: dict,
        pod_age_seconds: float,
        init: bool = False,
    ) -> dict | None:
        container_name = container.get("name", "unknown")
        prefix = f"init/{container_name}" if init else container_name
        state = container.get("state", {})
        last_state = container.get("lastState", {})

        waiting = state.get("waiting")
        if waiting:
            reason = waiting.get("reason", "Waiting")
            if reason in UNHEALTHY_WAITING_REASONS:
                if reason == "ContainerCreating" and pod_age_seconds < STUCK_CONTAINER_CREATING_SECONDS:
                    return None
                return {
                    "name": pod_name,
                    "namespace": namespace,
                    "status": reason,
                    "reason": waiting.get("message") or f"{prefix} is {reason}",
                    "container": container_name,
                }

        for state_key in (state, last_state):
            terminated = state_key.get("terminated")
            if terminated:
                reason = terminated.get("reason", "")
                if reason in UNHEALTHY_TERMINATED_REASONS:
                    return {
                        "name": pod_name,
                        "namespace": namespace,
                        "status": reason,
                        "reason": terminated.get("message")
                        or f"{prefix} terminated with {reason}",
                        "container": container_name,
                    }

        return None

    @staticmethod
    def _pod_age_seconds(creation_timestamp: str | None) -> float:
        if not creation_timestamp:
            return 0.0
        created = datetime.fromisoformat(creation_timestamp.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - created).total_seconds()
