#!/bin/bash

# Deploy both Frontend and Backend to Google Cloud Run
echo "🚀 Deploying Lumina Frontend and Backend to Google Cloud Run"
echo "=============================================================="

# Check if gcloud is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Please authenticate with gcloud first:"
    echo "   gcloud auth login"
    exit 1
fi

# Set project
PROJECT_ID="velvety-arc-470617-v8"
REGION="us-central1"

echo "📋 Using project: $PROJECT_ID"
echo "🌍 Region: $REGION"

# Deploy Backend
echo ""
echo "🔧 Deploying Backend..."
echo "Building backend Docker image..."

# Build and push backend
docker build -f Dockerfile.backend -t gcr.io/$PROJECT_ID/lumina-backend:latest .
docker push gcr.io/$PROJECT_ID/lumina-backend:latest

echo "Deploying backend to Cloud Run..."
gcloud run deploy lumina-backend \
  --image gcr.io/$PROJECT_ID/lumina-backend:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8000 \
  --memory 4Gi \
  --cpu 2 \
  --max-instances 5 \
  --timeout 900

# Get backend URL
BACKEND_URL=$(gcloud run services describe lumina-backend --region=$REGION --format='value(status.url)')
echo "✅ Backend deployed to: $BACKEND_URL"

# Deploy Frontend
echo ""
echo "🎨 Deploying Frontend..."
echo "Building frontend..."

# Build frontend
cd frontend
npm install
npm run build:prod
cd ..

echo "Building frontend Docker image..."
docker build -t gcr.io/$PROJECT_ID/lumina-frontend:latest .
docker push gcr.io/$PROJECT_ID/lumina-frontend:latest

echo "Deploying frontend to Cloud Run..."
gcloud run deploy lumina-frontend \
  --image gcr.io/$PROJECT_ID/lumina-frontend:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10

# Get frontend URL
FRONTEND_URL=$(gcloud run services describe lumina-frontend --region=$REGION --format='value(status.url)')
echo "✅ Frontend deployed to: $FRONTEND_URL"

echo ""
echo "🎉 Deployment Complete!"
echo "=============================================================="
echo "🌐 Frontend: $FRONTEND_URL"
echo "🔧 Backend: $BACKEND_URL"
echo ""
echo "📝 Next steps:"
echo "1. Update the frontend to use the backend URL: $BACKEND_URL"
echo "2. Test the complete application"
echo "3. Share your application with others!"
echo ""
echo "💡 To update the frontend API URL, you can:"
echo "   - Edit the frontend code and redeploy"
echo "   - Or use environment variables in Cloud Run" 