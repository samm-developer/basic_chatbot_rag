from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    history: list[ChatMessage] = Field(default_factory=list)


class Source(BaseModel):
    filename: str
    snippet: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


class DocumentOut(BaseModel):
    id: int
    filename: str
    source_path: str
    chunk_count: int
