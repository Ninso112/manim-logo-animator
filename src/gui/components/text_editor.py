"""Text editor component for upper and lower text."""

from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QFontDialog, QColorDialog, QComboBox
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt
from ...utils.constants import DEFAULT_FONT, DEFAULT_FONT_SIZE, DEFAULT_TEXT_COLOR, ANIMATION_TYPES


class TextEditor(QWidget):
    """Widget for editing text with font, color, and animation options."""
    
    def __init__(self, label_text: str = "Text") -> None:
        """
        Initialize the text editor widget.
        
        Args:
            label_text: Label text to display above the editor.
        """
        super().__init__()
        self.label_text = label_text
        self.font = QFont(DEFAULT_FONT, DEFAULT_FONT_SIZE)
        self.color = QColor(DEFAULT_TEXT_COLOR)
        self.text_edit: QTextEdit
        self.animation_combo: QComboBox
        self._setup_ui()
        
    def _setup_ui(self) -> None:
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
        
        # Animation selection
        animation_layout = QHBoxLayout()
        animation_label = QLabel("Animation:")
        animation_layout.addWidget(animation_label)
        
        self.animation_combo = QComboBox()
        self.animation_combo.addItem("None")  # No animation option
        self.animation_combo.addItems(list(ANIMATION_TYPES.keys()))
        animation_layout.addWidget(self.animation_combo)
        animation_layout.addStretch()
        layout.addLayout(animation_layout)
        
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
        
    def _select_font(self) -> None:
        """Open font dialog and update font if selected."""
        font, ok = QFontDialog.getFont(self.font, self)
        if ok:
            self.font = font
            self._update_text_formatting()
            
    def _select_color(self) -> None:
        """Open color dialog and update color if valid."""
        color = QColorDialog.getColor(self.color, self, "Select Text Color")
        if color.isValid():
            self.color = color
            self._update_text_formatting()
            
    def _update_text_formatting(self) -> None:
        """
        Update text formatting in the editor.
        
        Note: QTextEdit formatting is complex. For full formatting,
        we'd need to use QTextCharFormat. This is a placeholder
        for future enhancement.
        """
        # Placeholder for future formatting implementation
        pass
        
    def get_text(self) -> str:
        """
        Get the text content.
        
        Returns:
            str: The plain text content of the editor.
        """
        return self.text_edit.toPlainText()
        
    def get_font(self) -> QFont:
        """
        Get the selected font.
        
        Returns:
            QFont: The currently selected font.
        """
        return self.font
        
    def get_color(self) -> QColor:
        """
        Get the selected color.
        
        Returns:
            QColor: The currently selected color.
        """
        return self.color
        
    def get_animation_type(self) -> Optional[str]:
        """
        Get the selected animation type for the text.
        
        Returns:
            str: The animation type identifier, or None if "None" is selected.
        """
        current_text = self.animation_combo.currentText()
        if current_text == "None":
            return None
        return ANIMATION_TYPES.get(current_text)

