# Multi PDF Decrypter

Multi PDF Decrypter ist eine plattformübergreifende Desktop-Anwendung zum Entfernen von Passwortschutz aus PDF-Dateien. Die Anwendung läuft nativ auf macOS, Windows und Linux und bietet eine moderne, übersichtliche Benutzeroberfläche.


## Inhaltsverzeichnis

1. Funktionsübersicht
2. Systemvoraussetzungen
3. Installation
4. Starten der Anwendung
5. Bedienung
6. Einstellungen und Datenspeicherung
7. Rückgängig-Funktion
8. Gespeicherte Ordner
9. Build-Anleitung (eigenständige Anwendung)
10. Dateistruktur
11. Hinweise zur Sicherheit
12. Zukünftige Erweiterungen
13. Lizenz


## Funktionsübersicht

Die Anwendung bietet folgende Kernfunktionen:

PDFs per Drag-and-Drop oder Dateidialog hinzufügen (einzelne Dateien oder ganze Ordner)

Mehrere Passwörter verwalten und speichern, damit die Anwendung PDFs beim nächsten Start automatisch entschlüsseln kann

Alle ausgewählten PDFs mit einem Klick entschlüsseln

Nicht entschlüsselbare PDFs (falsches oder kein passendes Passwort) werden automatisch in einen Unterordner namens "Locked" verschoben

Optionaler "(Unlocked)"-Präfix vor dem Dateinamen der entschlüsselten PDFs

Gespeicherte Ordnerpfade, die beim Klick auf "Scannen" automatisch nach verschlüsselten PDFs durchsucht werden

Vollständige Rückgängig-Funktion für alle durchgeführten Vorgänge

Automatisches Speichern aller Einstellungen (Passwörter, Ordner, Fenstergröße, Design)

Unterstützung für helles und dunkles Design sowie automatische Systemanpassung


## Systemvoraussetzungen

Alle Plattformen:
Python 3.10 oder neuer

macOS:
macOS 11 (Big Sur) oder neuer

Windows:
Windows 10 oder neuer

Linux:
Eine aktuelle Distribution mit Tk/Tcl-Unterstützung (z. B. Ubuntu 22.04 oder neuer).
Das Paket "python3-tk" muss installiert sein:

```
sudo apt install python3-tk
```


## Installation

