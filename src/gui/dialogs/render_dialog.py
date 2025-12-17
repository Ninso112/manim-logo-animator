"""Render progress dialog."""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QProgressBar, QPushButton
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal as Signal


class RenderWorker(QThread):
    """Worker thread for rendering."""
    
    progress = Signal(str)
    finished = Signal(str)
    error = Signal(str)
    
    def __init__(self, renderer, config, output_path=None):
        super().__init__()
        self.renderer = renderer
        self.config = config
        self.output_path = output_path
        
    def run(self):
        """Execute rendering in thread."""
        try:
            def progress_callback(msg):
                self.progress.emit(msg)
                
            video_path = self.renderer.render(
                self.config,
                self.output_path,
                progress_callback
            )
            self.finished.emit(str(video_path))
        except Exception as e:
            self.error.emit(str(e))


class RenderDialog(QDialog):
    """Dialog showing render progress."""
    
    def __init__(self, parent, renderer, config, output_path=None):
        super().__init__(parent)
        self.renderer = renderer
        self.config = config
        self.output_path = output_path
        self.video_path = None
        
        self.setWindowTitle("Rendering...")
        self.setMinimumWidth(400)
        self.setModal(True)
        
        self._setup_ui()
        self._start_render()
        
    def _setup_ui(self):
        """Setup the UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        self.status_label = QLabel("Preparing render...")
        layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate
        layout.addWidget(self.progress_bar)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self._cancel_render)
        layout.addWidget(self.cancel_btn)
        
    def _start_render(self):
        """Start the rendering process."""
        self.worker = RenderWorker(self.renderer, self.config, self.output_path)
        self.worker.progress.connect(self._update_progress)
        self.worker.finished.connect(self._render_finished)
        self.worker.error.connect(self._render_error)
        self.worker.start()
        
    def _update_progress(self, message):
        """Update progress message."""
        self.status_label.setText(message)
        
    def _render_finished(self, video_path):
        """Handle render completion."""
        self.video_path = video_path
        self.status_label.setText(f"Render complete! Saved to: {video_path}")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        self.cancel_btn.setText("Close")
        self.cancel_btn.clicked.disconnect()
        self.cancel_btn.clicked.connect(self.accept)
        
    def _render_error(self, error_msg):
        """Handle render error."""
        self.status_label.setText(f"Error: {error_msg}")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.cancel_btn.setText("Close")
        self.cancel_btn.clicked.disconnect()
        self.cancel_btn.clicked.connect(self.reject)
        
    def _cancel_render(self):
        """Cancel rendering."""
        if self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        self.reject()
        
    def get_video_path(self):
        """Get the path to the rendered video."""
        return self.video_path

