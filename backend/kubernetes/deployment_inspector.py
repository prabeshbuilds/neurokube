import json

from kubernetes.kubectl_executor import KubectlExecutor


class DeploymentInspector:
    """Inspects deployments for replica and rollout issues."""

    def __init__(self, executor: KubectlExecutor) -> None:
        self.executor = executor

    def inspect(self) -> dict:
        result = self.executor.run("get", "deployments", "-A", "-o", "json")
        if not result.success:
            return {
                "healthy": False,
                "error": result.stderr.strip() or "Failed to fetch deployments",
                "problematic_deployments": [],
            }

        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            return {
                "healthy": False,
                "error": "Failed to parse deployment data",
                "problematic_deployments": [],
            }

        problematic = []
        for item in data.get("items", []):
            issue = self._inspect_deployment(item)
            if issue:
                problematic.append(issue)

        return {
            "healthy": len(problematic) == 0,
            "total_deployments": len(data.get("items", [])),
            "problematic_deployments": problematic,
        }

    def _inspect_deployment(self, deployment: dict) -> dict | None:
        metadata = deployment.get("metadata", {})
        spec = deployment.get("spec", {})
        status = deployment.get("status", {})

        name = metadata.get("name", "unknown")
        namespace = metadata.get("namespace", "default")
        desired = spec.get("replicas", 0) or 0
        available = status.get("availableReplicas", 0) or 0
        ready = status.get("readyReplicas", 0) or 0
        unavailable = status.get("unavailableReplicas", 0) or 0
        updated = status.get("updatedReplicas", 0) or 0

        issues: list[str] = []
        failed_conditions: list[dict] = []

        if desired > 0 and available < desired:
            issues.append(f"Only {available}/{desired} replicas available")
        if unavailable > 0:
            issues.append(f"{unavailable} unavailable replica(s)")
        if desired > 0 and ready < desired:
            issues.append(f"Only {ready}/{desired} replicas ready")
        if desired > 0 and updated < desired:
            issues.append(f"Rollout incomplete: {updated}/{desired} updated")

        for condition in status.get("conditions") or []:
            if condition.get("status") != "True":
                cond_type = condition.get("type", "Unknown")
                if cond_type in {"Available", "Progressing"}:
                    failed_conditions.append(
                        {
                            "type": cond_type,
                            "status": condition.get("status"),
                            "reason": condition.get("reason"),
                            "message": condition.get("message"),
                        }
                    )
                    reason = condition.get("reason") or cond_type
                    issues.append(f"Condition {cond_type} failed: {reason}")

        if not issues:
            return None

        return {
            "name": name,
            "namespace": namespace,
            "desired_replicas": desired,
            "available_replicas": available,
            "ready_replicas": ready,
            "unavailable_replicas": unavailable,
            "issues": issues,
            "conditions": failed_conditions,
        }
