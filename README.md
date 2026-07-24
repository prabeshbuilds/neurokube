# 🚀 AI Kubernetes Agent

An AI-powered Kubernetes troubleshooting platform that automatically investigates cluster issues, analyzes Kubernetes resources, and provides intelligent root cause analysis with actionable fixes.

---

## ✨ Features

- 🔍 Automated Kubernetes cluster investigation
- 🤖 AI-powered root cause analysis using LLMs
- ⚡ Real-time investigation progress
- 📊 Modern Next.js dashboard
- ☸️ Multi-cluster support via kubeconfig contexts
- 📜 Investigation history
- 📈 Grafana & Prometheus monitoring
- 📦 Docker Compose deployment
- 🧪 Built-in Kubernetes failure scenarios for testing

---

# Architecture

```text
                 +----------------+
                 |   Next.js UI   |
                 +--------+-------+
                          |
                          |
                 REST API / Realtime
                          |
                          ▼
                +--------------------+
                |   FastAPI Backend  |
                +---------+----------+
                          |
          +---------------+----------------+
          |                                |
          ▼                                ▼
 Kubernetes Investigation          InsForge Realtime
          |                                |
          +---------------+----------------+
                          |
                          ▼
                    AI Agent Pipeline
                          |
                          ▼
                  OpenRouter / LLM
                          |
                          ▼
               Diagnosis & Suggested Fix
```

---

# Tech Stack

### Frontend

- Next.js
- React
- Tailwind CSS
- TypeScript

### Backend

- FastAPI
- Python
- Kubernetes Python Client
- Pydantic

### AI

- OpenRouter
- GPT Models
- Prompt Engineering

### Monitoring

- Prometheus
- Grafana

### Infrastructure

- Docker
- Docker Compose
- Kubernetes

---

# Project Structure

```text
ai-kubernetes-agent/
│
├── backend/                  # FastAPI backend
│   ├── ai/
│   ├── api/
│   ├── kubernetes/
│   ├── models/
│   ├── services/
│   └── main.py
│
├── frontend/                 # Next.js application
│
├── prompts/                  # LLM prompt templates
│
├── docs/                     # Documentation
│
├── scripts/                  # Testing utilities
│
├── docker-compose.yml
│
└── README.md
```

---

# Quick Start

Clone the repository

```bash
git clone <repository-url>

cd ai-kubernetes-agent
```

Start everything

```bash
docker compose up --build
```

---

## Access the application

| Service | URL |
|----------|-----|
| Frontend | http://localhost:3000 |
| Backend | http://localhost:8000 |
| Health Check | http://localhost:8000/health |

---

# Local Development

## Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

uvicorn main:app --reload --port 8000
```

---

## Frontend

```bash
cd frontend

npm install

cp .env.example .env.local

npm run dev
```



---

# Environment Variables

## Backend (`backend/.env`)

```env
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_MODEL=openai/gpt-4o-mini

INSFORGE_ANON_KEY=your-insforge-anon-key

KUBECONFIG_PATH=/path/to/kubeconfig
```

---

## Frontend (`frontend/.env.local`)

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

NEXT_PUBLIC_INSFORGE_BASE_URL=https://your-project.insforge.app

NEXT_PUBLIC_INSFORGE_ANON_KEY=your-insforge-anon-key
```

---

# Authentication

1. Register an account.
2. Login to the dashboard.
3. Select a Kubernetes cluster from your kubeconfig.
4. Start an investigation.

---

# Dashboard Workflow

```text
Login
   │
   ▼
Select Kubernetes Context
   │
   ▼
Investigate Cluster
   │
   ▼
Collect Kubernetes Evidence
   │
   ▼
AI Analysis
   │
   ▼
Diagnosis
   │
   ▼
Suggested Fixes
```

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/health` | Service health check |
| GET | `/clusters` | List available kubeconfig contexts |
| POST | `/investigate` | Investigate selected Kubernetes cluster |

---

# Example Request

```bash
curl -X POST http://localhost:8000/investigate
```

Example response

```json
{
  "healthy": false,
  "diagnosis": {
    "root_cause": "ImagePullBackOff caused by an invalid image tag.",
    "severity": "High",
    "suggested_fix": [
      "Verify the image exists.",
      "Update the deployment image.",
      "Redeploy the workload."
    ]
  }
}
```

---

# AI Investigation Pipeline

The investigation pipeline follows these steps:

1. Connect to the selected Kubernetes cluster.
2. Collect cluster evidence.
3. Inspect pods, deployments, services, events, and namespaces.
4. Identify unhealthy resources.
5. Generate an AI prompt with collected evidence.
6. Send the prompt to the configured LLM.
7. Receive diagnosis and remediation suggestions.
8. Stream progress updates to the frontend.

---

# Integration Testing

Deploy intentionally broken Kubernetes resources.

Apply failures

```bash
./scripts/test-scenarios.sh apply <context>
```

Check status

```bash
./scripts/test-scenarios.sh status <context>
```

Delete failures

```bash
./scripts/test-scenarios.sh delete <context>
```

See

```text
docs/INTEGRATION_TESTING.md
```

for the complete testing guide.

---

# Monitoring

The platform supports monitoring using:

- Prometheus
- Grafana

This enables:

- Cluster metrics
- Pod resource usage
- Investigation observability
- Dashboard visualization

---




# Current Status

✅ Kubernetes Investigation

✅ AI Diagnosis

✅ Multi-cluster Support

✅ Authentication

✅ Investigation History

✅ Docker Deployment

✅ Real-time Progress Updates

✅ Prometheus Integration

✅ Grafana Dashboard

---

# Future Roadmap

- AI remediation execution
- Auto-healing workflows
- Slack notifications
- Microsoft Teams integration
- Kubernetes event correlation
- Cost optimization recommendations
- Helm release investigation
- GitOps integration
- RBAC auditing
- Multi-cloud cluster support

---

# Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/my-feature
```

3. Commit your changes

```bash
git commit -m "Add my feature"
```

4. Push to your branch

```bash
git push origin feature/my-feature
```

5. Open a Pull Request.

---

# License

MIT License

---

## Author

Built with ❤️ for simplifying Kubernetes troubleshooting through AI.