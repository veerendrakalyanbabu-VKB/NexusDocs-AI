"""Futuristic Streamlit interface for the AI Document Q&A Assistant."""

from __future__ import annotations

from pathlib import Path
import shutil

import streamlit as st

from src.config import SUPPORTED_EXTENSIONS, get_settings
from src.ingestion import (
    clear_knowledge_base,
    delete_uploaded_file,
    index_matches_library,
    ingest_documents,
    list_uploaded_files,
    read_index_manifest,
    save_uploaded_file,
)
from src.rag_pipeline import format_sources, retrieve_documents, stream_answer
from src.ui.components import (
    render_chat_header,
    render_file_library,
    render_footer,
    render_hero,
    render_metrics,
    render_pipeline,
    render_quick_actions,
    render_sidebar_progress,
    render_system_insights,
    render_welcome,
)
from src.ui.styles import inject_global_styles


st.set_page_config(
    page_title="NexusDocs AI | Document Q&A",
    page_icon=":material/auto_awesome:",
    layout="wide",
    initial_sidebar_state="expanded",
)

QUICK_ACTIONS = {
    "Summarize": "Provide a concise executive summary of the uploaded document.",
    "Key takeaways": "What are the most important insights and action items in these documents?",
    "Find definitions": "List the key terms, acronyms, and definitions mentioned in the documents.",
    "Compare sections": "Compare the main topics and themes covered across the uploaded documents.",
}


def init_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chunk_size" not in st.session_state:
        st.session_state.chunk_size = get_settings().chunk_size
    if "chunk_overlap" not in st.session_state:
        st.session_state.chunk_overlap = get_settings().chunk_overlap
    if "top_k" not in st.session_state:
        st.session_state.top_k = get_settings().top_k

    sync_index_state()


def sync_index_state() -> None:
    settings = get_settings()
    disk_ready = settings.index_ready and index_matches_library()
    st.session_state.index_ready = disk_ready


def load_demo_document() -> None:
    sample_path = Path("data/sample/portfolio-overview.txt")
    if not sample_path.exists():
        st.error("Demo document not found.")
        return

    uploads = get_settings().upload_dir
    uploads.mkdir(parents=True, exist_ok=True)
    shutil.copy(sample_path, uploads / sample_path.name)
    st.session_state.index_ready = False
    st.toast("Demo document loaded — build the knowledge base next.", icon=":material/auto_awesome:")


def handle_file_deletion() -> None:
    file_name = st.session_state.pop("file_to_delete", None)
    if not file_name:
        return

    delete_uploaded_file(Path(file_name))
    st.session_state.index_ready = False
    st.toast(f"Removed {file_name}. Rebuild the knowledge base.", icon=":material/delete:")
    st.rerun()


def render_sidebar() -> None:
    settings = get_settings()
    files = list_uploaded_files()

    with st.sidebar:
        st.markdown("### :material/hub: Command center")
        st.caption("Configure ingestion, retrieval, and session controls.")

        render_sidebar_progress(st.session_state.index_ready, len(files))

        with st.container(border=True):
            st.markdown("#### :material/upload_file: Document intake")

            uploaded_files = st.file_uploader(
                "Upload documents",
                type=[ext.lstrip(".") for ext in sorted(SUPPORTED_EXTENSIONS)],
                accept_multiple_files=True,
                label_visibility="collapsed",
                help="Supported formats: PDF, DOCX, and TXT.",
            )

            col_a, col_b = st.columns(2)
            with col_a:
                if uploaded_files and st.button(
                    "Save",
                    type="primary",
                    icon=":material/save:",
                    width="stretch",
                ):
                    for uploaded_file in uploaded_files:
                        save_uploaded_file(uploaded_file)
                    st.session_state.index_ready = False
                    st.toast(f"Saved {len(uploaded_files)} file(s).", icon=":material/check:")
                    st.rerun()

            with col_b:
                if st.button("Demo", icon=":material/science:", width="stretch"):
                    load_demo_document()
                    st.rerun()

        with st.container(border=True):
            st.markdown("#### :material/tune: Retrieval tuning")
            st.session_state.chunk_size = st.slider(
                "Chunk size",
                min_value=400,
                max_value=2000,
                value=st.session_state.chunk_size,
                step=100,
            )
            st.session_state.chunk_overlap = st.slider(
                "Chunk overlap",
                min_value=50,
                max_value=400,
                value=st.session_state.chunk_overlap,
                step=25,
            )
            st.session_state.top_k = st.slider(
                "Top-k results",
                min_value=1,
                max_value=8,
                value=st.session_state.top_k,
            )

            if st.button(
                "Build knowledge base",
                icon=":material/database:",
                width="stretch",
                disabled=not files,
                type="primary",
            ):
                with st.status("Indexing documents...", expanded=True) as status:
                    st.write("Extracting text from documents...")
                    st.write("Splitting into semantic chunks...")
                    st.write("Generating embeddings and building FAISS index...")
                    manifest = ingest_documents(
                        chunk_size=st.session_state.chunk_size,
                        chunk_overlap=st.session_state.chunk_overlap,
                    )
                    status.update(label="Index built successfully", state="complete")

                st.session_state.index_ready = True
                st.toast(
                    f"Indexed {manifest['chunk_count']} chunks from "
                    f"{manifest['document_count']} document(s).",
                    icon=":material/rocket_launch:",
                )
                st.rerun()

        with st.container(border=True):
            st.markdown("#### :material/folder_open: Document library")
            render_file_library(files)

        with st.container(border=True):
            st.markdown("#### :material/refresh: Session controls")
            if st.button("Clear conversation", icon=":material/chat:", width="stretch"):
                st.session_state.messages = []
                st.toast("Conversation cleared.", icon=":material/chat:")
                st.rerun()

            if st.button(
                "Reset knowledge base",
                icon=":material/delete_forever:",
                width="stretch",
                type="secondary",
            ):
                clear_knowledge_base()
                st.session_state.messages = []
                st.session_state.index_ready = False
                st.toast("Knowledge base reset.", icon=":material/warning:")
                st.rerun()


