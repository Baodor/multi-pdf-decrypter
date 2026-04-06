#!/bin/bash
# Build Multi PDF Decrypter as a standalone .app bundle for macOS

set -e

echo "==> Installiere Abhängigkeiten..."
pip install -r requirements.txt
pip install pyinstaller

echo "==> Erstelle macOS App Bundle..."
pyinstaller \
  --name "Multi PDF Decrypter" \
  --windowed \
  --onedir \
  --icon "" \
  --add-data "frames:frames" \
  --hidden-import customtkinter \
  --hidden-import pikepdf \
  --hidden-import tkinterdnd2 \
  --hidden-import PIL \
  --collect-all customtkinter \
  --collect-all tkinterdnd2 \
  main.py

echo ""
echo "==> Fertig! Die App befindet sich unter:"
echo "    dist/Multi PDF Decrypter.app"
