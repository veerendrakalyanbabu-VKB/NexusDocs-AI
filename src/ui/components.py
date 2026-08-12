"""Reusable UI components for the Streamlit app."""

from __future__ import annotations

import html

import streamlit as st

from src.config import get_settings


PIPELINE_STEPS = [
    ("01", "Ingest", "Parse documents"),
    ("02", "Chunk", "Split passages"),
    ("03", "Embed", "Vectorize text"),
    ("04", "Index", "FAISS store"),
    ("05", "Retrieve", "Semantic search"),
    ("06", "Generate", "Grounded answers"),
]


def _html(content: str) -> None:
    st.html(content)


def render_hero() -> None:
    settings = get_settings()
    provider = "OpenAI" if settings.llm_provider == "openai" else "FLAN-T5"

    _html(
        f"""
        <div class="hero-shell">
            <div class="hero-glow hero-glow-1"></div>
            <div class="hero-glow hero-glow-2"></div>
            <div class="hero-inner">
                <div class="hero-top">
                    <span class="hero-eyebrow">RAG · Embeddings · Vector search · 2026</span>
                    <span class="hero-chip">Engine: {html.escape(provider)}</span>
                </div>
                <h1 class="hero-title">AI document intelligence</h1>
                <p class="hero-subtitle">
                    Upload knowledge, index it with semantic embeddings, and converse with your
                    documents through a grounded retrieval-augmented generation pipeline.
                </p>
            </div>
        </div>
        """
    )


def render_metrics(
    *,
    document_count: int,
    chunk_count: int,
    top_k: int,
    index_ready: bool,
    message_count: int = 0,
) -> None:
    status_label = "Online" if index_ready else "Pending"
    status_class = "ready" if index_ready else "pending"
    query_count = message_count // 2 if message_count else 0

    cards = [
        ("Files", str(document_count), "files", ""),
        ("Chunks", str(chunk_count), "chunks", ""),
        ("Top-k", str(top_k), "depth", ""),
        ("Status", status_label, "status", status_class),
        ("Queries", str(query_count), "queries", ""),
    ]

    cards_html = "".join(
        f"""
        <div class="stat-card">
            <div class="stat-icon {icon}"></div>
            <div class="stat-label">{html.escape(label)}</div>
            <div class="stat-value {extra}">{html.escape(value)}</div>
        </div>
        """
        for label, value, icon, extra in cards
    )

    _html(f'<div class="stat-grid">{cards_html}</div>')


def render_pipeline(index_ready: bool) -> None:
    steps_html = []

    for index, (number, label, description) in enumerate(PIPELINE_STEPS):
        step_index = int(number)
        if index_ready:
            state = "live" if step_index == 6 else "complete"
        elif step_index <= 2:
            state = "complete" if step_index < 2 else "live"
        else:
            state = "idle"

        connector = '<span class="pipe-line"></span>' if index < len(PIPELINE_STEPS) - 1 else ""
        steps_html.append(
            f"""
            <div class="pipe-step-wrap">
                <div class="pipe-step {state}">
                    <div class="pipe-num">{number}</div>
                    <div class="pipe-label">{html.escape(label)}</div>
                    <div class="pipe-desc">{html.escape(description)}</div>
                </div>
                {connector}
            </div>
            """
        )

    _html(
        f"""
        <div class="panel-shell pipeline-panel">
            <div class="panel-title">Live RAG pipeline</div>
            <div class="pipeline-flow">{"".join(steps_html)}</div>
        </div>
        """
    )


def render_system_insights(manifest: dict) -> None:
    settings = get_settings()
    embedding = manifest.get("embedding_model", settings.embedding_model).split("/")[-1]

    _html(
        f"""
        <div class="panel-shell insight-panel">
            <div class="panel-title">System insights</div>
            <div class="insight-grid">
                <div class="insight-item"><span>Embedding</span><strong>{html.escape(embedding)}</strong></div>
                <div class="insight-item"><span>Documents</span><strong>{manifest.get("document_count", 0)}</strong></div>
                <div class="insight-item"><span>Chunks</span><strong>{manifest.get("chunk_count", 0)}</strong></div>
                <div class="insight-item"><span>LLM</span><strong>{html.escape(settings.llm_provider.title())}</strong></div>
            </div>
        </div>
        """
    )


def render_quick_actions(actions: dict[str, str]) -> None:
    _html('<div class="panel-title" style="margin-bottom:0.6rem">Quick actions</div>')

    labels = list(actions.keys())
    icons = {
        "Summarize": ":material/summarize:",
        "Key takeaways": ":material/lightbulb:",
        "Find definitions": ":material/search:",
        "Compare sections": ":material/compare:",
    }

    for row in (labels[:2], labels[2:]):
        if not row:
            continue
        cols = st.columns(len(row))
        for col, label in zip(cols, row):
            with col:
                if st.button(
                    label,
                    key=f"action_{label}",
                    icon=icons.get(label, ":material/bolt:"),
                    width="stretch",
                    disabled=not st.session_state.get("index_ready", False),
                ):
                    st.session_state.pending_prompt = actions[label]
                    st.rerun()


def render_chat_header(index_ready: bool) -> None:
    status_class = "online" if index_ready else "offline"
    status_text = "Neural index online" if index_ready else "Awaiting index build"

    _html(
        f"""
        <div class="chat-top">
            <div>
                <div class="chat-title">Conversation</div>
                <div class="chat-sub">Ask questions grounded in your uploaded documents</div>
            </div>
            <div class="status-pill {status_class}">
                <span class="status-dot"></span>{status_text}
            </div>
        </div>
        """
    )


def render_welcome(index_ready: bool) -> None:
    if not index_ready:
        _html(
            """
            <div class="welcome-shell">
                <div class="welcome-icon">◎</div>
                <h3>Initialize your knowledge base</h3>
                <p>Upload documents in the sidebar, then build the semantic index to unlock grounded Q&A.</p>
                <div class="welcome-flow">
                    <span class="flow-step">1 · Upload</span>
                    <span class="flow-arrow">→</span>
                    <span class="flow-step">2 · Index</span>
                    <span class="flow-arrow">→</span>
                    <span class="flow-step">3 · Ask</span>
                </div>
            </div>
            """
        )
        return

    _html(
        """
        <div class="welcome-shell ready">
            <div class="welcome-icon">✦</div>
            <h3>System ready for inference</h3>
            <p>Your documents are indexed. Ask a question below or tap a quick action to begin.</p>
        </div>
        """
    )


def render_file_library(files: list) -> None:
    if not files:
        st.caption("No documents in library yet.")
        return

    chips = "".join(
        f'<div class="file-chip"><span class="file-dot"></span>{html.escape(path.name)}</div>'
        for path in files
    )
    _html(f'<div class="file-list">{chips}</div>')


def render_sidebar_progress(index_ready: bool, file_count: int) -> None:
    progress = 100 if index_ready else (45 if file_count else 10)
    label = "Ready for Q&A" if index_ready else ("Files uploaded" if file_count else "Awaiting upload")

    _html(
        f"""
        <div class="sidebar-progress">
            <div class="sidebar-progress-label">
                <span>Setup progress</span><strong>{progress}%</strong>
            </div>
            <div class="sidebar-progress-track">
                <div class="sidebar-progress-fill" style="width:{progress}%"></div>
            </div>
            <div class="sidebar-progress-caption">{html.escape(label)}</div>
        </div>
        """
    )
