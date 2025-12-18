"""Manim renderer for executing Manim rendering commands."""

import subprocess
from pathlib import Path
from typing import Optional, Callable, Dict, Any
from manim.scene_generator import SceneGenerator
from utils.constants import QUALITY_FLAGS, QUALITY_NAMES, DEFAULT_QUALITY
import shutil


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
        
        # Manim uses -o for output directory, but we also need to ensure
        # the directory exists and is writable
        output_dir = Path(output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        
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
                # Include both stdout and stderr for better debugging
                full_output = ""
                if result.stdout:
                    full_output += f"STDOUT:\n{result.stdout}\n\n"
                if result.stderr:
                    full_output += f"STDERR:\n{result.stderr}\n\n"
                if not full_output:
                    full_output = "Unknown error - no output from Manim"
                
                # Try to extract the most relevant error message
                error_lines = []
                if result.stderr:
                    error_lines.extend(result.stderr.split('\n'))
                if result.stdout:
                    error_lines.extend(result.stdout.split('\n'))
                
                # Look for common error patterns
                relevant_errors = []
                for line in error_lines:
                    line_lower = line.lower()
                    if any(keyword in line_lower for keyword in ['error', 'exception', 'traceback', 'failed', 'not found']):
                        relevant_errors.append(line)
                
                if relevant_errors:
                    error_summary = "\n".join(relevant_errors[:10])  # Limit to first 10 relevant lines
                    error_msg = f"Manim rendering failed (exit code {result.returncode}):\n\nRelevant errors:\n{error_summary}\n\nFull output:\n{full_output}"
                else:
                    error_msg = f"Manim rendering failed (exit code {result.returncode}):\n{full_output}"
                
                if progress_callback:
                    progress_callback(f"Error: Manim failed with exit code {result.returncode}")
                raise RuntimeError(error_msg)
            
            if progress_callback:
                progress_callback("Render complete! Searching for video file...")
                
            # Find the output video file
            # Manim outputs to: output_dir/scene_class/quality/scene_class.mp4
            # But quality names can vary (480p15, 480p60, 1080p60, etc.)
            # They depend on both quality preset and FPS
            render_settings = config.get("render_settings", {})
            quality_name = self._get_quality_name(render_settings)
            fps = render_settings.get("fps", 60)
            
            # Generate possible quality names based on FPS
            # Manim uses format like "1080p60", "720p30", etc.
            def get_possible_quality_names(base_name: str, fps: int) -> list[str]:
                """Generate possible quality directory names."""
                names = [base_name]  # Start with the base name
                # Try variations with FPS
                if "p" in base_name:
                    parts = base_name.split("p")
                    if len(parts) == 2:
                        resolution = parts[0]
                        # Add FPS variations
                        names.append(f"{resolution}p{fps}")
                        names.append(f"{resolution}p15")  # Default FPS
                        names.append(f"{resolution}p30")
                        names.append(f"{resolution}p60")
                        names.append(f"{resolution}p90")
                        names.append(f"{resolution}p144")
                else:
                    # If no "p" in name, try adding FPS
                    names.append(f"{base_name}p{fps}")
                    names.append(f"{base_name}p15")
                    names.append(f"{base_name}p30")
                    names.append(f"{base_name}p60")
                return names
            
            possible_quality_names = get_possible_quality_names(quality_name, fps)
            
            # Search for video file recursively in output directory
            def find_video_file(search_dir: Path, scene_name: str) -> Optional[Path]:
                """Recursively search for the video file."""
                if not search_dir.exists():
                    return None
                
                # Try exact quality names first (most common case)
                for qname in possible_quality_names:
                    exact_path = search_dir / scene_class / qname / f"{scene_class}.mp4"
                    if exact_path.exists() and exact_path.is_file():
                        return exact_path
                
                # Search in scene_class directory for any quality subdirectory
                scene_dir = search_dir / scene_class
                if scene_dir.exists() and scene_dir.is_dir():
                    for subdir in scene_dir.iterdir():
                        if subdir.is_dir():
                            # Try exact scene name match first
                            video_file = subdir / f"{scene_class}.mp4"
                            if video_file.exists() and video_file.is_file():
                                return video_file
                            # Also try with partial scene name match
                            for mp4_file in subdir.glob("*.mp4"):
                                if mp4_file.is_file() and scene_class.lower() in mp4_file.stem.lower():
                                    return mp4_file
                
                # Search recursively in all subdirectories for any .mp4 file
                # Check files that might match the scene name
                for video_file in search_dir.rglob("*.mp4"):
                    if video_file.is_file():
                        # Check if scene name is in the file path or name
                        file_path_str = str(video_file).lower()
                        if scene_class.lower() in file_path_str:
                            return video_file
                
                # Last resort: get the most recently modified .mp4 file in the directory
                # This handles cases where Manim outputs with a different naming scheme
                mp4_files = [f for f in search_dir.rglob("*.mp4") if f.is_file()]
                if mp4_files:
                    # Sort by modification time, most recent first
                    mp4_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                    # Return the most recent file that was created after we started rendering
                    # (approximate: files modified in the last hour)
                    import time
                    current_time = time.time()
                    for mp4_file in mp4_files:
                        file_time = mp4_file.stat().st_mtime
                        # If file was modified in the last hour, it's likely our render
                        if current_time - file_time < 3600:
                            return mp4_file
                    # If no recent file, return the most recent one anyway
                    return mp4_files[0]
                
                return None
            
            # Search for video file
            video_path = find_video_file(output_dir, scene_class)
            
            # If custom output path specified, try to copy/move the file there
            if output_path:
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
                        Path.cwd() / "media" / "videos",
                        Path.home() / "manim_output"
                    ]
                    for search_dir in common_dirs:
                        if search_dir.exists():
                            found = find_video_file(search_dir, scene_class)
                            if found:
                                video_path = found
                                break
                
                # If we found a video but it's not at the requested location, copy it
                if video_path and video_path.exists() and video_path != output_path:
                    try:
                        import shutil
                        output_path = Path(output_path)
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(video_path, output_path)
                        video_path = output_path
                        if progress_callback:
                            progress_callback(f"Video copied to: {output_path}")
                    except Exception as e:
                        # If copy fails, use the original location
                        if progress_callback:
                            progress_callback(f"Warning: Could not copy to requested location: {e}")
                
                if not video_path or not video_path.exists():
                    # List all files in output directory for debugging
                    debug_info = f"Checked paths:\n"
                    debug_info += f"- Expected: {output_dir / scene_class / quality_name / f'{scene_class}.mp4'}\n"
                    for qname in possible_quality_names[:5]:  # Limit to first 5 to avoid too much output
                        debug_info += f"- Tried: {output_dir / scene_class / qname / f'{scene_class}.mp4'}\n"
                    debug_info += f"- Output dir: {output_dir}\n"
                    debug_info += f"- Requested path: {output_path}\n"
                    
                    # List actual files found (limit output)
                    if output_dir.exists():
                        debug_info += f"\nFiles found in output directory (first 20):\n"
                        file_count = 0
                        for item in output_dir.rglob("*"):
                            if item.is_file() and file_count < 20:
                                debug_info += f"  {item}\n"
                                file_count += 1
                        if file_count >= 20:
                            debug_info += f"  ... (and more files)\n"
                    
                    # Also check common Manim locations
                    for common_dir in [Path.cwd() / "media" / "videos", Path.home() / "manim_output"]:
                        if common_dir.exists():
                            debug_info += f"\nFiles found in {common_dir} (first 10):\n"
                            file_count = 0
                            for item in common_dir.rglob("*.mp4"):
                                if item.is_file() and file_count < 10:
                                    debug_info += f"  {item}\n"
                                    file_count += 1
                            if file_count >= 10:
                                debug_info += f"  ... (and more files)\n"
                    
                    raise RuntimeError(
                        f"Rendered video not found.\n{debug_info}\n"
                        f"Manim may have output the video to a different location. "
                        f"Please check the output directory manually or review Manim's output above."
                    )
            else:
                # No custom output path, just find the video
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
                        # Search in common Manim output locations
                        common_dirs = [
                            Path.cwd() / "media" / "videos",
                            Path.home() / "manim_output"
                        ]
                        for search_dir in common_dirs:
                            if search_dir.exists():
                                found = find_video_file(search_dir, scene_class)
                                if found:
                                    video_path = found
                                    break
                    
                    if not video_path or not video_path.exists():
                        # List all files in output directory for debugging
                        debug_info = f"Checked paths:\n"
                        debug_info += f"- Expected: {output_dir / scene_class / quality_name / f'{scene_class}.mp4'}\n"
                        for qname in possible_quality_names[:5]:  # Limit to first 5
                            debug_info += f"- Tried: {output_dir / scene_class / qname / f'{scene_class}.mp4'}\n"
                        debug_info += f"- Output dir: {output_dir}\n"
                        
                        # List actual files found (limit output)
                        if output_dir.exists():
                            debug_info += f"\nFiles found in output directory (first 20):\n"
                            file_count = 0
                            for item in output_dir.rglob("*"):
                                if item.is_file() and file_count < 20:
                                    debug_info += f"  {item}\n"
                                    file_count += 1
                            if file_count >= 20:
                                debug_info += f"  ... (and more files)\n"
                        
                        # Also check common Manim locations
                        for common_dir in [Path.cwd() / "media" / "videos", Path.home() / "manim_output"]:
                            if common_dir.exists():
                                debug_info += f"\nFiles found in {common_dir} (first 10):\n"
                                file_count = 0
                                for item in common_dir.rglob("*.mp4"):
                                    if item.is_file() and file_count < 10:
                                        debug_info += f"  {item}\n"
                                        file_count += 1
                                if file_count >= 10:
                                    debug_info += f"  ... (and more files)\n"
                        
                        raise RuntimeError(
                            f"Rendered video not found.\n{debug_info}\n"
                            f"Manim may have output the video to a different location. "
                            f"Please check the output directory manually or review Manim's output above."
                        )
            
            if not video_path or not video_path.exists():
                raise RuntimeError(f"Video file not found at: {video_path}")
            
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

