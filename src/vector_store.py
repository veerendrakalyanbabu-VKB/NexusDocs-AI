from pathlib import Path

from langchain_community.vectorstores import FAISS

from src.embeddings import create_embeddings


def build_vector_store(documents, index_path="data/faiss_index"):
    """
    Create a FAISS vector store from document chunks
    and save it locally.
    """

    embeddings = create_embeddings()

    vector_store = FAISS.from_documents(
        documents,
        embeddings
    )

    index_path = Path(index_path)
    index_path.mkdir(parents=True, exist_ok=True)

    vector_store.save_local(str(index_path))

    return vector_store


def load_vector_store(index_path="data/faiss_index"):
    """
    Load an existing FAISS vector store from disk.
    """

    embeddings = create_embeddings()

    return FAISS.load_local(
        index_path,
        embeddings,
        allow_dangerous_deserialization=True
    )