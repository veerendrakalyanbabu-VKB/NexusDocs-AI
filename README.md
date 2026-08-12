# AI-Powered Document Q&A Assistant

An AI-powered document question-answering application that lets users upload documents and receive **context-grounded answers** using a full **Retrieval-Augmented Generation (RAG)** pipeline.

Built with **Python**, **Streamlit**, **Hugging Face embeddings**, **FAISS vector search**, and optional **OpenAI** integration.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.61-red)
![RAG](https://img.shields.io/badge/RAG-Enabled-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## Project overview

Users upload documents, the system extracts and chunks the text, generates embeddings, stores them in a FAISS vector index, retrieves the most relevant passages for each question, and sends that context to an LLM for a grounded response.

## How it works

```text
User uploads document
        ↓
Document ingestion
        ↓
Text extraction
        ↓
Text chunking
        ↓
Embeddings generation
        ↓
Vector / semantic search
        ↓
Relevant context retrieval
        ↓
LLM
        ↓
Context-grounded answer
        ↓
Streamlit interface
```

## Features

- Document upload for **PDF**, **DOCX**, and **TXT**
- Configurable chunk size, overlap, and top-k retrieval
- Semantic embeddings with `sentence-transformers/all-MiniLM-L6-v2`
- FAISS vector search for fast similarity retrieval
- Grounded answer generation with **FLAN-T5** or **OpenAI**
- Futuristic Streamlit UI with chat, pipeline status, and source citations
- One-click demo document for quick testing

## Tech stack

| Layer | Technology |
|-------|------------|
| Language | Python |
| UI | Streamlit |
| RAG orchestration | LangChain |
| Embeddings | Hugging Face / Sentence Transformers |
| Vector search | FAISS |
| LLM | FLAN-T5 (local) or OpenAI API |
| Document parsing | PyPDF, python-docx |

## Quick start

### 1. Clone and install

```bash
git clone <your-repo-url>
cd AI-Document-QA-Assistant
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure environment (optional)

```bash
copy .env.example .env
```

Add your OpenAI key for stronger answers:

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
```

Without an API key, the app uses the local `google/flan-t5-small` model.

### 3. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501).

## Usage

1. Upload documents in the sidebar (or click **Demo**)
2. Click **Save**
3. Tune retrieval settings if needed
4. Click **Build knowledge base**
5. Ask questions in the chat panel
6. Review answers and expand source citations

## Project structure

```text
AI-Document-QA-Assistant/
├── app.py
├── src/
│   ├── config.py
│   ├── document_loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── ingestion.py
│   ├── rag_pipeline.py
│   └── ui/
├── tests/
├── docs/
│   ├── ARCHITECTURE.md
│   └── INTERVIEW_GUIDE.md
├── data/
│   ├── sample/
│   ├── uploads/
│   └── faiss_index/
├── .streamlit/config.toml
├── requirements.txt
└── README.md
```

## Testing

```bash
pytest tests/ -v
```

## What this project demonstrates

- How RAG works end to end
- Why documents are chunked before retrieval
- What embeddings and semantic search do
- Why retrieved context is passed to an LLM
- How prompt design reduces hallucination
- How Python integrates AI models and APIs
- How an AI application is exposed through a UI

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Interview guide](docs/INTERVIEW_GUIDE.md)

## Resume-ready summary

**AI-Powered Document Q&A Assistant | Python, LLM, RAG, Embeddings, Vector Search, Streamlit, APIs | 2026**

- Developed an AI-powered document question-answering application that enables users to upload documents and obtain context-grounded responses.
- Implemented a Retrieval-Augmented Generation (RAG) workflow covering document ingestion, text processing, chunking, embeddings, semantic retrieval, and LLM-based response generation.
- Designed retrieval and prompt workflows to provide relevant document context to the LLM and improve answer relevance.
- Built an interactive Streamlit interface for document upload and question-answer interaction.
- Structured the application for reproducible development, GitHub portfolio presentation, documentation, and future production enhancements.

## Roadmap

- [ ] Hybrid retrieval (semantic + keyword)
- [ ] Docker deployment
- [ ] Evaluation harness for answer quality
- [ ] GCP deployment integration (Project #3)

## License

MIT License. See [LICENSE](LICENSE).

## Author

**Veerendra Kalyan** — Portfolio project, 2026
