#!/usr/bin/env python3
"""
Persistent Parakeet model server.
Keeps the model loaded in memory for fast transcription.
"""

import sys
import os
import json
import time
import tempfile
import soundfile as sf
import numpy as np
import signal
import threading
from pathlib import Path

# Completely suppress ALL output from NeMo
import logging
import contextlib

# Set up logging to suppress everything
logging.getLogger().setLevel(logging.CRITICAL)
for name in ['nemo', 'nemo.collections', 'nemo.core', 'omegaconf', 'hydra']:
    logging.getLogger(name).setLevel(logging.CRITICAL)

@contextlib.contextmanager
def suppress_all_output():
    """Suppress both stdout and stderr during NeMo operations."""
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

class ParakeetServer:
    def __init__(self):
        self.model = None
        self.running = False
        self.request_dir = None
        self.response_dir = None
        
    def load_model(self):
        """Load the Parakeet model once and keep it in memory."""
        try:
            with suppress_all_output():
                import nemo.collections.asr as nemo_asr
                self.model = nemo_asr.models.ASRModel.from_pretrained('nvidia/parakeet-tdt-0.6b-v2')
            return True
        except Exception as e:
            return False
    
    def transcribe_audio_file(self, audio_file_path):
        """Transcribe an audio file using the loaded model."""
        try:
            if not os.path.exists(audio_file_path):
                return ""
                
            with suppress_all_output():
                result = self.model.transcribe([audio_file_path])
            
            if result and len(result) > 0:
                text = result[0].text if hasattr(result[0], 'text') else str(result[0])
                return text.strip()
            return ""
        except Exception as e:
            return ""
    
    def setup_communication_dirs(self):
        """Set up temporary directories for request/response communication."""
        temp_dir = tempfile.gettempdir()
        self.request_dir = os.path.join(temp_dir, 'parakeet_requests')
        self.response_dir = os.path.join(temp_dir, 'parakeet_responses')
        
        os.makedirs(self.request_dir, exist_ok=True)
        os.makedirs(self.response_dir, exist_ok=True)
    
    def process_requests(self):
        """Main request processing loop."""
        while self.running:
            try:
                # Check for new request files
                request_files = list(Path(self.request_dir).glob('*.json'))
                
                for request_file in request_files:
                    try:
                        # Add a small delay to ensure file is fully written
                        time.sleep(0.05)
                        
                        # Check if file still exists (may have been processed by another iteration)
                        if not os.path.exists(request_file):
                            continue
                        
                        # Read request with retry logic
                        request = None
                        for attempt in range(3):
                            try:
                                with open(request_file, 'r') as f:
                                    request = json.load(f)
                                break
                            except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
                                if attempt < 2:
                                    time.sleep(0.1)
                                    continue
                                else:
                                    print(f"Failed to read request file after 3 attempts: {e}")
                                    break
                        
                        if not request:
                            # Clean up unreadable file
                            try:
                                os.unlink(request_file)
                            except:
                                pass
                            continue
                        
                        audio_file = request.get('audio_file')
                        request_id = request.get('request_id')
                        
                        # Clean up request file immediately after reading
                        try:
                            os.unlink(request_file)
                        except:
                            pass
                        
                        if audio_file and request_id:
                            # Handle special ping test requests
                            if audio_file == 'test_ping':
                                response = {
                                    'request_id': request_id,
                                    'text': 'pong',
                                    'status': 'success'
                                }
                            else:
                                # Regular transcription
                                transcription = self.transcribe_audio_file(audio_file)
                                response = {
                                    'request_id': request_id,
                                    'text': transcription,
                                    'status': 'success'
                                }
                            
                            # Write response
                            response_file = os.path.join(self.response_dir, f'{request_id}.json')
                            with open(response_file, 'w') as f:
                                json.dump(response, f)
                        
                    except Exception as e:
                        # Write error response if possible
                        try:
                            if 'request_id' in locals() and request_id:
                                response = {
                                    'request_id': request_id,
                                    'text': '',
                                    'status': 'error',
                                    'error': str(e)
                                }
                                response_file = os.path.join(self.response_dir, f'{request_id}.json')
                                with open(response_file, 'w') as f:
                                    json.dump(response, f)
                        except:
                            pass
                
                # Short sleep to avoid busy waiting
                time.sleep(0.1)
                
            except Exception as e:
                time.sleep(1)  # Longer sleep on errors
    
    def start_server(self):
        """Start the persistent server."""
        print("Loading Parakeet model...")
        if not self.load_model():
            print("Failed to load model")
            return False
        
        print("Model loaded successfully!")
        
        self.setup_communication_dirs()
        self.running = True
        
        # Set up signal handler for graceful shutdown
        def signal_handler(sig, frame):
            print("Shutting down server...")
            self.running = False
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        print(f"Server ready. Request dir: {self.request_dir}")
        print("Server running. Press Ctrl+C to stop.")
        
        # Process requests
        self.process_requests()
        
        return True

def main():
    """Main function."""
    server = ParakeetServer()
    server.start_server()

if __name__ == "__main__":
    main() 