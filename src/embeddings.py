from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from src.config import get_settings


@lru_cache(maxsize=1)
def create_embeddings():
    """Create and cache the Hugging Face embedding model."""
    settings = get_settings()
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)
