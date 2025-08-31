#!/usr/bin/env python3
"""
Pre-download the Lumina model during Docker build to avoid startup delays.
"""

import torch
from diffusers import DiffusionPipeline
import gc
import os

def preload_model():
    print('Pre-downloading Lumina model...')
    try:
        # Set memory optimization
        gc.collect()
        
        # Set environment variables
        os.environ['TRANSFORMERS_CACHE'] = '/tmp/transformers_cache'
        os.environ['HF_HOME'] = '/tmp/huggingface_cache'
        
        pipe = DiffusionPipeline.from_pretrained(
            'Alpha-VLLM/Lumina-Image-2.0',
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
        )
        pipe.enable_model_cpu_offload()
        
        # Clear cache after loading
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        print('Model pre-downloaded successfully!')
        return True
    except Exception as e:
        print(f'Model pre-download failed: {e}')
        # Don't fail the build if model download fails
        return False

if __name__ == "__main__":
    preload_model() 