Schritt 1: Repository klonen oder herunterladen

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
pip install -r requirements.txt
```

Die folgenden Pakete werden installiert:

customtkinter wird für die moderne Benutzeroberfläche auf Basis von Tkinter verwendet.

pikepdf ist die PDF-Bibliothek zum Entfernen von Verschlüsselung. Sie basiert auf der quelloffenen Bibliothek QPDF.

Pillow wird für die Bildverarbeitung in UI-Elementen benötigt.

tkinterdnd2 ermöglicht Drag-and-Drop-Unterstützung. Dieses Paket ist optional, aber empfohlen.


## Starten der Anwendung

```
python3 main.py
```

Beim ersten Start wird automatisch eine Konfigurationsdatei angelegt (siehe Abschnitt "Einstellungen und Datenspeicherung").

Falls tkinterdnd2 nicht installiert ist, erscheint ein Hinweis in der Konsole und Drag-and-Drop ist deaktiviert. Alle anderen Funktionen bleiben vollständig nutzbar.


## Bedienung

### Dateien hinzufügen

Es gibt drei Möglichkeiten, PDFs zur Verarbeitungsliste hinzuzufügen.

Drag-and-Drop: PDF-Dateien oder einen Ordner direkt in das Programmfenster ziehen. Der Bereich wechselt automatisch zum Tab "Dateien" und hebt sich hervor, sobald Dateien über das Fenster gezogen werden.

Schaltfläche "Dateien wählen": Öffnet einen Dateiauswahldialog, in dem mehrere PDF-Dateien gleichzeitig ausgewählt werden können.

Schaltfläche "Ordner wählen": Öffnet einen Ordnerauswahldialog. Alle PDF-Dateien im ausgewählten Ordner und allen Unterordnern werden automatisch zur Liste hinzugefügt. Dateien in "Locked"- und ".pdf_backups"-Verzeichnissen werden dabei automatisch übersprungen.

### Passwörter eingeben und speichern

Im rechten Bereich des Fensters befindet sich die Passwortverwaltung.

Im Feld "Passwort eingeben" das gewünschte Passwort eintippen. Optional kann eine Bezeichnung vergeben werden (z. B. "Arbeit", "Privat", "Bank"), um Passwörter leichter zuzuordnen. Anschließend auf "+ Passwort hinzufügen" klicken.

Das Passwort erscheint nun in der Liste und wird dauerhaft gespeichert. Beim nächsten Start der Anwendung sind alle Passwörter automatisch wieder verfügbar.

Das Auge-Symbol neben einem Passwort blendet das Passwort im Klartext ein oder aus.

Das "X"-Symbol löscht ein Passwort dauerhaft aus der Liste.

### PDFs entschlüsseln

Sobald mindestens eine Datei in der Liste vorhanden ist und mindestens ein Passwort gespeichert wurde, kann auf "Alle entschlüsseln" geklickt werden.

Die Anwendung verarbeitet jede Datei einzeln und zeigt den aktuellen Status direkt in der Dateiliste an.

Der Status "Entschlüsselt" (grün) bedeutet, dass die PDF erfolgreich entschlüsselt und am ursprünglichen Speicherort gespeichert wurde.

Der Status "Kein passendes Passwort" (orange) bedeutet, dass kein gespeichertes Passwort gepasst hat. Die Datei wurde in den Unterordner "Locked" im selben Verzeichnis verschoben.

Der Status "Nicht verschlüsselt" (blau) bedeutet, dass die Datei bereits ohne Passwortschutz war und keine Änderung vorgenommen wurde.

Der Status "Fehler" (rot) bedeutet, dass bei der Verarbeitung ein Fehler aufgetreten ist, zum Beispiel weil die Datei beschädigt ist oder die Zugriffsrechte fehlen.

### "(Unlocked)"-Präfix

Im rechten Bereich unter "Optionen" befindet sich die Option '"(Unlocked)" vor Dateinamen'. Ist diese Option aktiviert, wird der entschlüsselten Datei das Präfix "(Unlocked) " vorangestellt.

Beispiel: Aus der Datei "Rechnung.pdf" wird "(Unlocked) Rechnung.pdf".

Diese Option ist standardmäßig deaktiviert und wird dauerhaft gespeichert.

### Dateien aus der Liste entfernen

Einzelne Dateien können mit dem "X"-Symbol in der jeweiligen Zeile aus der Liste entfernt werden, solange sie sich im Status "Ausstehend" befinden. Mit der Schaltfläche "Leeren" wird die gesamte Liste auf einmal geleert.


## Einstellungen und Datenspeicherung

Alle Einstellungen werden automatisch gespeichert und beim nächsten Start der Anwendung wiederhergestellt.

Speicherort der Konfigurationsdatei:

Auf macOS: ~/Library/Application Support/MultiPDFDecrypter/settings.json

Auf Windows: %APPDATA%\MultiPDFDecrypter\settings.json

Auf Linux: ~/.config/MultiPDFDecrypter/settings.json

Folgende Einstellungen werden gespeichert: alle Passwörter inklusive optionaler Bezeichnung, alle gespeicherten Ordnerpfade, die Aktivierung des "(Unlocked)"-Präfixes, das ausgewählte Design (Hell, Dunkel, System) sowie Fenstergröße und Position.


## Rückgängig-Funktion

Jeder Entschlüsselungsvorgang wird automatisch im Tab "Verlauf" protokolliert. Dort ist ersichtlich, wann wie viele Dateien entschlüsselt oder in den "Locked"-Ordner verschoben wurden.

Um einen Vorgang rückgängig zu machen, im Tab "Verlauf" auf "Rückgängig" neben dem entsprechenden Eintrag klicken. Alternativ kann über die Schaltfläche "Letzten rückgängig" in der unteren Leiste der zuletzt durchgeführte Vorgang mit einem Klick zurückgenommen werden.

Was beim Rückgängigmachen passiert:

Entschlüsselte Dateien: Die entschlüsselte Datei wird gelöscht und das Original aus dem versteckten Backup-Ordner ".pdf_backups" wiederhergestellt.

Verschobene Dateien: Dateien, die in "Locked" verschoben wurden, werden wieder an ihren ursprünglichen Speicherort zurückbewegt.

Der Backup-Ordner ".pdf_backups" liegt im selben Verzeichnis wie die Originaldatei und ist auf allen Plattformen standardmäßig versteckt (auf Windows durch das Hidden-Attribut, auf macOS und Linux durch den Punkt am Anfang des Namens).


## Gespeicherte Ordner

Im Tab "Gespeicherte Ordner" können häufig verwendete Ordnerpfade dauerhaft hinterlegt werden.

Ordner hinzufügen: Auf "+ Ordner" klicken und den gewünschten Ordner im Dialog auswählen. Der Ordnerpfad wird dauerhaft gespeichert und steht beim nächsten Start wieder zur Verfügung.

Einzelnen Ordner scannen: Auf "Scannen" neben dem gewünschten Ordner klicken. Die Anwendung durchsucht den Ordner und alle Unterordner rekursiv nach verschlüsselten PDFs und fügt sie automatisch der Dateiliste im Tab "Dateien" hinzu.

Alle Ordner scannen: Auf "Alle scannen" klicken, um alle gespeicherten Ordner auf einmal zu durchsuchen und verschlüsselte PDFs zu finden.

Ordner entfernen: Mit dem "X"-Symbol wird der gespeicherte Ordnerpfad dauerhaft aus der Liste entfernt. Die Dateien im Ordner werden dabei nicht verändert.


## Build-Anleitung (eigenständige Anwendung)

Mit PyInstaller kann die Anwendung als eigenständiges Programm gebaut werden, das ohne eine Python-Installation auf dem Zielrechner auskommt.

### macOS

```
chmod +x build_macos.sh
./build_macos.sh
```

Die fertige App befindet sich anschließend unter dist/Multi PDF Decrypter.app und kann in den Programme-Ordner verschoben werden.

### Windows

```
build_windows.bat
```

Die fertige Anwendung befindet sich anschließend unter dist\Multi PDF Decrypter\Multi PDF Decrypter.exe.

### Linux

```
chmod +x build_linux.sh
./build_linux.sh
```

Die fertige Anwendung befindet sich anschließend unter dist/multi-pdf-decrypter/multi-pdf-decrypter.


## Dateistruktur

```
multi-pdf-decrypter/
    main.py                   Einstiegspunkt und Abhängigkeitsprüfung
    app_window.py             Hauptfenster, Anwendungssteuerung und Threading
    models.py                 Datenmodelle für PDFFile, Passwort, Ordner und Undo
    pdf_processor.py          PDF-Verarbeitungslogik mit pikepdf
    settings_manager.py       Einstellungsverwaltung und JSON-Persistenz
    requirements.txt          Python-Abhängigkeiten
    build_macos.sh            Build-Skript für macOS
    build_windows.bat         Build-Skript für Windows
    build_linux.sh            Build-Skript für Linux
    frames/
        __init__.py
        files_tab.py          Tab "Dateien" mit Drop-Zone und Dateiliste
        folders_tab.py        Tab "Gespeicherte Ordner"
        history_tab.py        Tab "Verlauf" mit Rückgängig-Funktion
        password_panel.py     Rechtes Panel für Passwörter und Optionen
