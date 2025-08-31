import os
os.environ["TRANSFORMERS_NO_TORCHVISION"] = "1"

import io
from typing import Optional

import torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from diffusers import DiffusionPipeline

app = FastAPI(title="Lumina Text-to-Image API")

pipe: Optional[DiffusionPipeline] = None

@app.get("/health")
def health_check():
    if pipe is None:
        return {"status": "starting", "model_loaded": False, "version": "1.0.1", "message": "Model is still loading"}
    return {"status": "healthy", "model_loaded": True, "version": "1.0.1"}


class GenerateRequest(BaseModel):
    prompt: str
    height: int = 1024
    width: int = 1024
    guidance_scale: float = 4.0
    num_inference_steps: int = 30
    seed: Optional[int] = None


@app.on_event("startup")
def load_model() -> None:
    global pipe
    try:
        # Set memory optimization
        import gc
        import os
        gc.collect()
        
        # Set environment variables for better caching
        os.environ['TRANSFORMERS_CACHE'] = '/tmp/transformers_cache'
        os.environ['HF_HOME'] = '/tmp/huggingface_cache'
        os.environ['HF_DATASETS_CACHE'] = '/tmp/datasets_cache'
        os.environ['HF_METRICS_CACHE'] = '/tmp/metrics_cache'
        
        print("Starting model download...")
        pipe = DiffusionPipeline.from_pretrained(
            "Alpha-VLLM/Lumina-Image-2.0",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
        )
        pipe.enable_model_cpu_offload()
        
        # Clear cache after loading
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        print("Model loaded successfully!")
            
    except Exception as e:
        print(f"Failed to load pipeline: {e}")
        # Don't raise error, let the app start without model
        pipe = None


@app.post("/generate", response_class=Response)
def generate(req: GenerateRequest):
    if pipe is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    if not req.prompt or not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt must be non-empty")

    generator = None
    if req.seed is not None:
        generator = torch.Generator("cpu").manual_seed(int(req.seed))

    try:
        image = pipe(
            req.prompt,
            height=req.height,
            width=req.width,
            guidance_scale=req.guidance_scale,
            num_inference_steps=req.num_inference_steps,
            cfg_trunc_ratio=0.25,
            cfg_normalization=True,
            generator=generator,
        ).images[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e}")

    # Encode as PNG
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    png_bytes = buf.getvalue()
    return Response(content=png_bytes, media_type="image/png") # Backend test - Sun Aug 31 12:54:40 IST 2025
# Backend test fix - Sun Aug 31 13:17:01 IST 2025
