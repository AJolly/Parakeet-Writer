#!/usr/bin/env python3
"""
Standalone Parakeet transcriber module.
This module runs as a separate process to avoid import conflicts.
"""

import sys
import os
import json
import tempfile
import soundfile as sf
import numpy as np

# Completely suppress ALL output from NeMo
import logging
import contextlib

# Set up logging to suppress everything
logging.getLogger().setLevel(logging.CRITICAL)
for name in ['nemo', 'nemo.collections', 'nemo.core', 'omegaconf', 'hydra']:
    logging.getLogger(name).setLevel(logging.CRITICAL)

@contextlib.contextmanager
def suppress_all_output():
    """Suppress both stdout and stderr to prevent any NeMo output from interfering with JSON."""
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

def load_parakeet_model():
    """Load the Parakeet model using the same approach as the working Gradio interface."""
    try:
        with suppress_all_output():
            import nemo.collections.asr as nemo_asr
            model = nemo_asr.models.ASRModel.from_pretrained('nvidia/parakeet-tdt-0.6b-v2')
        return model
    except Exception as e:
        return None

def transcribe_audio_file(model, audio_file_path):
    """Transcribe an audio file using the Parakeet model."""
    try:
        if not os.path.exists(audio_file_path):
            return ""
            
        with suppress_all_output():
            result = model.transcribe([audio_file_path])
        
        if result and len(result) > 0:
            text = result[0].text if hasattr(result[0], 'text') else str(result[0])
            return text.strip()
        return ""
    except Exception as e:
        return ""

def main():
    """Main function for standalone transcription."""
    if len(sys.argv) != 2:
        # Send usage to stderr so it doesn't interfere with JSON output
        print("Usage: python parakeet_transcriber.py <audio_file_path>", file=sys.stderr)
        sys.exit(1)
    
    audio_file_path = sys.argv[1]
    
    # Load model
    model = load_parakeet_model()
    if model is None:
        result = {"text": "", "error": "Failed to load model"}
        print(json.dumps(result))
        sys.exit(1)
    
    # Transcribe
    transcription = transcribe_audio_file(model, audio_file_path)
    
    # Output result as clean JSON to stdout
    result = {"text": transcription}
    print(json.dumps(result))

if __name__ == "__main__":
    main() 