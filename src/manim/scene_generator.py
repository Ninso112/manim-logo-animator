"""Manim scene generator for creating animation scenes dynamically."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from utils.constants import (
    MANIM_ANIMATION_MAPPINGS, DEFAULT_FONT, DEFAULT_TEXT_COLOR, DEFAULT_BACKGROUND_COLOR
)


class SceneGenerator:
    """Generates Manim scene code dynamically."""
    
    def __init__(self) -> None:
        """Initialize the scene generator."""
        self.temp_scene_dir = Path(__file__).parent.parent.parent / "temp_scenes"
        self.temp_scene_dir.mkdir(exist_ok=True)
        
    def generate_scene_code(self, config: Dict[str, Any]) -> str:
        """
        Generate Manim scene code based on configuration.
        
        Args:
            config: Dictionary with keys:
                - svg_path: Path to SVG file
                - animation_type: Type of animation (fade_in, scale_up, etc.)
                - upper_text: Text to display above animation
                - lower_text: Text to display below animation
                - render_settings: Dictionary with width, height, fps
                - upper_font: Font name for upper text (optional)
                - upper_color: Color for upper text (optional)
                - lower_font: Font name for lower text (optional)
                - lower_color: Color for lower text (optional)
                
        Returns:
            str: Python code for the Manim scene
            
        Raises:
            KeyError: If required config keys are missing.
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
        anim_class = MANIM_ANIMATION_MAPPINGS.get(animation_type, "FadeIn")
        
        # Use repr() to properly escape the SVG path for Python string literal
        # repr() handles all special characters correctly, including backslashes
        svg_path_repr = repr(svg_path)
        
        # Escape text for Python strings (for use in double-quoted strings)
        def escape_text(text):
            # Escape backslashes, quotes, and newlines for double-quoted strings
            return text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        
        # Get text animation types
        upper_animation = config.get("upper_animation")
        lower_animation = config.get("lower_animation")
        
        # Helper function to get animation code
        def get_animation_code(obj_name: str, anim_type: Optional[str], is_text: bool = False) -> str:
            """Generate animation code for an object."""
            # If no animation type specified, use FadeIn as default
            if not anim_type:
                return f"self.play(FadeIn({obj_name}), run_time=1)"
            
            anim_class = MANIM_ANIMATION_MAPPINGS.get(anim_type, "FadeIn")
            
            # Special handling for different animation types
            if anim_type == "rotate":
                if is_text:
                    return f"self.play({anim_class}({obj_name}, angle=PI), run_time=1.5)"
                else:
                    return f"self.play({anim_class}({obj_name}, angle=2*PI), run_time=2)"
            elif anim_type == "spin":
                # Full rotation
                return f"self.play({anim_class}({obj_name}, angle=2*PI), run_time=2)"
            elif anim_type == "write":
                # Write only works with Text objects
                if is_text:
                    return f"self.play({anim_class}({obj_name}), run_time=1.5)"
                else:
                    return f"self.play(FadeIn({obj_name}), run_time=1.5)"
            elif anim_type == "wiggle":
                return f"self.play({anim_class}({obj_name}), run_time=1)"
            elif anim_type == "flash":
                return f"self.play({anim_class}({obj_name}), run_time=0.5)"
            elif anim_type == "grow_from_edge":
                # Using GrowFromCenter (GrowFromPoint may not exist)
                return f"self.play({anim_class}({obj_name}), run_time=1.5)"
            elif anim_type == "fade_in_from_edge":
                # Using FadeIn as fallback
                return f"self.play({anim_class}({obj_name}), run_time=1.5)"
            elif anim_type == "bounce_in":
                # Using FadeIn as fallback
                return f"self.play({anim_class}({obj_name}), run_time=1.5)"
            else:
                return f"self.play({anim_class}({obj_name}), run_time=1.5)"
        
        # Get background color and ensure it's a valid hex string
        background_color = config.get("background_color", DEFAULT_BACKGROUND_COLOR)
        # Ensure it starts with # if it's a hex color
        if background_color and not background_color.startswith("#"):
            # Try to convert QColor name format to hex
            if len(background_color) == 6 and all(c in "0123456789ABCDEFabcdef" for c in background_color):
                background_color = "#" + background_color
            else:
                # Fallback to default
                background_color = DEFAULT_BACKGROUND_COLOR
        
        # Generate scene code
        # Note: Resolution is handled by Manim quality flags, not in scene code
        scene_code = f'''from manim import *
import os

config.frame_rate = {fps}
config.background_color = "{background_color}"

class LogoScreen(Scene):
    def construct(self):
        # Set background color (both config and camera for compatibility)
        self.camera.background_color = "{background_color}"
        
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
        
        # Create text objects first (but don't add them yet if they have animations)
        upper_text_obj_code = ""
        lower_text_obj_code = ""
        
        if upper_text:
            upper_font = config.get("upper_font", DEFAULT_FONT)
            upper_color = config.get("upper_color", DEFAULT_TEXT_COLOR)
            upper_text_escaped = escape_text(upper_text)
            
            upper_text_obj_code = f'''        upper_text_obj = Text(
            "{upper_text_escaped}",
            font="{upper_font}",
            font_size=48,
            color="{upper_color}"
        )
        upper_text_obj.move_to(UP * 2.5)
