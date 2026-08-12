"""Unit tests for the document loader."""

from pathlib import Path

import pytest

from src.document_loader import load_document


def test_load_txt_document(sample_txt_path: Path):
    documents = load_document(sample_txt_path)

    assert len(documents) == 1
    assert documents[0].metadata["file_type"] == "txt"
    assert "Retrieval-augmented generation" in documents[0].page_content


def test_load_document_missing_file(tmp_path: Path):
    missing = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        load_document(missing)


def test_load_document_unsupported_type(tmp_path: Path):
    bad_file = tmp_path / "notes.csv"
    bad_file.write_text("a,b,c", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported file type"):
        load_document(bad_file)
