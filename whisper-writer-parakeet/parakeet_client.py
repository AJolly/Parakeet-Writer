#!/usr/bin/env python3
"""
Parakeet model client for communicating with persistent server.
"""

import os
import json
import time
import tempfile
import uuid
from pathlib import Path

class ParakeetClient:
    def __init__(self):
        temp_dir = tempfile.gettempdir()
        self.request_dir = os.path.join(temp_dir, 'parakeet_requests')
        self.response_dir = os.path.join(temp_dir, 'parakeet_responses')
        
        # Ensure directories exist
        os.makedirs(self.request_dir, exist_ok=True)
        os.makedirs(self.response_dir, exist_ok=True)
    
    def transcribe_audio_file(self, audio_file_path, timeout=30):
        """
        Send transcription request to server and wait for response.
        """
        try:
            if not os.path.exists(audio_file_path):
                print(f"DEBUG: Audio file not found: {audio_file_path}")
                return ""
            
            # Generate unique request ID
            request_id = str(uuid.uuid4())
            print(f"DEBUG: Generated request ID: {request_id}")
            
            # Create request
            request = {
                'request_id': request_id,
                'audio_file': audio_file_path
            }
            
            # Write request file
            request_file = os.path.join(self.request_dir, f'{request_id}.json')
            with open(request_file, 'w') as f:
                json.dump(request, f)
            print(f"DEBUG: Wrote request file: {request_file}")
            
            # Wait for response
            response_file = os.path.join(self.response_dir, f'{request_id}.json')
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                if os.path.exists(response_file):
                    try:
                        with open(response_file, 'r') as f:
                            response = json.load(f)
                        
                        print(f"DEBUG: Received response: {response}")
                        
                        # Clean up response file
                        os.unlink(response_file)
                        
                        if response.get('status') == 'success':
                            return response.get('text', '')
                        else:
                            print(f"DEBUG: Server returned error status: {response}")
                            return ""
                            
                    except Exception as e:
                        print(f"DEBUG: Error reading response: {e}")
                        return ""
                
                time.sleep(0.1)  # Check every 100ms
            
            print(f"DEBUG: Timeout after {timeout} seconds")
            # Timeout - clean up request file if it still exists
            try:
                if os.path.exists(request_file):
                    os.unlink(request_file)
                    print("DEBUG: Cleaned up request file after timeout")
            except:
                pass
                
            return ""
            
        except Exception as e:
            print(f"DEBUG: Client error: {e}")
            return ""
    
    def is_server_running(self):
        """Check if the server is running by testing the communication directories."""
        try:
            # Test if we can write to request dir
            test_file = os.path.join(self.request_dir, 'test.tmp')
            with open(test_file, 'w') as f:
                f.write('test')
            os.unlink(test_file)
            return True
        except:
            return False

def main():
    """Test the client."""
    import sys
    if len(sys.argv) != 2:
        print("Usage: python parakeet_client.py <audio_file_path>")
        sys.exit(1)
    
    client = ParakeetClient()
    if not client.is_server_running():
        print("Error: Server communication directories not accessible")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    result = client.transcribe_audio_file(audio_file)
    
    # Output as JSON for compatibility
    response = {"text": result}
    print(json.dumps(response))

if __name__ == "__main__":
    main() 