'''
        
        if lower_text:
            lower_font = config.get("lower_font", DEFAULT_FONT)
            lower_color = config.get("lower_color", DEFAULT_TEXT_COLOR)
            lower_text_escaped = escape_text(lower_text)
            
            lower_text_obj_code = f'''        lower_text_obj = Text(
            "{lower_text_escaped}",
            font="{lower_font}",
            font_size=48,
            color="{lower_color}"
        )
        lower_text_obj.move_to(DOWN * 2.5)
'''
        
        # Add text object creation code
        if upper_text_obj_code:
            scene_code += f'''        # Upper text
{upper_text_obj_code}'''
        
        if lower_text_obj_code:
            scene_code += f'''        # Lower text
{lower_text_obj_code}'''
        
        # Animate in sequence: upper text -> logo -> lower text
        scene_code += f'''
        # Animate in sequence
'''
        
        # Animate upper text if present
        if upper_text:
            upper_anim_code = get_animation_code("upper_text_obj", upper_animation, is_text=True)
            scene_code += f'''        {upper_anim_code}
        self.wait(0.5)
        
'''
        
        # Animate logo (always present)
        logo_anim_code = get_animation_code("logo", animation_type, is_text=False)
        scene_code += f'''        # Animate logo
        {logo_anim_code}
'''
        
        # Add wait only if there's lower text to animate
        if lower_text:
            scene_code += f'''        self.wait(0.5)
        
        # Animate lower text
        {get_animation_code("lower_text_obj", lower_animation, is_text=True)}
        
'''
        
        scene_code += f'''        self.wait(1)
'''
        
        return scene_code
        
    def save_scene_file(
        self, config: Dict[str, Any], scene_name: str = "logo_scene"
    ) -> Path:
        """
        Save generated scene code to a file.
        
        Args:
            config: Configuration dictionary
            scene_name: Name for the scene file (without .py extension)
            
        Returns:
            Path: Path to the saved scene file
            
        Raises:
            IOError: If file cannot be written.
        """
        scene_code = self.generate_scene_code(config)
        scene_file = self.temp_scene_dir / f"{scene_name}.py"
        
        try:
            with open(scene_file, 'w', encoding='utf-8') as f:
                f.write(scene_code)
        except IOError as e:
            raise IOError(f"Failed to save scene file: {e}") from e
            
        return scene_file
        
    @staticmethod
    def get_scene_class_name() -> str:
        """
        Get the scene class name used in generated code.
        
        Returns:
            str: The scene class name "LogoScreen".
        """
        return "LogoScreen"

