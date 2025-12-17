"""Manim renderer for executing Manim rendering commands."""

import subprocess
from pathlib import Path
from typing import Optional, Callable, Dict, Any
from .scene_generator import SceneGenerator
from ..utils.constants import QUALITY_FLAGS, QUALITY_NAMES, DEFAULT_QUALITY


class ManimRenderer:
    """Handles Manim rendering execution."""
    
    def __init__(self) -> None:
        """Initialize the Manim renderer."""
        self.scene_generator = SceneGenerator()
        self.output_dir = Path.home() / "manim_output"
        self.output_dir.mkdir(exist_ok=True)
        
    def render(
        self,
        config: Dict[str, Any],
        output_path: Optional[Path] = None,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> Path:
        """
        Render the animation.
        
        Args:
            config: Configuration dictionary with render_settings
            output_path: Optional custom output path
            progress_callback: Optional callback function for progress updates
            
        Returns:
            Path: Path to the rendered video file
            
        Raises:
            RuntimeError: If rendering fails or video file is not found.
            FileNotFoundError: If Manim is not installed.
        """
        if progress_callback:
            progress_callback("Generating scene code...")
            
        # Generate and save scene file
        scene_file = self.scene_generator.save_scene_file(config)
        scene_class = SceneGenerator.get_scene_class_name()
        
        if progress_callback:
            progress_callback("Starting Manim render...")
        
        # Determine output directory
        if output_path:
            output_dir = output_path.parent
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            output_dir = self.output_dir
            
        # Build Manim command
        # Format: manim -ql -o output_dir scene_file.py SceneClass
        # -ql = low quality (for faster preview)
        # -qh = high quality
        # -qm = medium quality
        
        quality_flag = self._get_quality_flag(config.get("render_settings", {}))
        
        cmd = [
            "manim",
            quality_flag,
            "-o", str(output_dir),
            str(scene_file),
            scene_class
        ]
        
        try:
            if progress_callback:
                progress_callback("Executing Manim...")
                
            # Execute Manim
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if progress_callback:
                progress_callback("Render complete!")
                
            # Find the output video file
            # Manim outputs to: output_dir/scene_class/quality/scene_class.mp4
            quality_name = self._get_quality_name(config.get("render_settings", {}))
            
            # If custom output path specified, use it
            if output_path:
                # Manim might have created it in a subdirectory, but we want the specified path
                # Check if Manim created it in the expected location first
                manim_path = output_dir / scene_class / quality_name / f"{scene_class}.mp4"
                if manim_path.exists():
                    # Copy or move to desired location, or just return the actual path
                    # For now, return the actual Manim output path
                    video_path = manim_path
                else:
                    # Try alternative locations
                    alt_paths = [
                        output_dir / f"{scene_class}.mp4",
                        output_path
                    ]
                    video_path = None
                    for path in alt_paths:
                        if path.exists():
                            video_path = path
                            break
                    
                    if not video_path:
                        raise RuntimeError(f"Rendered video not found. Check output directory: {output_dir}")
            else:
                video_path = output_dir / scene_class / quality_name / f"{scene_class}.mp4"
                
                if not video_path.exists():
                    # Try alternative paths
                    alt_paths = [
                        output_dir / f"{scene_class}.mp4",
                        output_dir / scene_class / f"{scene_class}.mp4"
                    ]
                    for path in alt_paths:
                        if path.exists():
                            video_path = path
                            break
                    
                    if not video_path.exists():
                        raise RuntimeError(f"Rendered video not found. Check output directory: {output_dir}")
                
            return video_path
            
        except subprocess.CalledProcessError as e:
            error_details = e.stderr if e.stderr else e.stdout if e.stdout else "Unknown error"
            error_msg = f"Manim rendering failed:\n{error_details}"
            if progress_callback:
                progress_callback(f"Error: {error_msg}")
            raise RuntimeError(error_msg)
        except FileNotFoundError:
            error_msg = "Manim not found. Please install Manim: pip install manim"
            if progress_callback:
                progress_callback(f"Error: {error_msg}")
            raise RuntimeError(error_msg)
            
    @staticmethod
    def _get_quality_flag(render_settings: Dict[str, Any]) -> str:
        """
        Get Manim quality flag based on render settings.
        
        Args:
            render_settings: Dictionary containing quality setting.
            
        Returns:
            str: Quality flag for Manim command.
        """
        quality = render_settings.get("quality", DEFAULT_QUALITY)
        return QUALITY_FLAGS.get(quality, QUALITY_FLAGS[DEFAULT_QUALITY])
            
    @staticmethod
    def _get_quality_name(render_settings: Dict[str, Any]) -> str:
        """
        Get Manim quality name for output directory.
        
        Args:
            render_settings: Dictionary containing quality setting.
            
        Returns:
            str: Quality name for output directory.
        """
        quality = render_settings.get("quality", DEFAULT_QUALITY)
        return QUALITY_NAMES.get(quality, QUALITY_NAMES[DEFAULT_QUALITY])

