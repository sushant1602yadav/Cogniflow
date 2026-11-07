# Cogniflow

### Intelligence That Drives Action.

**Cogniflow — Intelligent Business Workflows & Autonomous AI Platform**

Cogniflow is an AI-powered business operations platform designed to improve customer support, retrieve business knowledge, and assist with repetitive business workflows using Generative AI, Retrieval-Augmented Generation (RAG), and Agentic AI.

The platform combines an AI assistant, business data access, and human approval workflows to support safer and more informed business operations.

## Project Vision

Cogniflow aims to build an intelligent business platform that can:

- Understand and classify customer requests.
- Retrieve relevant information from company policies and documents.
- Access business data through backend services.
- Assist with customer support decisions.
- Generate context-aware responses using Large Language Models.
- Recommend appropriate business actions.
- Require human approval before sensitive business actions.

## Key Features

### 1. AI-Powered Customer Ticket Classification
- Classifies customer complaints into categories.
- Assigns priority levels.
- Recommends appropriate next actions.

### 2. Retrieval-Augmented Generation (RAG)
- Retrieves relevant information from company policy documents.
- Uses ChromaDB for vector storage and similarity search.
- Generates policy-grounded responses using an LLM.
- Returns relevant document sources.

### 3. AI Support Agent
- Uses LangGraph to orchestrate support workflows.
- Combines ticket classification, policy retrieval, and customer information.
- Produces structured recommendations.

### 4. Human Approval Workflow
- Creates approval requests for proposed business actions.
- Supports approval and rejection by a human reviewer.
- Records review details.

### 5. Business Action Management
- Supports approved ticket-resolution actions.
- Clearly identifies actions that require external integrations.
- Does not independently execute unsupported financial or sensitive actions.

### 6. Audit and Activity Logging
- Records approval and business workflow events.
- Provides an activity-monitoring interface.
- Supports reviewing and exporting audit records.

### 7. Interactive Dashboard
- Built using Streamlit.
- Provides customer ticket management.
- Includes AI analysis, policy assistance, agent workflows, approvals, and audit monitoring.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Backend API | FastAPI |
| Frontend | Streamlit |
| AI orchestration | LangGraph |
| LLM integration | LangChain |
| Local language model | Ollama |
| Vector database | ChromaDB |
| Relational database | SQLite |
| Embeddings | Sentence Transformers / ChromaDB embedding function |
| Document processing | PyPDF |
| Data validation | Pydantic |
| Testing framework | Pytest |
| HTTP communication | HTTPX |

## Project Architecture

```text
Cogniflow/
│
├── agents/
│   └── support_agent.py
│
├── backend/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   └── services/
│
├── data/
│
├── docs/
│
├── knowledge_base/
│   ├── refund_policy.txt
│   ├── delivery_policy.txt
│   └── return_policy.txt
│
├── tests/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

Install the following:

- Python 3.12
- Git
- Ollama
- Visual Studio Code (recommended)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Cogniflow.git
cd Cogniflow
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file by copying `.env.example`.

```powershell
Copy-Item .env.example .env
```

The default configuration uses Ollama:

```dotenv
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
DATABASE_URL=sqlite:///./cogniflow.db
CHROMA_PERSIST_DIRECTORY=./chroma_db
REQUIRE_HUMAN_APPROVAL=true
```

### 5. Install the language model

Start Ollama and download the model:

```bash
ollama pull llama3.2:3b
```

Cogniflow uses this model as its default local language model.

## Running Cogniflow

Open two terminals in the project directory.

### Terminal 1 — Start the FastAPI backend

```bash
uvicorn backend.main:app --reload --port 8000
```

Backend:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

### Terminal 2 — Start the Streamlit dashboard

```bash
streamlit run app.py
```

Dashboard:

`http://localhost:8501`

## Knowledge Base

Cogniflow includes sample business policy documents covering:

- Refund policy
- Delivery policy
- Return policy

These documents provide the knowledge source for the RAG-based policy assistant.

Additional policy documents can be added to the knowledge base as the platform evolves.

## Human-in-the-Loop AI

Cogniflow follows a human-in-the-loop approach for sensitive business operations.

The AI agent can analyze requests and recommend actions, but recommendations are not equivalent to authorization.

Sensitive actions require human review and approval. External integrations, such as payment gateways and customer messaging systems, are not included in this MVP.

## Security and MVP Limitations

This release is an educational and development-oriented MVP.

- API endpoints do not yet implement production authentication or role-based authorization.
- Reviewer identities are not independently authenticated.
- Refund processing and payment gateway integration are not implemented.
- Customer messaging and advanced support-routing integrations are not implemented.
- Audit logging is intended for demonstration and development, not as a tamper-proof compliance system.
- The application should not be exposed publicly or used with sensitive production customer data without additional security controls.

## Development Roadmap

1. Project foundation and configuration.
2. Backend API and database integration.
3. Generative AI and ticket classification.
4. Retrieval-Augmented Generation.
5. LangGraph-based AI support agent.
6. Human approval and business action workflows.
7. Audit logging and interactive dashboard.
8. Comprehensive testing and documentation.
9. GitHub publication and future improvements.

## Future