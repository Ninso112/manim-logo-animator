"""Main entry point for Manim Logo Animator."""

import sys
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
    
    # Enable high DPI scaling
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

