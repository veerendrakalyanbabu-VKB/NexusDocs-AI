"""Cloud Storage sync for uploads and FAISS index artifacts."""

from __future__ import annotations

import logging
from pathlib import Path

from src.config import get_settings

logger = logging.getLogger(__name__)

UPLOAD_PREFIX = "uploads"
INDEX_PREFIX = "faiss_index"


def _get_bucket():
    settings = get_settings()
    if not settings.gcs_bucket:
        return None

    from google.cloud import storage

    client = storage.Client(project=settings.gcp_project)
    return client.bucket(settings.gcs_bucket)


def _upload_directory(local_dir: Path, prefix: str) -> None:
    bucket = _get_bucket()
    if bucket is None or not local_dir.exists():
        return

    for file_path in local_dir.rglob("*"):
        if file_path.is_file():
            blob_name = f"{prefix}/{file_path.relative_to(local_dir).as_posix()}"
            bucket.blob(blob_name).upload_from_filename(str(file_path))


def _download_directory(local_dir: Path, prefix: str) -> None:
    bucket = _get_bucket()
    if bucket is None:
        return

    local_dir.mkdir(parents=True, exist_ok=True)
    blobs = bucket.list_blobs(prefix=f"{prefix}/")

    for blob in blobs:
        if blob.name.endswith("/"):
            continue
        relative_path = blob.name.removeprefix(f"{prefix}/")
        destination = local_dir / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(str(destination))


def _delete_prefix(prefix: str) -> None:
    bucket = _get_bucket()
    if bucket is None:
        return

    blobs = list(bucket.list_blobs(prefix=f"{prefix}/"))
    if blobs:
        bucket.delete_blobs(blobs)


def sync_from_gcs() -> None:
    """Download persisted data from Cloud Storage on startup."""
    settings = get_settings()
    if not settings.gcs_enabled:
        return

    try:
        _download_directory(settings.upload_dir, UPLOAD_PREFIX)
        _download_directory(settings.index_dir, INDEX_PREFIX)
        logger.info("Synced uploads and index from gs://%s", settings.gcs_bucket)
    except Exception as error:
        logger.warning("GCS download skipped: %s", error)


def sync_to_gcs() -> None:
    """Upload local uploads and index artifacts to Cloud Storage."""
    settings = get_settings()
    if not settings.gcs_enabled:
        return

    try:
        _upload_directory(settings.upload_dir, UPLOAD_PREFIX)
        if settings.index_ready:
            _upload_directory(settings.index_dir, INDEX_PREFIX)
        logger.info("Synced uploads and index to gs://%s", settings.gcs_bucket)
    except Exception as error:
        logger.warning("GCS upload failed: %s", error)


def clear_gcs_data() -> None:
    """Remove all persisted objects for this application."""
    if not get_settings().gcs_enabled:
        return

    try:
        _delete_prefix(UPLOAD_PREFIX)
        _delete_prefix(INDEX_PREFIX)
        logger.info("Cleared Cloud Storage prefixes for uploads and index")
    except Exception as error:
        logger.warning("GCS clear failed: %s", error)
