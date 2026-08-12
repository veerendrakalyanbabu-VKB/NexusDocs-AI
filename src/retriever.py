from src.vector_store import load_vector_store


def create_retriever(index_path="data/faiss_index", k=3):
    """
    Load the FAISS vector store and create a similarity retriever.
    """
    vector_store = load_vector_store(index_path)

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )