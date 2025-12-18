# Manim Logo Animator

A cross-platform GUI application for animating SVG logos using Manim. Create professional logo animations with customizable text, animation types, and render settings.

## Features

- **SVG Logo Animation**: Animate any SVG logo with various animation types
- **Animation Types**: Choose from Fade In, Scale Up, Rotate, or Draw animations
- **Text Support**: Add upper and lower text with customizable fonts and colors
- **Flexible Render Settings**:
  - Aspect ratios: 1:1, 16:9, 500x500, 1920x1080
  - Frame rates: 30, 60, 90, 144 FPS
  - Quality presets: Low (480p), Medium (720p), High (1080p), Ultra (4K)
- **Preview**: Preview animations before final rendering
- **Cross-Platform**: Works on Windows and Linux

## Requirements

- **Python 3.8 - 3.12** (Python 3.13+ may have compatibility issues with Manim dependencies)
- Manim (Community Edition)
- PyQt6
- System dependencies for Manim (varies by platform)

**Important**: Python 3.13 and 3.14 are not yet fully supported by Manim and its dependencies (especially `av` and `skia-python`). Please use Python 3.11 or 3.12 for best compatibility.

## Installation

### Automated Installation (Linux)

The easiest way to install on Linux is using the provided installation script:

```bash
# Clone or download this repository
git clone https://github.com/Ninso112/manim-logo-animator.git
cd manim-logo-animator

# Run the installation script (will prompt for sudo when needed)
./install.sh
```

The script will:
- Automatically detect your Linux distribution
- Install all required system dependencies
- Install Python dependencies
- Install Manim

**Note**: The script requires sudo privileges for system package installation. It will prompt you when needed.

### Manual Installation

#### 1. Clone or download this repository

```bash
git clone https://github.com/Ninso112/manim-logo-animator.git
cd manim-logo-animator
```

#### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

#### 3. Install Manim

Manim installation varies by platform. Please refer to the [official Manim documentation](https://docs.manim.community/en/stable/installation.html) for detailed instructions.

### Linux Distribution-Specific Instructions

#### Ubuntu / Debian

```bash
# Update package list
sudo apt update

# Install system dependencies
sudo apt install -y \
    build-essential \
    python3-dev \
    python3-pip \
    libcairo2-dev \
    libpango1.0-dev \
    libgirepository1.0-dev \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev

# Install Python dependencies
pip install -r requirements.txt

# Install Manim
pip install manim
```

#### Fedora / RHEL / CentOS

```bash
# Install system dependencies
sudo dnf install -y \
    gcc \
    gcc-c++ \
    python3-devel \
    cairo-devel \
    pango-devel \
    gobject-introspection-devel \
    ffmpeg \
    ffmpeg-devel \
    SDL2-devel \
    SDL2_image-devel \
    SDL2_mixer-devel \
    SDL2_ttf-devel

# Install Python dependencies
pip install -r requirements.txt

# Install Manim
pip install manim
```

#### Arch Linux / Manjaro

```bash
# Install system dependencies
sudo pacman -S --needed \
    base-devel \
    python \
    python-pip \
    cairo \
    pango \
    gobject-introspection \
    ffmpeg \
    sdl2 \
    sdl2_image \
    sdl2_mixer \
    sdl2_ttf

# Install Python dependencies
pip install -r requirements.txt

# Install Manim
pip install manim
```

#### openSUSE

```bash
# Install system dependencies
sudo zypper install -y \
    gcc \
    gcc-c++ \
    python3-devel \
    cairo-devel \
    pango-devel \
    gobject-introspection-devel \
    ffmpeg \
    ffmpeg-devel \
    libSDL2-devel \
    libSDL2_image-devel \
    libSDL2_mixer-devel \
    libSDL2_ttf-devel

# Install Python dependencies
pip install -r requirements.txt

# Install Manim
pip install manim
```

#### Additional Notes for Linux

- **LaTeX (Optional)**: For better text rendering, you may want to install LaTeX:
  - Ubuntu/Debian: `sudo apt install texlive-full`
  - Fedora: `sudo dnf install texlive-scheme-full`
  - Arch: `sudo pacman -S texlive-most`
  - openSUSE: `sudo zypper install texlive-scheme-full`

- **GStreamer (for video preview)**: Some distributions may need GStreamer plugins:
  - Ubuntu/Debian: `sudo apt install gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad`
  - Fedora: `sudo dnf install gstreamer1-plugins-base gstreamer1-plugins-good gstreamer1-plugins-bad-free`
  - Arch: `sudo pacman -S gst-plugins-base gst-plugins-good gst-plugins-bad`
  - openSUSE: `sudo zypper install gstreamer-plugins-base gstreamer-plugins-good gstreamer-plugins-bad`

**Quick install (Windows):**
```bash
# Install via pip (requires Visual C++ Build Tools)
pip install manim
```

**Note**: Manim has additional system dependencies. On Linux, you may need to install:
- FFmpeg
- Cairo
- Pango
- LaTeX (optional, for text rendering)

## Usage

### Running the Application

```bash
python src/main.py
```

Or from the project root:

```bash
python -m src.main
```

### Using the Application

1. **Select SVG File**: Click "Browse..." to select your SVG logo file
2. **Choose Animation Type**: Select from Fade In, Scale Up, Rotate, or Draw
3. **Add Text** (optional):
   - Enter upper text that appears above the logo
   - Enter lower text that appears below the logo
   - Customize fonts and colors using the "Font..." and "Color..." buttons
4. **Configure Render Settings**:
   - Select aspect ratio (1:1, 16:9, 500x500, or 1920x1080)
   - Choose frame rate (30, 60, 90, or 144 FPS)
   - Select quality preset
5. **Preview**: Click "Preview" (Ctrl+P) to generate a low-quality preview
6. **Render**: Click "Render Video..." (Ctrl+R) to render the final video

### Keyboard Shortcuts

- `Ctrl+O`: Open SVG file
- `Ctrl+P`: Preview animation
- `Ctrl+R`: Render video
- `Ctrl+Q`: Quit application

## Project Structure

```
manim-logo-animator/
├── src/
│   ├── main.py                 # Application entry point
│   ├── gui/
│   │   ├── main_window.py      # Main window
│   │   ├── components/         # GUI components
│   │   └── dialogs/            # Dialog windows
│   ├── manim/
│   │   ├── scene_generator.py  # Manim scene code generator
│   │   └── renderer.py         # Manim renderer
│   └── utils/                  # Utility modules
├── install.sh                  # Automated installation script (Linux)
├── LICENSE                     # MIT License
├── requirements.txt
└── README.md
```

## Platform-Specific Notes

### Windows

- Ensure you have Visual C++ Build Tools installed for Manim dependencies
- Paths with spaces are handled automatically
- Video preview may require additional codecs

### Linux

- Install system dependencies before installing Manim (see [Linux Distribution-Specific Instructions](#linux-distribution-specific-instructions) above)
- May require `sudo` for system package installation
- Ensure FFmpeg is properly installed and accessible
- For video preview functionality, GStreamer plugins may be required (see distribution-specific instructions)

## Troubleshooting

### Installation Script Issues

If the automated installation script (`install.sh`) fails:

1. **Check script permissions**: Make sure the script is executable
   ```bash
   chmod +x install.sh
   ```

2. **Run with verbose output**: Add `set -x` at the beginning of the script or run with:
   ```bash
   bash -x install.sh
   ```

3. **Manual installation**: If the script doesn't work, follow the [manual installation instructions](#manual-installation) for your specific distribution

4. **Unsupported distribution**: If your distribution is not detected, you can manually install dependencies following the patterns in the script

### Python Version Compatibility Issues

If you encounter errors like:
- `Failed building wheel for av`
- `No matching distribution found for skia-python`
- `struct AVStream has no member named 'nb_side_data'`

This usually means you're using Python 3.13 or 3.14, which are not yet fully supported by Manim dependencies.

**Solution**: Use Python 3.11 or 3.12 instead:

```bash
# Check your Python version
python3 --version

# If you have Python 3.13+, install Python 3.12:
# Ubuntu/Debian:
sudo apt install python3.12 python3.12-venv python3.12-pip

# Arch Linux:
sudo pacman -S python312

# Fedora:
sudo dnf install python3.12 python3.12-pip

# Then create a virtual environment with Python 3.12:
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Manim Not Found

If you get an error that Manim is not found:
```bash
pip install manim
```

Verify installation:
```bash
manim --version
```

### SVG Loading Issues

- Ensure your SVG file is valid and well-formed
- Some complex SVGs may not render correctly
- Try simplifying the SVG or converting it to a simpler format

### Rendering Errors

- Check that all dependencies are installed
- Ensure sufficient disk space for output files
- Check console output for detailed error messages
- Verify that the SVG file path is correct and accessible

### Preview Not Working

- Preview requires video codec support
- On Linux, ensure `gstreamer` plugins are installed
- Try rendering a full video instead of preview

## Output

Rendered videos are saved to:
- **Default**: `~/manim_output/` (home directory)
- **Custom**: Location specified in the save dialog

Videos are saved as MP4 files and can be played in any standard video player.

## Development

To contribute or modify the application:

1. Fork the repository
2. Create a virtual environment
3. Install development dependencies
4. Make your changes
5. Test on both Windows and Linux if possible

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Manim](https://www.manim.community/) - Mathematical Animation Engine
- GUI framework: [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
