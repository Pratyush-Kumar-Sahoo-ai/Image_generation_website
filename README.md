# Lumina Text-to-Image API

A FastAPI-based service for generating images from text prompts using the Lumina-Image-2.0 model.

## Features

- Text-to-image generation using Alpha-VLLM/Lumina-Image-2.0
- Configurable image dimensions, guidance scale, and inference steps
- Seed-based reproducible generation
- RESTful API with automatic model loading

## Prerequisites

- Python 3.8+
- CUDA-compatible GPU (recommended)
- At least 8GB GPU memory

## Installation

1. **Clone the repository and navigate to the Lumina directory:**
   ```bash
   cd repo_AI_somex/Diffusion_Models/Lumina
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or using conda:
   ```bash
   conda install -c conda-forge diffusers fairscale accelerate tensorboard transformers gradio torchdiffeq click torchvision
   ```

3. **Install FastAPI and uvicorn:**
   ```bash
   pip install fastapi uvicorn
   ```

## Running the API

### Start the server:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation:
- Interactive docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Interactive Testing

### Using the Web Interface:
1. Open your browser and go to `http://localhost:8000/docs`
2. Click on the `/generate` endpoint
3. Click "Try it out"
4. Enter your prompt and adjust parameters as needed
5. Click "Execute" to generate an image
6. The generated image will be displayed in the browser

### Example Test:
- **Prompt**: "A majestic dragon flying over a castle"
- **Height**: 1024
- **Width**: 1024
- **Guidance Scale**: 4.0
- **Num Inference Steps**: 30

## API Usage

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

## Curl Commands

### Basic image generation:
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A majestic dragon flying over a castle"}' \
  --output generated_image.png
```

### Custom parameters:
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A futuristic cityscape at night",
    "height": 768,
    "width": 1024,
    "guidance_scale": 7.5,
    "num_inference_steps": 50,
    "seed": 12345
  }' \
  --output futuristic_city.png
```

### High-quality generation:
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A detailed portrait of a wise old wizard with glowing eyes",
    "height": 1024,
    "width": 1024,
    "guidance_scale": 8.0,
    "num_inference_steps": 100
  }' \
  --output wizard_portrait.png
```

## Model Information

- **Model**: Alpha-VLLM/Lumina-Image-2.0
- **Framework**: Diffusers
- **Precision**: bfloat16
- **Optimization**: CPU offloading enabled

## Troubleshooting

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

### Performance Tips:

- Use smaller image dimensions for faster generation
- Lower `num_inference_steps` for quicker results (trade-off with quality)
- Higher `guidance_scale` values produce more prompt-following images
- Set a `seed` for reproducible results

## License

This project uses the Lumina-Image-2.0 model. Please refer to the model's license for usage terms. 