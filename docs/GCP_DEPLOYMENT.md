# GCP Generative AI Application — Project 3

This document describes the **cloud architecture actually implemented** in this repository. Use it for deployment, interviews, and resume wording **after** you have deployed and verified the stack.

## What Project 3 adds

Project 3 extends **NexusDocs AI** (Project 2) with Google Cloud integration:

| Service | Role in this application |
|---------|--------------------------|
| **Cloud Run** | Hosts the containerized Streamlit application |
| **Cloud Storage** | Persists uploaded documents and FAISS index artifacts |
| **BigQuery** | Stores structured event data for document and query analytics |
| **Vertex AI (Gemini)** | Generates grounded answers in cloud deployments |
| **IAM** | Service account with least-privilege roles for Cloud Run |

## Architecture

```text
User (Browser)
      ↓
Streamlit App (Cloud Run)
      ↓
┌─────┴──────────────────────────────────────┐
│  RAG Pipeline (same as Project 2)            │
│  Upload → Chunk → Embed → FAISS → Retrieve   │
└─────┬──────────────────────────────────────┘
      ↓
Google Cloud
├── Cloud Storage   → uploads/, faiss_index/
├── BigQuery        → document_events, query_events
├── Vertex AI       → Gemini answer generation
└── IAM             → dedicated service account
      ↓
Grounded AI response + source citations
```

## Code modules

| Module | Purpose |
|--------|---------|
| `src/cloud/gcs_storage.py` | Sync uploads/index to Cloud Storage |
| `src/cloud/bigquery_logger.py` | Log events + run SQL analytics |
| `src/cloud/vertex_ai.py` | Vertex AI Gemini integration |
| `src/config.py` | Cloud environment configuration |
| `gcp/bigquery/schema.sql` | BigQuery table definitions |
| `gcp/iam/service-account-roles.md` | IAM role documentation |
| `Dockerfile` | Container image for Cloud Run |
| `scripts/gcp-setup.ps1` | One-time GCP resource setup |
| `scripts/gcp-deploy.ps1` | Build and deploy to Cloud Run |

## Prerequisites

1. [Google Cloud account](https://cloud.google.com/) with billing enabled
2. [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated
3. A GCP project with Owner or Editor access

## One-time setup

```powershell
cd AI-Document-QA-Assistant
.\scripts\gcp-setup.ps1 -ProjectId YOUR_PROJECT_ID
```

This script:

- Enables required GCP APIs
- Creates an Artifact Registry repository
- Creates a Cloud Storage bucket
- Creates a BigQuery dataset and tables
- Creates a service account with IAM roles

## Deploy to Cloud Run

```powershell
.\scripts\gcp-deploy.ps1 -ProjectId YOUR_PROJECT_ID
```

The command prints your live Cloud Run URL when deployment succeeds.

## Environment variables

| Variable | Description |
|----------|-------------|
| `GCP_PROJECT` | Google Cloud project ID |
| `GCS_BUCKET` | Bucket for uploads and index |
| `BQ_DATASET` | BigQuery dataset name |
| `GCP_REGION` | Vertex AI / Cloud Run region |
| `VERTEX_MODEL` | Gemini model ID |
| `DEPLOYMENT_ENV` | `cloud` on Cloud Run, `local` otherwise |

See `.env.example` for the full list.

## BigQuery analytics

The app logs:

- **document_events** — uploads, indexing, deletions
- **query_events** — questions, providers, latency, relevance scores

Example SQL:

```sql
SELECT provider, COUNT(*) AS queries
FROM `YOUR_PROJECT.nexusdocs_analytics.query_events`
GROUP BY provider;
```

## Local development

Cloud modules are **optional locally**. Without GCP env vars, the app runs exactly like Project 2 using local storage and FLAN-T5/OpenAI.

To test GCP packages locally:

```bash
pip install -r requirements-gcp.txt
```

Set `GCP_PROJECT`, `GCS_BUCKET`, and `BQ_DATASET` in `.env` to enable cloud features.

## Verification checklist

Before claiming this on your resume:

- [ ] `gcp-setup.ps1` completed without errors
- [ ] `gcp-deploy.ps1` returns a live Cloud Run URL
- [ ] Upload → index → ask flow works on the deployed URL
- [ ] Files appear in Cloud Storage bucket
- [ ] Rows appear in BigQuery tables after queries
- [ ] Vertex AI generates answers (check `provider = vertex` in logs)

## Resume wording (use only after verification)

> **GCP Generative AI Application** | Python, Google Cloud Platform, BigQuery, Cloud Storage, IAM, Vertex AI | 2026
>
> Deployed a cloud-based RAG application on Cloud Run integrating Cloud Storage for document persistence, BigQuery for query analytics, IAM service accounts for secure access, and Vertex AI Gemini for grounded answer generation.

## Production improvements (future)

- Secret Manager for API keys
- Authenticated Cloud Run (remove public access)
- Per-user session isolation
- Cloud Logging dashboards
- CI/CD with GitHub Actions + Cloud Build triggers
