from collections.abc import Callable

from loguru import logger

from core.config import settings
from kubernetes.cluster_config import verify_cluster_access
from kubernetes.deployment_inspector import DeploymentInspector
from kubernetes.events_analyzer import EventsAnalyzer
from kubernetes.kubectl_executor import KubectlExecutor
from kubernetes.logs_collector import LogsCollector
from kubernetes.network_inspector import NetworkInspector
from kubernetes.pod_inspector import PodInspector
from models.investigation import (
    DeploymentsInvestigation,
    EventsInvestigation,
    InvestigationPayload,
    LogsInvestigation,
    NetworkInvestigation,
    PodsInvestigation,
)

ProgressCallback = Callable[[str, str], None]


class InvestigationError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class InvestigationService:
    """Orchestrates Kubernetes evidence collection like a junior DevOps engineer."""

    def __init__(
        self,
        kubeconfig_path: str | None = None,
        cluster_context: str | None = None,
    ) -> None:
        path = kubeconfig_path if kubeconfig_path is not None else settings.kubeconfig_path
        context = cluster_context or ""
        self.executor = KubectlExecutor(kubeconfig_path=path, context=context)
        self.pod_inspector = PodInspector(self.executor)
        self.logs_collector = LogsCollector(self.executor)
        self.events_analyzer = EventsAnalyzer(self.executor)
        self.deployment_inspector = DeploymentInspector(self.executor)
        self.network_inspector = NetworkInspector(self.executor)

    def run(self, on_progress: ProgressCallback | None = None) -> InvestigationPayload:
        logger.info("Starting Kubernetes investigation")

        cluster_error = verify_cluster_access(
            kubeconfig_path=self.executor.kubeconfig_path,
            context=self.executor.context,
        )
        if cluster_error:
            raise InvestigationError(cluster_error)

        self._emit(on_progress, "checking_pods", "Checking Pods")
        pods_data = self.pod_inspector.inspect()
        logger.info(
            "Pod inspection complete: {} problematic pod(s)",
            len(pods_data.get("problematic_pods", [])),
        )

        self._emit(on_progress, "reading_logs", "Reading Logs")
        logs_data = self.logs_collector.collect(pods_data.get("problematic_pods", []))
        logger.info("Log collection complete: {} entr(ies)", logs_data.get("collected", 0))

        self._emit(on_progress, "analyzing_events", "Analyzing Events")
        events_data = self.events_analyzer.analyze()
        logger.info("Events analysis complete: {}", events_data.get("summary"))

        self._emit(on_progress, "inspecting_deployments", "Inspecting Deployments")
        deployments_data = self.deployment_inspector.inspect()
        logger.info(
            "Deployment inspection complete: {} problematic deployment(s)",
            len(deployments_data.get("problematic_deployments", [])),
        )

        self._emit(on_progress, "checking_networking", "Checking Networking")
        network_data = self.network_inspector.inspect()
        logger.info(
            "Network inspection complete: {} finding(s)",
            len(network_data.get("findings", [])),
        )

        return InvestigationPayload(
            pods=PodsInvestigation.model_validate(pods_data),
            logs=LogsInvestigation.model_validate(logs_data),
            events=EventsInvestigation.model_validate(events_data),
            deployments=DeploymentsInvestigation.model_validate(deployments_data),
            network=NetworkInvestigation.model_validate(network_data),
        )

    @staticmethod
    def _emit(
        on_progress: ProgressCallback | None,
        step: str,
        label: str,
    ) -> None:
        if on_progress:
            on_progress(step, label)


def run_investigation(
    kubeconfig_path: str | None = None,
    cluster_context: str | None = None,
    on_progress: ProgressCallback | None = None,
) -> InvestigationPayload:
    return InvestigationService(
        kubeconfig_path=kubeconfig_path,
        cluster_context=cluster_context,
    ).run(on_progress=on_progress)


def is_cluster_healthy(investigation: InvestigationPayload) -> bool:
    return (
        investigation.pods.healthy
        and investigation.logs.collected == 0
        and investigation.events.total_findings == 0
        and investigation.deployments.healthy
        and investigation.network.healthy
        and not investigation.pods.error
        and not investigation.deployments.error
        and not investigation.network.error
    )
