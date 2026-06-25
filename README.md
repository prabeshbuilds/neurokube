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

Foundation setup complete. Kubernetes investigation and AI diagnosis are available via `POST /investigate`.

### Investigate endpoint

```bash
curl -X POST http://localhost:8000/investigate
```

Collects Kubernetes evidence, runs LLM reasoning via OpenRouter, and returns root cause + suggested fix.

Configure AI in `backend/.env`:

```env
OPENROUTER_API_KEY=your-insforge-provisioned-key
OPENROUTER_MODEL=openai/gpt-4o-mini
INSFORGE_ANON_KEY=your-insforge-anon-key
```

Configure frontend in `frontend/.env.local`:

```env
NEXT_PUBLIC_INSFORGE_BASE_URL=https://g95zitdu.us-east.insforge.app
NEXT_PUBLIC_INSFORGE_ANON_KEY=your-insforge-anon-key
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Dashboard

1. Sign up / sign in at http://localhost:3000/login
2. **Select a cluster** from your kubeconfig (all contexts are listed)
3. Click **Investigate Cluster**
4. Watch live progress via InsForge Realtime
5. View diagnosis (or healthy-cluster message) and investigation history

### Integration testing

Deploy intentional Kubernetes failures and validate AI diagnosis:

```bash
./scripts/test-scenarios.sh apply <your-context>
./scripts/test-scenarios.sh status <your-context>
./scripts/test-scenarios.sh delete <your-context>
```

See [docs/INTEGRATION_TESTING.md](docs/INTEGRATION_TESTING.md) for the full checklist.

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Service health check |
| GET | `/clusters` | List kubeconfig contexts (auth required) |
| POST | `/investigate` | Investigate selected cluster and return AI diagnosis |
