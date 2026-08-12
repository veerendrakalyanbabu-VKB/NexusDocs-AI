"""Unit tests for ingestion helpers."""

from pathlib import Path

from src.ingestion import list_uploaded_files, read_index_manifest, write_index_manifest


def test_list_uploaded_files_filters_supported_types(tmp_path: Path):
    (tmp_path / "report.txt").write_text("hello", encoding="utf-8")
    (tmp_path / "ignore.csv").write_text("a,b", encoding="utf-8")

    files = list_uploaded_files(tmp_path)

    assert len(files) == 1
    assert files[0].name == "report.txt"


def test_index_manifest_round_trip(tmp_path: Path):
    manifest = {
        "documents": ["report.txt"],
        "document_count": 1,
        "chunk_count": 3,
    }

    write_index_manifest(manifest, tmp_path)
    loaded = read_index_manifest(tmp_path)

    assert loaded == manifest
