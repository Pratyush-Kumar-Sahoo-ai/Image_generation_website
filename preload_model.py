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
        
        # Set environment variables for better disk usage
        os.environ['TRANSFORMERS_CACHE'] = '/tmp/transformers_cache'
        os.environ['HF_HOME'] = '/tmp/huggingface_cache'
        os.environ['HF_DATASETS_CACHE'] = '/tmp/datasets_cache'
        os.environ['HF_METRICS_CACHE'] = '/tmp/metrics_cache'
        
        # Check available disk space
        import shutil
        total, used, free = shutil.disk_usage('/tmp')
        print(f'Available disk space: {free // (1024**3)} GB')
        
        if free < 10 * (1024**3):  # Less than 10GB
            print('Warning: Low disk space, skipping model pre-download')
            return False
        
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