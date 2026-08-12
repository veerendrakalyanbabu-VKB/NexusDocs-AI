# IAM roles for the NexusDocs AI Cloud Run service account
#
# Create a dedicated service account instead of using default compute credentials.
# Replace PROJECT_ID and SERVICE_ACCOUNT with your values.

# Recommended roles (principle of least privilege for portfolio scope):
#
# roles/storage.objectAdmin        - read/write GCS bucket objects
# roles/bigquery.dataEditor        - insert analytics rows
# roles/bigquery.jobUser           - run SQL analytics queries
# roles/aiplatform.user            - call Vertex AI Gemini
# roles/run.invoker                - (optional) if using authenticated Cloud Run

# Example setup commands:
#
# gcloud iam service-accounts create nexusdocs-runner \
#   --display-name="NexusDocs AI Cloud Run"
#
# gcloud projects add-iam-policy-binding PROJECT_ID \
#   --member="serviceAccount:nexusdocs-runner@PROJECT_ID.iam.gserviceaccount.com" \
#   --role="roles/storage.objectAdmin"
#
# gcloud projects add-iam-policy-binding PROJECT_ID \
#   --member="serviceAccount:nexusdocs-runner@PROJECT_ID.iam.gserviceaccount.com" \
#   --role="roles/bigquery.dataEditor"
#
# gcloud projects add-iam-policy-binding PROJECT_ID \
#   --member="serviceAccount:nexusdocs-runner@PROJECT_ID.iam.gserviceaccount.com" \
#   --role="roles/bigquery.jobUser"
#
# gcloud projects add-iam-policy-binding PROJECT_ID \
#   --member="serviceAccount:nexusdocs-runner@PROJECT_ID.iam.gserviceaccount.com" \
#   --role="roles/aiplatform.user"
