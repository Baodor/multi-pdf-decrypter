#!/bin/bash
# Build Multi PDF Decrypter fuer macOS
# Ausgabe: dist/Multi PDF Decrypter.app  und  dist/Multi.PDF.Decrypter-macOS.dmg

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/../../src"
OUT_DIR="$SCRIPT_DIR/dist"

echo "================================================="
echo " Multi PDF Decrypter -- macOS Build"
echo "================================================="
echo

echo "[1/4] Installiere Abhaengigkeiten..."
pip install --upgrade pip
pip install -r "$SRC_DIR/requirements.txt"
pip install pyinstaller
echo

echo "[2/4] Erstelle .app Bundle mit PyInstaller..."
cd "$SRC_DIR"
pyinstaller \
  --name "Multi PDF Decrypter" \
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
  --osx-bundle-identifier "com.baodor.multi-pdf-decrypter" \
  main.py
echo

echo "[3/4] Setze App-Berechtigungen..."
chmod +x "$OUT_DIR/Multi PDF Decrypter.app/Contents/MacOS/Multi PDF Decrypter"
echo

echo "[4/4] Erstelle DMG..."
hdiutil create \
  -volname "Multi PDF Decrypter" \
  -srcfolder "$OUT_DIR/Multi PDF Decrypter.app" \
  -ov \
  -format UDZO \
  "$OUT_DIR/Multi.PDF.Decrypter-macOS.dmg"

echo
echo "================================================="
echo " Fertig!"
echo " App:  $OUT_DIR/Multi PDF Decrypter.app"
echo " DMG:  $OUT_DIR/Multi.PDF.Decrypter-macOS.dmg"
echo "================================================="
