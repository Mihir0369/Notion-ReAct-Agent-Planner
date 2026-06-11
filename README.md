# ReAct Agent Planner

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![LangChain](https://img.shields.io/badge/LangChain-121212)](https://www.langchain.com/)
[![Deploy to AWS EC2](https://github.com/Mihir0369/Notion-ReAct-Agent-Planner/actions/workflows/deploy.yml/badge.svg)](https://github.com/Mihir0369/Notion-ReAct-Agent-Planner/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A FastAPI-based planner assistant powered by a ReAct-style LangChain agent.  
It can answer questions and use tools for weather, Notion notes, and Notion calendar events.

## Features

- ReAct agent with tool calling
- Weather lookup via Open-Meteo
- Notion notes support (read/add)
- Notion calendar support (read/add)
- FastAPI backend with static frontend serving
- Docker support and CI/CD deployment workflow

## Tech Stack

- Python 3.12+
- FastAPI + Uvicorn
- LangChain
- Groq model integration (`langchain-groq`)
- Notion API
- Docker, Docker Compose, GitHub Actions

## Project Structure

```text
ReAct Agent Planner/
|-- agent/
|   `-- bot.py                       # LLM and ReAct agent setup
|-- api/
|   `-- server.py                    # FastAPI app and API routes
|-- scripts/
|   |-- setup_notion_databases.py    # Notion database bootstrap helper
|   `-- test_agent.py                # Local agent test script
|-- static/
|   |-- index.html                   # Frontend markup
|   |-- script.js                    # Frontend logic
|   `-- style.css                    # Frontend styles
|-- tools/
|   |-- notion_calender.py           # Notion calendar tools
|   |-- notion_notes.py              # Notion notes tools
|   `-- weather.py                   # Weather tool (Open-Meteo)
|-- utils/
|   `-- logger.py                    # Logging helper
|-- .github/
|   `-- workflows/
|       `-- deploy.yml               # CI/CD deploy workflow
|-- docker-compose.yml               # Local container orchestration
|-- Dockerfile                       # App image build
|-- main.py                          # App entrypoint (runs Uvicorn)
|-- pyproject.toml                   # Project metadata and dependencies
|-- requirements.txt                 # pip dependency list
|-- README.md                        # Project documentation
`-- LICENSE                          # MIT license
```

## Quick Start

### 1) Clone and install

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=optional_if_needed
NOTION_API_KEY=your_notion_integration_api_key
NOTION_CALENDAR_DB_ID=your_calendar_database_id
NOTION_NOTES_DB_ID=your_notes_database_id
```

Notes:
- `GROQ_API_KEY` is required for the agent to start.
- `OPENAI_API_KEY` is included in deployment variables but this project primarily uses Groq in current code.

### 3) Run locally

```bash
python main.py
```

App URL:
- `http://localhost:8000`

## API Endpoints

- `POST /chat` - sends a user message to the agent
  - Example body:
    ```json
    { "message": "What's the weather in Toronto?" }
    ```
- `GET /calendar?date=YYYY-MM-DD` - get calendar events for a date
- `GET /notes` - get pending notes
- `GET /health` - health check

## Notion Setup Helper

To create required Notion databases:

```bash
python scripts/setup_notion_databases.py
```

The script prompts for a parent page and prints database IDs to add to `.env`.

## Docker

Run with Docker Compose:

```bash
docker compose up --build
```

Exposes `8000:8000` and loads env vars from `.env`.

## Deployment

The workflow in `.github/workflows/deploy.yml`:
- builds and pushes image to GitHub Container Registry
- deploys to EC2 over SSH
- runs the container with environment variables from GitHub secrets

## Troubleshooting

- Agent fails to initialize:
  - verify `GROQ_API_KEY`
  - reinstall dependencies (`pip install -r requirements.txt`)
- Notion API errors:
  - check integration access to your page/databases
  - verify `NOTION_API_KEY`, `NOTION_CALENDAR_DB_ID`, and `NOTION_NOTES_DB_ID`
- Port conflict on `8000`:
  - stop the process using the port or change port in `main.py`

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
