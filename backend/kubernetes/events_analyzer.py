import json

from kubernetes.kubectl_executor import KubectlExecutor

WATCH_REASONS = {
    "FailedScheduling",
    "BackOff",
    "FailedMount",
    "FailedPull",
    "ErrImagePull",
    "Unhealthy",
}

MAX_EVENTS = 50


class EventsAnalyzer:
    """Reads Kubernetes events and summarizes troubleshooting signals."""

    def __init__(self, executor: KubectlExecutor) -> None:
        self.executor = executor

    def analyze(self) -> dict:
        result = self.executor.run(
            "get",
            "events",
            "-A",
            "--sort-by=.lastTimestamp",
            "-o",
            "json",
        )
        if not result.success:
            return {
                "summary": "Failed to fetch events",
                "error": result.stderr.strip() or "Unknown error",
                "findings": [],
            }

        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            return {
                "summary": "Failed to parse events",
                "error": "Invalid JSON from kubectl",
                "findings": [],
            }

        findings = []
        for item in data.get("items", []):
            finding = self._parse_event(item)
            if finding:
                findings.append(finding)

        findings = findings[-MAX_EVENTS:]
        summary = self._build_summary(findings)

        return {
            "summary": summary,
            "total_findings": len(findings),
            "findings": findings,
        }

    def _parse_event(self, event: dict) -> dict | None:
        reason = event.get("reason", "")
        if reason not in WATCH_REASONS:
            return None

        involved = event.get("involvedObject", {})
        return {
            "reason": reason,
            "type": event.get("type", "Unknown"),
            "message": event.get("message", ""),
            "namespace": involved.get("namespace", "default"),
            "resource": f"{involved.get('kind', 'Unknown')}/{involved.get('name', 'unknown')}",
            "count": event.get("count", 1),
            "last_seen": event.get("lastTimestamp") or event.get("eventTime"),
        }

    @staticmethod
    def _build_summary(findings: list[dict]) -> str:
        if not findings:
            return "No critical warning events detected"

        reason_counts: dict[str, int] = {}
        for finding in findings:
            reason = finding["reason"]
            reason_counts[reason] = reason_counts.get(reason, 0) + 1

        parts = [f"{reason}: {count}" for reason, count in sorted(reason_counts.items())]
        return f"Detected {len(findings)} relevant events ({', '.join(parts)})"
