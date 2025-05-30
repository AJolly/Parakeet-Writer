PARAKEET-WRITER
===============

A modification of WhisperWriter that uses NVIDIA NeMo's Parakeet ASR models instead of OpenAI Whisper for speech-to-text transcription.

OVERVIEW
--------
Parakeet-Writer is a desktop speech-to-text application built upon the excellent WhisperWriter project by savbell. This modified version replaces the Whisper speech recognition engine with NVIDIA's state-of-the-art Parakeet ASR models from the NeMo framework, providing enhanced transcription accuracy and performance.

The application maintains the core functionality of the original WhisperWriter - real-time speech transcription with customizable hotkeys and recording modes - while leveraging the advanced capabilities of NVIDIA's Parakeet models.

WHAT'S NEW IN PARAKEET-WRITER
-----------------------------
• Replaced OpenAI Whisper with NVIDIA NeMo Parakeet ASR models
• Added support for Parakeet-TDT-0.6B model (state-of-the-art accuracy)
• Included both desktop application and web interface options
• Created separate virtual environment setup for NeMo dependencies
• Added Gradio web interface for browser-based transcription
• Implemented client-server architecture for flexible deployment
• Enhanced audio processing with NeMo's optimized pipelines

KEY FEATURES
------------
• Real-time speech-to-text transcription using Parakeet models
• Multiple recording modes (continuous, voice activity detection, push-to-talk)
• Customizable keyboard shortcuts
• Desktop GUI application (PyQt5-based)
• Web interface option (Gradio-based)
• High accuracy transcription with punctuation and capitalization
• Automatic text insertion into active applications
• Configurable audio settings and post-processing options

IMPORTANT LIMITATIONS & SETTINGS COMPATIBILITY
----------------------------------------------
⚠️ CRITICAL: Many settings from the original WhisperWriter will cause crashes if used with Parakeet-Writer.

UNSAFE SETTINGS (will cause crashes):
• Model selection/paths (use only Parakeet models)
• Compute type settings (int8/float16/float32)
• Device selection (handled automatically by NeMo)
• VAD filter settings
• Condition on previous text
• API-related settings (base_url, api_key)

SAFE SETTINGS (can be modified):
• Hotkey combinations (activation_key)
• Recording modes
• Audio device selection (sound_device)
• Post-processing options (remove_trailing_period, add_trailing_space)
• Recording duration and silence thresholds
• Writing key press delay
• Status window visibility

SYSTEM REQUIREMENTS
-------------------
• Windows 11 (tested) or Windows 10
• Python 3.8 or higher
• NVIDIA GPU recommended (CPU support available but slower)
• At least 4GB RAM (8GB+ recommended)
• 5GB+ free disk space for models and dependencies
• Microphone/audio input device

INSTALLATION GUIDE FOR WINDOWS 11
---------------------------------

1. INSTALL PYTHON
   Download and install Python 3.8+ from python.org
   Ensure "Add Python to PATH" is checked during installation

2. CLONE OR DOWNLOAD THE PROJECT
   Download the Parakeet-Writer folder to your desired location

3. CREATE VIRTUAL ENVIRONMENT
   Open Command Prompt or PowerShell in the Parakeet-Writer directory:
   
   python -m venv venv_parakeet
   venv_parakeet\Scripts\activate

4. INSTALL PYTORCH (GPU VERSION RECOMMENDED)
   For NVIDIA GPU:
   pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
   
   For CPU only:
   pip install torch torchaudio

5. INSTALL CORE DEPENDENCIES
   pip install omegaconf hydra-core

6. INSTALL NEMO TOOLKIT
   pip install nemo-toolkit[asr]

7. INSTALL WHISPERWRITER DEPENDENCIES
   pip install PyQt5 pynput audioplayer sounddevice scipy

8. VERIFY INSTALLATION
   python -c "import nemo; print('NeMo installed successfully')"

RUNNING PARAKEET-WRITER
-----------------------

Option 1: Desktop Application
   1. Activate virtual environment: venv_parakeet\Scripts\activate
   2. Run: python run_whisperwriter_parakeet.py
   3. Configure settings (use safe settings only!)
   4. Press "Start" to begin listening
   5. Use your configured hotkey to start/stop transcription

Option 2: Web Interface
   1. Activate virtual environment: venv_parakeet\Scripts\activate
   2. Run: python run_gradio.py
   3. Open browser to http://localhost:7860
   4. Upload audio or use microphone for transcription

