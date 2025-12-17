"""Main window for Manim Logo Animator."""

from typing import Dict, Any
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMenuBar, QStatusBar, QMenu, QAction, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence
from pathlib import Path

from .components.file_selector import FileSelector
from .components.animation_selector import AnimationSelector
from .components.text_editor import TextEditor
from .components.render_settings import RenderSettings
from .components.preview_widget import PreviewWidget
from .dialogs.render_dialog import RenderDialog
from ..manim.renderer import ManimRenderer
from ..utils.constants import (
    APP_NAME, APP_VERSION, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT,
    SPLITTER_LEFT_SIZE, SPLITTER_RIGHT_SIZE, PREVIEW_QUALITY
)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        
        # Initialize renderer
        self.renderer = ManimRenderer()
        
        # Initialize components
        self.file_selector = FileSelector()
        self.animation_selector = AnimationSelector()
        self.upper_text_editor = TextEditor("Upper Text")
        self.lower_text_editor = TextEditor("Lower Text")
        self.render_settings = RenderSettings()
        self.preview_widget = PreviewWidget()
        
        self._setup_ui()
        self._setup_menu_bar()
        self._setup_status_bar()
        
    def _setup_ui(self):
        """Setup the main UI layout."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - Controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)
        
        left_layout.addWidget(self.file_selector)
        left_layout.addWidget(self.animation_selector)
        left_layout.addWidget(self.upper_text_editor)
        left_layout.addWidget(self.lower_text_editor)
        left_layout.addWidget(self.render_settings)
        left_layout.addStretch()
        
        # Right panel - Preview
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(self.preview_widget)
        
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setSizes([SPLITTER_LEFT_SIZE, SPLITTER_RIGHT_SIZE])
        
    def _setup_menu_bar(self):
        """Setup the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open SVG...", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self.file_selector.browse_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Render menu
        render_menu = menubar.addMenu("&Render")
        
        preview_action = QAction("&Preview", self)
        preview_action.setShortcut(QKeySequence("Ctrl+P"))
        preview_action.triggered.connect(self._preview_animation)
        render_menu.addAction(preview_action)
        
        render_action = QAction("&Render Video...", self)
        render_action.setShortcut(QKeySequence("Ctrl+R"))
        render_action.triggered.connect(self._render_video)
        render_menu.addAction(render_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
    def _setup_status_bar(self):
        """Setup the status bar."""
        self.statusBar().showMessage("Ready")
        
    def _preview_animation(self):
        """Preview the animation."""
        if not self.file_selector.get_file_path():
            QMessageBox.warning(self, "No File Selected", 
                              "Please select an SVG file first.")
            return
        
        try:
            self.statusBar().showMessage("Generating preview...")
            
            # Get configuration for preview (use low quality for faster preview)
            config = self.get_animation_config()
            preview_config = config.copy()
            preview_config["render_settings"] = config["render_settings"].copy()
            preview_config["render_settings"]["quality"] = PREVIEW_QUALITY
            
            # Render preview
            preview_path = self.renderer.render(
                preview_config,
                progress_callback=lambda msg: self.statusBar().showMessage(f"Preview: {msg}")
            )
            
            # Display preview
            if preview_path and Path(preview_path).exists():
                self.preview_widget.set_preview(str(preview_path))
                self.statusBar().showMessage("Preview ready")
            else:
                QMessageBox.warning(self, "Preview Failed", 
                                  "Could not generate preview. Please check the console for errors.")
                self.statusBar().showMessage("Preview failed")
                
        except Exception as e:
            QMessageBox.critical(self, "Preview Error", 
                               f"An error occurred while generating preview:\n{str(e)}")
            self.statusBar().showMessage("Preview error")
        
    def _render_video(self):
        """Render the video."""
        if not self.file_selector.get_file_path():
            QMessageBox.warning(self, "No File Selected", 
                              "Please select an SVG file first.")
            return
        
        # Ask for output location
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Video As",
            "",
            "MP4 Files (*.mp4);;All Files (*)"
        )
        
        if not output_path:
            return
            
        # Ensure .mp4 extension
        if not output_path.endswith('.mp4'):
            output_path += '.mp4'
        
        try:
            config = self.get_animation_config()
            
            # Show render dialog
            dialog = RenderDialog(self, self.renderer, config, Path(output_path))
            dialog.exec()
            
            if dialog.video_path:
                self.statusBar().showMessage(f"Video saved to: {dialog.video_path}")
                # Optionally set as preview
                self.preview_widget.set_preview(dialog.video_path)
            else:
                self.statusBar().showMessage("Render cancelled or failed")
                
        except Exception as e:
            QMessageBox.critical(self, "Render Error", 
                               f"An error occurred while rendering:\n{str(e)}")
            self.statusBar().showMessage("Render error")
        
    def _show_about(self) -> None:
        """Show about dialog."""
        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            f"{APP_NAME}\n\n"
            "A GUI application for animating SVG logos using Manim.\n\n"
            f"Version {APP_VERSION}"
        )
        
    def get_animation_config(self) -> Dict[str, Any]:
        """
        Get current animation configuration.
        
        Returns:
            Dict containing all animation configuration settings.
        """
        config = {
            "svg_path": self.file_selector.get_file_path(),
            "animation_type": self.animation_selector.get_animation_type(),
            "upper_text": self.upper_text_editor.get_text(),
            "lower_text": self.lower_text_editor.get_text(),
            "render_settings": self.render_settings.get_settings()
        }
        
        # Add font and color info if available
        upper_font = self.upper_text_editor.get_font()
        upper_color = self.upper_text_editor.get_color()
        config["upper_font"] = upper_font.family()
        config["upper_color"] = upper_color.name()
        
        lower_font = self.lower_text_editor.get_font()
        lower_color = self.lower_text_editor.get_color()
        config["lower_font"] = lower_font.family()
        config["lower_color"] = lower_color.name()
        
        return config

