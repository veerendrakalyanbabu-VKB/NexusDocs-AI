"""Reusable UI components for the Streamlit app."""

from __future__ import annotations

import html

import streamlit as st

from src.config import get_settings


PIPELINE_STEPS = [
    ("01", "Ingest", "Parse documents", "upload_file"),
    ("02", "Chunk", "Split passages", "content_cut"),
    ("03", "Embed", "Vectorize text", "hub"),
    ("04", "Index", "FAISS store", "database"),
    ("05", "Retrieve", "Semantic search", "search"),
    ("06", "Generate", "Grounded answers", "psychology"),
]

FILE_TYPE_ICONS = {
    "pdf": "picture_as_pdf",
    "docx": "description",
    "txt": "article",
}


def _html(content: str) -> None:
    st.html(content)


def render_hero() -> None:
    settings = get_settings()
    provider = "OpenAI" if settings.llm_provider == "openai" else "FLAN-T5"
    model_label = (
        settings.openai_model.split("/")[-1]
        if settings.llm_provider == "openai"
        else settings.local_llm_model.split("/")[-1]
    )

    _html(
        f"""
        <div class="hero-shell">
            <div class="hero-glow hero-glow-1"></div>
            <div class="hero-glow hero-glow-2"></div>
            <div class="hero-glow hero-glow-3"></div>
            <div class="hero-inner">
                <div class="hero-top">
                    <div class="hero-brand">
                        <span class="hero-logo">✦</span>
                        <span class="hero-eyebrow">NexusDocs AI · RAG · 2026</span>
                    </div>
                    <div class="hero-chips">
                        <span class="hero-chip chip-engine">Engine: {html.escape(provider)}</span>
                        <span class="hero-chip chip-model">{html.escape(model_label)}</span>
                    </div>
                </div>
                <h1 class="hero-title">Your documents,<br><span class="hero-accent">intelligently answered</span></h1>
                <p class="hero-subtitle">
                    Upload knowledge, index it with semantic embeddings, and converse with your
                    documents through a grounded retrieval-augmented generation pipeline.
                </p>
                <div class="hero-tags">
                    <span class="hero-tag">PDF</span>
                    <span class="hero-tag">DOCX</span>
                    <span class="hero-tag">TXT</span>
                    <span class="hero-tag">FAISS</span>
                    <span class="hero-tag">Citations</span>
                </div>
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
        ("Documents", str(document_count), "files", ""),
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


def render_pipeline(index_ready: bool, file_count: int = 0) -> None:
    steps_html = []

    for index, (number, label, description, _icon) in enumerate(PIPELINE_STEPS):
        step_index = int(number)
        if index_ready:
            state = "live" if step_index == 6 else "complete"
        elif file_count > 0 and step_index <= 2:
            state = "complete" if step_index < 2 else "live"
        elif file_count > 0:
            state = "idle"
        else:
            state = "complete" if step_index == 1 else "idle"

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

    status_text = (
        "All systems operational"
        if index_ready
        else ("Documents loaded — ready to index" if file_count else "Awaiting document upload")
    )

    _html(
        f"""
        <div class="panel-shell pipeline-panel">
            <div class="panel-header">
                <div class="panel-title">Live RAG pipeline</div>
                <span class="panel-badge">{html.escape(status_text)}</span>
            </div>
            <div class="pipeline-flow">{"".join(steps_html)}</div>
        </div>
        """
    )


def render_system_insights(manifest: dict) -> None:
    settings = get_settings()
    embedding = manifest.get("embedding_model", settings.embedding_model).split("/")[-1]
    provider_label = (
        f"{settings.llm_provider.title()} · {settings.openai_model.split('/')[-1]}"
        if settings.llm_provider == "openai"
        else f"Local · {settings.local_llm_model.split('/')[-1]}"
    )

    _html(
        f"""
        <div class="panel-shell insight-panel">
            <div class="panel-title">System insights</div>
            <div class="insight-grid">
                <div class="insight-item"><span>Embedding</span><strong>{html.escape(embedding)}</strong></div>
                <div class="insight-item"><span>Documents</span><strong>{manifest.get("document_count", 0)}</strong></div>
                <div class="insight-item"><span>Chunks</span><strong>{manifest.get("chunk_count", 0)}</strong></div>
                <div class="insight-item"><span>LLM</span><strong>{html.escape(provider_label)}</strong></div>
            </div>
        </div>
        """
    )


def render_quick_actions(actions: dict[str, str]) -> None:
    _html(
        """
        <div class="panel-shell actions-panel">
            <div class="panel-title">Quick actions</div>
            <p class="actions-hint">One-click prompts to explore your documents</p>
        </div>
        """
    )

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


def render_welcome(index_ready: bool, file_count: int = 0) -> None:
    if not index_ready and file_count == 0:
        _html(
            """
            <div class="welcome-shell">
                <div class="welcome-icon-ring"><span class="welcome-icon">◎</span></div>
                <h3>Welcome to NexusDocs AI</h3>
                <p>Upload documents in the sidebar, build your semantic index, and start asking grounded questions.</p>
                <div class="welcome-flow">
                    <span class="flow-step">1 · Upload</span>
                    <span class="flow-arrow">→</span>
                    <span class="flow-step">2 · Save</span>
                    <span class="flow-arrow">→</span>
                    <span class="flow-step">3 · Index</span>
                    <span class="flow-arrow">→</span>
                    <span class="flow-step">4 · Ask</span>
                </div>
                <p class="welcome-tip">Tip: Click <strong>Demo</strong> in the sidebar to load a sample document instantly.</p>
            </div>
            """
        )
        return

    if not index_ready and file_count > 0:
        _html(
            """
            <div class="welcome-shell partial">
                <div class="welcome-icon-ring"><span class="welcome-icon">◉</span></div>
                <h3>Documents ready for indexing</h3>
                <p>Your files are in the library. Click <strong>Build knowledge base</strong> in the sidebar to enable Q&A.</p>
            </div>
            """
        )
        return

    _html(
        """
        <div class="welcome-shell ready">
            <div class="welcome-icon-ring ready"><span class="welcome-icon">✦</span></div>
            <h3>System ready for inference</h3>
            <p>Your documents are indexed. Ask a question below or tap a quick action to begin.</p>
        </div>
        """
    )


def render_file_library(files: list) -> None:
    if not files:
        st.caption("No documents in library yet.")
        return

    for path in files:
        file_type = path.suffix.lstrip(".").lower()
        icon = FILE_TYPE_ICONS.get(file_type, "insert_drive_file")
        size_kb = max(path.stat().st_size / 1024, 0.1)

        col_info, col_action = st.columns([0.82, 0.18])
        with col_info:
            _html(
                f"""
                <div class="file-chip">
                    <span class="file-dot"></span>
                    <span class="file-name">{html.escape(path.name)}</span>
                    <span class="file-meta">{html.escape(file_type.upper())} · {size_kb:.1f} KB</span>
                </div>
                """
            )
        with col_action:
            if st.button(
                "",
                key=f"delete_{path.name}",
                icon=":material/close:",
                help=f"Remove {path.name}",
            ):
                st.session_state.file_to_delete = path.name
                st.rerun()


def render_sidebar_progress(index_ready: bool, file_count: int) -> None:
    if index_ready:
        progress, label = 100, "Ready for Q&A"
    elif file_count:
        progress, label = 55, "Files uploaded — build index next"
    else:
        progress, label = 15, "Awaiting document upload"

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


def render_footer() -> None:
    _html(
        """
        <div class="app-footer">
            <div class="footer-inner">
                <span class="footer-brand">✦ NexusDocs AI</span>
                <span class="footer-divider">·</span>
                <span class="footer-text">Built with RAG · FAISS · Streamlit</span>
                <span class="footer-divider">·</span>
                <span class="footer-text">Portfolio Project 2026</span>
            </div>
        </div>
        """
    )
