# Deploy NexusDocs AI to Cloud Run (Project 3)

param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectId,

    [string]$Region = "us-central1",
    [string]$ServiceName = "nexusdocs-ai",
    [string]$BucketName = "",
    [string]$Dataset = "nexusdocs_analytics",
    [string]$ServiceAccount = "nexusdocs-runner"
)

$ErrorActionPreference = "Stop"

if (-not $BucketName) {
    $BucketName = "$ProjectId-nexusdocs-data"
}

$Image = "$Region-docker.pkg.dev/$ProjectId/nexusdocs/$ServiceName`:latest"
$SaEmail = "$ServiceAccount@$ProjectId.iam.gserviceaccount.com"

Write-Host "Building container image..."
gcloud builds submit --tag $Image --project $ProjectId

Write-Host "Deploying to Cloud Run..."
gcloud run deploy $ServiceName `
    --image $Image `
    --region $Region `
    --platform managed `
    --allow-unauthenticated `
    --service-account $SaEmail `
    --memory 4Gi `
    --cpu 2 `
    --timeout 300 `
    --port 8080 `
    --set-env-vars "DEPLOYMENT_ENV=cloud,GCP_PROJECT=$ProjectId,GCP_REGION=$Region,GCS_BUCKET=$BucketName,BQ_DATASET=$Dataset,VERTEX_MODEL=gemini-2.0-flash-001" `
    --project $ProjectId

Write-Host ""
Write-Host "Deployment complete."
gcloud run services describe $ServiceName --region $Region --format="value(status.url)"
