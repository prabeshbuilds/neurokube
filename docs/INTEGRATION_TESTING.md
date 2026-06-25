# Integration Testing Guide

End-to-end validation for the AI Kubernetes Agent.

## Prerequisites

- Docker Compose running (`docker compose up --build`)
- InsForge env vars configured (auth + anon key)
- `OPENROUTER_API_KEY` set on backend
- kubectl access from backend container (`~/.kube` mounted)
- At least one cluster context in kubeconfig
- If your kubeconfig API server uses `127.0.0.1`, run the backend with host networking so the container can reach the host-local API server

## End-to-End Flow

```text
Login → Select cluster → Investigate → Progress updates → Diagnosis → History saved
```

### Manual checklist

1. Open http://localhost:3000/login and sign in
2. Confirm **Kubernetes Clusters** lists all contexts from your kubeconfig
3. Click a cluster card to select it
4. Click **Investigate Cluster**
5. Verify progress steps update (Checking Pods → AI Reasoning)
6. Verify diagnosis or healthy-cluster message appears
7. Confirm entry appears in **Recent Investigations**

## Test Failure Scenarios

Deploy intentional failures:

```bash
chmod +x scripts/test-scenarios.sh

# List your contexts
kubectl config get-contexts

# Deploy all scenarios on a specific cluster
./scripts/test-scenarios.sh apply kind-kind

# Check pod status
./scripts/test-scenarios.sh status kind-kind

# Clean up
./scripts/test-scenarios.sh delete kind-kind
```

| Scenario | Resource | Expected AI finding |
|---|---|---|
| CrashLoopBackOff | `crashloop-missing-env` | Missing `DATABASE_URL` env var |
| ImagePullBackOff | `imagepull-wrong-tag` | Invalid nginx image tag |
| OOMKilled | `oom-low-memory` | Memory limit too low |
| Selector mismatch | `selector-mismatch-svc` | Service labels don't match pods |

After deploying, select the target cluster in the dashboard and run **Investigate Cluster**.

## Error Handling Validation

| Condition | Expected UX |
|---|---|
| Cluster unreachable | Friendly kubeconfig / connectivity message |
| Missing OpenRouter key | AI configuration error (no stack trace) |
| Expired auth session | "Please sign in again" |
| Healthy cluster | Green banner: no critical issues detected |
| API timeout | Timeout message with retry guidance |

## API Smoke Tests

```bash
# Health (public)
curl http://localhost:8000/health

# Clusters (requires Bearer token)
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/clusters

# Investigate (requires token + investigation_id + cluster_context)
curl -X POST http://localhost:8000/investigate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"investigation_id":"<uuid>","cluster_context":"minikube"}'
```

## Troubleshooting

**No clusters shown**

- Verify `KUBECONFIG_PATH` / `~/.kube` mount in docker-compose
- Confirm backend container has read access to kubeconfig

**Investigation fails immediately**

- Run `kubectl --context <name> get nodes` from the host
- Ensure selected cluster API server is reachable from Docker

**AI returns 503**

- Set `OPENROUTER_API_KEY` in backend `.env` and rebuild
