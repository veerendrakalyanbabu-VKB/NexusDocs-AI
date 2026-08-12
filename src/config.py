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


@dataclass(frozen=True)
class AppSettings:
    upload_dir: Path
    index_dir: Path
    chunk_size: int
    chunk_overlap: int
    top_k: int
    huggingface_embedding_model: str
    openai_embedding_model: str
    local_llm_model: str
    openai_model: str
    openai_api_key: str | None

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
    return AppSettings(
        upload_dir=UPLOAD_DIR,
        index_dir=INDEX_DIR,
        chunk_size=DEFAULT_CHUNK_SIZE,
        chunk_overlap=DEFAULT_CHUNK_OVERLAP,
        top_k=DEFAULT_TOP_K,
        huggingface_embedding_model=DEFAULT_HUGGINGFACE_EMBEDDING_MODEL,
        openai_embedding_model=os.getenv(
            "OPENAI_EMBEDDING_MODEL",
            DEFAULT_OPENAI_EMBEDDING_MODEL,
        ),
        local_llm_model=DEFAULT_LOCAL_LLM,
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        openai_api_key=os.getenv("OPENAI_API_KEY") or None,
    )
