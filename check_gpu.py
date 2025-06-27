#!/usr/bin/env python3
"""
GPU Verification Script for Parakeet-Writer
This script checks if your system is properly configured for GPU-accelerated transcription.
"""

import sys
import os
import time
import traceback

def print_header(title):
    """Print a formatted header."""
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_section(title):
    """Print a formatted section header."""
    print(f"\n--- {title} ---")

def check_python_version():
    """Check Python version compatibility."""
    print_section("Python Version Check")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor == 11:
        print("✓ Python 3.11 detected - COMPATIBLE")
        return True
    elif version.major == 3 and version.minor >= 12:
        print("⚠️  Python 3.12+ detected - May have compatibility issues")
        print("   Recommended: Python 3.11.x for best compatibility")
        return True
    else:
        print("❌ Incompatible Python version")
        print("   Required: Python 3.11.x")
        return False

def check_pytorch():
    """Check PyTorch installation and CUDA support."""
    print_section("PyTorch & CUDA Check")
    
    try:
        import torch
        print(f"✓ PyTorch version: {torch.__version__}")
        
        # Check CUDA availability
        cuda_available = torch.cuda.is_available()
        print(f"CUDA available: {cuda_available}")
        
        if cuda_available:
            print(f"✓ CUDA device count: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                device_name = torch.cuda.get_device_name(i)
                print(f"  GPU {i}: {device_name}")
            
            print(f"✓ CUDA version: {torch.version.cuda}")
            
            # Test GPU performance
            print("\nTesting GPU performance...")
            device = torch.device('cuda')
            x = torch.randn(1000, 1000, device=device)
            y = torch.randn(1000, 1000, device=device)
            
            start_time = time.time()
            z = torch.matmul(x, y)
            torch.cuda.synchronize()  # Wait for GPU operation to complete
            gpu_time = time.time() - start_time
            
            print(f"✓ GPU matrix multiplication: {gpu_time:.4f} seconds")
            
            # Check memory
            memory_allocated = torch.cuda.memory_allocated() / 1024**2  # MB
            memory_reserved = torch.cuda.memory_reserved() / 1024**2    # MB
            print(f"  GPU memory allocated: {memory_allocated:.1f} MB")
            print(f"  GPU memory reserved: {memory_reserved:.1f} MB")
            
            return True
        else:
            print("❌ CUDA not available")
            print("   Possible causes:")
            print("   - No NVIDIA GPU installed")
            print("   - NVIDIA drivers not installed")
            print("   - PyTorch CPU-only version installed")
            return False
            
    except ImportError:
        print("❌ PyTorch not installed")
        print("   Install with: pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121")
        return False
    except Exception as e:
        print(f"❌ Error checking PyTorch: {e}")
        return False

def check_nemo():
    """Check NeMo installation."""
    print_section("NeMo Framework Check")
    
    try:
        import nemo
        print(f"✓ NeMo version: {nemo.__version__}")
        
        # Test ASR module
        import nemo.collections.asr as nemo_asr
        print("✓ NeMo ASR module available")
        
        return True
        
    except ImportError as e:
        print(f"❌ NeMo not installed: {e}")
        print("   Install with: pip install nemo-toolkit[asr]")
        return False
    except Exception as e:
        print(f"❌ Error checking NeMo: {e}")
        return False

def check_parakeet_model():
    """Test Parakeet model loading."""
    print_section("Parakeet Model Test")
    
    try:
        import torch
        import nemo.collections.asr as nemo_asr
        
        print("Loading Parakeet model (this may take a moment)...")
        start_time = time.time()
        
        model = nemo_asr.models.ASRModel.from_pretrained('nvidia/parakeet-tdt-0.6b-v2')
        load_time = time.time() - start_time
        
        print(f"✓ Model loaded in {load_time:.2f} seconds")
        
        # Check model device
        device = next(model.parameters()).device
        print(f"✓ Model device: {device}")
        
        # Move to GPU if available and not already there
        if torch.cuda.is_available() and device.type == 'cpu':
            print("Moving model to GPU...")
            model = model.to('cuda')
            device = next(model.parameters()).device
            print(f"✓ Model moved to: {device}")
        
        # Test with sample audio if available
        sample_audio = "sample_audio.wav"
        if os.path.exists(sample_audio):
            print(f"Testing transcription with {sample_audio}...")
            start_time = time.time()
            result = model.transcribe([sample_audio])
            transcribe_time = time.time() - start_time
            
            print(f"✓ Transcription completed in {transcribe_time:.2f} seconds")
            if result and len(result) > 0:
                text = result[0].text if hasattr(result[0], 'text') else str(result[0])
                print(f"✓ Transcription result: '{text[:100]}{'...' if len(text) > 100 else ''}'")
        else:
            print(f"⚠️  Sample audio file '{sample_audio}' not found for testing")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Parakeet model: {e}")
        traceback.print_exc()
        return False

def check_additional_dependencies():
    """Check additional required dependencies."""
    print_section("Additional Dependencies Check")
    
    dependencies = [
        ('webrtcvad', 'Voice Activity Detection'),
        ('dotenv', 'Environment variables'),
        ('openai', 'API compatibility'),
        ('PyQt5', 'GUI framework'),
        ('sounddevice', 'Audio I/O'),
        ('scipy', 'Scientific computing'),
    ]
    
    missing = []
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"✓ {module} - {description}")
        except ImportError:
            print(f"❌ {module} - {description} (MISSING)")
            missing.append(module)
    
    if missing:
        print(f"\nMissing dependencies: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    return True

def check_cuda_optimization():
    """Check for additional CUDA optimizations."""
    print_section("CUDA Optimization Check")
    
    try:
        import cuda
        print("✓ cuda-python installed - GPU graphs optimization available")
        return True
    except ImportError:
        print("⚠️  cuda-python not installed")
        print("   Install for better performance: pip install cuda-python")
        return False

def main():
    """Main verification function."""
    print_header("Parakeet-Writer GPU Verification")
    print("This script will check if your system is properly configured.")
    print("Please wait while we run the tests...\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("PyTorch & CUDA", check_pytorch),
        ("NeMo Framework", check_nemo),
        ("Additional Dependencies", check_additional_dependencies),
        ("CUDA Optimization", check_cuda_optimization),
        ("Parakeet Model", check_parakeet_model),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} check failed: {e}")
            results.append((name, False))
    
    # Summary
    print_header("Verification Summary")
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 Your system is fully configured for Parakeet-Writer!")
        print("   Expected transcription speed: 1-2 seconds")
    elif passed >= total - 2:
        print("\n⚠️  Your system should work, but with potential issues.")
        print("   Please address the failed checks above.")
    else:
        print("\n❌ Your system needs configuration before using Parakeet-Writer.")
        print("   Please install missing dependencies and fix issues above.")
    
    print("\nFor installation help, see:")
    print("- install.bat (automated installation)")
    print("- requirements.txt (manual installation)")
    print("- GitHub documentation")

if __name__ == "__main__":
    main() 