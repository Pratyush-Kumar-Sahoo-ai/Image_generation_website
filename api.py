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
    return {"status": "healthy", "model_loaded": pipe is not None}


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
        pipe = DiffusionPipeline.from_pretrained(
            "Alpha-VLLM/Lumina-Image-2.0",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
        )
        pipe.enable_model_cpu_offload()
    except Exception as e:
        raise RuntimeError(f"Failed to load pipeline: {e}")


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
    return Response(content=png_bytes, media_type="image/png") 