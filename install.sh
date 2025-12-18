#!/bin/bash

# Manim Logo Animator Installation Script
# This script detects the Linux distribution and installs all required dependencies

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python version
check_python_version() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    print_info "Detected Python version: $PYTHON_VERSION"
    
    # Manim supports Python 3.8-3.12
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        print_error "Python 3.8 or higher is required. Found: $PYTHON_VERSION"
        exit 1
    fi
    
    if [ "$PYTHON_MAJOR" -gt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -gt 12 ]); then
        print_warning "Python $PYTHON_VERSION detected. Manim officially supports Python 3.8-3.12."
        print_warning "You may encounter compatibility issues. Consider using Python 3.11 or 3.12."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Installation cancelled. Please install Python 3.11 or 3.12."
            exit 1
        fi
    fi
}

# Check if running as root (for package installation)
check_root() {
    if [ "$EUID" -ne 0 ]; then 
        print_error "This script needs sudo privileges to install system packages."
        print_info "Please run: sudo $0"
        exit 1
    fi
}

# Detect Linux distribution
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
        DISTRO_VERSION=$VERSION_ID
    elif [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        DISTRO=$(echo $DISTRIB_ID | tr '[:upper:]' '[:lower:]')
    elif [ -f /etc/debian_version ]; then
        DISTRO="debian"
    elif [ -f /etc/fedora-release ]; then
        DISTRO="fedora"
    elif [ -f /etc/arch-release ]; then
        DISTRO="arch"
    elif [ -f /etc/SuSE-release ]; then
        DISTRO="opensuse"
    else
        DISTRO="unknown"
    fi
    
    print_info "Detected distribution: $DISTRO"
}

# Install dependencies for Ubuntu/Debian
install_debian() {
    print_info "Installing dependencies for Ubuntu/Debian..."
    
    apt-get update
    apt-get install -y \
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
        libsdl2-ttf-dev \
        gstreamer1.0-plugins-base \
        gstreamer1.0-plugins-good \
        gstreamer1.0-plugins-bad
    
    print_success "System dependencies installed for Ubuntu/Debian"
}

# Install dependencies for Fedora/RHEL/CentOS
install_fedora() {
    print_info "Installing dependencies for Fedora/RHEL/CentOS..."
    
    dnf install -y \
        gcc \
        gcc-c++ \
        python3-devel \
        python3-pip \
        cairo-devel \
        pango-devel \
        gobject-introspection-devel \
        ffmpeg \
        ffmpeg-devel \
        SDL2-devel \
        SDL2_image-devel \
        SDL2_mixer-devel \
        SDL2_ttf-devel \
        gstreamer1-plugins-base \
        gstreamer1-plugins-good \
        gstreamer1-plugins-bad-free
    
    print_success "System dependencies installed for Fedora/RHEL/CentOS"
}

# Install dependencies for Arch Linux/Manjaro
install_arch() {
    print_info "Installing dependencies for Arch Linux/Manjaro..."
    
    pacman -S --needed --noconfirm \
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
        sdl2_ttf \
        gst-plugins-base \
        gst-plugins-good \
        gst-plugins-bad
    
    print_success "System dependencies installed for Arch Linux/Manjaro"
}

# Install dependencies for openSUSE
install_opensuse() {
    print_info "Installing dependencies for openSUSE..."
    
    zypper install -y \
        gcc \
        gcc-c++ \
        python3-devel \
        python3-pip \
        cairo-devel \
        pango-devel \
        gobject-introspection-devel \
        ffmpeg \
        ffmpeg-devel \
        libSDL2-devel \
        libSDL2_image-devel \
        libSDL2_mixer-devel \
        libSDL2_ttf-devel \
        gstreamer-plugins-base \
        gstreamer-plugins-good \
        gstreamer-plugins-bad
    
    print_success "System dependencies installed for openSUSE"
}

