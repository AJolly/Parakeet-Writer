import io
import os
import numpy as np
import soundfile as sf
import tempfile
import subprocess
import json
import sys
from openai import OpenAI

from utils import ConfigManager

def transcribe_with_server(audio_data, sample_rate=16000):
    """
    Transcribe audio using the persistent server for fast transcription.
    """
    try:
        # Import the client here to avoid circular imports
        from parakeet_client import ParakeetClient
        
        # Create temporary audio file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Convert audio data to proper format if needed
            if isinstance(audio_data, np.ndarray):
                # Ensure audio is float32 and properly scaled
                if audio_data.dtype != np.float32:
                    audio_data = audio_data.astype(np.float32)
                
                # Normalize if needed
                if np.max(np.abs(audio_data)) > 1.0:
                    audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Save audio to temporary file
            sf.write(temp_path, audio_data, sample_rate)
            
            # Use client to communicate with server
            client = ParakeetClient()
            
            # Check if server is accessible
            if not client.is_server_running():
                ConfigManager.console_print('Parakeet server not accessible. Falling back to subprocess.')
                return transcribe_with_subprocess_fallback(audio_data, sample_rate)
            
            # Get transcription from server with longer timeout
            ConfigManager.console_print('DEBUG: Sending request to Parakeet server...')
            transcription = client.transcribe_audio_file(temp_path, timeout=30)
            ConfigManager.console_print(f'DEBUG: Server response: "{transcription}"')
            
            # Create result object with text attribute
            class TranscriptionResult:
                def __init__(self, text):
                    self.text = text
            
            return TranscriptionResult(transcription)
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        ConfigManager.console_print(f'Server transcription error: {str(e)}. Falling back to subprocess.')
        return transcribe_with_subprocess_fallback(audio_data, sample_rate)

def transcribe_with_subprocess_fallback(audio_data, sample_rate=16000):
    """
    Fallback transcription using subprocess (slower but more reliable).
    """
    try:
        # Create temporary audio file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Convert audio data to proper format if needed
            if isinstance(audio_data, np.ndarray):
                # Ensure audio is float32 and properly scaled
                if audio_data.dtype != np.float32:
                    audio_data = audio_data.astype(np.float32)
                
                # Normalize if needed
                if np.max(np.abs(audio_data)) > 1.0:
                    audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Save audio to temporary file
            sf.write(temp_path, audio_data, sample_rate)
            
            # Get the path to the parakeet transcriber
            script_dir = os.path.dirname(os.path.abspath(__file__))
            transcriber_path = os.path.join(script_dir, 'parakeet_transcriber.py')
            
            # Get the python executable from the current environment
            python_exe = sys.executable
            
            # Call the transcriber subprocess
            result = subprocess.run(
                [python_exe, transcriber_path, temp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,  # Suppress all stderr to avoid log interference
                text=True,
                timeout=60  # 60 second timeout
            )
            
            if result.returncode == 0:
                # Parse JSON output - strip any whitespace that might interfere
                stdout_clean = result.stdout.strip()
                if stdout_clean:
                    try:
                        response = json.loads(stdout_clean)
                        transcription = response.get('text', '')
                        
                        # Create result object with text attribute
                        class TranscriptionResult:
                            def __init__(self, text):
                                self.text = text
                        
                        return TranscriptionResult(transcription)
                    except json.JSONDecodeError as e:
                        ConfigManager.console_print(f'JSON decode error: {e}. Raw output: "{stdout_clean}"')
                        class ErrorResult:
                            def __init__(self):
                                self.text = ""
                        return ErrorResult()
                else:
                    ConfigManager.console_print('Empty output from transcriber')
                    class ErrorResult:
                        def __init__(self):
                            self.text = ""
                    return ErrorResult()
            else:
                ConfigManager.console_print(f'Transcriber subprocess returned code: {result.returncode}')
                class ErrorResult:
                    def __init__(self):
                        self.text = ""
                return ErrorResult()
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        ConfigManager.console_print(f'Subprocess transcription error: {str(e)}')
        class ErrorResult:
            def __init__(self):
                self.text = ""
        return ErrorResult()

def create_local_model():
    """
    Dummy function for compatibility - actual model loading happens in server.
    """
    ConfigManager.console_print('Parakeet model server should be started separately for best performance.')
    ConfigManager.console_print('Run: python whisper-writer-parakeet/parakeet_server.py')
    return True  # Return something truthy

def transcribe(model, audio_data, sample_rate=16000, language=None, task='transcribe', **kwargs):
    """
    Transcribe audio using the server approach (fast) with subprocess fallback.
    """
    return transcribe_with_server(audio_data, sample_rate)

def transcribe_openai(openai_model, audio_data, sample_rate=16000, language=None, task='transcribe'):
    """
    Transcribe audio using OpenAI API (fallback option).
    """
    try:
        client = OpenAI()
        
        # Create temporary audio file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_path = temp_file.name
            
        try:
            # Save audio to temporary file
            sf.write(temp_path, audio_data, sample_rate)
            
            # Transcribe using OpenAI
            with open(temp_path, 'rb') as audio_file:
                result = client.audio.transcriptions.create(
                    model=openai_model,
                    file=audio_file,
                    language=language
                )
            
            class OpenAIResult:
                def __init__(self, text):
                    self.text = text
            
            return OpenAIResult(result.text)
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        ConfigManager.console_print(f'OpenAI transcription error: {str(e)}')
        class ErrorResult:
            def __init__(self):
                self.text = ""
        return ErrorResult()

def post_process_transcription(transcription):
    """
    Apply post-processing to the transcription.
    """
    transcription = transcription.strip()
    post_processing = ConfigManager.get_config_section('post_processing')
    if post_processing['remove_trailing_period'] and transcription.endswith('.'):
        transcription = transcription[:-1]
    if post_processing['add_trailing_space']:
        transcription += ' '
    if post_processing['remove_capitalization']:
        transcription = transcription.lower()

    return transcription

def transcribe_audio(audio_data, local_model=None):
    """
    Transcribe audio data using the OpenAI API or a local Parakeet model, depending on config.
    """
    if audio_data is None:
        return ''

    if ConfigManager.get_config_value('model_options', 'use_api'):
        transcription = transcribe_openai(ConfigManager.get_config_section('model_options')['api']['model'], audio_data)
    else:
        transcription = transcribe(None, audio_data)

    return post_process_transcription(transcription.text) 