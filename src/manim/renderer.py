"""Manim renderer for executing Manim rendering commands."""

import subprocess
from pathlib import Path
from typing import Optional, Callable, Dict, Any
from manim.scene_generator import SceneGenerator
from utils.constants import QUALITY_FLAGS, QUALITY_NAMES, DEFAULT_QUALITY


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
        
        # Use absolute path for scene file
        scene_file_abs = scene_file.resolve()
        
        cmd = [
            "manim",
            quality_flag,
            "-o", str(output_dir),
            str(scene_file_abs),
            scene_class
        ]
        
        try:
            if progress_callback:
                progress_callback("Executing Manim...")
                
            # Execute Manim with better error handling
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,  # Don't raise on error, we'll handle it
                cwd=str(scene_file_abs.parent)  # Run from scene file directory
            )
            
            # Check if command failed
            if result.returncode != 0:
                error_details = result.stderr if result.stderr else result.stdout if result.stdout else "Unknown error"
                error_msg = f"Manim rendering failed (exit code {result.returncode}):\n{error_details}"
                if progress_callback:
                    progress_callback(f"Error: {error_msg}")
                raise RuntimeError(error_msg)
            
            if progress_callback:
                progress_callback("Render complete! Searching for video file...")
                
            # Find the output video file
            # Manim outputs to: output_dir/scene_class/quality/scene_class.mp4
            # But quality names can vary (480p15, 480p60, 1080p60, etc.)
            quality_name = self._get_quality_name(config.get("render_settings", {}))
            
            # Search for video file recursively in output directory
            def find_video_file(search_dir: Path, scene_name: str) -> Optional[Path]:
                """Recursively search for the video file."""
                # Try exact quality name first
                exact_path = search_dir / scene_class / quality_name / f"{scene_class}.mp4"
                if exact_path.exists():
                    return exact_path
                
                # Search in scene_class directory for any quality subdirectory
                scene_dir = search_dir / scene_class
                if scene_dir.exists():
                    for subdir in scene_dir.iterdir():
                        if subdir.is_dir():
                            video_file = subdir / f"{scene_class}.mp4"
                            if video_file.exists():
                                return video_file
                
                # Search recursively in all subdirectories
                for video_file in search_dir.rglob(f"{scene_class}.mp4"):
                    if video_file.is_file():
                        return video_file
                
                return None
            
            # If custom output path specified, use it
            if output_path:
                # First try to find in the output directory
                video_path = find_video_file(output_dir, scene_class)
                
                if not video_path:
                    # Try alternative locations
                    alt_paths = [
                        output_dir / f"{scene_class}.mp4",
                        output_path
                    ]
                    for path in alt_paths:
                        if Path(path).exists():
                            video_path = Path(path)
                            break
                
                if not video_path or not video_path.exists():
                    # Last resort: search in common Manim output locations
                    common_dirs = [
                        output_dir,
                        Path.cwd() / "media" / "videos" / scene_class,
                        Path.home() / "manim_output" / scene_class
                    ]
                    for search_dir in common_dirs:
                        if search_dir.exists():
                            found = find_video_file(search_dir, scene_class)
                            if found:
                                video_path = found
                                break
                    
                    if not video_path or not video_path.exists():
                        raise RuntimeError(
                            f"Rendered video not found. Checked:\n"
                            f"- {output_dir / scene_class / quality_name / f'{scene_class}.mp4'}\n"
                            f"- {output_dir}\n"
                            f"- {output_path}\n"
                            f"Please check the output directory manually."
                        )
            else:
                video_path = find_video_file(output_dir, scene_class)
                
                if not video_path or not video_path.exists():
                    # Try alternative paths
                    alt_paths = [
                        output_dir / f"{scene_class}.mp4",
                        output_dir / scene_class / f"{scene_class}.mp4",
                        Path.cwd() / "media" / "videos" / scene_class / quality_name / f"{scene_class}.mp4"
                    ]
                    for path in alt_paths:
                        if Path(path).exists():
                            video_path = Path(path)
                            break
                    
                    if not video_path or not video_path.exists():
                        raise RuntimeError(
                            f"Rendered video not found. Checked:\n"
                            f"- {output_dir / scene_class / quality_name / f'{scene_class}.mp4'}\n"
                            f"- {output_dir}\n"
                            f"Please check the output directory manually."
                        )
                
            return video_path
            
        except FileNotFoundError:
            error_msg = "Manim not found. Please install Manim: pip install manim"
            if progress_callback:
                progress_callback(f"Error: {error_msg}")
            raise RuntimeError(error_msg)
        except RuntimeError:
            # Re-raise RuntimeErrors (already handled above)
            raise
        except Exception as e:
            error_msg = f"Unexpected error during rendering: {str(e)}"
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

