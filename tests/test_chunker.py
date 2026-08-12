"""Unit tests for the document chunker."""

from langchain_core.documents import Document

from src.chunker import split_documents


def test_split_documents_returns_empty_for_empty_input():
    assert split_documents([]) == []


def test_split_documents_assigns_chunk_ids():
    documents = [
        Document(
            page_content="A" * 500 + "\n\n" + "B" * 500,
            metadata={"source": "sample.txt", "file_type": "txt"},
        )
    ]

    chunks = split_documents(documents, chunk_size=400, chunk_overlap=50)

    assert len(chunks) >= 2
    assert chunks[0].metadata["chunk_id"] == 0
    assert chunks[1].metadata["chunk_id"] == 1


def test_split_documents_rejects_invalid_overlap():
    documents = [Document(page_content="hello", metadata={})]

    try:
        split_documents(documents, chunk_size=200, chunk_overlap=200)
        assert False, "Expected ValueError"
    except ValueError as error:
        assert "chunk_overlap" in str(error)
