"""Manim scene generator for creating animation scenes dynamically."""

import os
from pathlib import Path


class SceneGenerator:
    """Generates Manim scene code dynamically."""
    
    ANIMATION_MAPPINGS = {
        "fade_in": "FadeIn",
        "scale_up": "GrowFromCenter",
        "rotate": "Rotate",
        "draw": "DrawBorderThenFill"
    }
    
    def __init__(self):
        self.temp_scene_dir = Path(__file__).parent.parent.parent / "temp_scenes"
        self.temp_scene_dir.mkdir(exist_ok=True)
        
    def generate_scene_code(self, config):
        """
        Generate Manim scene code based on configuration.
        
        Args:
            config: Dictionary with keys:
                - svg_path: Path to SVG file
                - animation_type: Type of animation (fade_in, scale_up, etc.)
                - upper_text: Text to display above animation
                - lower_text: Text to display below animation
                - render_settings: Dictionary with width, height, fps
                
        Returns:
            str: Python code for the Manim scene
        """
        svg_path = config["svg_path"]
        animation_type = config["animation_type"]
        upper_text = config.get("upper_text", "")
        lower_text = config.get("lower_text", "")
        render_settings = config.get("render_settings", {})
        
        width = render_settings.get("width", 1920)
        height = render_settings.get("height", 1080)
        fps = render_settings.get("fps", 60)
        
        # Get animation class name
        anim_class = self.ANIMATION_MAPPINGS.get(animation_type, "FadeIn")
        
        # Use repr() to properly escape the SVG path for Python string literal
        # repr() handles all special characters correctly, including backslashes
        svg_path_repr = repr(svg_path)
        
        # Escape text for Python strings (for use in double-quoted strings)
        def escape_text(text):
            # Escape backslashes, quotes, and newlines for double-quoted strings
            return text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        
        # Generate scene code
        scene_code = f'''from manim import *
import os

config.frame_rate = {fps}

class LogoScreen(Scene):
    def construct(self):
        # Set resolution
        self.camera.frame_width = {width}
        self.camera.frame_height = {height}
        
        # Load SVG
        svg_path = {svg_path_repr}
        if not os.path.exists(svg_path):
            raise FileNotFoundError(f"SVG file not found: {{svg_path}}")
        
        try:
            logo = SVGMobject(svg_path)
            logo.scale_to_fit_height(3)  # Adjust size as needed
            logo.move_to(ORIGIN)
        except Exception as e:
            raise RuntimeError(f"Failed to load SVG: {{e}}")
        
        # Upper text
'''
        
        if upper_text:
            upper_font = config.get("upper_font", "Arial")
            upper_color = config.get("upper_color", "#FFFFFF")
            upper_text_escaped = escape_text(upper_text)
            scene_code += f'''        upper_text_obj = Text(
            "{upper_text_escaped}",
            font="{upper_font}",
            font_size=48,
            color="{upper_color}"
        )
        upper_text_obj.move_to(UP * 2.5)
        self.add(upper_text_obj)
        
'''
        
        scene_code += f'''        # Lower text
'''
        
        if lower_text:
            lower_font = config.get("lower_font", "Arial")
            lower_color = config.get("lower_color", "#FFFFFF")
            lower_text_escaped = escape_text(lower_text)
            scene_code += f'''        lower_text_obj = Text(
            "{lower_text_escaped}",
            font="{lower_font}",
            font_size=48,
            color="{lower_color}"
        )
        lower_text_obj.move_to(DOWN * 2.5)
        self.add(lower_text_obj)
        
'''
        
        scene_code += f'''        # Animate logo
        self.play({anim_class}(logo), run_time=2)
        self.wait(1)
'''
        
        return scene_code
        
    def save_scene_file(self, config, scene_name="logo_scene"):
        """
        Save generated scene code to a file.
        
        Args:
            config: Configuration dictionary
            scene_name: Name for the scene file (without .py extension)
            
        Returns:
            Path: Path to the saved scene file
        """
        scene_code = self.generate_scene_code(config)
        scene_file = self.temp_scene_dir / f"{scene_name}.py"
        
        with open(scene_file, 'w', encoding='utf-8') as f:
            f.write(scene_code)
            
        return scene_file
        
    def get_scene_class_name(self):
        """Get the scene class name used in generated code."""
        return "LogoScreen"

