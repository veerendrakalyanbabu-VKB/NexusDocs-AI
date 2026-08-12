from functools import lru_cache

from src.config import get_settings


@lru_cache(maxsize=1)
def create_embeddings():
    """Create and cache the embedding model (OpenAI on cloud, Hugging Face locally)."""
    settings = get_settings()

    if settings.openai_api_key:
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings(
            model=settings.embedding_model,
            api_key=settings.openai_api_key,
        )

    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError as error:
        raise ImportError(
            "Local embeddings require optional dependencies. "
            "Run: pip install -r requirements-local.txt "
            "Or set OPENAI_API_KEY for cloud-compatible embeddings."
        ) from error

    return HuggingFaceEmbeddings(model_name=settings.huggingface_embedding_model)
