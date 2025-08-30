# 🚀 Lumina CI/CD Setup Guide

This guide will walk you through setting up the complete CI/CD pipeline for your Lumina text-to-image application.

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ A GitHub repository with your Lumina code
- ✅ A Google Cloud Platform account
- ✅ Google Cloud CLI installed (`gcloud`)
- ✅ Docker installed (for local testing)

## 🛠️ Step-by-Step Setup

### 1. Google Cloud Platform Setup

#### Option A: Automated Setup (Recommended)
```bash
# Run the automated setup script
./setup-gcp.sh
```

#### Option B: Manual Setup
If you prefer to set up manually:

1. **Install Google Cloud CLI**
   ```bash
   # macOS
   brew install google-cloud-sdk
   
   # Or download from: https://cloud.google.com/sdk/docs/install
   ```

2. **Authenticate with GCP**
   ```bash
   gcloud auth login
   ```

3. **Create a GCP Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Note your Project ID

4. **Enable Required APIs**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   gcloud services enable cloudrun.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

5. **Create Service Account**
   ```bash
   gcloud iam service-accounts create lumina-cicd \
     --display-name="Lumina CI/CD Service Account"
   
   SA_EMAIL="lumina-cicd@YOUR_PROJECT_ID.iam.gserviceaccount.com"
   
   # Grant necessary roles
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:$SA_EMAIL" \
     --role="roles/run.admin"
   
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:$SA_EMAIL" \
     --role="roles/storage.admin"
   
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:$SA_EMAIL" \
     --role="roles/iam.serviceAccountUser"
   ```

6. **Create Service Account Key**
   ```bash
   gcloud iam service-accounts keys create lumina-cicd-key.json \
     --iam-account="$SA_EMAIL"
   ```

### 2. GitHub Secrets Setup

1. **Go to your GitHub repository**
2. **Navigate to Settings > Secrets and variables > Actions**
3. **Add the following secrets:**

   **GCP_PROJECT_ID**
   - Name: `GCP_PROJECT_ID`
   - Value: Your Google Cloud Project ID

   **GCP_SA_KEY**
   - Name: `GCP_SA_KEY`
   - Value: The entire content of the `lumina-cicd-key.json` file

### 3. Test Your Setup

#### Local Testing
```bash
# Test the frontend build
cd frontend
npm install
npm run build

# Test Docker build
docker build -t lumina-frontend .
docker run -p 8080:8080 lumina-frontend
```

#### Push to Trigger CI/CD
```bash
# Commit and push your changes
git add .
git commit -m "Add CI/CD pipeline setup"
git push origin main
```

## 🔍 Monitoring Your Deployment

### GitHub Actions
1. Go to your repository on GitHub
2. Click on the "Actions" tab
3. Monitor the CI/CD pipeline progress

### Google Cloud Run
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to Cloud Run
3. Find your `lumina-frontend` service
4. Click on it to see deployment details and logs

## 🐛 Troubleshooting

### Common Issues

#### 1. "Permission denied" errors
- Ensure your service account has the correct roles
- Verify the service account key is properly formatted in GitHub secrets

#### 2. "API not enabled" errors
- Make sure all required APIs are enabled in your GCP project
- Run: `gcloud services enable cloudrun.googleapis.com`

#### 3. "Docker build failed" errors
- Check that your Dockerfile is in the root directory
- Verify the nginx.conf file exists
- Ensure the frontend builds successfully locally

#### 4. "Container registry access denied"
- Run: `gcloud auth configure-docker`
- Verify your service account has Storage Admin role

### Debugging Steps

1. **Check GitHub Actions logs**
   - Go to Actions tab in your repository
   - Click on the failed workflow
   - Review the detailed logs

2. **Check GCP logs**
   ```bash
   gcloud logging read "resource.type=cloud_run_revision" --limit=50
   ```

3. **Test locally**
   ```bash
   # Test frontend build
   cd frontend && npm run build
   
   # Test Docker build
   docker build -t test-lumina .
   docker run -p 8080:8080 test-lumina
   ```

## 📊 Deployment Information

### What Gets Deployed
- ✅ React frontend (built and optimized)
- ✅ Nginx web server
- ✅ Static file serving with caching
- ✅ Security headers
- ✅ Gzip compression

### Deployment Configuration
- **Platform**: Google Cloud Run
- **Region**: us-central1 (configurable)
- **Memory**: 512Mi
- **CPU**: 1
- **Max Instances**: 10
- **Port**: 8080
- **Authentication**: Public (unauthenticated)

### Environment Variables
- `NODE_ENV=production`
- Customizable via Cloud Run console

## 🔄 Updating Your Deployment

### Automatic Updates
- Every push to `main` or `master` branch triggers a new deployment
- Previous deployments are automatically replaced

### Manual Updates
```bash
# Build and deploy manually
docker build -t gcr.io/YOUR_PROJECT_ID/lumina-frontend:latest .
docker push gcr.io/YOUR_PROJECT_ID/lumina-frontend:latest

gcloud run deploy lumina-frontend \
  --image gcr.io/YOUR_PROJECT_ID/lumina-frontend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 📈 Scaling and Performance

### Automatic Scaling
- Cloud Run automatically scales to zero when not in use
- Scales up based on incoming requests
- Maximum 10 instances (configurable)

### Performance Optimization
- Static assets are cached for 1 year
- HTML files cached for 1 hour
- Gzip compression enabled
- Optimized React build

## 🔒 Security Considerations

### What's Secured
- ✅ HTTPS enforced by Cloud Run
- ✅ Security headers configured
- ✅ Content Security Policy set
- ✅ XSS protection enabled
- ✅ Frame options configured

### Best Practices
- Keep service account keys secure
- Regularly rotate service account keys
- Monitor Cloud Run logs for suspicious activity
- Use environment variables for sensitive configuration

## 📞 Support

If you encounter issues:

1. **Check the troubleshooting section above**
2. **Review GitHub Actions logs**
3. **Check GCP Cloud Run logs**
4. **Open an issue on GitHub**

## 🎉 Success!

Once your pipeline is working, you'll have:
- ✅ Automated testing on every push
- ✅ Automated deployment to production
- ✅ Zero-downtime deployments
- ✅ Scalable, secure hosting
- ✅ Easy rollback capabilities

Your Lumina frontend will be available at the URL provided in the GitHub Actions logs! 