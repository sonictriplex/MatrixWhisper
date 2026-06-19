# 🏠 MatrixWhisper Wiki – Willkommen

<p align="center">
  <img src="https://raw.githubusercontent.com/sonictriplex/MatrixWhisper/main/media/media-matrix-logo.png" alt="MatrixWhisper Logo" width="128" height="128">
</p>

<h1 align="center">MatrixWhisper v2.8.0</h1>

<p align="center">
  <strong>Ein hochoptimierter, nativer WhatsApp Web Client für Linux Desktops.</strong><br>
  <em>Gebaut mit Python 3, PyQt6 und QtWebEngine – komplett ohne schweren Electron-Bloat.</em>
</p>

---

## 🚀 Schnellstart

```bash
# Repository klonen
git clone https://github.com/sonictriplex/MatrixWhisper.git
cd MatrixWhisper

# Abhängigkeiten installieren (Fedora)
sudo dnf install python3-pyqt6 python3-pyqt6-webengine

# App starten
python3 matrixwhisper.py
```

Weitere Details findest du auf der Seite [[Installation & Setup]].

---

## 📚 Wiki-Inhalte

### Erste Schritte
- [[Home]] – Diese Seite
- [[Installation & Setup]] – Systemvoraussetzungen und Installation
- [[CLI-Controller]] – Steuerung über die Kommandozeile

### Konfiguration
- [[Einstellungen (Settings)]] – Alle Optionen im Detail
- [[Cache & Session-Reset Guide]] – Wie der Cache funktioniert und wie man ihn zurücksetzt
- [[GPU-Drosselung (Power Saver)]] – Stromsparmodus für Laptops

### Lokalisierung
- [[Sprachunterstützung (i18n)]] – Übersetzungen und Sprachauswahl

### Technische Details
- [[Architektur & Single-Instance]] – IPC-Sperre und CLI-Controller
- [[QWebEngine-Caching im Hintergrund]] – Wie die Qt WebEngine Daten speichert
- [[Smart Mute (Lautloser Wächter)]] – Temporäre Stummschaltung

### Bekannte Probleme
- [[Roadmap & Known Issues]] – Bugs und zukünftige Pläne

### Mitwirken
- [[Contributing]] – Wie du helfen kannst
- [[Lizenz (MIT)]] – Lizenzinformationen

---

## 🎯 Hauptfunktionen auf einen Blick

| Funktion | Beschreibung |
|----------|--------------|
| 🚀 **Leichtgewichtig** | Minimaler RAM- und CPU-Verbrauch (kein Electron) |
| 🌍 **Live-Lokalisierung** | 8 Sprachen, dynamisch umschaltbar |
| 🔋 **GPU-Drosselung** | Hardware-Beschleunigung abschaltbar |
| 📢 **Smart Mute** | Audio für 1h/8h stummschalten |
| 🔍 **HiDPI Zoom** | Skalierung 80 % – 130 % |
| 📥 **Tray-Integration** | Minimieren in den Systemabschnitt |
| 🌙 **Dark Theme** | Erzwungenes dunkles WhatsApp-Design |
| 🧹 **Session-Reset** | Ein Klick löscht alle lokalen Daten |
| 🖥️ **Single-Instance** | Nur eine Instanz, CLI-Steuerung |
| ⚙️ **Sub-Sidebar** | Drei Tabs in den Einstellungen |
| 📂 **Download-Verzeichnis** | Eigener Ordner für Downloads |
| 🚀 **Tray-Start** | Direkt in den Tray starten |
| 🔔 **Native Benachrichtigungen** | System-Notifications bei geschlossenem Fenster |
| 🎧 **Audio-Ausgabegerät** | Auswahl des Audiogeräts (geplant) |

---

## 🐛 Bekannte Probleme

Siehe [[Roadmap & Known Issues]] für eine vollständige Liste.

---

## 🤝 Mitwirken

Beiträge sind willkommen! Erstelle ein Issue oder einen Pull Request im [GitHub-Repository](https://github.com/sonictriplex/MatrixWhisper).

---

<p align="center">
  <sub>Entwickelt mit ❤️ von <strong>sonictriplex</strong></sub>
</p>
