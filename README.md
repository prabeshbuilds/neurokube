# AI Kubernetes Agent

On-demand Kubernetes troubleshooting system powered by AI.

## Architecture

```text
Frontend → FastAPI Backend → Kubernetes Investigation → AI Agent → LLM → Diagnosis
```

## Quick Start

```bash
docker compose up --build
```

Access:

- Frontend: http://localhost:3000
- Backend health: http://localhost:8000/health

## Project Structure

```text
ai-kubernetes-agent/
├── backend/          # FastAPI orchestrator
├── frontend/         # Next.js UI
├── docs/             # Documentation
├── prompts/          # AI prompt templates
├── docker-compose.yml
└── README.md
```

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description |
|---|---|
| `OPENROUTER_API_KEY` | OpenRouter API key (future) |
| `OPENROUTER_MODEL` | LLM model name (future) |
| `KUBECONFIG_PATH` | Path to kubeconfig (future) |

### Frontend (`frontend/.env.local`)

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_BASE_URL` | Backend API URL (default: `http://localhost:8000`) |

## Status

Foundation setup complete. Kubernetes investigation and AI reasoning are not yet implemented.
