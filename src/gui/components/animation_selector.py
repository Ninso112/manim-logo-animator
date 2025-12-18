"""Animation type selector component."""

from typing import Dict
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from ...utils.constants import ANIMATION_TYPES


class AnimationSelector(QWidget):
    """Widget for selecting animation type."""
    
    def __init__(self) -> None:
        """Initialize the animation selector widget."""
        super().__init__()
        self.combo_box: QComboBox
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        """Setup the UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        title = QLabel("Logo Animation Type")
        title.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addWidget(title)
        
        self.combo_box = QComboBox()
        self.combo_box.addItems(list(ANIMATION_TYPES.keys()))
        layout.addWidget(self.combo_box)
        
    def get_animation_type(self) -> str:
        """
        Get the selected animation type.
        
        Returns:
            str: The animation type identifier (e.g., "fade_in").
        """
        current_text = self.combo_box.currentText()
        return ANIMATION_TYPES.get(current_text, "fade_in")

