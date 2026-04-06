# Multi PDF Decrypter - macOS

## Voraussetzungen

Python 3.10 oder neuer muss installiert sein.
Empfohlen via Homebrew:

```
brew install python
```

## Lokal bauen

```
chmod +x platforms/macos/build.sh
./platforms/macos/build.sh
```

Das Skript installiert alle Abhängigkeiten automatisch und erstellt:

```
platforms/macos/dist/Multi PDF Decrypter.app
platforms/macos/dist/Multi.PDF.Decrypter-macOS.dmg
```

## Release herunterladen

Fertige macOS-Builds sind unter "Releases" im Repository verfügbar.
Die Datei `Multi.PDF.Decrypter-macOS.dmg` öffnen, die App in den
Programme-Ordner ziehen und starten.

## Sicherheitshinweis (Gatekeeper)

Da die App nicht mit einem Apple Developer-Zertifikat signiert ist,
erscheint beim ersten Start möglicherweise eine Sicherheitswarnung.

Um die App trotzdem zu öffnen:
Systemeinstellungen aufrufen, dann "Datenschutz und Sicherheit",
dort erscheint die App mit einem "Trotzdem öffnen"-Knopf.

Alternativ im Terminal:

```
xattr -cr "/Applications/Multi PDF Decrypter.app"
```

## Systemanforderungen

macOS 11 (Big Sur) oder neuer, 64-Bit (Intel oder Apple Silicon).
Eine Python-Installation ist bei den vorgefertigten Release-Builds nicht erforderlich.