def render_source_cards(sources: list[dict]) -> None:
    if not sources:
        st.caption("No supporting passages were retrieved.")
        return

    st.markdown("**:material/source: Grounded sources**")
    for index, source in enumerate(sources, start=1):
        label = source.get("source", "Unknown")
        chunk_id = source.get("chunk_id", "N/A")
        file_type = source.get("file_type", "file").upper()
        page = source.get("page")
        relevance = source.get("relevance", 0)

        meta_parts = [file_type, f"chunk {chunk_id}"]
        if page:
            meta_parts.append(f"page {page}")

        with st.expander(
            f"Source {index} · {label} · {' · '.join(meta_parts)} · {relevance}% match",
            expanded=index == 1,
        ):
            st.progress(relevance / 100)
            st.caption(source.get("preview", ""))


def render_chat_history() -> None:
    files = list_uploaded_files()

    if not st.session_state.messages:
        render_welcome(st.session_state.index_ready, len(files))
        return

    for message in st.session_state.messages:
        role = message["role"]
        avatar = ":material/person:" if role == "user" else ":material/psychology:"

        with st.chat_message(role, avatar=avatar):
            st.markdown(message["content"])

            if role == "assistant" and message.get("sources"):
                render_source_cards(message["sources"])


def queue_user_prompt(prompt: str) -> None:
    prompt = prompt.strip()
    if not prompt:
        return

    if not st.session_state.index_ready:
        st.toast(
            "Build the knowledge base before asking questions.",
            icon=":material/warning:",
        )
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.generating_for = prompt
    st.rerun()


def generate_assistant_response() -> None:
    prompt = st.session_state.pop("generating_for", None)
    if not prompt:
        return

    with st.chat_message("assistant", avatar=":material/psychology:"):
        try:
            with st.spinner("Retrieving context and synthesizing answer..."):
                top_k = st.session_state.get("top_k", get_settings().top_k)
                documents = retrieve_documents(prompt, k=top_k)
                sources = format_sources(documents)

            response = st.write_stream(stream_answer(prompt, documents))
            render_source_cards(sources)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response,
                    "sources": sources,
                }
            )
        except FileNotFoundError as error:
            st.error(str(error))
        except Exception as error:
            st.error(f"Inference failed: {error}")


def main() -> None:
    inject_global_styles()
    init_session_state()
    handle_file_deletion()

    settings = get_settings()
    if settings.llm_provider == "local":
        try:
            import torch  # noqa: F401
            import transformers  # noqa: F401
        except ImportError:
            st.warning(
                "Running in cloud-compatible mode. Add **OPENAI_API_KEY** in "
                "`.env` or Streamlit Secrets for full AI answers, or run "
                "`pip install -r requirements-local.txt` for offline FLAN-T5.",
                icon=":material/info:",
            )

    render_sidebar()

    render_hero()

    manifest = read_index_manifest()
    uploaded_files = list_uploaded_files()
    message_count = len(st.session_state.messages)

    render_metrics(
        document_count=manifest.get("document_count", len(uploaded_files)),
        chunk_count=manifest.get("chunk_count", 0),
        top_k=st.session_state.get("top_k", get_settings().top_k),
        index_ready=st.session_state.index_ready,
        message_count=message_count,
    )

    left_col, right_col = st.columns([0.36, 0.64], gap="large")

    with left_col:
        render_pipeline(st.session_state.index_ready, len(uploaded_files))
        render_system_insights(manifest)
        render_quick_actions(QUICK_ACTIONS)

    with right_col:
        with st.container(border=True):
            render_chat_header(st.session_state.index_ready)

            with st.container():
                render_chat_history()

                if st.session_state.get("generating_for"):
                    generate_assistant_response()
                    st.rerun()

            if not st.session_state.messages and st.session_state.index_ready:
                st.caption("Try: Summarize the document · List key takeaways · Find definitions")

    pending_prompt = st.session_state.pop("pending_prompt", None)
    prompt = st.chat_input(
        "Ask anything about your documents...",
        disabled=not st.session_state.index_ready,
    )

    if pending_prompt:
        queue_user_prompt(pending_prompt)
    elif prompt:
        queue_user_prompt(prompt)

    render_footer()


if __name__ == "__main__":
    main()
