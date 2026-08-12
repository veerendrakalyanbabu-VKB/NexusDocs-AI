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
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_LOCAL_LLM = "google/flan-t5-small"


def _is_cloud_run() -> bool:
    return bool(os.getenv("K_SERVICE"))


@dataclass(frozen=True)
class AppSettings:
    upload_dir: Path
    index_dir: Path
    chunk_size: int
    chunk_overlap: int
    top_k: int
    embedding_model: str
    local_llm_model: str
    openai_model: str
    openai_api_key: str | None
    gcp_project: str | None
    gcs_bucket: str | None
    bq_dataset: str
    gcp_region: str
    vertex_model: str
    deployment_env: str

    @property
    def is_cloud_deployment(self) -> bool:
        return self.deployment_env == "cloud" or _is_cloud_run()

    @property
    def gcs_enabled(self) -> bool:
        return bool(self.gcs_bucket)

    @property
    def bigquery_enabled(self) -> bool:
        return bool(self.gcp_project and self.bq_dataset)

    @property
    def vertex_enabled(self) -> bool:
        return bool(self.gcp_project and self.gcp_region)

    @property
    def llm_provider(self) -> str:
        if self.is_cloud_deployment and self.vertex_enabled:
            return "vertex"
        if self.openai_api_key:
            return "openai"
        return "local"

    @property
    def index_ready(self) -> bool:
        return (self.index_dir / "index.faiss").exists()


def get_settings() -> AppSettings:
    deployment_env = os.getenv("DEPLOYMENT_ENV", "cloud" if _is_cloud_run() else "local")

    return AppSettings(
        upload_dir=UPLOAD_DIR,
        index_dir=INDEX_DIR,
        chunk_size=DEFAULT_CHUNK_SIZE,
        chunk_overlap=DEFAULT_CHUNK_OVERLAP,
        top_k=DEFAULT_TOP_K,
        embedding_model=DEFAULT_EMBEDDING_MODEL,
        local_llm_model=DEFAULT_LOCAL_LLM,
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        openai_api_key=os.getenv("OPENAI_API_KEY") or None,
        gcp_project=os.getenv("GCP_PROJECT") or os.getenv("GOOGLE_CLOUD_PROJECT") or None,
        gcs_bucket=os.getenv("GCS_BUCKET") or None,
        bq_dataset=os.getenv("BQ_DATASET", "nexusdocs_analytics"),
        gcp_region=os.getenv("GCP_REGION", "us-central1"),
        vertex_model=os.getenv("VERTEX_MODEL", "gemini-2.0-flash-001"),
        deployment_env=deployment_env,
    )
