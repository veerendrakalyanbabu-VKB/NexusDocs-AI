"""Retrieval-augmented generation pipeline with local and OpenAI backends."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Generator, Iterable

import torch
from langchain_core.documents import Document
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from src.config import AppSettings, get_settings
from src.retriever import create_retriever


SYSTEM_PROMPT = """You are an expert document analyst.
Answer the question using ONLY the provided context.
Rules:
- Be clear, structured, and concise.
- Use bullet points when listing multiple items.
- Quote or reference specific details from the context when helpful.
- If the answer is not in the context, reply exactly:
"I don't know based on the provided document."
- Do not invent facts or use outside knowledge."""


def build_prompt(question: str, context: str) -> str:
    return f"""{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}

Answer:"""


@lru_cache(maxsize=1)
def create_local_llm(model_name: str):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def generate(prompt: str) -> str:
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        )

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=220,
                do_sample=False,
                repetition_penalty=1.2,
                num_beams=4,
                early_stopping=True,
            )

        return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    return generate


@lru_cache(maxsize=1)
def create_openai_llm(model_name: str, api_key: str):
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=model_name,
        temperature=0.2,
        api_key=api_key,
    )


def retrieve_documents(
    question: str,
    *,
    index_path: str | None = None,
    k: int | None = None,
) -> list[Document]:
    settings = get_settings()
    target_index = index_path or str(settings.index_dir)

    if not (Path(target_index) / "index.faiss").exists():
        raise FileNotFoundError(
            "No knowledge base found. Upload documents and build the index first."
        )

    retriever = create_retriever(index_path=target_index, k=k or settings.top_k)
    return retriever.invoke(question)


def format_sources(documents: Iterable[Document]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []

    for document in documents:
        metadata = dict(document.metadata)
        metadata["preview"] = document.page_content[:280].strip()
        if len(document.page_content) > 280:
            metadata["preview"] += "..."
        sources.append(metadata)

    return sources


def generate_answer(
    question: str,
    documents: list[Document],
    *,
    provider: str | None = None,
) -> str:
    settings = get_settings()
    provider_name = provider or settings.llm_provider
    context = "\n\n".join(document.page_content for document in documents)

    if not context.strip():
        return "I don't know based on the provided document."

    if provider_name == "openai":
        llm = create_openai_llm(
            settings.openai_model,
            settings.openai_api_key or "",
        )
        prompt = build_prompt(question, context)
        response = llm.invoke(prompt)
        return response.content.strip()

    llm = create_local_llm(settings.local_llm_model)
    return llm(build_prompt(question, context))


def stream_answer(
    question: str,
    documents: list[Document],
    *,
    provider: str | None = None,
) -> Generator[str, None, str]:
    """Yield answer text for Streamlit streaming widgets."""
    answer = generate_answer(question, documents, provider=provider)
    words = answer.split(" ")
    streamed = ""

    for index, word in enumerate(words):
        chunk = word if index == 0 else f" {word}"
        streamed += chunk
        yield chunk

    return streamed


def ask_question(
    question: str,
    *,
    index_path: str | None = None,
    k: int | None = None,
    provider: str | None = None,
) -> dict[str, Any]:
    settings = get_settings()
    target_index = index_path or str(settings.index_dir)

    if not (settings.index_dir / "index.faiss").exists():
        raise FileNotFoundError(
            "No knowledge base found. Upload documents and build the index first."
        )

    documents = retrieve_documents(
        question,
        index_path=target_index,
        k=k,
    )

    answer = generate_answer(question, documents, provider=provider)

    return {
        "answer": answer,
        "sources": format_sources(documents),
        "provider": provider or settings.llm_provider,
    }
