#!/bin/bash
# Build Multi PDF Decrypter fuer Linux (Ubuntu/Debian)
# Ausgabe: dist/multi-pdf-decrypter/  und  dist/Multi.PDF.Decrypter-Linux.tar.gz

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/../../src"
OUT_DIR="$SCRIPT_DIR/dist"

echo "================================================="
echo " Multi PDF Decrypter -- Linux Build"
echo "================================================="
echo

echo "[1/4] Installiere System-Abhaengigkeiten..."
sudo apt-get update -qq
sudo apt-get install -y python3-tk python3-pip
echo

echo "[2/4] Installiere Python-Abhaengigkeiten..."
pip install --upgrade pip
pip install -r "$SRC_DIR/requirements.txt"
pip install pyinstaller
echo

echo "[3/4] Erstelle Binary mit PyInstaller..."
cd "$SRC_DIR"
pyinstaller \
  --name "multi-pdf-decrypter" \
  --windowed \
  --onedir \
  --distpath "$OUT_DIR" \
  --workpath "$SCRIPT_DIR/build_tmp" \
  --specpath "$SCRIPT_DIR" \
  --add-data "frames:frames" \
  --hidden-import customtkinter \
  --hidden-import pikepdf \
  --hidden-import tkinterdnd2 \
  --hidden-import PIL \
  --collect-all customtkinter \
  --collect-all tkinterdnd2 \
  main.py
echo

echo "[4/4] Erstelle tar.gz Archiv..."
# Copy desktop integration file
cp "$SCRIPT_DIR/multi-pdf-decrypter.desktop" "$OUT_DIR/multi-pdf-decrypter/"
tar -czf "$OUT_DIR/Multi.PDF.Decrypter-Linux.tar.gz" -C "$OUT_DIR" "multi-pdf-decrypter"

echo
echo "================================================="
echo " Fertig!"
echo " Binary: $OUT_DIR/multi-pdf-decrypter/multi-pdf-decrypter"
echo " Archiv: $OUT_DIR/Multi.PDF.Decrypter-Linux.tar.gz"
echo "================================================="
