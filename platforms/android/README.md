# Multi PDF Decrypter - Android

## Status

Die Android-Version befindet sich in Planung und wird in einer zukünftigen Version veröffentlicht.

## Geplante Technologie

Die Android-App wird mit Flutter entwickelt, um maximale Code-Wiederverwendung
mit der iOS-Version zu erzielen. Die Kernlogik zur PDF-Entschlüsselung wird
über eine plattformübergreifende Dart-Bibliothek bereitgestellt.

Geplanter Tech-Stack:

Flutter (Dart) für die Benutzeroberfläche

syncfusion_flutter_pdf oder ein nativer PDF-Binding via dart:ffi

SharedPreferences für persistente Einstellungen (Passwörter, Ordner)

file_picker für die Dateiauswahl

share_plus für die Ausgabe entschlüsselter PDFs

## Geplante Funktionen

Alle Kernfunktionen der Desktop-Version werden auch in der mobilen App verfügbar sein.

Dateiauswahl aus dem Gerätespeicher und Cloud-Diensten (iCloud, Google Drive, etc.)

Mehrere Passwörter speichern und verwalten

"(Unlocked)"-Präfix optional aktivierbar

Entschlüsselte PDFs in einem wählbaren Ausgabeordner speichern

Verlauf mit Rückgängig-Funktion

Einstellungen werden auf dem Gerät gespeichert

## Benötigte Entwicklungsumgebung (wenn bereit)

Flutter SDK 3.x oder neuer (https://flutter.dev)

Android Studio mit Android SDK

Android 8.0 (API Level 26) oder neuer als Zielplattform

## Beitrag leisten

Entwickler die an der Android-Version mitarbeiten möchten,
sind herzlich willkommen. Bitte ein Issue im Repository eröffnen
oder einen Pull Request einreichen.
