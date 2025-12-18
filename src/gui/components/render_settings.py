"""Render settings component."""

from typing import Dict, Any, Tuple
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QColorDialog
)
from PyQt6.QtGui import QColor
from utils.constants import (
    ASPECT_RATIOS, FPS_OPTIONS, QUALITY_PRESETS,
    DEFAULT_FPS, DEFAULT_QUALITY, DEFAULT_BACKGROUND_COLOR
)


class RenderSettings(QWidget):
    """Widget for render settings (aspect ratio, FPS, quality)."""
    
    def __init__(self) -> None:
        """Initialize the render settings widget."""
        super().__init__()
        self.aspect_combo: QComboBox
        self.fps_combo: QComboBox
        self.quality_combo: QComboBox
        self.background_color = QColor(DEFAULT_BACKGROUND_COLOR)
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        """Setup the UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        title = QLabel("Render Settings")
        title.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addWidget(title)
        
        # Aspect Ratio
        aspect_layout = QHBoxLayout()
        aspect_label = QLabel("Aspect Ratio:")
        aspect_layout.addWidget(aspect_label)
        
        self.aspect_combo = QComboBox()
        self.aspect_combo.addItems(list(ASPECT_RATIOS.keys()))
        aspect_layout.addWidget(self.aspect_combo)
        aspect_layout.addStretch()
        layout.addLayout(aspect_layout)
        
        # FPS
        fps_layout = QHBoxLayout()
        fps_label = QLabel("FPS:")
        fps_layout.addWidget(fps_label)
        
        self.fps_combo = QComboBox()
        self.fps_combo.addItems([str(fps) for fps in FPS_OPTIONS])
        self.fps_combo.setCurrentText(str(DEFAULT_FPS))
        fps_layout.addWidget(self.fps_combo)
        fps_layout.addStretch()
        layout.addLayout(fps_layout)
        
        # Quality
        quality_layout = QHBoxLayout()
        quality_label = QLabel("Quality:")
        quality_layout.addWidget(quality_label)
        
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(list(QUALITY_PRESETS.keys()))
        self.quality_combo.setCurrentText(DEFAULT_QUALITY)
        quality_layout.addWidget(self.quality_combo)
        quality_layout.addStretch()
        layout.addLayout(quality_layout)
        
        # Background Color
        bg_color_layout = QHBoxLayout()
        bg_color_label = QLabel("Background:")
        bg_color_layout.addWidget(bg_color_label)
        
        self.bg_color_btn = QPushButton("Color...")
        self.bg_color_btn.clicked.connect(self._select_background_color)
        self._update_bg_color_button()
        bg_color_layout.addWidget(self.bg_color_btn)
        bg_color_layout.addStretch()
        layout.addLayout(bg_color_layout)
        
    def get_settings(self) -> Dict[str, Any]:
        """
        Get current render settings.
        
        Returns:
            Dict containing aspect_ratio, width, height, fps, and quality.
        """
        aspect_key = self.aspect_combo.currentText()
        aspect_ratio = ASPECT_RATIOS.get(aspect_key, (16, 9))
        
        try:
            fps = int(self.fps_combo.currentText())
        except ValueError:
            fps = DEFAULT_FPS
        
        quality_key = self.quality_combo.currentText()
        quality = QUALITY_PRESETS.get(
            quality_key,
            QUALITY_PRESETS[DEFAULT_QUALITY]
        )
        
        # Determine final resolution
        if aspect_key in ["500x500", "1920x1080"]:
            width, height = aspect_ratio
        else:
            # Use quality preset but maintain aspect ratio
            width = quality["width"]
            height = quality["height"]
            if aspect_key == "1:1":
                height = width  # Square
            
        return {
            "aspect_ratio": aspect_ratio,
            "width": width,
            "height": height,
            "fps": fps,
            "quality": quality_key,
            "background_color": self.background_color.name()
        }
        
    def _select_background_color(self) -> None:
        """Open color dialog and update background color if valid."""
        color = QColorDialog.getColor(self.background_color, self, "Select Background Color")
        if color.isValid():
            self.background_color = color
            self._update_bg_color_button()
            
    def _update_bg_color_button(self) -> None:
        """Update the background color button appearance."""
        color_name = self.background_color.name()
        self.bg_color_btn.setText(f"Color... ({color_name})")
        self.bg_color_btn.setStyleSheet(
            f"QPushButton {{ background-color: {color_name}; color: {'white' if self.background_color.lightness() < 128 else 'black'}; }}"
        )

