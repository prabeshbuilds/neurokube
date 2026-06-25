import json

from kubernetes.kubectl_executor import KubectlExecutor


class NetworkInspector:
    """Inspects services, endpoints, and common networking issues."""

    def __init__(self, executor: KubectlExecutor) -> None:
        self.executor = executor

    def inspect(self) -> dict:
        services_result = self.executor.run("get", "svc", "-A", "-o", "json")
        endpoints_result = self.executor.run("get", "endpoints", "-A", "-o", "json")

        if not services_result.success:
            return {
                "healthy": False,
                "error": services_result.stderr.strip() or "Failed to fetch services",
                "findings": [],
            }

        try:
            services = json.loads(services_result.stdout).get("items", [])
        except json.JSONDecodeError:
            return {
                "healthy": False,
                "error": "Failed to parse service data",
                "findings": [],
            }

        endpoints_by_key = self._index_endpoints(endpoints_result)
        findings = []

        for service in services:
            service_findings = self._inspect_service(service, endpoints_by_key)
            findings.extend(service_findings)

        return {
            "healthy": len(findings) == 0,
            "total_services": len(services),
            "findings": findings,
        }

    def _index_endpoints(self, result) -> dict[str, dict]:
        if not result.success:
            return {}

        try:
            items = json.loads(result.stdout).get("items", [])
        except json.JSONDecodeError:
            return {}

        indexed: dict[str, dict] = {}
        for item in items:
            metadata = item.get("metadata", {})
            key = f"{metadata.get('namespace', 'default')}/{metadata.get('name', '')}"
            indexed[key] = item
        return indexed

    def _inspect_service(
        self, service: dict, endpoints_by_key: dict[str, dict]
    ) -> list[dict]:
        metadata = service.get("metadata", {})
        spec = service.get("spec", {})
        name = metadata.get("name", "unknown")
        namespace = metadata.get("namespace", "default")
        selector = spec.get("selector") or {}
        service_type = spec.get("type", "ClusterIP")
        findings: list[dict] = []

        if service_type == "ExternalName" or not selector:
            return findings

        key = f"{namespace}/{name}"
        endpoint = endpoints_by_key.get(key)
        has_addresses = self._endpoint_has_addresses(endpoint)

        if not has_addresses:
            selector_issue = self._check_selector_match(namespace, selector)
            findings.append(
                {
                    "service": name,
                    "namespace": namespace,
                    "type": service_type,
                    "issue": "missing_endpoints",
                    "message": "Service has no ready endpoints",
                    "selector": selector,
                    "selector_match": selector_issue,
                }
            )

        if spec.get("clusterIP") == "None" and not has_addresses:
            findings.append(
                {
                    "service": name,
                    "namespace": namespace,
                    "type": service_type,
                    "issue": "headless_no_backends",
                    "message": "Headless service has no backing pods",
                    "selector": selector,
                }
            )

        return findings

    def _check_selector_match(self, namespace: str, selector: dict) -> dict:
        if not selector:
            return {"matched_pods": 0, "note": "Service has no selector"}

        label_selector = ",".join(f"{k}={v}" for k, v in selector.items())
        result = self.executor.run(
            "get",
            "pods",
            "-n",
            namespace,
            "-l",
            label_selector,
            "-o",
            "json",
        )

        if not result.success:
            return {
                "matched_pods": 0,
                "note": result.stderr.strip() or "Failed to check selector",
            }

        try:
            count = len(json.loads(result.stdout).get("items", []))
        except json.JSONDecodeError:
            return {"matched_pods": 0, "note": "Failed to parse pod selector results"}

        if count == 0:
            return {
                "matched_pods": 0,
                "likely_selector_mismatch": True,
                "note": "No pods match service selector labels",
            }

        return {
            "matched_pods": count,
            "note": "Pods match selector but none are ready for endpoints",
        }

    @staticmethod
    def _endpoint_has_addresses(endpoint: dict | None) -> bool:
        if not endpoint:
            return False

        subsets = endpoint.get("subsets") or []
        for subset in subsets:
            if subset.get("addresses"):
                return True
        return False
