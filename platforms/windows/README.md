# Multi PDF Decrypter - Windows

## Voraussetzungen

Python 3.10 oder neuer muss installiert sein (https://www.python.org/downloads/).
Bei der Installation bitte "Add Python to PATH" aktivieren.

## Lokal bauen

```
platforms\windows\build.bat
```

Das Skript installiert alle Abhängigkeiten automatisch und erstellt die Anwendung unter:

```
platforms\windows\dist\Multi PDF Decrypter\Multi PDF Decrypter.exe
```

Sowie ein ZIP-Archiv zur Weitergabe:

```
platforms\windows\dist\Multi.PDF.Decrypter-Windows.zip
```

## Release herunterladen

Fertige Windows-Builds sind unter "Releases" im Repository verfügbar.
Die Datei `Multi.PDF.Decrypter-Windows.zip` entpacken und
`Multi PDF Decrypter.exe` starten. Eine Installation ist nicht notwendig.

## Systemanforderungen

Windows 10 (64-Bit) oder neuer.
Eine Python-Installation ist bei den vorgefertigten Release-Builds nicht erforderlich,
da alle Abhängigkeiten im Build enthalten sind.
