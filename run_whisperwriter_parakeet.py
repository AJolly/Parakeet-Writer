#!/usr/bin/env python3
"""
WhisperWriter with Parakeet ASR - Main Runner Script
====================================================

This script runs the WhisperWriter application using NVIDIA's Parakeet-TDT-0.6B 
model instead of OpenAI's Whisper for speech-to-text transcription.

Features:
- Real-time speech transcription using NVIDIA Parakeet
- Live typing simulation
- Multiple recording modes
- System tray integration
- Customizable hotkeys and settings
- Fast transcription via persistent model server

Usage:
    python run_whisperwriter_parakeet.py

Requirements:
- The parakeet_env virtual environment must be activated
- PyQt5, NeMo, and other dependencies must be installed
"""

import os
import sys
import subprocess
import time
import tempfile
import atexit
import signal
import uuid
import json

def is_server_running():
    """Check if the Parakeet server is actually running and responsive."""
    try:
        temp_dir = tempfile.gettempdir()
        request_dir = os.path.join(temp_dir, 'parakeet_requests')
        response_dir = os.path.join(temp_dir, 'parakeet_responses')
        
        # Check if directories exist
        if not (os.path.exists(request_dir) and os.path.exists(response_dir)):
            return False
        
        # Test if server is responsive by sending a test request
        test_id = str(uuid.uuid4())
        test_request = {
            'request_id': test_id,
            'audio_file': 'test_ping'  # Special test request
        }
        
        # Write test request
        test_request_file = os.path.join(request_dir, f'{test_id}.json')
        with open(test_request_file, 'w') as f:
            json.dump(test_request, f)
        
        # Wait for response (short timeout)
        test_response_file = os.path.join(response_dir, f'{test_id}.json')
        start_time = time.time()
        
        while time.time() - start_time < 3:  # 3 second timeout for ping
            if os.path.exists(test_response_file):
                try:
                    os.unlink(test_response_file)  # Clean up
                except:
                    pass
                return True
            time.sleep(0.1)
        
        # Clean up test request if no response
        try:
            os.unlink(test_request_file)
        except:
            pass
            
        return False
        
    except Exception as e:
        return False

def start_parakeet_server(src_dir):
    """Start the Parakeet server in the background."""
    server_script = os.path.join(src_dir, 'parakeet_server.py')
    if not os.path.exists(server_script):
        print("Warning: parakeet_server.py not found. Transcription will use slower subprocess method.")
        return None
    
    print("🚀 Starting Parakeet model server...")
    try:
        # Start server in background
        server_process = subprocess.Popen(
            [sys.executable, server_script],
            cwd=src_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
        )
        
        # Wait for server to be ready (check for up to 30 seconds)
        for i in range(30):
            if is_server_running():
                print("✅ Parakeet server ready!")
                return server_process
            time.sleep(1)
            if i % 5 == 0:
                print(f"   Waiting for server... ({i+1}/30)")
        
        print("⚠️  Server startup timeout. Will use slower subprocess method.")
        try:
            server_process.terminate()
        except:
            pass
        return None
        
    except Exception as e:
        print(f"⚠️  Failed to start server: {e}. Will use slower subprocess method.")
        return None

def cleanup_server(server_process):
    """Clean up the server process and communication directories."""
    if server_process:
        try:
            if sys.platform == 'win32':
                server_process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                server_process.terminate()
            
            # Wait a bit for graceful shutdown
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()
                
        except Exception as e:
            print(f"Warning: Error stopping server: {e}")
    
    # Clean up communication directories to prevent stale detection
    try:
        import shutil
        temp_dir = tempfile.gettempdir()
        request_dir = os.path.join(temp_dir, 'parakeet_requests')
        response_dir = os.path.join(temp_dir, 'parakeet_responses')
        
        for directory in [request_dir, response_dir]:
            if os.path.exists(directory):
                shutil.rmtree(directory, ignore_errors=True)
                
    except Exception as e:
        print(f"Warning: Error cleaning up directories: {e}")

def main():
    print("🦜 Starting WhisperWriter with Parakeet ASR...")
    print("Note: First run may take longer due to model loading.")
    print()
    
    # Change to the whisper-writer-parakeet directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(script_dir, 'whisper-writer-parakeet')
    
    if not os.path.exists(src_dir):
        print(f"Error: Directory '{src_dir}' not found!")
        print("Please ensure you're running this script from the correct directory.")
        return 1
    
    # Change to the source directory
    os.chdir(src_dir)
    
    server_process = None
    
    try:
        # Check if server is already running
        if is_server_running():
            print("✅ Parakeet server already running!")
        else:
            # Start the Parakeet server
            server_process = start_parakeet_server(src_dir)
        
        # Register cleanup function
        if server_process:
            atexit.register(cleanup_server, server_process)
        
        print("🎯 Starting WhisperWriter application...")
        print()
        
        # Run the main application
        subprocess.run([sys.executable, 'main.py'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error running the application: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        return 0
    finally:
        # Clean up server if we started it
        if server_process:
            print("🛑 Stopping Parakeet server...")
            cleanup_server(server_process)
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 