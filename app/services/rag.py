from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Chunk, Document
from app.schemas import ChatMessage, Source
from app.services.embedder import embed_query, get_client

SYSTEM_PROMPT = """You are the Brightpath Solutions company assistant.
Answer the employee's question using ONLY the document excerpts provided below.
If the excerpts do not contain the answer, say you do not have that information in the company documents.
Do not invent policies, numbers, dates, or product details.
When you use a fact, mention the source filename in parentheses.
Be concise, accurate, and professional.
"""


def answer_question(
    db: Session, message: str, history: list[ChatMessage]
) -> tuple[str, list[Source]]:
    query_embedding = embed_query(message)
    hits = _retrieve(db, query_embedding, settings.retrieve_k)
    relevant = [
        hit for hit in hits if hit["distance"] <= settings.max_cosine_distance
    ]

    if not relevant:
        return (
            "I do not have that information in the company documents. "
            "Try asking about leave, IT security, the product, or engineering onboarding.",
            [],
        )

    sources = [
        Source(filename=hit["filename"], snippet=_snippet(hit["content"]))
        for hit in relevant
    ]
    context = _build_context(relevant)
    answer = _generate(message, history, context)
    return answer, _unique_sources(sources)


def _retrieve(db: Session, query_embedding: list[float], k: int) -> list[dict]:
    distance = Chunk.embedding.cosine_distance(query_embedding)
    stmt = (
        select(Chunk.content, Document.filename, distance.label("distance"))
        .join(Document, Document.id == Chunk.document_id)
        .order_by(distance)
        .limit(k)
    )
    rows = db.execute(stmt).all()
    return [
        {"content": row.content, "filename": row.filename, "distance": float(row.distance)}
        for row in rows
    ]


def _build_context(hits: list[dict]) -> str:
    blocks = []
    for i, hit in enumerate(hits, start=1):
        blocks.append(
            f"[Excerpt {i} | {hit['filename']}]\n{hit['content']}"
        )
    return "\n\n".join(blocks)


def _generate(message: str, history: list[ChatMessage], context: str) -> str:
    client = get_client()
    recent = history[-settings.max_history_turns :]
    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "system",
            "content": f"Document excerpts:\n\n{context}",
        },
    ]
    for turn in recent:
        messages.append({"role": turn.role, "content": turn.content})
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=settings.openai_chat_model,
        messages=messages,
        temperature=0.2,
    )
    return (response.choices[0].message.content or "").strip()


def _snippet(content: str, limit: int = 220) -> str:
    compact = " ".join(content.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"


def _unique_sources(sources: list[Source]) -> list[Source]:
    seen: set[str] = set()
    unique: list[Source] = []
    for source in sources:
        if source.filename in seen:
            continue
        seen.add(source.filename)
        unique.append(source)
    return unique
