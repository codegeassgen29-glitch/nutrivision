# NutriVision AI

An AI-powered food recognition and nutrition analysis platform.

> 🚧 Under active development — this is Milestone 1 (project scaffolding). The full README (architecture, screenshots, deployment) gets built out in the final milestone.

## Tech Stack
- **Backend:** FastAPI, PostgreSQL, SQLAlchemy, Alembic
- **Frontend:** React, TypeScript, Tailwind CSS, Vite
- **AI/CV:** YOLOv8, OpenCV, PyTorch (added starting Milestone 5)
- **Infra:** Docker, Docker Compose

## Running Locally

1. Copy the environment template and fill in real values:
   ```bash
   cp .env.example .env
   ```
2. Start everything with Docker Compose:
   ```bash
   docker compose up --build
   ```
3. Visit:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs

## Project Structure

See `backend/app/` for the FastAPI application and `frontend/src/` for the React app. Full structure notes live in `docs/` (added later).
