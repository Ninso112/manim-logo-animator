"""Main entry point for Manim Logo Animator."""

import sys
from pathlib import Path

# Add the src directory to the Python path BEFORE any other imports
# This ensures relative imports work when running the script directly
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from typing import NoReturn
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from gui.main_window import MainWindow
from utils.constants import APP_NAME


def main() -> NoReturn:
    """
    Run the application.
    
    Raises:
        SystemExit: When the application exits.
    """
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    
    # High DPI scaling is enabled by default in PyQt6
    # No need to set these attributes (they were removed in PyQt6)
    
    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

