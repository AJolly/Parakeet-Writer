import os
import sys
import time
from audioplayer import AudioPlayer
from pynput.keyboard import Controller
from PyQt5.QtCore import QObject, QProcess
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox

from key_listener import KeyListener
from result_thread import ResultThread
from ui.main_window import MainWindow
from ui.settings_window import SettingsWindow
from ui.status_window import StatusWindow
from transcription_parakeet import create_local_model
from input_simulation import InputSimulator
from utils import ConfigManager


class WhisperWriterApp(QObject):
    def __init__(self):
        """
        Initialize the application, opening settings window if no configuration file is found.
        """
        super().__init__()
        self.app = QApplication(sys.argv)
        
        # Set application icon with fallback
        try:
            # Try to use a built-in microphone icon from PyQt5's standard icon set
            icon = QIcon.fromTheme('audio-input-microphone')
            
            # If theme icon is not available, use a fallback approach
            if icon.isNull():
                # Try to load from assets directory with proper path resolution
                assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
                logo_path = os.path.join(assets_path, 'ww-logo.png')
                
                if os.path.exists(logo_path):
                    icon = QIcon(logo_path)
                else:
                    # Use PyQt5's built-in microphone icon as final fallback
                    from PyQt5.QtWidgets import QStyle
                    icon = self.app.style().standardIcon(QStyle.SP_MediaVolume)
            
            self.app.setWindowIcon(icon)
        except Exception as e:
            print(f"Error setting application icon: {e}")
            # Continue without icon if there's an error

        ConfigManager.initialize()

        self.settings_window = SettingsWindow()
        self.settings_window.settings_closed.connect(self.on_settings_closed)
        self.settings_window.settings_saved.connect(self.restart_app)

        if ConfigManager.config_file_exists():
            self.initialize_components()
        else:
            print('No valid configuration file found. Opening settings window...')
            self.settings_window.show()

    def initialize_components(self):
        """
        Initialize the components of the application.
        """
        self.input_simulator = InputSimulator()

        self.key_listener = KeyListener()
        self.key_listener.add_callback("on_activate", self.on_activation)
        self.key_listener.add_callback("on_deactivate", self.on_deactivation)

        model_options = ConfigManager.get_config_section('model_options')
        model_path = model_options.get('local', {}).get('model_path')
        self.local_model = create_local_model() if not model_options.get('use_api') else None

        self.result_thread = None

        self.main_window = MainWindow()
        self.main_window.openSettings.connect(self.settings_window.show)
        self.main_window.startListening.connect(self.key_listener.start)
        self.main_window.closeApp.connect(self.exit_app)

        if not ConfigManager.get_config_value('misc', 'hide_status_window'):
            self.status_window = StatusWindow()

        self.create_tray_icon()
        self.main_window.show()

    def create_tray_icon(self):
        """
        Create the system tray icon and its context menu.
        """
        try:
            # Try to use a built-in microphone icon from PyQt5's standard icon set
            icon = QIcon.fromTheme('audio-input-microphone')
            
            # If theme icon is not available, use a fallback approach
            if icon.isNull():
                # Try to load from assets directory with proper path resolution
                assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
                logo_path = os.path.join(assets_path, 'ww-logo.png')
                
                if os.path.exists(logo_path):
                    icon = QIcon(logo_path)
                else:
                    # Use PyQt5's built-in microphone icon as final fallback
                    from PyQt5.QtWidgets import QStyle
                    icon = self.app.style().standardIcon(QStyle.SP_MediaVolume)
            
            # Create the tray icon
            self.tray_icon = QSystemTrayIcon(icon, self.app)
            
            # Set tooltip for better user experience
            self.tray_icon.setToolTip('WhisperWriter - Voice to Text')
            
            # Create context menu
            tray_menu = QMenu()

            show_action = QAction('WhisperWriter Main Menu', self.app)
            show_action.triggered.connect(self.main_window.show)
            tray_menu.addAction(show_action)

            settings_action = QAction('Open Settings', self.app)
            settings_action.triggered.connect(self.settings_window.show)
            tray_menu.addAction(settings_action)

            exit_action = QAction('Exit', self.app)
            exit_action.triggered.connect(self.exit_app)
            tray_menu.addAction(exit_action)

            self.tray_icon.setContextMenu(tray_menu)
            
            # Show the tray icon
            if self.tray_icon.isSystemTrayAvailable():
                self.tray_icon.show()
                # Connect double-click to show main window
                self.tray_icon.activated.connect(self.on_tray_icon_activated)
                print("System tray icon created successfully")
            else:
                print("Warning: System tray is not available on this system")
                self.tray_icon = None
                
        except Exception as e:
            print(f"Error creating tray icon: {e}")
            self.tray_icon = None

    def on_tray_icon_activated(self, reason):
        """
        Handle tray icon activation events.
        """
        if reason == QSystemTrayIcon.DoubleClick:
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()

    def cleanup(self):
        if self.key_listener:
            self.key_listener.stop()
        if self.input_simulator:
            self.input_simulator.cleanup()
        if hasattr(self, 'tray_icon') and self.tray_icon:
            self.tray_icon.hide()
            self.tray_icon = None

    def exit_app(self):
        """
        Exit the application.
        """
        self.cleanup()
        QApplication.quit()

    def restart_app(self):
        """Restart the application to apply the new settings."""
        self.cleanup()
        QApplication.quit()
        QProcess.startDetached(sys.executable, sys.argv)

    def on_settings_closed(self):
        """
        If settings is closed without saving on first run, initialize the components with default values.
        """
        if not os.path.exists(os.path.join('src', 'config.yaml')):
            QMessageBox.information(
                self.settings_window,
                'Using Default Values',
                'Settings closed without saving. Default values are being used.'
            )
            self.initialize_components()

    def on_activation(self):
        """
        Called when the activation key combination is pressed.
        """
        if self.result_thread and self.result_thread.isRunning():
            recording_mode = ConfigManager.get_config_value('recording_options', 'recording_mode')
            if recording_mode == 'press_to_toggle':
                self.result_thread.stop_recording()
            elif recording_mode == 'continuous':
                self.stop_result_thread()
            return

        self.start_result_thread()

    def on_deactivation(self):
        """
        Called when the activation key combination is released.
        """
        if ConfigManager.get_config_value('recording_options', 'recording_mode') == 'hold_to_record':
            if self.result_thread and self.result_thread.isRunning():
                self.result_thread.stop_recording()

    def start_result_thread(self):
        """
        Start the result thread to record audio and transcribe it.
        """
        if self.result_thread and self.result_thread.isRunning():
            return

        self.result_thread = ResultThread(self.local_model)
        if not ConfigManager.get_config_value('misc', 'hide_status_window'):
            self.result_thread.statusSignal.connect(self.status_window.updateStatus)
            self.status_window.closeSignal.connect(self.stop_result_thread)
        self.result_thread.resultSignal.connect(self.on_transcription_complete)
        self.result_thread.start()

    def stop_result_thread(self):
        """
        Stop the result thread.
        """
        if self.result_thread and self.result_thread.isRunning():
            self.result_thread.stop()

    def on_transcription_complete(self, result):
        """
        When the transcription is complete, type the result and start listening for the activation key again.
        """
#        ConfigManager.console_print(f'DEBUG: Received transcription result: "{result}" (length: {len(result)})')
        
        if result and result.strip():
            ConfigManager.console_print(f'DEBUG: Typing text: "{result}"')
            self.input_simulator.typewrite(result)
#        else:
#            ConfigManager.console_print('DEBUG: Empty or whitespace-only result, not typing anything')

        if ConfigManager.get_config_value('misc', 'noise_on_completion'):
            AudioPlayer(os.path.join('assets', 'beep.wav')).play(block=True)

        if ConfigManager.get_config_value('recording_options', 'recording_mode') == 'continuous':
            self.start_result_thread()
        else:
            self.key_listener.start()

    def run(self):
        """
        Start the application.
        """
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    app = WhisperWriterApp()
    app.run()
