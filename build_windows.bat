@echo off
REM Build Multi PDF Decrypter als eigenstaendige .exe fuer Windows

echo ==> Installiere Abhaengigkeiten...
pip install -r requirements.txt
pip install pyinstaller

echo ==> Erstelle Windows Executable...
pyinstaller ^
  --name "Multi PDF Decrypter" ^
  --windowed ^
  --onedir ^
  --add-data "frames;frames" ^
  --hidden-import customtkinter ^
  --hidden-import pikepdf ^
  --hidden-import tkinterdnd2 ^
  --hidden-import PIL ^
  --collect-all customtkinter ^
  --collect-all tkinterdnd2 ^
  main.py

echo.
echo ==> Fertig! Die Anwendung befindet sich unter:
echo     dist\Multi PDF Decrypter\Multi PDF Decrypter.exe
pause
