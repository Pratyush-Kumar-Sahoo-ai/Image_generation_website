#!/bin/bash

echo "🔍 Testing GCP Authentication"
echo "=============================="

# Check if service account key exists
if [ ! -f "lumina-cicd-key.json" ]; then
    echo "❌ Service account key file not found!"
    exit 1
fi

echo "✅ Service account key file found"

# Activate service account
echo "🔐 Activating service account..."
gcloud auth activate-service-account --key-file=lumina-cicd-key.json

# Test authentication
echo "🧪 Testing authentication..."
gcloud auth list

# Test project access
echo "📋 Testing project access..."
gcloud config set project velvety-arc-470617-v8
gcloud config list project

# Test container registry access
echo "🐳 Testing container registry access..."
gcloud auth configure-docker

echo "✅ Authentication test complete!"
echo ""
echo "📋 Next steps:"
echo "1. Add the GCP_SA_KEY secret to your GitHub repository"
echo "2. The secret value should be the entire content of lumina-cicd-key.json"
echo "3. Push your code to trigger the deployment" 