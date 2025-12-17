"""SVG file selector component."""

from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
import os


class FileSelector(QWidget):
    """Widget for selecting SVG files."""
    
    def __init__(self) -> None:
        """Initialize the file selector widget."""
        super().__init__()
        self.file_path: str = ""
        self.path_edit: QLineEdit
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        title = QLabel("SVG File")
        title.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addWidget(title)
        
        # File path display and browse button
        file_layout = QHBoxLayout()
        
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setPlaceholderText("No file selected")
        file_layout.addWidget(self.path_edit)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        
        layout.addLayout(file_layout)
        
    def browse_file(self) -> None:
        """Open file dialog to select SVG file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select SVG File",
            "",
            "SVG Files (*.svg);;All Files (*)"
        )
        
        if file_path:
            if self._validate_svg(file_path):
                self.file_path = file_path
                self.path_edit.setText(file_path)
            else:
                QMessageBox.warning(
                    self,
                    "Invalid File",
                    "The selected file does not appear to be a valid SVG file."
                )
                
    def _validate_svg(self, file_path: str) -> bool:
        """
        Validate that the file is an SVG file.
        
        Args:
            file_path: Path to the file to validate.
            
        Returns:
            bool: True if file is a valid SVG, False otherwise.
        """
        if not file_path or not os.path.exists(file_path):
            return False
            
        # Check file extension
        if not file_path.lower().endswith('.svg'):
            return False
            
        # Check file content (basic check)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(1000)  # Read first 1000 chars
                return 'svg' in content.lower() or '<svg' in content
        except (IOError, OSError, UnicodeDecodeError):
            return False
        except Exception:
            return False
        
    def get_file_path(self) -> str:
        """
        Get the selected file path.
        
        Returns:
            str: The selected file path, or empty string if none selected.
        """
        return self.file_path

