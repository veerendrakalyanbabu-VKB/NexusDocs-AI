"""Tests for cloud configuration and optional GCP integrations."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.config import AppSettings, get_settings


def test_local_defaults_disable_cloud_features(monkeypatch):
    monkeypatch.delenv("GCS_BUCKET", raising=False)
    monkeypatch.delenv("GCP_PROJECT", raising=False)
    monkeypatch.delenv("GOOGLE_CLOUD_PROJECT", raising=False)
    monkeypatch.delenv("K_SERVICE", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("DEPLOYMENT_ENV", "local")

    settings = get_settings()

    assert settings.deployment_env == "local"
    assert settings.gcs_enabled is False
    assert settings.bigquery_enabled is False
    assert settings.llm_provider == "local"


def test_cloud_settings_enable_gcp_features(monkeypatch):
    monkeypatch.setenv("DEPLOYMENT_ENV", "cloud")
    monkeypatch.setenv("GCP_PROJECT", "demo-project")
    monkeypatch.setenv("GCS_BUCKET", "demo-bucket")
    monkeypatch.setenv("BQ_DATASET", "nexusdocs_analytics")
    monkeypatch.setenv("GCP_REGION", "us-central1")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    settings = get_settings()

    assert settings.is_cloud_deployment is True
    assert settings.gcs_enabled is True
    assert settings.bigquery_enabled is True
    assert settings.vertex_enabled is True
    assert settings.llm_provider == "vertex"


@patch("src.cloud.gcs_storage._get_bucket")
def test_sync_to_gcs_skips_without_bucket(mock_get_bucket, tmp_path, monkeypatch):
    monkeypatch.setenv("GCS_BUCKET", "")
    from src.cloud.gcs_storage import sync_to_gcs

    sync_to_gcs()
    mock_get_bucket.assert_not_called()


def test_analytics_summary_when_bigquery_disabled(monkeypatch):
    monkeypatch.delenv("GCP_PROJECT", raising=False)
    from src.cloud.bigquery_logger import get_analytics_summary

    summary = get_analytics_summary()
    assert summary["enabled"] is False
    assert summary["total_queries"] == 0


@patch("src.cloud.bigquery_logger.get_settings")
@patch("src.cloud.bigquery_logger._get_client")
def test_log_query_event_inserts_row(mock_get_client, mock_settings):
    mock_settings.return_value = AppSettings(
        upload_dir=Path("data/uploads"),
        index_dir=Path("data/faiss_index"),
        chunk_size=1000,
        chunk_overlap=200,
        top_k=4,
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        local_llm_model="google/flan-t5-small",
        openai_model="gpt-4o-mini",
        openai_api_key=None,
        gcp_project="demo-project",
        gcs_bucket="demo-bucket",
        bq_dataset="nexusdocs_analytics",
        gcp_region="us-central1",
        vertex_model="gemini-2.0-flash-001",
        deployment_env="cloud",
    )
    mock_client = MagicMock()
    mock_client.insert_rows_json.return_value = []
    mock_get_client.return_value = mock_client

    from src.cloud.bigquery_logger import log_query_event

    log_query_event(
        question="What formats are supported?",
        answer_preview="PDF, DOCX, and TXT.",
        provider="vertex",
        chunks_retrieved=3,
        top_relevance=88.0,
        response_ms=1200,
    )

    mock_client.insert_rows_json.assert_called_once()
    rows = mock_client.insert_rows_json.call_args[0][1]
    assert rows[0]["provider"] == "vertex"
    assert rows[0]["chunks_retrieved"] == 3
