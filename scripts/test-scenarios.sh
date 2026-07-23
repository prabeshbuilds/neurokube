#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="${ROOT_DIR}/k8s/test-scenarios/all-scenarios.yaml"
CONTEXT="${KUBE_CONTEXT:-}"

kubectl_args=()
if [[ -n "${CONTEXT}" ]]; then
  kubectl_args+=(--context "${CONTEXT}")
fi

usage() {
  echo "Usage: $0 apply|delete|status [context-name]"
  echo ""
  echo "Deploy or remove Kubernetes failure test scenarios in namespace ai-agent-test."
  echo ""
  echo "Scenarios:"
  echo "  1. crashloop-missing-env   — CrashLoopBackOff (missing env var)"
  echo "  2. imagepull-wrong-tag     — ImagePullBackOff (bad image tag)"
  echo "  3. oom-low-memory          — OOMKilled (low memory limit)"
  echo "  4. selector-mismatch-svc     — Service selector mismatch"
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

ACTION="$1"
if [[ $# -ge 2 ]]; then
  kubectl_args+=(--context "$2")
fi

case "${ACTION}" in
  apply)
    kubectl "${kubectl_args[@]}" apply -f "${MANIFEST}"
    echo ""
    echo "Test scenarios deployed. Wait ~30s for pods to fail, then investigate in the dashboard."
    ;;
  delete)
    kubectl "${kubectl_args[@]}" delete -f "${MANIFEST}" --ignore-not-found
    echo "Test scenarios removed."
    ;;
  status)
    kubectl "${kubectl_args[@]}" get pods,svc,deploy -n ai-agent-test
    ;;
  *)
    usage
    exit 1
    ;;
esac


