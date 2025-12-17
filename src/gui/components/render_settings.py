"""Render settings component."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QGroupBox
)


class RenderSettings(QWidget):
    """Widget for render settings (aspect ratio, FPS, quality)."""
    
    ASPECT_RATIOS = {
        "1:1": (1, 1),
        "16:9": (16, 9),
        "500x500": (500, 500),
        "1920x1080": (1920, 1080)
    }
    
    FPS_OPTIONS = [30, 60, 90, 144]
    
    QUALITY_PRESETS = {
        "Low (480p)": {"width": 854, "height": 480},
        "Medium (720p)": {"width": 1280, "height": 720},
        "High (1080p)": {"width": 1920, "height": 1080},
        "Ultra (4K)": {"width": 3840, "height": 2160}
    }
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
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
        self.aspect_combo.addItems(list(self.ASPECT_RATIOS.keys()))
        aspect_layout.addWidget(self.aspect_combo)
        aspect_layout.addStretch()
        layout.addLayout(aspect_layout)
        
        # FPS
        fps_layout = QHBoxLayout()
        fps_label = QLabel("FPS:")
        fps_layout.addWidget(fps_label)
        
        self.fps_combo = QComboBox()
        self.fps_combo.addItems([str(fps) for fps in self.FPS_OPTIONS])
        self.fps_combo.setCurrentText("60")
        fps_layout.addWidget(self.fps_combo)
        fps_layout.addStretch()
        layout.addLayout(fps_layout)
        
        # Quality
        quality_layout = QHBoxLayout()
        quality_label = QLabel("Quality:")
        quality_layout.addWidget(quality_label)
        
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(list(self.QUALITY_PRESETS.keys()))
        self.quality_combo.setCurrentText("High (1080p)")
        quality_layout.addWidget(self.quality_combo)
        quality_layout.addStretch()
        layout.addLayout(quality_layout)
        
    def get_settings(self):
        """Get current render settings."""
        aspect_key = self.aspect_combo.currentText()
        aspect_ratio = self.ASPECT_RATIOS.get(aspect_key, (16, 9))
        
        fps = int(self.fps_combo.currentText())
        
        quality_key = self.quality_combo.currentText()
        quality = self.QUALITY_PRESETS.get(quality_key, {"width": 1920, "height": 1080})
        
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
            "quality": quality_key
        }

