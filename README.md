# devops-todo

A small to-do REST API used to practice a full DevOps workflow.

**Stack:** Python (Flask), PostgreSQL, Docker, Docker Compose, GitHub Actions

## Run locally

1. Create a `.env` file:
   ```
   POSTGRES_DB=todo
   POSTGRES_USER=todo
   POSTGRES_PASSWORD=choose_a_password
   ```
2. Start everything:
   ```
   docker compose up -d --build
   ```
3. Try it:
   - `GET  http://localhost:5000/health`
   - `GET  http://localhost:5000/tasks`
   - `POST http://localhost:5000/tasks` with `{"title": "my task"}`

## CI

Every push to `main` builds the images, starts the stack and tests the API (see `.github/workflows/ci.yml`)