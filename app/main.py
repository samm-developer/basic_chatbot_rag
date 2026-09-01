import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.db import SessionLocal, init_db
from app.routers import chat, documents
from app.services.ingest import ingest_documents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    if not settings.openai_api_key:
        logger.warning("OPENAI_API_KEY is not set. Chat and ingest will fail until it is configured.")
    else:
        db = SessionLocal()
        try:
            ingested = ingest_documents(db)
            logger.info("Startup ingest complete (%s new file(s))", ingested)
        except Exception:
            logger.exception("Document ingest failed on startup")
        finally:
            db.close()
    yield


app = FastAPI(title="Brightpath RAG Chatbot", lifespan=lifespan)
app.include_router(chat.router)
app.include_router(documents.router)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
