# GCP setup script for NexusDocs AI (Project 3)
# Run from project root in PowerShell with gcloud CLI authenticated.

param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectId,

    [string]$Region = "us-central1",
    [string]$BucketName = "",
    [string]$Dataset = "nexusdocs_analytics",
    [string]$ServiceAccount = "nexusdocs-runner"
)

$ErrorActionPreference = "Stop"

if (-not $BucketName) {
    $BucketName = "$ProjectId-nexusdocs-data"
}

Write-Host "Setting project to $ProjectId..."
gcloud config set project $ProjectId

Write-Host "Enabling required APIs..."
gcloud services enable `
    run.googleapis.com `
    cloudbuild.googleapis.com `
    artifactregistry.googleapis.com `
    storage.googleapis.com `
    bigquery.googleapis.com `
    aiplatform.googleapis.com `
    secretmanager.googleapis.com

Write-Host "Creating Artifact Registry repository..."
gcloud artifacts repositories create nexusdocs `
    --repository-format=docker `
    --location=$Region `
    --description="NexusDocs AI container images" `
    2>$null

Write-Host "Creating Cloud Storage bucket gs://$BucketName..."
gsutil mb -l $Region "gs://$BucketName" 2>$null

Write-Host "Creating BigQuery dataset $Dataset..."
bq --location=$Region mk --dataset "$ProjectId`:$Dataset" 2>$null

Write-Host "Creating BigQuery tables..."
Get-Content "gcp/bigquery/schema.sql" | bq query --use_legacy_sql=false --project_id=$ProjectId

Write-Host "Creating service account $ServiceAccount..."
gcloud iam service-accounts create $ServiceAccount `
    --display-name="NexusDocs AI Cloud Run" `
    2>$null

$SaEmail = "$ServiceAccount@$ProjectId.iam.gserviceaccount.com"

foreach ($Role in @(
    "roles/storage.objectAdmin",
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
    "roles/aiplatform.user"
)) {
    gcloud projects add-iam-policy-binding $ProjectId `
        --member="serviceAccount:$SaEmail" `
        --role=$Role `
        --quiet | Out-Null
}

Write-Host ""
Write-Host "Setup complete."
Write-Host "Bucket:      gs://$BucketName"
Write-Host "Dataset:     $ProjectId.$Dataset"
Write-Host "Service acct: $SaEmail"
Write-Host ""
Write-Host "Next: run scripts/gcp-deploy.ps1 -ProjectId $ProjectId"
