"""Document ingestion pipeline: load, chunk, embed, and index."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from src.chunker import split_documents
from src.config import SUPPORTED_EXTENSIONS, get_settings
from src.document_loader import load_document
from src.vector_store import build_vector_store


def save_uploaded_file(uploaded_file, upload_dir: Path | None = None) -> Path:
    """Persist an uploaded Streamlit file object to disk."""
    settings = get_settings()
    target_dir = upload_dir or settings.upload_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    destination = target_dir / uploaded_file.name
    with destination.open("wb") as handle:
        handle.write(uploaded_file.getbuffer())

    return destination


def list_uploaded_files(upload_dir: Path | None = None) -> list[Path]:
    settings = get_settings()
    directory = upload_dir or settings.upload_dir

    if not directory.exists():
        return []

    return sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def delete_uploaded_file(file_path: Path, upload_dir: Path | None = None) -> None:
    """Remove a single file from the upload directory."""
    settings = get_settings()
    directory = upload_dir or settings.upload_dir
    target = file_path if file_path.is_absolute() else directory / file_path.name

    if target.exists() and target.is_file():
        target.unlink()


def index_matches_library(index_dir: Path | None = None, upload_dir: Path | None = None) -> bool:
    """Return True when the on-disk index reflects the current upload library."""
    settings = get_settings()
    manifest = read_index_manifest(index_dir or settings.index_dir)
    if not manifest:
        return False

    current_files = {path.name for path in list_uploaded_files(upload_dir)}
    indexed_files = set(manifest.get("documents", []))
    return current_files == indexed_files and bool(current_files)


def load_all_documents(file_paths: list[Path]) -> list:
    documents = []

    for file_path in file_paths:
        documents.extend(load_document(file_path))

    return documents


def write_index_manifest(
    manifest: dict[str, Any],
    index_dir: Path | None = None,
) -> None:
    settings = get_settings()
    target_dir = index_dir or settings.index_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = target_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def read_index_manifest(index_dir: Path | None = None) -> dict[str, Any]:
    settings = get_settings()
    target_dir = index_dir or settings.index_dir
    manifest_path = target_dir / "manifest.json"

    if not manifest_path.exists():
        return {}

    return json.loads(manifest_path.read_text(encoding="utf-8"))


def ingest_documents(
    *,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
    index_path: str | Path | None = None,
    upload_dir: Path | None = None,
) -> dict[str, Any]:
    """Build a FAISS index from every supported file in the upload directory."""
    settings = get_settings()
    files = list_uploaded_files(upload_dir)

    if not files:
        raise ValueError("Upload at least one PDF, DOCX, or TXT file before indexing.")

    documents = load_all_documents(files)
    chunks = split_documents(
        documents,
        chunk_size=chunk_size or settings.chunk_size,
        chunk_overlap=chunk_overlap or settings.chunk_overlap,
    )

    if not chunks:
        raise ValueError("No text could be extracted from the uploaded documents.")

    index_target = Path(index_path) if index_path else settings.index_dir
    if index_target.exists():
        shutil.rmtree(index_target)

    build_vector_store(chunks, index_path=str(index_target))

    manifest = {
        "documents": [path.name for path in files],
        "document_count": len(files),
        "chunk_count": len(chunks),
        "chunk_size": chunk_size or settings.chunk_size,
        "chunk_overlap": chunk_overlap or settings.chunk_overlap,
        "embedding_model": settings.embedding_model,
    }
    write_index_manifest(manifest, index_target)

    return manifest


def clear_knowledge_base(
    upload_dir: Path | None = None,
    index_dir: Path | None = None,
) -> None:
    settings = get_settings()
    uploads = upload_dir or settings.upload_dir
    index = index_dir or settings.index_dir

    if uploads.exists():
        shutil.rmtree(uploads)
    if index.exists():
        shutil.rmtree(index)

    uploads.mkdir(parents=True, exist_ok=True)
