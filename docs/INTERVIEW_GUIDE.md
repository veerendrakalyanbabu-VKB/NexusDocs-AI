# Interview guide

Use this guide to explain the project clearly in GenAI, AI application, and junior AI engineer interviews.

## 30-second elevator pitch

"I built an AI document Q&A assistant using Python and Streamlit. Users upload PDF, DOCX, or TXT files, the system chunks and embeds the content, stores it in a FAISS vector index, retrieves the most relevant passages for each question, and sends that context to an LLM to generate grounded answers with source citations."

## What problem does it solve?

Organizations often need to query long documents without manually reading everything. A plain LLM can hallucinate or miss document-specific details. RAG solves this by retrieving relevant passages first and forcing the model to answer from that evidence.

## How do you explain RAG?

RAG = **Retrieval** + **Augmented** + **Generation**

1. **Retrieval**: find relevant document chunks for the user's question
2. **Augmented**: add those chunks to the LLM prompt as context
3. **Generation**: the LLM produces an answer grounded in retrieved text

## Common interview questions

### Why do we chunk documents?

Because full documents are too large for efficient retrieval and may exceed model context limits. Smaller chunks improve precision and let the system return only the most relevant sections.

### What are embeddings?

Embeddings are numerical vector representations of text. Similar meaning produces similar vectors, which enables semantic search.

### What is vector search?

Vector search compares the question embedding against document chunk embeddings and returns the closest matches. In this project, that is implemented with FAISS.

### Why not send the whole document to the LLM?

Large documents are expensive, slow, and noisy. Retrieval narrows the context to the most relevant evidence and improves answer quality.

### How do prompts influence the response?

The prompt tells the model to:
- answer only from provided context
- stay concise and structured
- admit when the answer is not in the document

This reduces hallucination and improves trust.

### What happens if the answer is not in the document?

The prompt instructs the model to respond with:
`"I don't know based on the provided document."`

### What technologies did you use?

- **Python** for backend logic
- **Streamlit** for the UI
- **LangChain** for document handling and retrieval plumbing
- **Hugging Face embeddings** for semantic vectors
- **FAISS** for vector search
- **FLAN-T5** or **OpenAI API** for answer generation

## Demo flow for interviews

1. Open **NexusDocs AI** (`streamlit run app.py`)
2. Click **Demo** or upload a document and click **Save**
3. Click **Build knowledge base**
4. Ask: "Which file formats are supported?"
5. Show the answer and expand **Sources** (note real FAISS similarity scores)

This proves the full pipeline works live.

## What makes this project credible?

- Real ingestion pipeline, not a mock chatbot
- Source citations for traceability
- Modular code structure
- Local and API-based LLM support
- Tests for core components
- Architecture documentation

## What to say you would improve next

- Hybrid retrieval for better keyword matching
- Evaluation framework for retrieval quality
- Dockerized deployment
- Cloud deployment on GCP after Project #3

## Resume bullet mapping

| Resume bullet | What to demonstrate |
|---------------|---------------------|
| Document ingestion | Upload PDF/DOCX/TXT in the app |
| RAG workflow | Explain upload → chunk → embed → retrieve → generate |
| Retrieval and prompt design | Show top-k setting and grounded prompt rules |
| Streamlit interface | Live demo of chat + sources |
| Portfolio-ready structure | GitHub repo, README, docs, tests |