```


## Hinweise zur Sicherheit

Passwörter werden im Klartext in der JSON-Konfigurationsdatei gespeichert. Dies ist für den persönlichen Einsatz auf dem eigenen Rechner ausreichend. Für höhere Sicherheitsanforderungen sollte die Konfigurationsdatei verschlüsselt oder Passwörter ausschließlich in einem dedizierten Passwort-Manager aufbewahrt werden.

Die Anwendung entfernt ausschließlich den Benutzerpasswortschutz von PDFs. Dokumente mit zusätzlichem digitalen Rechtemanagementsystem (DRM) oder proprietären Schutzmechanismen werden möglicherweise nicht vollständig entsperrt.

Die Originaldateien werden vor dem Überschreiben immer zuerst in einem versteckten Ordner ".pdf_backups" gesichert, sodass durch eine fehlgeschlagene Verarbeitung keine Daten verloren gehen können.

Die Anwendung läuft vollständig lokal auf dem eigenen Rechner. Es werden keinerlei Dateien, Passwörter oder Metadaten an externe Server übertragen.


## Zukünftige Erweiterungen

Eine native iOS- und Android-App ist für einen späteren Zeitpunkt geplant. Die Architektur wurde bewusst so gestaltet, dass die Verarbeitungslogik in pdf_processor.py ohne großen Aufwand in einen plattformübergreifenden Dienst oder in eine Flutter-App überführt werden kann.

Mögliche weitere Funktionen in zukünftigen Versionen:

Unterstützung für Batch-Verarbeitung mit detaillierter Fortschrittsanzeige

Automatischer Watch-Modus für gespeicherte Ordner, der neu hinzugefügte PDFs sofort erkennt und verarbeitet

Integrierte PDF-Vorschau

Export der Verarbeitungsprotokolle als CSV oder Text

Unterstützung weiterer Verschlüsselungsarten und PDF-Standards

Native iOS-App und Android-App auf Basis von Flutter


## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Details sind in der Datei LICENSE enthalten.
