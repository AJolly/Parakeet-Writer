# Contributing to Parakeet-Writer

Thank you for your interest in contributing to Parakeet-Writer! This project welcomes contributions from the community.

## 🤝 How to Contribute

### Reporting Issues
- Use the [Issues](https://github.com/WarneDoc/Parakeet-Writer/issues) tab to report bugs or request features
- Search existing issues first to avoid duplicates
- Provide detailed information including:
  - Operating system and version
  - Python version
  - Steps to reproduce the issue
  - Expected vs actual behavior

### Contributing Code

1. **Fork the Repository**
   - Click the "Fork" button on GitHub
   - Clone your fork locally: `git clone https://github.com/YOUR_USERNAME/Parakeet-Writer.git`

2. **Set Up Development Environment**
   ```bash
   cd Parakeet-Writer
   python -m venv venv_parakeet
   venv_parakeet\Scripts\activate  # Windows
   pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
   pip install nemo-toolkit[asr] PyQt5 pynput audioplayer sounddevice scipy omegaconf hydra-core
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**
   - Follow the existing code style
   - Test your changes thoroughly
   - Ensure compatibility with both desktop and web interfaces

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   - Go to GitHub and create a Pull Request
   - Provide a clear description of your changes

## 🛡️ Development Guidelines

### Safe Settings Only
- **CRITICAL**: Only modify safe settings to prevent crashes
- Safe: hotkeys, recording modes, audio devices, post-processing
- Unsafe: model paths, compute types, VAD filters, API settings

### Code Style
- Follow the existing code structure
- Maintain compatibility with the original WhisperWriter architecture
- Add comments for complex logic
- Update documentation for new features

### Testing
- Test with both desktop application (`run_whisperwriter_parakeet.py`)
- Test with web interface (`run_gradio.py`)
- Verify on Windows 10/11 systems
- Test with different audio devices if possible

## 📝 Types of Contributions Welcome

### High Priority
- 🐛 **Bug fixes** - Especially crash issues or compatibility problems
- 📖 **Documentation improvements** - Better setup guides, troubleshooting
- 🎛️ **UI/UX enhancements** - Better user experience in desktop or web interface
- ⚡ **Performance optimizations** - Faster transcription, lower memory usage

### Medium Priority
- 🔧 **New features** - Additional recording modes, export options
- 🌐 **Platform support** - macOS, Linux compatibility
- 🎯 **Model improvements** - Support for additional Parakeet models
- 🔌 **Integrations** - Support for more applications or platforms

### Ideas for Contributions
- Better error handling and user feedback
- Improved audio preprocessing
- Configuration file management
- Unit tests and automated testing
- Performance benchmarking tools
- Installation scripts or packages

## 🚫 What NOT to Change

- Core NeMo/Parakeet model integration (unless you're an expert)
- Unsafe configuration options that cause crashes
- License files or attribution
- Core WhisperWriter architecture without discussion

## 💬 Communication

- **Issues**: Use for bug reports and feature requests
- **Discussions**: Use for questions and general discussion
- **Pull Requests**: Include detailed description of changes
- **Reviews**: Be respectful and constructive

## 📜 License

By contributing, you agree that your contributions will be licensed under the same GPL-3.0 license as the project.

## 🙏 Recognition

All contributors will be acknowledged in the project documentation. Significant contributors may be added to the credits section of the README.

---

**Need Help?** Don't hesitate to ask questions in Issues or Discussions! 