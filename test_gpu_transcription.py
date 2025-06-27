#!/usr/bin/env python3
"""
Test script to verify GPU usage and transcription speed.
"""

import torch
import time
import sys
import os

def test_pytorch_gpu():
    """Test if PyTorch can use GPU."""
    print("=== PyTorch GPU Test ===")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA device count: {torch.cuda.device_count()}")
        print(f"CUDA device name: {torch.cuda.get_device_name(0)}")
        print(f"CUDA version: {torch.version.cuda}")
        
        # Test a simple tensor operation on GPU
        x = torch.randn(1000, 1000).cuda()
        y = torch.randn(1000, 1000).cuda()
        
        start_time = time.time()
        z = torch.matmul(x, y)
        gpu_time = time.time() - start_time
        print(f"GPU matrix multiplication time: {gpu_time:.4f} seconds")
        
        # Test on CPU for comparison
        x_cpu = x.cpu()
        y_cpu = y.cpu()
        start_time = time.time()
        z_cpu = torch.matmul(x_cpu, y_cpu)
        cpu_time = time.time() - start_time
        print(f"CPU matrix multiplication time: {cpu_time:.4f} seconds")
        print(f"GPU speedup: {cpu_time/gpu_time:.2f}x")
    else:
        print("CUDA not available")

def test_nemo_model():
    """Test NeMo model loading and device placement."""
    print("\n=== NeMo Model Test ===")
    try:
        import nemo.collections.asr as nemo_asr
        
        print("Loading Parakeet model...")
        start_time = time.time()
        model = nemo_asr.models.ASRModel.from_pretrained('nvidia/parakeet-tdt-0.6b-v2')
        load_time = time.time() - start_time
        print(f"Model loaded in {load_time:.2f} seconds")
        
        # Check device
        device = next(model.parameters()).device
        print(f"Model device: {device}")
        
        # Move to GPU if not already there
        if torch.cuda.is_available() and device.type == 'cpu':
            print("Moving model to GPU...")
            model = model.to('cuda')
            device = next(model.parameters()).device
            print(f"Model device after moving: {device}")
        
        model.eval()
        
        # Test transcription with sample audio
        sample_audio_path = "sample_audio.wav"
        if os.path.exists(sample_audio_path):
            print(f"Testing transcription with {sample_audio_path}...")
            start_time = time.time()
            result = model.transcribe([sample_audio_path])
            transcribe_time = time.time() - start_time
            print(f"Transcription completed in {transcribe_time:.2f} seconds")
            if result:
                text = result[0].text if hasattr(result[0], 'text') else str(result[0])
                print(f"Transcription result: '{text}'")
            else:
                print("No transcription result")
        else:
            print(f"Sample audio file {sample_audio_path} not found")
            
    except Exception as e:
        print(f"Error testing NeMo model: {e}")

def test_parakeet_transcriber():
    """Test the standalone parakeet transcriber."""
    print("\n=== Parakeet Transcriber Test ===")
    sample_audio_path = "sample_audio.wav"
    if os.path.exists(sample_audio_path):
        print("Testing standalone parakeet transcriber...")
        import subprocess
        
        transcriber_path = os.path.join("whisper-writer-parakeet", "parakeet_transcriber.py")
        if os.path.exists(transcriber_path):
            start_time = time.time()
            result = subprocess.run(
                [sys.executable, transcriber_path, sample_audio_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            transcribe_time = time.time() - start_time
            
            print(f"Transcriber completed in {transcribe_time:.2f} seconds")
            print(f"Return code: {result.returncode}")
            if result.stdout:
                print(f"Output: {result.stdout}")
            if result.stderr:
                print(f"Errors: {result.stderr}")
        else:
            print(f"Transcriber script not found at {transcriber_path}")
    else:
        print(f"Sample audio file {sample_audio_path} not found")

if __name__ == "__main__":
    test_pytorch_gpu()
    test_nemo_model()
    test_parakeet_transcriber() 