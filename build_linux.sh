#!/bin/bash
# Build Multi PDF Decrypter als eigenstaendige Anwendung fuer Linux

set -e

echo "==> Installiere Abhaengigkeiten..."
pip install -r requirements.txt
pip install pyinstaller

echo "==> Erstelle Linux Binary..."
pyinstaller \
  --name "multi-pdf-decrypter" \
  --windowed \
  --onedir \
  --add-data "frames:frames" \
  --hidden-import customtkinter \
  --hidden-import pikepdf \
  --hidden-import tkinterdnd2 \
  --hidden-import PIL \
  --collect-all customtkinter \
  --collect-all tkinterdnd2 \
  main.py

echo ""
echo "==> Fertig! Die Anwendung befindet sich unter:"
echo "    dist/multi-pdf-decrypter/multi-pdf-decrypter"
