import os
import subprocess
from dataclasses import dataclass

from loguru import logger


@dataclass
class KubectlResult:
    success: bool
    stdout: str
    stderr: str
    return_code: int
    command: list[str]


class KubectlExecutor:
    """Safely runs kubectl commands via subprocess and returns structured output."""

    def __init__(self, kubeconfig_path: str = "", context: str = "") -> None:
        self.kubeconfig_path = kubeconfig_path
        self.context = context

    def run(self, *args: str, timeout: int = 60) -> KubectlResult:
        command = self._build_command(*args)
        logger.info("Running kubectl: {}", " ".join(command))

        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=self._build_env(),
            )
        except subprocess.TimeoutExpired:
            logger.error("kubectl timed out: {}", " ".join(command))
            return KubectlResult(
                success=False,
                stdout="",
                stderr=f"Command timed out after {timeout}s",
                return_code=-1,
                command=command,
            )
        except FileNotFoundError:
            logger.error("kubectl binary not found")
            return KubectlResult(
                success=False,
                stdout="",
                stderr="kubectl not found in PATH",
                return_code=-1,
                command=command,
            )

        if completed.returncode != 0:
            logger.warning(
                "kubectl failed (code {}): {}",
                completed.returncode,
                completed.stderr.strip() or completed.stdout.strip(),
            )
        else:
            logger.debug("kubectl succeeded: {}", " ".join(command))

        return KubectlResult(
            success=completed.returncode == 0,
            stdout=completed.stdout,
            stderr=completed.stderr,
            return_code=completed.returncode,
            command=command,
        )

    def _build_command(self, *args: str) -> list[str]:
        command = ["kubectl"]
        if self.kubeconfig_path:
            command.extend(["--kubeconfig", self.kubeconfig_path])
        if self.context:
            command.extend(["--context", self.context])
        command.extend(args)
        return command

    def _build_env(self) -> dict[str, str]:
        env = os.environ.copy()
        if self.kubeconfig_path:
            env["KUBECONFIG"] = self.kubeconfig_path
        return env
