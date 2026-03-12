# 🏥 BMHS-AI — Hospital AI Agent

> **Intelligent hospital information system** powered by [Google ADK](https://google.github.io/adk-docs/) (Agent Development Kit}, **Gemini 2.5 Flash**, and the **Agent-to-Agent (A2A)** protocol.

BMHS-AI is a multi-agent system designed to assist hospital staff and users with two core capabilities:

1. **Hospital Operations** — Search for doctors by specialization, look up patients by name, and retrieve visit history by complaint. Backed by **BigQuery** via [MCP Toolbox for Databases](https://googleapis.github.io/genai-toolbox/getting-started/introduction/).
2. **JKN Tariff Regulations** — Query national health insurance (JKN) tariff standards based on *Peraturan Menteri Kesehatan RI No. 3 Tahun 2023*, including INA-CBG rates, capitation fees, and regional pricing. Powered by **Vertex AI Search**.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 Multi-Agent Architecture | A root coordinator agent delegates to specialized sub-agents |
| 🔍 Vertex AI Search | Retrieves government health tariff regulations from a managed data store |
| 🗄️ BigQuery + MCP Toolbox | SQL-based tools for querying hospital operational data (doctors, patients, visits) |
| 🔗 A2A Protocol | Agent-to-Agent communication for inter-service interoperability |
| 🔐 OAuth 2.0 Authentication | Google OAuth2-based email allowlisting for securing the A2A endpoint |
| ☁️ Cloud Run Ready | Dockerized for deployment on Google Cloud Run |

---

## 📁 Project Structure

```
bmhs-ai/
├── bmhs_ai_agent/              # Core agent (for ADK Web UI)
│   ├── __init__.py
│   ├── agent.py                # Root agent + sub-agents definition
│   ├── toolbox.py              # Standalone MCP Toolbox client for testing
│   └── .env                    # Environment variables (local)
│
├── bmhs_ai_agent_a2a/          # A2A-enabled agent (server mode)
│   ├── __init__.py
│   ├── agent.py                # A2A server with OAuth2 middleware
│   ├── agent.json              # Agent card for production deployment
│   ├── agent_local.json        # Agent card for local development
│   └── .env                    # Environment variables (local)
│
├── bmhs_ai_agent_proxy/        # Remote A2A proxy agent
│   ├── __init__.py
│   ├── agent.py                # RemoteA2aAgent connecting to A2A server
│   └── .env                    # Environment variables (local)
│
├── tools.yaml                  # MCP Toolbox tool definitions (BigQuery SQL)
├── main.py                     # Entry point (Hello World)
├── pyproject.toml              # Project metadata & dependencies (uv)
├── uv.lock                     # Dependency lock file
├── Dockerfile                  # Container image for Cloud Run deployment
├── .gitignore                  # Git ignore rules
├── .dockerignore               # Docker ignore rules
├── .python-version             # Python version (3.13)
│
├── command.MD                  # CLI reference for gcloud, uv, MCP Toolbox, ADK & A2A
├── script.MD                   # Additional deployment scripts
├── query.md                    # BigQuery DDL & seed data for dummy hospital database
└── agent-card.MD               # Agent card examples & OAuth2 configuration reference
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Root Agent                        │
│          (Koordinator Utama / Coordinator)           │
│              Gemini 2.5 Flash                       │
└──────────────┬──────────────────┬───────────────────┘
               │                  │
       ┌───────▼───────┐  ┌──────▼────────┐
       │  Vertex AI     │  │  MCP Agent    │
       │  Search Agent  │  │  (Hospital    │
       │  (JKN Tariff)  │  │   Operations) │
       └───────┬────────┘  └──────┬────────┘
               │                  │
       ┌───────▼────────┐  ┌─────▼──────────┐
       │  Vertex AI     │  │  MCP Toolbox   │
       │  Data Store    │  │  (BigQuery)    │
       │  (PMK No.3/    │  │  ┌───────────┐ │
       │   2023)        │  │  │ dokter    │ │
       └────────────────┘  │  │ pasien    │ │
                           │  │ kunjungan │ │
                           │  └───────────┘ │
                           └────────────────┘
```

---

## 🛠️ Tech Stack

- **Python** 3.13
- **Google ADK** (`google-adk[a2a]`) — Agent Development Kit with A2A support
- **Google GenAI** (`google-genai`) — Gemini model integration
- **Toolbox Core** (`toolbox-core`) — MCP Toolbox client for database tools
- **Google Cloud BigQuery** (`google-cloud-bigquery`) — Data warehouse for hospital data
- **Vertex AI Search** — RAG-based retrieval for health regulation documents
- **FastAPI / Uvicorn** — A2A server runtime
- **uv** — Fast Python package manager
- **Docker** — Containerization for Cloud Run

---

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (`gcloud` CLI)
- A Google Cloud project with BigQuery, Vertex AI Search, and Cloud Run APIs enabled

### 1. Clone the repository

```bash
git clone https://github.com/ahmadluay9/bmhs-ai.git
cd bmhs-ai
```

### 2. Install dependencies

```bash
uv venv
uv sync
```

### 3. Set up environment variables

Create a `.env` file inside each agent directory (`bmhs_ai_agent/`, `bmhs_ai_agent_a2a/`, `bmhs_ai_agent_proxy/`) with the required variables:

```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=1
TOOLBOX_URL=http://localhost:5000
```

### 4. Set up the database

Use the queries in [`query.md`](query.md) to create the BigQuery tables and insert dummy data in the `dummy_hospital` dataset.

### 5. Start the MCP Toolbox server

```bash
./toolbox --tools-file "tools.yaml"
```

### 6. Run the agent (ADK Web UI)

```bash
adk web
```

### 7. Run the A2A server (optional)

```bash
uv run uvicorn bmhs_ai_agent_a2a.agent:a2a_app --host 127.0.0.1 --port 8001
```

Visit the agent card at: `http://127.0.0.1:8001/.well-known/agent-card.json`

---

## ☁️ Deployment

The project is containerized and ready for **Google Cloud Run** deployment. See [`command.MD`](command.MD) for detailed deployment instructions including:

- Service account creation & IAM permissions
- Storing `tools.yaml` in Secret Manager
- Deploying MCP Toolbox to Cloud Run
- Deploying the A2A agent to Cloud Run

---

## 📄 License

This project is for educational and demonstration purposes.
