from manim import *
import os

config.frame_rate = 60
# Set background color (Manim accepts hex strings directly)
config.background_color = "#00ff00"

class LogoScreen(Scene):
    def construct(self):
        # Set background color (both config and camera for compatibility)
        self.camera.background_color = "#00ff00"
        
        # Load SVG
        svg_path = '/home/ninso/Downloads/Antifasistische_Aktion_logo.svg'
        if not os.path.exists(svg_path):
            raise FileNotFoundError(f"SVG file not found: {svg_path}")
        
        try:
            logo = SVGMobject(svg_path)
            logo.scale_to_fit_height(3)  # Adjust size as needed
            logo.move_to(ORIGIN)
        except Exception as e:
            raise RuntimeError(f"Failed to load SVG: {e}")
        
        # Upper text
        # Upper text
        upper_text_obj = Text(
            "test2",
            font="Arial",
            font_size=48,
            color="#ffffff"
        )
        upper_text_obj.move_to(UP * 2.5)
        # Lower text
        lower_text_obj = Text(
            "test4",
            font="Arial",
            font_size=48,
            color="#ffffff"
        )
        lower_text_obj.move_to(DOWN * 2.5)

        # Animate in sequence
        self.play(Write(upper_text_obj), run_time=1.5)
        self.wait(0.5)
        
        # Animate logo
        self.play(DrawBorderThenFill(logo), run_time=1.5)
        self.wait(0.5)
        
        # Animate lower text
        self.play(Write(lower_text_obj), run_time=1.5)
        
        self.wait(1)
