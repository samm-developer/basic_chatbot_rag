import logging
from pathlib import Path
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Chunk, Document
from app.services.chunker import chunk_text
from app.services.embedder import embed_texts
from app.services.parsers import SUPPORTED_SUFFIXES, load_document

logger = logging.getLogger(__name__)


def ingest_documents(db: Session, documents_dir: Optional[Path] = None) -> int:
    directory = documents_dir or settings.documents_dir
    if not directory.exists():
        logger.warning("Documents directory does not exist: %s", directory)
        return 0

    files = sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )
    ingested = 0
    for path in files:
        if _already_ingested(db, path.name):
            logger.info("Skipping already ingested file: %s", path.name)
            continue
        try:
            _ingest_file(db, path)
            db.commit()
            ingested += 1
        except Exception:
            db.rollback()
            logger.exception("Failed to ingest %s", path.name)

    if ingested:
        logger.info("Ingested %s new document(s)", ingested)
    return ingested


def _already_ingested(db: Session, filename: str) -> bool:
    return db.scalar(select(Document.id).where(Document.filename == filename)) is not None


def _ingest_file(db: Session, path: Path) -> None:
    text = load_document(path)
    chunks = chunk_text(text, settings.chunk_size, settings.chunk_overlap)
    if not chunks:
        logger.warning("No text extracted from %s", path.name)
        return

    embeddings = embed_texts(chunks)
    document = Document(filename=path.name, source_path=str(path.resolve()))
    db.add(document)
    db.flush()

    if len(chunks) != len(embeddings):
        raise RuntimeError(
            f"Embedding count mismatch for {path.name}: {len(chunks)} chunks, {len(embeddings)} vectors"
        )
    for index, (content, embedding) in enumerate(zip(chunks, embeddings)):
        db.add(
            Chunk(
                document_id=document.id,
                content=content,
                chunk_index=index,
                embedding=embedding,
            )
        )
    logger.info("Ingested %s (%s chunks)", path.name, len(chunks))