USAGE TIPS
----------
• First run will download the Parakeet model (may take several minutes)
• Start with default settings and modify only safe settings
• Use continuous recording mode for best experience
• Ensure microphone permissions are granted to Python
• For best accuracy, speak clearly with minimal background noise
• Test with the web interface first to verify setup

TROUBLESHOOTING
--------------
• If model download fails, check internet connection and try again
• For GPU issues, ensure NVIDIA drivers are up to date
• If transcription is slow, consider using CPU mode or smaller model
• For permission errors, run as administrator
• Check that no other applications are blocking microphone access

TECHNICAL ARCHITECTURE
----------------------
The project consists of several key components:

• transcription_parakeet.py: Core NeMo integration and audio processing
• run_whisperwriter_parakeet.py: Main desktop application launcher
• parakeet_web.py: Gradio web interface implementation
• parakeet_server.py / parakeet_client.py: Client-server architecture
• config_parakeet.yaml: Safe default configuration settings

FILE STRUCTURE
--------------
Parakeet-Writer/
├── run_whisperwriter_parakeet.py    # Main desktop app
├── run_gradio.py                    # Web interface launcher
├── parakeet_web.py                  # Gradio interface
├── transcription_parakeet.py        # Core transcription logic
├── whisper-writer-parakeet/         # Modified WhisperWriter source
├── config_parakeet.yaml             # Safe configuration
├── LICENSES.txt                     # Open source licenses
└── README.txt                       # This file

PERFORMANCE NOTES
----------------
• First transcription may be slower due to model initialization
• GPU acceleration provides significant speed improvements
• Model caching improves subsequent performance
• Audio preprocessing can affect transcription quality
• Network connectivity required for initial model download

CREDITS
-------
This project builds upon the excellent work of many contributors:

• Original WhisperWriter Project: https://github.com/savbell/whisper-writer
  Created by savbell and contributors (dariox1337, GrahamboJangles, McEsgow, 
  KernAlan, josher19, uberkael, Martinligabue, and others)

• NVIDIA NeMo Framework: https://github.com/NVIDIA/NeMo
  Advanced ASR capabilities and Parakeet model implementation

• Development Assistance:
  - Cursor AI: Code editor and development environment
  - Anthropic's Claude 4 Sonnet: AI assistance for code modification and integration

• Core Dependencies:
  - PyQt5: Desktop GUI framework
  - Gradio: Web interface framework
  - PyTorch: Machine learning framework
  - NVIDIA NeMo: ASR model framework

LICENSING
---------
This project incorporates components under various open source licenses:

• Parakeet-Writer modifications: GNU General Public License v3.0 (GPL-3.0)
• Original WhisperWriter: GNU General Public License v3.0 (GPL-3.0)
• NVIDIA NeMo: Apache License 2.0
• PyQt5: GPL-3.0 or Commercial License
• Other dependencies: Various (see LICENSES.txt for complete details)

📄 **Main License**: [LICENSE](LICENSE) (GPL-3.0)  
📄 **Complete License Information**: [LICENSES.txt](LICENSES.txt)

For complete license information, see the LICENSES.txt file in this directory.
This ensures compliance with all open source license requirements.

When uploading to GitHub, the license information will be automatically
detected from the LICENSE file in the repository root.

SUPPORT & ISSUES
---------------
This is a community modification of WhisperWriter. For issues specific to:
• Parakeet integration: Create issues in your GitHub repository
• Original WhisperWriter features: See https://github.com/savbell/whisper-writer
• NeMo/Parakeet models: See https://github.com/NVIDIA/NeMo

CONTRIBUTING
-----------
Contributions are welcome! When contributing:
• Maintain compatibility with safe settings only
• Test thoroughly with both desktop and web interfaces
• Follow the coding style of the original WhisperWriter project
• Update documentation for any new features
• Ensure all changes maintain open source license compatibility

🤝 **How to Contribute:**
- 🐛 **Report bugs**: Use the [Issues](https://github.com/WarneDoc/Parakeet-Writer/issues) tab
- 💡 **Suggest features**: Submit feature requests via Issues
- 🔧 **Submit code**: Fork the repo and create pull requests
- 📖 **Improve docs**: Help make installation and usage clearer

📋 **See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines**

**Current Priority Areas:**
- Bug fixes and stability improvements
- Better documentation and setup guides
- UI/UX enhancements for desktop and web interfaces
- Performance optimizations
- Cross-platform compatibility (macOS, Linux)

VERSION INFORMATION
------------------
Parakeet-Writer Version: 1.0
Based on WhisperWriter: Latest (2024)
NeMo Framework: 2.3.1+
Parakeet Model: TDT-0.6B

Last Updated: January 2025 