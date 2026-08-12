"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
INDEX_DIR = DATA_DIR / "faiss_index"

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200
DEFAULT_TOP_K = 4
DEFAULT_HUGGINGFACE_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_LOCAL_LLM = "google/flan-t5-small"
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


@dataclass(frozen=True)
class AppSettings:
    upload_dir: Path = UPLOAD_DIR
    index_dir: Path = INDEX_DIR
    chunk_size: int = DEFAULT_CHUNK_SIZE
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
    top_k: int = DEFAULT_TOP_K
    huggingface_embedding_model: str = DEFAULT_HUGGINGFACE_EMBEDDING_MODEL
    openai_embedding_model: str = os.getenv(
        "OPENAI_EMBEDDING_MODEL",
        DEFAULT_OPENAI_EMBEDDING_MODEL,
    )
    local_llm_model: str = DEFAULT_LOCAL_LLM
    openai_model: str = DEFAULT_OPENAI_MODEL
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")

    @property
    def embedding_model(self) -> str:
        if self.openai_api_key:
            return self.openai_embedding_model
        return self.huggingface_embedding_model

    @property
    def llm_provider(self) -> str:
        return "openai" if self.openai_api_key else "local"

    @property
    def index_ready(self) -> bool:
        return (self.index_dir / "index.faiss").exists()


def get_settings() -> AppSettings:
    return AppSettings()
