from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Chunk, Document
from app.schemas import DocumentOut

router = APIRouter(prefix="/api", tags=["documents"])


@router.get("/documents", response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db)) -> list[DocumentOut]:
    chunk_count = func.count(Chunk.id).label("chunk_count")
    stmt = (
        select(
            Document.id,
            Document.filename,
            Document.source_path,
            chunk_count,
        )
        .outerjoin(Chunk, Chunk.document_id == Document.id)
        .group_by(Document.id)
        .order_by(Document.filename)
    )
    rows = db.execute(stmt).all()
    return [
        DocumentOut(
            id=row.id,
            filename=row.filename,
            source_path=row.source_path,
            chunk_count=row.chunk_count,
        )
        for row in rows
    ]
