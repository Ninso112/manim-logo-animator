"""Text editor component for upper and lower text."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QFontDialog, QColorDialog
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt


class TextEditor(QWidget):
    """Widget for editing text with font and color options."""
    
    def __init__(self, label_text="Text"):
        super().__init__()
        self.label_text = label_text
        self.font = QFont("Arial", 24)
        self.color = QColor(255, 255, 255)  # White
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        title = QLabel(self.label_text)
        title.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addWidget(title)
        
        # Text edit
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(f"Enter {self.label_text.lower()} here...")
        self.text_edit.setMaximumHeight(100)
        layout.addWidget(self.text_edit)
        
        # Font and color controls
        controls_layout = QHBoxLayout()
        
        font_btn = QPushButton("Font...")
        font_btn.clicked.connect(self._select_font)
        controls_layout.addWidget(font_btn)
        
        color_btn = QPushButton("Color...")
        color_btn.clicked.connect(self._select_color)
        controls_layout.addWidget(color_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
    def _select_font(self):
        """Open font dialog."""
        font, ok = QFontDialog.getFont(self.font, self)
        if ok:
            self.font = font
            self._update_text_formatting()
            
    def _select_color(self):
        """Open color dialog."""
        color = QColorDialog.getColor(self.color, self, "Select Text Color")
        if color.isValid():
            self.color = color
            self._update_text_formatting()
            
    def _update_text_formatting(self):
        """Update text formatting in the editor."""
        # Note: QTextEdit formatting is complex, this is a simplified approach
        # For full formatting, we'd need to use QTextCharFormat
        pass
        
    def get_text(self):
        """Get the text content."""
        return self.text_edit.toPlainText()
        
    def get_font(self):
        """Get the selected font."""
        return self.font
        
    def get_color(self):
        """Get the selected color."""
        return self.color

