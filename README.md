# Brightpath RAG Chatbot

Ask questions against sample company documents. FastAPI embeds the files with OpenAI, stores them in PostgreSQL + pgvector, and answers only from retrieved chunks.

## Prerequisites

- Python 3.9+
- Docker (for Postgres with pgvector), **or** a local PostgreSQL 16+ install that already has the `vector` extension
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Setup

```bash
cd ChatBot
cp .env.example .env
```

Edit `.env` and set `OPENAI_API_KEY`.

**Option A — Docker (matches `.env.example`):**

```bash
docker compose up -d
```

**Option B — existing Postgres with pgvector** (for example Postgres.app). Create a database and enable the extension, then point `DATABASE_URL` at it:

```bash
createdb rag
psql rag -c "CREATE EXTENSION IF NOT EXISTS vector;"
# DATABASE_URL=postgresql+psycopg://YOUR_USER@localhost:5432/rag
```

Then install and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). On first start the app ingests everything in `data/documents/` (files already in the database are skipped).

## Environment

| Variable | Default | Purpose |
| --- | --- | --- |
| `OPENAI_API_KEY` | (required) | Embeddings and chat |
| `DATABASE_URL` | `postgresql+psycopg://rag:rag@localhost:5432/rag` | Postgres connection |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | Vector embeddings (1536 dims) |
| `OPENAI_CHAT_MODEL` | `gpt-4o-mini` | Answer generation |

## Example questions

- How many casual leave days do we get?
- How many WFH days per week are allowed?
- What is the minimum password length?
- What is the Pro plan price for Pulse?
- When do engineers join the on-call rotation?
- Can Pulse send replies without an agent?

If a question is not in the documents, the assistant should say it does not know.

## Add your own documents

Drop `.md`, `.txt`, `.pdf`, or `.docx` files into `data/documents/` and restart the server. New filenames are ingested automatically.

## API

- `GET /` — chat UI
- `GET /api/documents` — ingested files
- `POST /api/chat` — `{ "message": "...", "history": [{ "role": "user", "content": "..." }] }`
# basic_chatbot_rag
