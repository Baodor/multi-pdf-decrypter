#!/usr/bin/env python3
"""
Multi PDF Decrypter
Entfernt Passwortschutz von PDF-Dateien.

Unterstützte Plattformen: macOS, Windows, Linux
"""

import sys


def check_dependencies():
    missing = []
    try:
        import customtkinter  # noqa: F401
    except ImportError:
        missing.append("customtkinter")
    try:
        import pikepdf  # noqa: F401
    except ImportError:
        missing.append("pikepdf")
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        missing.append("Pillow")

    if missing:
        print(
            "Fehlende Abhängigkeiten:\n"
            + "\n".join(f"  - {m}" for m in missing)
            + "\n\nBitte ausführen:\n  pip install -r requirements.txt"
        )
        sys.exit(1)

    try:
        import tkinterdnd2  # noqa: F401
    except ImportError:
        print(
            "Hinweis: 'tkinterdnd2' nicht gefunden.\n"
            "Drag-and-Drop wird nicht unterstützt.\n"
            "Installation: pip install tkinterdnd2\n"
        )


if __name__ == "__main__":
    check_dependencies()

    from app_window import MultiPDFDecrypterWindow

    app = MultiPDFDecrypterWindow()
    app.run()
