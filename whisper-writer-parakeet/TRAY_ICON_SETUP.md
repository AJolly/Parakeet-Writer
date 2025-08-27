# Tray Icon Setup for WhisperWriter

## Overview
The tray icon functionality has been implemented with robust error handling, fallback options, and **state-based visual feedback**. The application now dynamically changes the tray icon and tooltip to indicate the current status.

## How It Works
1. **Primary Icon**: The app first tries to load `assets/ww-logo.png`
2. **Microphone Icon**: If no custom logo exists, it uses `assets/microphone-icon.svg` (custom microphone design)
3. **Fallback Icon**: If neither exists, it uses PyQt5's built-in `SP_ComputerIcon`
4. **Error Handling**: If icon creation fails, the app continues without a tray icon

## State-Based Visual Feedback
The tray icon now changes to indicate the current application state:

- **🖥️ Idle**: Default state - ready to record
- **🖥️ Recording**: Currently recording audio
- **🖥️ Processing**: Processing recorded audio
- **⚠️ Error**: An error has occurred

## Adding a Custom Icon
To use your own icon:

1. Place your icon file in the `assets/` directory
2. Name it `ww-logo.png` (PNG format recommended) for highest priority
3. Or use `microphone-icon.svg` for a custom microphone design
4. Recommended size: 32x32 pixels or 64x64 pixels
5. The icon should be square and have a transparent background for best results

## Tray Icon Features
- **Context Menu**: Right-click to access options
- **Double-Click**: Double-click to show the main window
- **Dynamic Tooltips**: Tooltip changes based on current state
- **State Indication**: Visual feedback for different app states
- **Menu Options**:
  - WhisperWriter Main Menu
  - Open Settings
  - Exit

## State Transitions
The tray icon automatically updates when:
- Starting recording (→ Recording state)
- Processing audio (→ Processing state)
- Completing transcription (→ Idle state)
- Stopping recording (→ Idle state)
- Errors occurring (→ Error state)

## Troubleshooting
If the tray icon doesn't appear:
1. Check the console output for error messages
2. Ensure the assets directory exists
3. Verify file permissions
4. The app will continue to function even without the tray icon

## Windows Compatibility
This implementation is optimized for Windows and will work reliably on all Windows systems that support system tray functionality.

## Custom Microphone Icon
A custom SVG microphone icon (`microphone-icon.svg`) is included that provides a more appropriate visual representation for a voice-to-text application than generic system icons.
