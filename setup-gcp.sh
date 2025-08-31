#!/bin/bash

# Lumina GCP Setup Script
# This script helps set up Google Cloud Platform for the CI/CD pipeline

set -e

echo "🚀 Setting up Google Cloud Platform for Lumina CI/CD Pipeline"
echo "=============================================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI is not installed."
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "🔐 Please authenticate with Google Cloud:"
    gcloud auth login
fi

# Get project ID
echo "📋 Enter your Google Cloud Project ID:"
read -r PROJECT_ID

# Set the project
echo "Setting project to: $PROJECT_ID"
gcloud config set project "$PROJECT_ID"

# Enable required APIs
echo "🔧 Enabling required APIs..."
#gcloud services enable cloudrun.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Configure Docker for Container Registry
echo "🐳 Configuring Docker for Container Registry..."
gcloud auth configure-docker

# Create service account
echo "👤 Creating service account for CI/CD..."
gcloud iam service-accounts create lumina-cicd \
    --display-name="Lumina CI/CD Service Account" \
    --description="Service account for Lumina CI/CD pipeline"

# Get the service account email
SA_EMAIL="lumina-cicd@$PROJECT_ID.iam.gserviceaccount.com"

# Grant necessary roles
echo "🔑 Granting necessary roles..."
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/cloudbuild.builds.builder"

# Create and download key
echo "📄 Creating service account key..."
gcloud iam service-accounts keys create lumina-cicd-key.json \
    --iam-account="$SA_EMAIL"

echo ""
echo "✅ GCP Setup Complete!"
echo "=============================================================="
echo ""
echo "📋 Next Steps:"
echo "1. Add the following secrets to your GitHub repository:"
echo "   - GCP_PROJECT_ID: $PROJECT_ID"
echo "   - GCP_SA_KEY: (content of lumina-cicd-key.json file)"
echo ""
echo "2. To add the secrets:"
echo "   - Go to your GitHub repository"
echo "   - Navigate to Settings > Secrets and variables > Actions"
echo "   - Add the secrets with the values above"
echo ""
echo "3. The service account key file 'lumina-cicd-key.json' has been created"
echo "   Copy its contents for the GCP_SA_KEY secret"
echo ""
echo "4. Push your code to trigger the CI/CD pipeline!"
echo ""
echo "⚠️  Security Note: Keep the lumina-cicd-key.json file secure and don't commit it to your repository" 