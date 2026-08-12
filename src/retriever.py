"""Semantic retrieval with FAISS similarity scores."""

from __future__ import annotations

from langchain_core.documents import Document

from src.vector_store import load_vector_store


def _score_to_relevance(distance: float) -> int:
    """Convert FAISS L2 distance to a 0–100 relevance percentage."""
    # L2 distances for normalized embeddings typically fall in [0, 2].
    normalized = max(0.0, min(1.0, 1.0 - distance / 2.0))
    return round(normalized * 100)


def create_retriever(index_path: str = "data/faiss_index", k: int = 3):
    """Load the FAISS vector store and create a similarity retriever."""
    vector_store = load_vector_store(index_path)

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )


def retrieve_with_scores(
    question: str,
    *,
    index_path: str = "data/faiss_index",
    k: int = 3,
) -> list[Document]:
    """Retrieve documents ranked by similarity, attaching score metadata."""
    vector_store = load_vector_store(index_path)
    results = vector_store.similarity_search_with_score(question, k=k)

    documents: list[Document] = []
    for document, distance in results:
        metadata = dict(document.metadata)
        metadata["distance"] = float(distance)
        metadata["relevance"] = _score_to_relevance(float(distance))
        documents.append(
            Document(page_content=document.page_content, metadata=metadata)
        )

    return documents
