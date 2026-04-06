# Multi PDF Decrypter

Multi PDF Decrypter ist eine plattformübergreifende Desktop-Anwendung zum Entfernen von Passwortschutz aus PDF-Dateien.
Die Anwendung läuft nativ auf Windows, macOS und Linux und bietet eine moderne, übersichtliche Benutzeroberfläche.
Native Apps für Android und iOS/iPadOS sind in Planung.

## Plattformen

| Plattform | Status | Technologie |
|-----------|--------|-------------|
| Windows 10/11 | Verfügbar | Python + CustomTkinter |
| macOS 11+ | Verfügbar | Python + CustomTkinter |
| Linux (Ubuntu 22.04+) | Verfügbar | Python + CustomTkinter |
| Android | In Planung | Flutter |
| iOS / iPadOS | In Planung | Flutter |

## Releases herunterladen

Fertige Builds für alle Desktop-Plattformen sind unter
[Releases](https://github.com/baodor/multi-pdf-decrypter/releases) verfügbar.
Keine Installation von Python oder sonstigen Abhängigkeiten erforderlich.

| Plattform | Datei |
|-----------|-------|
| Windows | `Multi.PDF.Decrypter-Windows-vX.Y.Z.zip` |
| macOS | `Multi.PDF.Decrypter-macOS-vX.Y.Z.dmg` |
| Linux | `Multi.PDF.Decrypter-Linux-vX.Y.Z.tar.gz` |


## Inhaltsverzeichnis

1. Funktionsübersicht
2. Repository-Struktur
3. Systemvoraussetzungen
4. Aus Quellcode starten
5. Lokale Builds erstellen
6. Automatische Releases via GitHub Actions
7. Bedienung
8. Einstellungen und Datenspeicherung
9. Rückgängig-Funktion
10. Gespeicherte Ordner
11. Hinweise zur Sicherheit
12. Mobile Plattformen (Ausblick)
13. Lizenz


## Funktionsübersicht

PDFs per Drag-and-Drop oder Dateidialog hinzufügen, einzelne Dateien oder ganze Ordner

Mehrere Passwörter speichern und wiederverwenden, damit alle PDFs beim nächsten Start automatisch entschlüsselt werden können

Alle ausgewählten PDFs mit einem Klick entschlüsseln

Nicht entschlüsselbare PDFs (kein passendes Passwort) werden automatisch in einen Unterordner namens "Locked" verschoben

Optionaler "(Unlocked)"-Präfix vor dem Dateinamen, standardmäßig deaktiviert

Gespeicherte Ordnerpfade mit automatischer Suche nach verschlüsselten PDFs

Vollständige Rückgängig-Funktion für alle durchgeführten Vorgänge

Alle Einstellungen werden automatisch gespeichert und beim nächsten Start wiederhergestellt

Helles Design, dunkles Design und automatische Systemanpassung


## Repository-Struktur

```
multi-pdf-decrypter/
    src/                              Gemeinsame Python-Quellcode-Basis (Desktop)
        main.py                       Einstiegspunkt und Abhängigkeitsprüfung
        app_window.py                 Hauptfenster, Steuerung und Threading
        models.py                     Datenmodelle (PDFFile, Passwort, Ordner, Undo)
        pdf_processor.py              PDF-Verarbeitungslogik mit pikepdf
        settings_manager.py           JSON-Persistenz für alle Einstellungen
        requirements.txt              Python-Abhängigkeiten
        frames/
            __init__.py
            files_tab.py              Tab "Dateien" mit Drop-Zone und Dateiliste
            folders_tab.py            Tab "Gespeicherte Ordner"
            history_tab.py            Tab "Verlauf" mit Rückgängig-Schaltflächen
            password_panel.py         Rechtes Panel für Passwörter und Optionen
    platforms/
        windows/
            build.bat                 Lokales Build-Skript für Windows
            README.md                 Windows-spezifische Dokumentation
        macos/
            build.sh                  Lokales Build-Skript für macOS
            README.md                 macOS-spezifische Dokumentation
        linux/
            build.sh                  Lokales Build-Skript für Linux
            multi-pdf-decrypter.desktop   Desktop-Integrationsdatei
            README.md                 Linux-spezifische Dokumentation
        android/
            README.md                 Planung und Roadmap (in Entwicklung)
        ios/
            README.md                 Planung und Roadmap (in Entwicklung)
    .github/
        workflows/
            release.yml               GitHub Actions: Build + Release bei Tag-Push
    LICENSE
    README.md
```


## Systemvoraussetzungen

Für das direkte Ausführen aus dem Quellcode wird Python 3.10 oder neuer benötigt.
Die vorgefertigten Release-Builds benötigen keine Python-Installation.

Windows: Windows 10 oder neuer (64-Bit)

macOS: macOS 11 (Big Sur) oder neuer (Intel und Apple Silicon)

Linux: Ubuntu 22.04 oder neuer, mit `python3-tk` installiert


## Aus Quellcode starten

Schritt 1: Repository klonen

```
git clone https://github.com/baodor/multi-pdf-decrypter.git
cd multi-pdf-decrypter
```

Schritt 2: Virtuelle Umgebung erstellen (empfohlen)

```
python3 -m venv venv
```

Aktivieren auf macOS und Linux:

```
source venv/bin/activate
```

Aktivieren auf Windows:

```
venv\Scripts\activate
```

Schritt 3: Abhängigkeiten installieren

```
pip install -r src/requirements.txt
```

Schritt 4: Anwendung starten

```
python3 src/main.py
```

Installierte Abhängigkeiten:

customtkinter, für die moderne Benutzeroberfläche auf Basis von Tkinter

pikepdf, für die PDF-Entschlüsselung, basiert auf der quelloffenen Bibliothek QPDF

Pillow, für die Bildverarbeitung in UI-Elementen

tkinterdnd2, für Drag-and-Drop-Unterstützung (optional, alle anderen Funktionen bleiben nutzbar)


## Lokale Builds erstellen

Eigenständige Anwendungen können lokal gebaut werden. Eine Python-Installation
ist danach auf dem Zielrechner nicht mehr erforderlich.

### Windows

```
platforms\windows\build.bat
```

Ausgabe: `platforms\windows\dist\Multi PDF Decrypter\Multi PDF Decrypter.exe`

### macOS

```
chmod +x platforms/macos/build.sh
./platforms/macos/build.sh
```

Ausgabe: `platforms/macos/dist/Multi PDF Decrypter.app` und `*.dmg`

### Linux

```
chmod +x platforms/linux/build.sh
./platforms/linux/build.sh
```

Ausgabe: `platforms/linux/dist/multi-pdf-decrypter/multi-pdf-decrypter`

Plattformspezifische Details sind in den jeweiligen `platforms/<plattform>/README.md` beschrieben.


## Automatische Releases via GitHub Actions

Ein GitHub Actions Workflow (`.github/workflows/release.yml`) baut automatisch
alle drei Desktop-Plattformen und erstellt einen GitHub Release.

Der Workflow wird ausgelöst, wenn ein Git-Tag mit dem Muster `v*.*.*` gepusht wird.

Neuen Release erstellen:

```
git tag v1.0.0
git push origin v1.0.0
```

Danach startet GitHub Actions und baut parallel auf:

Windows (windows-latest Runner), erzeugt `Multi.PDF.Decrypter-Windows-v1.0.0.zip`

macOS (macos-latest Runner), erzeugt `Multi.PDF.Decrypter-macOS-v1.0.0.dmg`

Linux (ubuntu-latest Runner), erzeugt `Multi.PDF.Decrypter-Linux-v1.0.0.tar.gz`

Alle drei Dateien werden automatisch als GitHub Release-Assets veröffentlicht.
Tags mit Bindestrich (z. B. `v1.0.0-beta1`) werden als Pre-Release markiert.


## Bedienung

### Dateien hinzufügen

Es gibt drei Möglichkeiten, PDFs zur Verarbeitungsliste hinzuzufügen.

Drag-and-Drop: PDF-Dateien oder einen Ordner direkt in das Programmfenster ziehen.
Das Fenster wechselt automatisch zum Tab "Dateien" und hebt sich hervor.

Schaltfläche "Dateien wählen": Öffnet einen Dateiauswahldialog für mehrere PDFs.

Schaltfläche "Ordner wählen": Öffnet einen Ordnerauswahldialog. Alle PDFs
im Ordner und allen Unterordnern werden zur Liste hinzugefügt.
Dateien in "Locked"- und ".pdf_backups"-Verzeichnissen werden übersprungen.

### Passwörter eingeben und speichern

Im rechten Bereich des Fensters befindet sich die Passwortverwaltung.
Das Passwort eingeben, optional eine Bezeichnung vergeben und auf
"Passwort hinzufügen" klicken. Passwörter werden dauerhaft gespeichert
und beim nächsten Start automatisch wiederhergestellt.

Das Auge-Symbol blendet das Passwort im Klartext ein oder aus.
Das X-Symbol löscht ein Passwort dauerhaft.

### PDFs entschlüsseln

Auf "Alle entschlüsseln" klicken. Die Anwendung verarbeitet jede Datei einzeln.

"Entschlüsselt" (grün): Erfolgreich entschlüsselt und am Originalort gespeichert.

"Kein passendes Passwort" (orange): Kein Passwort hat gepasst. Die Datei wurde in den "Locked"-Unterordner verschoben.

"Nicht verschlüsselt" (blau): Die Datei war bereits ohne Passwortschutz.

"Fehler" (rot): Verarbeitungsfehler, z. B. beschädigte Datei oder fehlende Rechte.

### "(Unlocked)"-Präfix

Unter "Optionen" im rechten Panel die Option aktivieren. Dann wird vor den
Dateinamen der entschlüsselten PDF das Präfix "(Unlocked) " geschrieben.
Aus "Rechnung.pdf" wird "(Unlocked) Rechnung.pdf". Standardmäßig deaktiviert.


## Einstellungen und Datenspeicherung

Alle Einstellungen werden automatisch gespeichert.

Speicherort der Konfigurationsdatei:

macOS: ~/Library/Application Support/MultiPDFDecrypter/settings.json

Windows: %APPDATA%\MultiPDFDecrypter\settings.json

Linux: ~/.config/MultiPDFDecrypter/settings.json

Gespeicherte Einstellungen: alle Passwörter mit Bezeichnung, alle Ordnerpfade,
Aktivierung des Präfixes, Design (Hell, Dunkel, System), Fenstergröße und Position.


## Rückgängig-Funktion

Jeder Entschlüsselungsvorgang wird automatisch im Tab "Verlauf" protokolliert.

Um einen Vorgang rückgängig zu machen, im Tab "Verlauf" auf "Rückgängig"
neben dem entsprechenden Eintrag klicken. Alternativ kann über
"Letzten rückgängig" in der unteren Leiste der zuletzt durchgeführte Vorgang
mit einem Klick zurückgenommen werden.

Entschlüsselte Dateien: Die entschlüsselte Datei wird gelöscht und das
Original aus dem versteckten Backup-Ordner ".pdf_backups" wiederhergestellt.

Verschobene Dateien: Dateien aus dem "Locked"-Ordner werden wieder an
ihren ursprünglichen Speicherort zurückbewegt.


## Gespeicherte Ordner

Im Tab "Gespeicherte Ordner" können häufig verwendete Ordnerpfade dauerhaft
hinterlegt werden. Beim Klick auf "Scannen" werden alle verschlüsselten PDFs
im Ordner und allen Unterordnern gefunden und zur Dateiliste hinzugefügt.
"Alle scannen" durchsucht alle gespeicherten Ordner auf einmal.


## Hinweise zur Sicherheit

Passwörter werden im Klartext in der JSON-Konfigurationsdatei gespeichert.
Dies ist für den persönlichen Einsatz ausreichend. Für höhere Sicherheitsanforderungen
sollten Passwörter ausschließlich in einem dedizierten Passwort-Manager gespeichert werden.

Die Originaldateien werden vor dem Überschreiben immer im versteckten Ordner ".pdf_backups"
gesichert. Es gehen keine Daten verloren.

Die Anwendung läuft vollständig lokal. Es werden keine Dateien, Passwörter oder
Metadaten an externe Server übertragen.


## Mobile Plattformen (Ausblick)

Native Apps für Android und iOS/iPadOS sind geplant. Sie werden mit Flutter
entwickelt, um eine gemeinsame Codebasis zu nutzen. Details dazu in den
jeweiligen Plattform-Ordnern:

platforms/android/README.md

platforms/ios/README.md


## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Details sind in der Datei LICENSE enthalten.
