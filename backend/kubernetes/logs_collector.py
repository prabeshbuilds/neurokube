import re

from kubernetes.kubectl_executor import KubectlExecutor

LOG_TAIL_LINES = 100
MAX_LINES_PER_POD = 30
MAX_PODS = 10

ERROR_PATTERNS = re.compile(
    r"(?i)(exception|error|fail|fatal|panic|connection refused|"
    r"connection reset|timeout|no such file|not found|denied|"
    r"missing env|undefined|crash|back-off|imagepull|oom|killed|"
    r"unable to|could not|cannot|startup)",
)


class LogsCollector:
    """Collects concise logs from failed or unhealthy pods."""

    def __init__(self, executor: KubectlExecutor) -> None:
        self.executor = executor

    def collect(self, problematic_pods: list[dict]) -> dict:
        if not problematic_pods:
            return {"collected": 0, "entries": []}

        entries = []
        for pod in problematic_pods[:MAX_PODS]:
            entry = self._collect_pod_logs(pod)
            if entry:
                entries.append(entry)

        return {"collected": len(entries), "entries": entries}

    def _collect_pod_logs(self, pod: dict) -> dict | None:
        name = pod.get("name")
        namespace = pod.get("namespace", "default")
        container = pod.get("container")

        if not name:
            return None

        logs = self._fetch_logs(name, namespace, container)
        if not logs and pod.get("status") in {"CrashLoopBackOff", "Error", "OOMKilled"}:
            logs = self._fetch_logs(name, namespace, container, previous=True)

        if not logs:
            return {
                "pod": name,
                "namespace": namespace,
                "container": container,
                "lines": [],
                "note": "No logs available",
            }

        relevant_lines = self._filter_relevant_lines(logs)
        return {
            "pod": name,
            "namespace": namespace,
            "container": container,
            "lines": relevant_lines,
        }

    def _fetch_logs(
        self,
        name: str,
        namespace: str,
        container: str | None,
        previous: bool = False,
    ) -> str:
        args = [
            "logs",
            name,
            "-n",
            namespace,
            f"--tail={LOG_TAIL_LINES}",
        ]
        if container:
            args.extend(["-c", container])
        if previous:
            args.append("--previous")

        result = self.executor.run(*args, timeout=30)
        if not result.success:
            return ""
        return result.stdout

    def _filter_relevant_lines(self, logs: str) -> list[str]:
        lines = [line.strip() for line in logs.splitlines() if line.strip()]
        if not lines:
            return []

        matched = [line for line in lines if ERROR_PATTERNS.search(line)]
        if matched:
            return matched[-MAX_LINES_PER_POD:]

        return lines[-MAX_LINES_PER_POD:]
