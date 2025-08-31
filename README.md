# Lumina Text-to-Image API & Frontend

A complete text-to-image generation system with a FastAPI backend and React frontend, featuring automated CI/CD deployment to Google Cloud Platform.

## 🚀 Features

### Backend (FastAPI)
- Text-to-image generation using Alpha-VLLM/Lumina-Image-2.0
- Configurable image dimensions, guidance scale, and inference steps
- Seed-based reproducible generation
- RESTful API with automatic model loading

### Frontend (React)
- Modern, responsive UI built with React and TypeScript
- Real-time image generation with loading states
- Parameter controls for fine-tuning generation
- Image download functionality
- Mobile-friendly design

### CI/CD Pipeline
- Automated testing and building
- Deployment to Google Cloud Run
- Docker containerization
- GitHub Actions workflow

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- CUDA-compatible GPU (recommended for backend)
- At least 8GB GPU memory
- Google Cloud Platform account
- Docker

## 🛠️ Installation

### 1. Clone the repository
   ```bash
git clone <your-repo-url>
cd Lumina
   ```

### 2. Backend Setup
   ```bash
# Activate your conda environment
conda activate diffusion

# Install Python dependencies
   pip install -r requirements.txt

# Install FastAPI and uvicorn
pip install fastapi uvicorn
   ```

### 3. Frontend Setup
   ```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start development server
npm start
   ```

## 🚀 Running the Application

### Backend API
```bash
# Start the FastAPI server
uvicorn api:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend
```bash
# In the frontend directory
npm start
```

The frontend will be available at `http://localhost:3000`

## 🏗️ CI/CD Setup

### 1. Google Cloud Platform Setup

#### Create a GCP Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Cloud Run API
   - Container Registry API
   - Cloud Build API

#### Create a Service Account
1. Go to IAM & Admin > Service Accounts
2. Create a new service account with the following roles:
   - Cloud Run Admin
   - Storage Admin
   - Service Account User
3. Create and download a JSON key file

#### Enable Container Registry
```bash
gcloud auth configure-docker
```

### 2. GitHub Secrets Setup

Add the following secrets to your GitHub repository (Settings > Secrets and variables > Actions):

- `GCP_PROJECT_ID`: Your Google Cloud Project ID
- `GCP_SA_KEY`: The entire content of your service account JSON key file

### 3. Deploy

The CI/CD pipeline will automatically:
1. Run tests on every push and pull request
2. Build the frontend for production
3. Deploy to Google Cloud Run on main/master branch pushes
4. Provide deployment URLs in pull request comments

## 📖 API Usage

### Endpoint: `POST /generate`

Generates an image from a text prompt.

#### Request Body:
```json
{
  "prompt": "A beautiful sunset over mountains",
  "height": 1024,
  "width": 1024,
  "guidance_scale": 4.0,
  "num_inference_steps": 30,
  "seed": 42
}
```

#### Parameters:
- `prompt` (required): Text description of the image to generate
- `height` (optional): Image height in pixels (default: 1024)
- `width` (optional): Image width in pixels (default: 1024)
- `guidance_scale` (optional): Controls how closely the image follows the prompt (default: 4.0)
- `num_inference_steps` (optional): Number of denoising steps (default: 30)
- `seed` (optional): Random seed for reproducible generation

#### Response:
Returns a PNG image file.

## 🔧 Development

### Frontend Development
```bash
cd frontend
npm start          # Start development server
npm run build      # Build for production
npm test           # Run tests
```

### Backend Development
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Start development server with auto-reload
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Docker Development
```bash
# Build the frontend container
docker build -t lumina-frontend .

# Run locally
docker run -p 8080:8080 lumina-frontend
```

## 🌐 Deployment

### Manual Deployment to GCP
```bash
# Build and push Docker image
docker build -t gcr.io/YOUR_PROJECT_ID/lumina-frontend:latest .
docker push gcr.io/YOUR_PROJECT_ID/lumina-frontend:latest

# Deploy to Cloud Run
gcloud run deploy lumina-frontend \
  --image gcr.io/YOUR_PROJECT_ID/lumina-frontend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

### Environment Variables

The frontend can be configured with environment variables:

- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:8000)
- `REACT_APP_ENVIRONMENT`: Environment name (development/production)

## 🐛 Troubleshooting

### Common Issues:

1. **Out of Memory Error:**
   - Reduce image dimensions (height/width)
   - Lower `num_inference_steps`
   - Ensure sufficient GPU memory

2. **Model Loading Failed:**
   - Check internet connection
   - Verify sufficient disk space
   - Ensure all dependencies are installed

3. **CUDA Errors:**
   - Install CUDA-compatible PyTorch version
   - Check GPU driver compatibility

4. **Frontend Build Issues:**
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check Node.js version compatibility
   - Verify all environment variables are set

5. **Deployment Issues:**
   - Verify GCP credentials and permissions
   - Check GitHub secrets are properly configured
   - Ensure Cloud Run API is enabled

### Performance Tips:

- Use smaller image dimensions for faster generation
- Lower `num_inference_steps` for quicker results (trade-off with quality)
- Higher `guidance_scale` values produce more prompt-following images
- Set a `seed` for reproducible results

## 📝 License

This project uses the Lumina-Image-2.0 model. Please refer to the model's license for usage terms. 

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the API documentation at `/docs`
3. Open an issue on GitHub # Updated Sun Aug 31 12:31:07 IST 2025
