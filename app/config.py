from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        extra="ignore",
    )

    openai_api_key: str = ""
    database_url: str = "postgresql+psycopg://rag:rag@localhost:5432/rag"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_chat_model: str = "gpt-4o-mini"
    embedding_dimensions: int = 1536
    chunk_size: int = 800
    chunk_overlap: int = 150
    retrieve_k: int = 5
    max_history_turns: int = 6
    max_cosine_distance: float = 0.55
    documents_dir: Path = PROJECT_ROOT / "data" / "documents"


settings = Settings()
