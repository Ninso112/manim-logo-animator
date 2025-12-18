"""Preview widget for animation preview."""

from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from pathlib import Path
from utils.constants import PREVIEW_MIN_WIDTH, PREVIEW_MIN_HEIGHT


class PreviewWidget(QWidget):
    """Widget for displaying animation preview."""
    
    def __init__(self) -> None:
        """Initialize the preview widget."""
        super().__init__()
        self.video_path: Optional[str] = None
        self.media_player: Optional[QMediaPlayer] = None
        self.video_widget: Optional[QVideoWidget] = None
        self.preview_label: Optional[QLabel] = None
        self.use_video_widget = False
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        """Setup the UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        title = QLabel("Preview")
        title.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addWidget(title)
        
        # Preview area - try to use QVideoWidget, fallback to QLabel
        try:
            self.video_widget = QVideoWidget()
            self.video_widget.setMinimumSize(PREVIEW_MIN_WIDTH, PREVIEW_MIN_HEIGHT)
            layout.addWidget(self.video_widget)
            
            # Setup media player
            self.audio_output = QAudioOutput()
            self.media_player = QMediaPlayer()
            self.media_player.setAudioOutput(self.audio_output)
            self.media_player.setVideoOutput(self.video_widget)
            
            self.use_video_widget = True
        except Exception:
            # Fallback to label if video widget not available
            self.preview_label = QLabel()
            self.preview_label.setMinimumSize(PREVIEW_MIN_WIDTH, PREVIEW_MIN_HEIGHT)
            self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.preview_label.setStyleSheet(
                "background-color: #1e1e1e; border: 1px solid #555;"
            )
            self.preview_label.setText("Preview will appear here")
            layout.addWidget(self.preview_label)
            self.use_video_widget = False
        
        # Controls
        controls_layout = QHBoxLayout()
        controls_layout.addStretch()
        
        self.play_btn = QPushButton("Play")
        self.play_btn.setEnabled(False)
        self.play_btn.clicked.connect(self._play)
        controls_layout.addWidget(self.play_btn)
        
        self.pause_btn = QPushButton("Pause")
        self.pause_btn.setEnabled(False)
        self.pause_btn.clicked.connect(self._pause)
        controls_layout.addWidget(self.pause_btn)
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self._stop)
        controls_layout.addWidget(self.stop_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
    def set_preview(self, video_path: str) -> None:
        """
        Set the preview video.
        
        Args:
            video_path: Path to the video file to preview.
        """
        self.video_path = video_path
        
        if not Path(video_path).exists():
            if not self.use_video_widget and self.preview_label:
                self.preview_label.setText(f"Video file not found: {video_path}")
            return
            
        if self.use_video_widget and self.media_player:
            url = QUrl.fromLocalFile(video_path)
            self.media_player.setSource(url)
            self.play_btn.setEnabled(True)
            self.pause_btn.setEnabled(True)
            self.stop_btn.setEnabled(True)
        else:
            self.preview_label.setText(f"Preview ready: {Path(video_path).name}")
            self.play_btn.setEnabled(True)
            self.pause_btn.setEnabled(True)
            self.stop_btn.setEnabled(True)
        
    def clear_preview(self) -> None:
        """Clear the preview."""
        if self.media_player:
            self.media_player.stop()
            
        if self.use_video_widget and self.video_widget:
            self.video_widget.clear()
        elif self.preview_label:
            self.preview_label.setText("Preview will appear here")
            
        self.play_btn.setEnabled(False)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.video_path = None
        
    def _play(self) -> None:
        """Play the video."""
        if self.media_player:
            self.media_player.play()
            
    def _pause(self) -> None:
        """Pause the video."""
        if self.media_player:
            self.media_player.pause()
            
    def _stop(self) -> None:
        """Stop the video."""
        if self.media_player:
            self.media_player.stop()

