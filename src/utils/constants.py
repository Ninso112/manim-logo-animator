"""Application constants."""

from typing import Dict, Tuple

# Application metadata
APP_NAME = "Manim Logo Animator"
APP_VERSION = "1.0.0"

# Animation types mapping
ANIMATION_TYPES: Dict[str, str] = {
    "Fade In": "fade_in",
    "Fade Out": "fade_out",
    "Scale Up": "scale_up",
    "Scale Down": "scale_down",
    "Rotate": "rotate",
    "Draw": "draw",
    "Write": "write",
    "Grow From Center": "grow_from_center",
    "Grow From Edge": "grow_from_edge",
    "Shrink To Center": "shrink_to_center",
    "Wiggle": "wiggle",
    "Flash": "flash",
    "Circumscribe": "circumscribe",
    "Indicate": "indicate",
    "Spin": "spin",
    "Bounce In": "bounce_in",
    "Fade In From Edge": "fade_in_from_edge"
}

# Manim animation mappings
# Note: Some animations require specific parameters or work differently
# Using only animations that are confirmed to exist in Manim Community Edition
MANIM_ANIMATION_MAPPINGS: Dict[str, str] = {
    "fade_in": "FadeIn",
    "fade_out": "FadeOut",
    "scale_up": "GrowFromCenter",
    "scale_down": "ShrinkToCenter",
    "rotate": "Rotate",
    "draw": "DrawBorderThenFill",
    "write": "Write",
    "grow_from_center": "GrowFromCenter",
    "grow_from_edge": "GrowFromPoint",  # Using GrowFromPoint instead of GrowFromEdge
    "shrink_to_center": "ShrinkToCenter",
    "wiggle": "Wiggle",
    "flash": "Flash",
    "circumscribe": "Circumscribe",
    "indicate": "Indicate",
    "spin": "Rotate",  # Rotate with full rotation
    "bounce_in": "FadeIn",  # BounceIn doesn't exist, using FadeIn
    "fade_in_from_edge": "FadeIn"  # FadeInFromEdge doesn't exist, using FadeIn
}

# Aspect ratios
ASPECT_RATIOS: Dict[str, Tuple[int, int]] = {
    "1:1": (1, 1),
    "16:9": (16, 9),
    "500x500": (500, 500),
    "1920x1080": (1920, 1080)
}

# FPS options
FPS_OPTIONS = [30, 60, 90, 144]
DEFAULT_FPS = 60

# Quality presets
QUALITY_PRESETS: Dict[str, Dict[str, int]] = {
    "Low (480p)": {"width": 854, "height": 480},
    "Medium (720p)": {"width": 1280, "height": 720},
    "High (1080p)": {"width": 1920, "height": 1080},
    "Ultra (4K)": {"width": 3840, "height": 2160}
}

DEFAULT_QUALITY = "High (1080p)"

# Quality flags for Manim
QUALITY_FLAGS: Dict[str, str] = {
    "Low (480p)": "-ql",
    "Medium (720p)": "-qm",
    "High (1080p)": "-qh",
    "Ultra (4K)": "-qh"
}

# Quality names for Manim output directories
QUALITY_NAMES: Dict[str, str] = {
    "Low (480p)": "480p15",
    "Medium (720p)": "720p30",
    "High (1080p)": "1080p60",
    "Ultra (4K)": "2160p60"
}

# Default text settings
DEFAULT_FONT = "Arial"
DEFAULT_FONT_SIZE = 24
DEFAULT_TEXT_COLOR = "#FFFFFF"

# Window settings
MIN_WINDOW_WIDTH = 1200
MIN_WINDOW_HEIGHT = 800
SPLITTER_LEFT_SIZE = 400
SPLITTER_RIGHT_SIZE = 800

# Preview settings
PREVIEW_QUALITY = "Low (480p)"
PREVIEW_MIN_WIDTH = 640
PREVIEW_MIN_HEIGHT = 360

