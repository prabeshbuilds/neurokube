import json
from dataclasses import dataclass

from kubernetes.kubectl_executor import KubectlExecutor


@dataclass
class ClusterContext:
    name: str
    cluster: str
    server: str
    namespace: str
    is_current: bool


def list_clusters(
    kubeconfig_path: str = "",
) -> tuple[list[ClusterContext], str | None]:
    executor = KubectlExecutor(kubeconfig_path=kubeconfig_path)

    if not _kubectl_available(executor):
        return [], "kubectl is not installed or not available in PATH."

    current_result = executor.run("config", "current-context")
    current_context = current_result.stdout.strip() if current_result.success else ""

    view_result = executor.run("config", "view", "-o", "json")
    if not view_result.success:
        return [], _friendly_config_error(view_result.stderr)

    try:
        config = json.loads(view_result.stdout)
    except json.JSONDecodeError:
        return [], "Failed to parse kubeconfig file."

    cluster_servers = {
        item.get("name", ""): item.get("cluster", {}).get("server", "unknown")
        for item in config.get("clusters", [])
    }

    contexts: list[ClusterContext] = []
    for item in config.get("contexts", []):
        name = item.get("name", "")
        ctx = item.get("context", {})
        cluster_name = ctx.get("cluster", name)
        contexts.append(
            ClusterContext(
                name=name,
                cluster=cluster_name,
                server=cluster_servers.get(cluster_name, "unknown"),
                namespace=ctx.get("namespace", "default"),
                is_current=name == current_context,
            )
        )

    if not contexts:
        return [], "No Kubernetes contexts found in kubeconfig."

    return contexts, None


def verify_cluster_access(
    kubeconfig_path: str = "",
    context: str = "",
) -> str | None:
    executor = KubectlExecutor(kubeconfig_path=kubeconfig_path, context=context)
    result = executor.run("get", "nodes", "--request-timeout=10s")
    if result.success:
        return None
    return _friendly_kubectl_error(result.stderr or result.stdout)


def _kubectl_available(executor: KubectlExecutor) -> bool:
    result = executor.run("version", "--client=true")
    return result.success or "not found" not in result.stderr.lower()


def _friendly_config_error(stderr: str) -> str:
    text = stderr.lower()
    if "no such file" in text or "cannot find" in text:
        return (
            "Kubeconfig file not found.\n"
            "Please verify:\n"
            "- KUBECONFIG_PATH is set correctly\n"
            "- ~/.kube/config exists on the backend host"
        )
    return _friendly_kubectl_error(stderr)


def _friendly_kubectl_error(stderr: str) -> str:
    text = stderr.lower()
    if "unable to connect" in text or "connection refused" in text or "dial tcp" in text:
        return (
            "Unable to connect to Kubernetes cluster.\n"
            "Please verify:\n"
            "- kubeconfig path\n"
            "- cluster is running\n"
            "- cluster access and kubectl permissions"
        )
    if "context" in text and "does not exist" in text:
        return (
            "The selected cluster context was not found in kubeconfig.\n"
            "Please choose a different cluster or refresh the cluster list."
        )
    if "the connection to the server" in text and "was refused" in text:
        return (
            "Unable to connect to Kubernetes cluster.\n"
            "Please verify:\n"
            "- kubeconfig path\n"
            "- cluster access\n"
            "- kubectl permissions"
        )
    if "forbidden" in text or "unauthorized" in text:
        return (
            "kubectl permission denied for this cluster.\n"
            "Please verify your RBAC permissions and kubeconfig credentials."
        )
    if "not found" in text and "kubectl" in text:
        return "kubectl is not installed or not available in PATH."
    if "timed out" in text or "timeout" in text:
        return (
            "Kubernetes cluster request timed out.\n"
            "Please verify the cluster is reachable and try again."
        )
    return stderr.strip() or "Kubernetes command failed."


def cluster_contexts_to_dict(contexts: list[ClusterContext]) -> list[dict]:
    return [
        {
            "name": ctx.name,
            "cluster": ctx.cluster,
            "server": ctx.server,
            "namespace": ctx.namespace,
            "is_current": ctx.is_current,
        }
        for ctx in contexts
    ]