# Install Python dependencies
install_python_deps() {
    print_info "Installing Python dependencies..."
    
    # Check if requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found. Please run this script from the project root directory."
        exit 1
    fi
    
    # Use pip3 or pip depending on what's available
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
    else
        print_error "pip not found. Please install pip first."
        exit 1
    fi
    
    # Try to install dependencies, with fallback for av/skia issues
    if ! $PIP_CMD install --user -r requirements.txt 2>&1 | tee /tmp/manim_install.log; then
        if grep -q "Failed building wheel for av\|skia-python" /tmp/manim_install.log; then
            print_warning "Installation failed due to Python version compatibility."
            print_error "Python 3.13+ is not yet supported by Manim dependencies."
            print_info "Please use Python 3.11 or 3.12 instead."
            print_info "You can install Python 3.12 and create a virtual environment:"
            print_info "  python3.12 -m venv venv"
            print_info "  source venv/bin/activate"
            print_info "  pip install -r requirements.txt"
            exit 1
        else
            print_error "Failed to install dependencies. Check the error above."
            exit 1
        fi
    fi
    
    print_success "Python dependencies installed"
}

# Install Manim
install_manim() {
    print_info "Installing Manim..."
    
    # Use pip3 or pip depending on what's available
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
    else
        print_error "pip not found. Please install pip first."
        exit 1
    fi
    
    $PIP_CMD install --user manim
    
    print_success "Manim installed"
}

# Optional: Install LaTeX
install_latex() {
    read -p "Do you want to install LaTeX for better text rendering? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Installing LaTeX..."
        
        case $DISTRO in
            ubuntu|debian)
                apt-get install -y texlive-full
                ;;
            fedora|rhel|centos)
                dnf install -y texlive-scheme-full
                ;;
            arch|manjaro)
                pacman -S --needed --noconfirm texlive-most
                ;;
            opensuse*)
                zypper install -y texlive-scheme-full
                ;;
            *)
                print_warning "LaTeX installation not configured for $DISTRO. Please install manually."
                ;;
        esac
        
        print_success "LaTeX installed"
    else
        print_info "Skipping LaTeX installation"
    fi
}

# Main installation function
main() {
    print_info "Manim Logo Animator Installation Script"
    print_info "========================================"
    echo
    
    # Check Python version first
    check_python_version
    
    # Detect distribution
    detect_distro
    
    # Check if we need root (for system packages)
    if [ "$EUID" -ne 0 ]; then
        print_warning "This script needs sudo privileges for system package installation."
        print_info "The script will prompt for sudo when needed."
        echo
    fi
    
    # Install system dependencies based on distribution
    case $DISTRO in
        ubuntu|debian)
            if [ "$EUID" -eq 0 ]; then
                install_debian
            else
                sudo bash -c "$(declare -f install_debian); install_debian"
            fi
            ;;
        fedora|rhel|centos)
            if [ "$EUID" -eq 0 ]; then
                install_fedora
            else
                sudo bash -c "$(declare -f install_fedora); install_fedora"
            fi
            ;;
        arch|manjaro)
            if [ "$EUID" -eq 0 ]; then
                install_arch
            else
                sudo bash -c "$(declare -f install_arch); install_arch"
            fi
            ;;
        opensuse*)
            if [ "$EUID" -eq 0 ]; then
                install_opensuse
            else
                sudo bash -c "$(declare -f install_opensuse); install_opensuse"
            fi
            ;;
        *)
            print_error "Unsupported distribution: $DISTRO"
            print_info "Please install dependencies manually. See README.md for instructions."
            exit 1
            ;;
    esac
    
    # Install Python dependencies (doesn't need root)
    install_python_deps
    
    # Install Manim (doesn't need root)
    install_manim
    
    # Optional LaTeX installation
    if [ "$EUID" -eq 0 ]; then
        install_latex
    else
        print_info "To install LaTeX (optional), run: sudo $0 --latex"
    fi
    
    echo
    print_success "Installation complete!"
    print_info "You can now run the application with: python src/main.py"
    echo
    print_info "Note: If 'manim' command is not found, you may need to add ~/.local/bin to your PATH"
    print_info "Add this to your ~/.bashrc or ~/.zshrc: export PATH=\"\$HOME/.local/bin:\$PATH\""
}

# Handle --latex flag
if [ "$1" == "--latex" ]; then
    detect_distro
    if [ "$EUID" -ne 0 ]; then
        print_error "LaTeX installation requires sudo. Please run: sudo $0 --latex"
        exit 1
    fi
    install_latex
    exit 0
fi

# Run main function
main

