# 🦜 WhisperWriter with Parakeet ASR - Complete Guide

## ✅ **Setup Complete!** 

Your environment is now configured and ready to use! Here's everything you need to know:

## 🚀 **How to Start the Application**

1. **Open PowerShell** in the `C:\Users\bw429\parakeet-asr` directory
2. **Activate the environment**: `.\parakeet_env\Scripts\Activate.ps1`
3. **Run the application**: `python run_whisperwriter_parakeet.py`

## ⚠️ **Critical Settings Information**

### 🚫 **AVOID These Settings (Will Cause Crashes):**

**In the GUI Settings, DO NOT touch these Whisper-specific options:**
- ❌ Model Path/Directory selection
- ❌ Model Size selection (tiny, base, small, medium, large)
- ❌ Compute Type settings (int8, float16, float32)
- ❌ Device selection for models (CPU/GPU) 
- ❌ VAD Filter settings
- ❌ "Condition on Previous Text" option
- ❌ Any "Local Model" configuration options

### ✅ **SAFE Settings You Can Use:**

**Recording & Audio Settings:**
- ✅ Recording Mode (continuous, voice activity detection, press-to-toggle, hold-to-record)
- ✅ Audio input device selection
- ✅ Sample rate (16000 Hz is recommended for Parakeet)
- ✅ Minimum recording duration
- ✅ Silence detection duration

**Hotkeys & Controls:**
- ✅ Recording hotkey combinations
- ✅ Activation key settings

**Post-Processing:**
- ✅ Remove trailing periods
- ✅ Add trailing spaces
- ✅ Remove capitalization
- ✅ Input method selection

**Misc Options:**
- ✅ Hide status window
- ✅ Completion sound
- ✅ Terminal output options

## 🎯 **How It Works**

1. **Model Loading**: On first run, Parakeet-TDT-0.6B will be downloaded (~600MB)
2. **Hotkey Activation**: Default is `Ctrl+Shift+Space` (configurable)
3. **Recording Modes**:
   - **Voice Activity Detection**: Automatically starts/stops based on speech
   - **Press to Toggle**: Press once to start, press again to stop
   - **Hold to Record**: Hold the hotkey while speaking
   - **Continuous**: Always listening (battery intensive)
4. **Real-time Typing**: Transcribed text appears as you speak

## 🎮 **Usage Examples**

### Basic Voice-to-Text:
1. Press `Ctrl+Shift+Space`
2. Speak clearly into your microphone
3. The text will appear where your cursor is

### Continuous Dictation:
1. Set recording mode to "Continuous"
2. Start the application
3. Speak naturally - it will keep transcribing

### Meeting Notes:
1. Use "Voice Activity Detection" mode
2. Position cursor in your note-taking app
3. Let it automatically detect when you're speaking

## 🔧 **Performance Tips**

- **First Run**: Model download may take several minutes
- **GPU Acceleration**: Automatically used if available (CUDA)
- **Audio Quality**: Use a good microphone for best results
- **Background Noise**: Voice Activity Detection helps filter noise

## 🆚 **Parakeet vs Whisper Differences**

| Feature | Parakeet | Original Whisper |
|---------|----------|------------------|
| **Model Size** | 600MB | 244MB - 1.55GB |
| **Speed** | Faster | Moderate |
| **Accuracy** | Excellent | Excellent |
| **Language Support** | English-focused | 100+ languages |
| **Offline** | ✅ Yes | ✅ Yes |
| **GPU Support** | ✅ CUDA | ✅ CUDA/OpenCL |

## 🐛 **Troubleshooting**

### Application Won't Start:
```bash
# Check if environment is activated
.\parakeet_env\Scripts\Activate.ps1

# Verify imports work
python -c "import nemo.collections.asr as asr; print('NeMo OK')"
```

### Model Loading Issues:
- Ensure you have internet connection for first download
- Check available disk space (need ~2GB free)
- Antivirus may block model download - add exception

### Audio Not Working:
- Check microphone permissions in Windows
- Test microphone in other applications
- Try different recording modes

### Settings Crash:
- **Never modify Whisper-specific settings**
- Use the safe configuration file provided
- Restart application if settings get corrupted

## 📁 **File Structure**

```
parakeet-asr/
├── parakeet_env/                    # Virtual environment (DO NOT MODIFY)
├── whisper-writer-parakeet/         # Application source code
│   ├── main.py                      # Main application entry
│   ├── transcription_parakeet.py    # Parakeet integration
│   ├── config.yaml                  # Safe configuration
│   └── ui/                          # User interface files
├── run_whisperwriter_parakeet.py    # Startup script
└── PARAKEET_WHISPERWRITER_GUIDE.md  # This guide
```

## 🔄 **Updates & Maintenance**

- **Model Updates**: Automatic via HuggingFace
- **Dependencies**: Handled by virtual environment
- **Configuration**: Backup `config.yaml` before major changes

## 🆘 **If Something Goes Wrong**

1. **Safe Mode**: Delete `config.yaml` to reset to defaults
2. **Clean Restart**: Close application, restart PowerShell, reactivate environment
3. **Nuclear Option**: Re-run the setup process from scratch

## 🎉 **Enjoy Your New Voice-to-Text Setup!**

You now have a powerful, offline speech-to-text system using cutting-edge AI technology. Happy dictating! 🎙️✨ 