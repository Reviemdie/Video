from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Video Cutter Pro")
    app.setOrganizationName("VideoTools")

    presets_dir = Path(__file__).resolve().parent.parent / "presets"
    presets_dir.mkdir(parents=True, exist_ok=True)

    window = MainWindow(presets_dir=presets_dir)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
