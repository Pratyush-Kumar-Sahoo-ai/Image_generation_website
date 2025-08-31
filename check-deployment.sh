#!/bin/bash

echo "🔍 Checking Lumina Deployment Status"
echo "====================================="

# Check if gcloud is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Please authenticate with gcloud first:"
    echo "   gcloud auth login"
    exit 1
fi

REGION="asia-south1"

echo "🌍 Checking Cloud Run services in region: $REGION"
echo ""

# Check Frontend
echo "🎨 Frontend Status:"
FRONTEND_URL=$(gcloud run services describe lumina-frontend --region=$REGION --format='value(status.url)' 2>/dev/null)
if [ $? -eq 0 ] && [ ! -z "$FRONTEND_URL" ]; then
    echo "✅ Frontend is deployed: $FRONTEND_URL"
    
    # Test frontend health
    echo "🧪 Testing frontend..."
    if curl -s -f "$FRONTEND_URL" > /dev/null; then
        echo "✅ Frontend is responding"
    else
        echo "⚠️  Frontend is not responding"
    fi
else
    echo "❌ Frontend is not deployed"
fi

echo ""

# Check Backend
echo "🔧 Backend Status:"
BACKEND_URL=$(gcloud run services describe lumina-backend --region=$REGION --format='value(status.url)' 2>/dev/null)
if [ $? -eq 0 ] && [ ! -z "$BACKEND_URL" ]; then
    echo "✅ Backend is deployed: $BACKEND_URL"
    
    # Test backend health
    echo "🧪 Testing backend health..."
    if curl -s -f "$BACKEND_URL/health" > /dev/null; then
        echo "✅ Backend health check passed"
    else
        echo "⚠️  Backend health check failed"
    fi
    
    # Test API docs
    echo "📚 Testing API docs..."
    if curl -s -f "$BACKEND_URL/docs" > /dev/null; then
        echo "✅ API docs are accessible"
    else
        echo "⚠️  API docs are not accessible"
    fi
else
    echo "❌ Backend is not deployed"
fi

echo ""
echo "📋 Summary:"
echo "====================================="
if [ ! -z "$FRONTEND_URL" ]; then
    echo "🌐 Frontend: $FRONTEND_URL"
fi
if [ ! -z "$BACKEND_URL" ]; then
    echo "🔧 Backend: $BACKEND_URL"
fi

echo ""
echo "💡 Next steps:"
if [ ! -z "$BACKEND_URL" ] && [ ! -z "$FRONTEND_URL" ]; then
    echo "✅ Both services are deployed!"
    echo "🎯 Update frontend to use backend URL: $BACKEND_URL"
    echo "🧪 Test the complete application"
elif [ ! -z "$FRONTEND_URL" ]; then
    echo "⚠️  Only frontend is deployed"
    echo "🔧 Wait for backend deployment to complete"
else
    echo "❌ No services are deployed yet"
    echo "⏳ Check GitHub Actions for deployment progress"
fi 