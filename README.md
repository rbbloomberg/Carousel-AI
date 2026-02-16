# AdForge AI (Carousel-AI)

A fully agentic advertising agency platform. AI agent teams collaborate to deliver end-to-end advertising campaigns — from strategy through live execution.

## Architecture

```
Client Dashboard (Next.js 14)
        │
   API Gateway (FastAPI + Redis)
        │
   Agent Orchestration (LangGraph + Claude)
        │
  ┌─────┼─────┐
  │     │     │
Strategy  Creative  Media
  Pod     Pod      Pod
        │
   Data Layer (PostgreSQL + Redis)
        │
   Integrations (Meta Ads, Google Ads, ...)
```

## MVP Scope

- **Brief submission** — guided form to define campaign objectives
- **Strategy & Insights pod** — market research + brand strategy agents
- **CX & Creative pod** — copywriting + visual creative agents
- **LangGraph orchestration** — coordinates agents in a DAG pipeline
- **Meta Ads integration** — campaign creation (mock available)
- **Dashboard** — campaign status, metrics, approval flow
- **SSE streaming** — real-time agent progress updates

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, React 18, Tailwind CSS, React Query |
| Backend | FastAPI, Python 3.11, Pydantic v2 |
| Orchestration | LangGraph, Celery |
| LLM | Claude Sonnet 4.5 (Anthropic) |
| Database | PostgreSQL 15, SQLAlchemy 2, Alembic |
| Cache/Broker | Redis 7 |
| Real-time | SSE (Server-Sent Events) |
| Infra | Docker Compose |

## Quick Start

```bash
# 1. Clone and configure
cp .env.example .env
# Edit .env with your API keys (optional — mock mode works without keys)

# 2. Start all services
make up-build

# 3. Run database migrations
make db-upgrade

# 4. Open the dashboard
open http://localhost:3000
```

## Development

```bash
make help          # Show all available commands
make up            # Start services
make logs-api      # Tail API logs
make shell-api     # Shell into API container
make shell-db      # Open psql
make db-migrate msg="description"  # Create new migration
make test          # Run backend tests
make lint          # Lint backend code
```

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Settings (env-based)
│   │   ├── database.py          # SQLAlchemy async setup
│   │   ├── worker.py            # Celery worker config
│   │   ├── api/v1/              # API routes (auth, briefs, campaigns, agents)
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── agents/              # Agent implementations
│   │   │   ├── base.py          # BaseAgent class
│   │   │   ├── tasks.py         # Celery tasks
│   │   │   ├── strategy/        # Market research + brand strategy agents
│   │   │   ├── creative/        # Copywriting + visual creative agents
│   │   │   └── workflows/       # LangGraph DAG definitions
│   │   ├── integrations/        # External APIs (LLM, Meta Ads)
│   │   └── services/            # Business logic
│   ├── alembic/                 # Database migrations
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── app/                     # Next.js 14 pages (App Router)
│   │   ├── dashboard/           # Overview dashboard
│   │   ├── briefs/new/          # Brief submission form
│   │   └── campaigns/[id]/      # Campaign detail + approval
│   ├── components/              # React components
│   ├── lib/                     # API client, utilities
│   └── package.json
├── docker-compose.yml           # Full stack (Postgres, Redis, API, Celery, Web)
├── Makefile                     # Dev shortcuts
└── .env.example                 # Environment template
```

## Pipeline Flow

```
Brief Submitted → Market Research Agent → Brand Strategy Agent
    → Copywriting Agent → Visual Creative Agent
    → Client Approval → Meta Ads Campaign Launch
```

All agents emit real-time SSE events so the dashboard shows live progress.
