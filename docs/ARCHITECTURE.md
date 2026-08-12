# Architecture

## System overview

The AI-Powered Document Q&A Assistant is a Retrieval-Augmented Generation (RAG) application. Instead of asking an LLM to answer from memory alone, the system first retrieves relevant passages from uploaded documents and passes only that context to the model.

This reduces hallucinations and makes answers traceable through source citations.

## End-to-end flow

```text
User uploads document
        ↓
Document ingestion          (document_loader.py)
        ↓
Text extraction             (PDF / DOCX / TXT parsers)
        ↓
Text chunking               (chunker.py)
        ↓
Embeddings generation       (embeddings.py)
        ↓
Vector index build          (vector_store.py + FAISS)
        ↓
User asks question
        ↓
Semantic retrieval          (retriever.py)
        ↓
Prompt construction         (rag_pipeline.py)
        ↓
LLM response generation     (FLAN-T5 local or OpenAI API)
        ↓
Answer + source citations   (Streamlit UI)
```

## Component responsibilities

| Module | Responsibility |
|--------|----------------|
| `app.py` | Streamlit UI, session state, upload workflow, chat interface |
| `src/config.py` | Paths, defaults, environment variables |
| `src/document_loader.py` | Parse PDF, DOCX, and TXT into LangChain `Document` objects |
| `src/chunker.py` | Split long text into overlapping chunks for retrieval |
| `src/embeddings.py` | Convert text chunks into dense vectors |
| `src/vector_store.py` | Build and persist a FAISS index |
| `src/retriever.py` | Retrieve top-k similar chunks for a user question |
| `src/ingestion.py` | Orchestrate upload, indexing, and manifest tracking |
| `src/rag_pipeline.py` | Build prompts, call the LLM, format grounded answers |
| `src/ui/` | Reusable futuristic UI components and styling |

## Design decisions

### Why chunk documents?

LLMs and embedding models work best on smaller, focused passages. Chunking improves retrieval precision and keeps prompts within token limits.

### Why embeddings?

Embeddings convert text into numerical vectors so semantically similar content is close in vector space. This enables meaning-based search instead of exact keyword matching.

### Why FAISS?

FAISS is a fast, local vector index suitable for portfolio-scale document sets without requiring a managed vector database.

### Why pass retrieved context to the LLM?

The model is instructed to answer only from supplied context. This grounds responses in uploaded material and makes the system more suitable for document Q&A use cases.

### Why support both local and OpenAI LLMs?

- **Local FLAN-T5**: free, offline-friendly, good for demos and learning
- **OpenAI API**: stronger answer quality for portfolio presentations and interviews

## Data storage

```text
data/
├── uploads/          # Raw uploaded files
├── faiss_index/      # Persisted vector index
│   ├── index.faiss
│   ├── index.pkl
│   └── manifest.json
└── sample/           # Demo document for quick testing
```

## Future production enhancements

- Authentication and multi-user session isolation
- Async ingestion for large document batches
- Hybrid retrieval (semantic + keyword/BM25)
- Docker deployment
- Evaluation metrics for retrieval and answer quality
