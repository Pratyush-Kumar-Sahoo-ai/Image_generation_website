import os
os.environ["TRANSFORMERS_NO_TORCHVISION"] = "1"

import torch
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained(
    "Alpha-VLLM/Lumina-Image-2.0",
    dtype=torch.bfloat16,
    trust_remote_code=True
)
pipe.enable_model_cpu_offload() #save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power

prompt = "A lone tree in a desert"
image = pipe(
    prompt,
    height=1024,
    width=1024,
    guidance_scale=4.0,
    num_inference_steps=50,
    cfg_trunc_ratio=0.25,
    cfg_normalization=True,
    generator=torch.Generator("cpu").manual_seed(0) # initial cpu
).images[0]
image.save("lumina_demo.png")