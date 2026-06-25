"""Kubernetes investigation layer — delegates to specialized inspectors."""

from kubernetes.deployment_inspector import DeploymentInspector
from kubernetes.events_analyzer import EventsAnalyzer
from kubernetes.kubectl_executor import KubectlExecutor
from kubernetes.logs_collector import LogsCollector
from kubernetes.network_inspector import NetworkInspector
from kubernetes.pod_inspector import PodInspector


def inspect_pods(executor: KubectlExecutor | None = None) -> dict:
    return PodInspector(executor or KubectlExecutor()).inspect()


def inspect_events(executor: KubectlExecutor | None = None) -> dict:
    return EventsAnalyzer(executor or KubectlExecutor()).analyze()


def inspect_logs(problematic_pods: list[dict], executor: KubectlExecutor | None = None) -> dict:
    return LogsCollector(executor or KubectlExecutor()).collect(problematic_pods)
