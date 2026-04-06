# Multi PDF Decrypter - Linux (Ubuntu)

## Voraussetzungen

```
sudo apt install python3 python3-pip python3-tk
```

## Lokal bauen

```
chmod +x platforms/linux/build.sh
./platforms/linux/build.sh
```

Das Skript installiert alle Abhängigkeiten automatisch und erstellt:

```
platforms/linux/dist/multi-pdf-decrypter/multi-pdf-decrypter
platforms/linux/dist/Multi.PDF.Decrypter-Linux.tar.gz
```

## Release herunterladen

Fertige Linux-Builds sind unter "Releases" im Repository verfügbar.
Das Archiv `Multi.PDF.Decrypter-Linux.tar.gz` entpacken und die
Binary starten:

```
tar -xzf Multi.PDF.Decrypter-Linux.tar.gz
./multi-pdf-decrypter/multi-pdf-decrypter
```

## Desktop-Integration

Die enthaltene `.desktop`-Datei kann ins Systemmenü integriert werden:

```
sudo cp multi-pdf-decrypter/multi-pdf-decrypter.desktop /usr/share/applications/
sudo cp -r multi-pdf-decrypter /opt/
sudo chmod +x /opt/multi-pdf-decrypter/multi-pdf-decrypter
```

## Systemanforderungen

Ubuntu 22.04 oder neuer (oder kompatible Debian-Distribution).
Eine Python-Installation ist bei den vorgefertigten Release-Builds nicht erforderlich.
