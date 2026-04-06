@echo off
setlocal enabledelayedexpansion
REM Build Multi PDF Decrypter fuer Windows
REM Ausgabe: dist\Multi PDF Decrypter\Multi PDF Decrypter.exe

set "SCRIPT_DIR=%~dp0"
set "SRC_DIR=%SCRIPT_DIR%..\..\src"
set "OUT_DIR=%SCRIPT_DIR%dist"

echo =================================================
echo  Multi PDF Decrypter -- Windows Build
echo =================================================
echo.

echo [1/3] Installiere Abhaengigkeiten...
pip install --upgrade pip
pip install -r "%SRC_DIR%\requirements.txt"
pip install pyinstaller
echo.

echo [2/3] Erstelle Executable mit PyInstaller...
cd /d "%SRC_DIR%"
pyinstaller ^
  --name "Multi PDF Decrypter" ^
  --windowed ^
  --onedir ^
  --distpath "%OUT_DIR%" ^
  --workpath "%SCRIPT_DIR%build_tmp" ^
  --specpath "%SCRIPT_DIR%" ^
  --add-data "frames;frames" ^
  --hidden-import customtkinter ^
  --hidden-import pikepdf ^
  --hidden-import tkinterdnd2 ^
  --hidden-import PIL ^
  --collect-all customtkinter ^
  --collect-all tkinterdnd2 ^
  main.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo FEHLER: PyInstaller Build fehlgeschlagen.
    pause
    exit /b 1
)
echo.

echo [3/3] Erstelle ZIP-Archiv...
cd /d "%OUT_DIR%"
powershell -Command "Compress-Archive -Path 'Multi PDF Decrypter' -DestinationPath 'Multi.PDF.Decrypter-Windows.zip' -Force"
echo.

echo =================================================
echo  Fertig!
echo  Anwendung: %OUT_DIR%\Multi PDF Decrypter\Multi PDF Decrypter.exe
echo  Archiv:    %OUT_DIR%\Multi.PDF.Decrypter-Windows.zip
echo =================================================
pause
