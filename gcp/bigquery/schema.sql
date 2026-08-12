-- BigQuery schema for NexusDocs AI cloud analytics (Project 3)
-- Dataset: nexusdocs_analytics (configurable via BQ_DATASET)

CREATE TABLE IF NOT EXISTS document_events (
  event_id STRING NOT NULL,
  event_type STRING NOT NULL,
  file_name STRING,
  file_type STRING,
  file_size_bytes INT64,
  chunk_count INT64,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS query_events (
  query_id STRING NOT NULL,
  question STRING,
  answer_preview STRING,
  provider STRING,
  chunks_retrieved INT64,
  top_relevance FLOAT64,
  response_ms INT64,
  created_at TIMESTAMP NOT NULL
);

-- Example analytics queries used by the application
-- Total queries:
-- SELECT COUNT(*) AS total_queries FROM `PROJECT.nexusdocs_analytics.query_events`;

-- Provider breakdown:
-- SELECT provider, COUNT(*) AS query_count
-- FROM `PROJECT.nexusdocs_analytics.query_events`
-- GROUP BY provider;
