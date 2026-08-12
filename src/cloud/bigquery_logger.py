"""BigQuery event logging and analytics for cloud deployments."""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from src.config import get_settings

logger = logging.getLogger(__name__)

DOCUMENT_EVENTS_TABLE = "document_events"
QUERY_EVENTS_TABLE = "query_events"


def _get_client():
    settings = get_settings()
    if not settings.bigquery_enabled:
        return None

    from google.cloud import bigquery

    return bigquery.Client(project=settings.gcp_project)


def _table_id(table_name: str) -> str:
    settings = get_settings()
    return f"{settings.gcp_project}.{settings.bq_dataset}.{table_name}"


def _insert_rows(table_name: str, rows: list[dict[str, Any]]) -> None:
    client = _get_client()
    if client is None or not rows:
        return

    table_id = _table_id(table_name)
    errors = client.insert_rows_json(table_id, rows)
    if errors:
        logger.warning("BigQuery insert errors for %s: %s", table_name, errors)


def log_document_event(
    *,
    event_type: str,
    file_name: str,
    file_type: str = "",
    file_size_bytes: int = 0,
    chunk_count: int = 0,
) -> None:
    """Record upload, index, or delete events."""
    _insert_rows(
        DOCUMENT_EVENTS_TABLE,
        [
            {
                "event_id": str(uuid.uuid4()),
                "event_type": event_type,
                "file_name": file_name,
                "file_type": file_type,
                "file_size_bytes": file_size_bytes,
                "chunk_count": chunk_count,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        ],
    )


def log_query_event(
    *,
    question: str,
    answer_preview: str,
    provider: str,
    chunks_retrieved: int,
    top_relevance: float,
    response_ms: int,
) -> None:
    """Record a grounded Q&A interaction."""
    _insert_rows(
        QUERY_EVENTS_TABLE,
        [
            {
                "query_id": str(uuid.uuid4()),
                "question": question[:500],
                "answer_preview": answer_preview[:500],
                "provider": provider,
                "chunks_retrieved": chunks_retrieved,
                "top_relevance": top_relevance,
                "response_ms": response_ms,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        ],
    )


def get_analytics_summary() -> dict[str, Any]:
    """Run SQL analytics against logged events."""
    client = _get_client()
    settings = get_settings()

    if client is None:
        return {
            "enabled": False,
            "total_queries": 0,
            "total_documents": 0,
            "providers": [],
            "recent_queries": [],
        }

    dataset = f"{settings.gcp_project}.{settings.bq_dataset}"

    try:
        query_stats = list(
            client.query(
                f"""
                SELECT
                  COUNT(*) AS total_queries,
                  AVG(response_ms) AS avg_response_ms
                FROM `{dataset}.{QUERY_EVENTS_TABLE}`
                """
            ).result()
        )
        doc_stats = list(
            client.query(
                f"""
                SELECT COUNT(*) AS total_documents
                FROM `{dataset}.{DOCUMENT_EVENTS_TABLE}`
                WHERE event_type = 'upload'
                """
            ).result()
        )
        provider_stats = list(
            client.query(
                f"""
                SELECT provider, COUNT(*) AS query_count
                FROM `{dataset}.{QUERY_EVENTS_TABLE}`
                GROUP BY provider
                ORDER BY query_count DESC
                """
            ).result()
        )
        recent = list(
            client.query(
                f"""
                SELECT question, provider, response_ms, created_at
                FROM `{dataset}.{QUERY_EVENTS_TABLE}`
                ORDER BY created_at DESC
                LIMIT 5
                """
            ).result()
        )

        query_row = query_stats[0] if query_stats else {}
        doc_row = doc_stats[0] if doc_stats else {}

        return {
            "enabled": True,
            "total_queries": int(query_row.get("total_queries", 0) or 0),
            "avg_response_ms": int(query_row.get("avg_response_ms", 0) or 0),
            "total_documents": int(doc_row.get("total_documents", 0) or 0),
            "providers": [
                {"provider": row["provider"], "count": int(row["query_count"])}
                for row in provider_stats
            ],
            "recent_queries": [
                {
                    "question": row["question"],
                    "provider": row["provider"],
                    "response_ms": int(row["response_ms"] or 0),
                    "created_at": str(row["created_at"]),
                }
                for row in recent
            ],
        }
    except Exception as error:
        logger.warning("BigQuery analytics query failed: %s", error)
        return {
            "enabled": True,
            "total_queries": 0,
            "total_documents": 0,
            "providers": [],
            "recent_queries": [],
            "error": str(error),
        }
