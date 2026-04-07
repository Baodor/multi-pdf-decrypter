# Multi PDF Decrypter - iOS / iPadOS

## Status

Die iOS- und iPadOS-Version befindet sich in Planung und wird in einer
zukünftigen Version veröffentlicht.

## Geplante Technologie

Die iOS/iPadOS-App wird mit Flutter entwickelt, um maximale Code-Wiederverwendung
mit der Android-Version zu erzielen. Beide mobilen Plattformen teilen sich
eine gemeinsame Codebasis.

Geplanter Tech-Stack:

Flutter (Dart) für die Benutzeroberfläche

PDF-Entschlüsselung über native iOS-Bibliotheken via Platform Channels
(z. B. PDFKit unter iOS 11+) oder dart:ffi

NSUbiquitousKeyValueStore / UserDefaults (via shared_preferences) für
persistente Einstellungen

file_picker für die Dateiauswahl aus dem Gerätespeicher und iCloud Drive

share_plus / open_filex für die Ausgabe entschlüsselter PDFs

## Geplante Funktionen

Alle Kernfunktionen der Desktop-Version werden auch auf iOS und iPadOS
verfügbar sein.

Dateiauswahl aus dem Gerätespeicher, iCloud Drive und anderen
Dokumenten-Providern über den nativen iOS-Dateidialog

Mehrere Passwörter speichern und sicher im Keychain ablegen

"(Unlocked)"-Präfix optional aktivierbar

Entschlüsselte PDFs in einem wählbaren Ausgabeordner speichern
oder direkt teilen

Verlauf mit Rückgängig-Funktion

Einstellungen werden auf dem Gerät gespeichert und über iCloud
auf anderen Geräten synchronisiert (optional)

iPad-optimiertes Layout mit Sidebar-Navigation

## Benötigte Entwicklungsumgebung (wenn bereit)

Flutter SDK 3.x oder neuer (https://flutter.dev)

Xcode 15 oder neuer (nur auf macOS)

Apple Developer Account für TestFlight und App Store Veröffentlichung

iOS 15 oder neuer als Zielplattform

## Hinweis zu Apple App Store

Die Veröffentlichung im App Store erfordert ein aktives Apple Developer Program
Abonnement (99 USD pro Jahr). Die App wird dann auch für iPadOS verfügbar sein.

## Beitrag leisten

Entwickler die an der iOS-Version mitarbeiten möchten,
sind herzlich willkommen. Bitte ein Issue im Repository eröffnen
oder einen Pull Request einreichen.
