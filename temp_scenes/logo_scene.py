from manim import *
import os

config.frame_rate = 60

class LogoScreen(Scene):
    def construct(self):
        # Set resolution
        self.camera.frame_width = 854
        self.camera.frame_height = 854
        
        # Load SVG
        svg_path = '/home/ninso/Downloads/antifa (1).svg'
        if not os.path.exists(svg_path):
            raise FileNotFoundError(f"SVG file not found: {svg_path}")
        
        try:
            logo = SVGMobject(svg_path)
            logo.scale_to_fit_height(3)  # Adjust size as needed
            logo.move_to(ORIGIN)
        except Exception as e:
            raise RuntimeError(f"Failed to load SVG: {e}")
        
        # Upper text
        upper_text_obj = Text(
            "test",
            font="Sans Serif",
            font_size=48,
            color="#ffffff"
        )
        upper_text_obj.move_to(UP * 2.5)
        self.add(upper_text_obj)
        
        # Lower text
        lower_text_obj = Text(
            "test",
            font="Arial",
            font_size=48,
            color="#ffffff"
        )
        lower_text_obj.move_to(DOWN * 2.5)
        self.play(FadeOut(lower_text_obj), run_time=1.5)
        
        # Animate logo
        self.play(DrawBorderThenFill(logo), run_time=1.5)
        self.wait(1)
