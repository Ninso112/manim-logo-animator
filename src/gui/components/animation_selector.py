"""Animation type selector component."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox


class AnimationSelector(QWidget):
    """Widget for selecting animation type."""
    
    ANIMATION_TYPES = {
        "Fade In": "fade_in",
        "Scale Up": "scale_up",
        "Rotate": "rotate",
        "Draw": "draw"
    }
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        title = QLabel("Animation Type")
        title.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addWidget(title)
        
        self.combo_box = QComboBox()
        self.combo_box.addItems(list(self.ANIMATION_TYPES.keys()))
        layout.addWidget(self.combo_box)
        
    def get_animation_type(self):
        """Get the selected animation type."""
        current_text = self.combo_box.currentText()
        return self.ANIMATION_TYPES.get(current_text, "fade_in")

