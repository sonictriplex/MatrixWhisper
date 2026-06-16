<p align="center">
  <img src="media/media-matrix-logo.png" alt="MatrixWhisper Logo" width="128" height="128">
</p>

<h1 align="center">MatrixWhisper v2.3</h1>

<p align="center">
  <strong>A highly optimized, native, and lightweight WhatsApp Web Client for Linux Desktops.</strong><br>
  <em>Built with Python 3, PyQt6, and QtWebEngine — completely free of heavy Electron bloat.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Linux-blue?style=flat-square&logo=linux" alt="Linux">
  <img src="https://img.shields.io/badge/Language-Python%203-green?style=flat-square&logo=python" alt="Python 3">
  <img src="https://img.shields.io/badge/Framework-PyQt6-darkbadge?style=flat-square&logo=qt" alt="PyQt6">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="MIT License">
</p>

---

## 🇩🇪 Beschreibung (Deutsch)

**MatrixWhisper** ist ein maßgeschneiderter, nativer WhatsApp-Client für Linux-Desktops (perfekt optimiert für KDE Plasma, Fedora, Arch und CachyOS). Im Gegensatz zu offiziellen Desktop-Apps oder generischen Wrappern verzichtet MatrixWhisper komplett auf das ressourcenfressende Electron-Framework und setzt stattdessen auf eine schlanke, native Qt6-Architektur. 

### Hauptmerkmale:
* 🚀 **Extrem Leichtgewichtig:** Minimaler RAM- und CPU-Verbrauch dank nativem PyQt6 & QtWebEngine.
* 🌍 **Echte Live-Lokalisierung:** Vollwertige, dynamische On-The-Fly-Übersetzung der Benutzeroberfläche in 8 Sprachen (DE, EN, ES, FR, IT, NL, PT, PL).
* 🔋 **Stromsparmodus (GPU-Drossel):** Schaltet auf Wunsch die Hardware-Beschleunigung der WebEngine komplett ab – ideal, um unterwegs im Camper-Einsatz oder auf Laptops wertvolle Akkulaufzeit zu sparen.
* 📢 **Lautloser Wächter (Smart Mute):** Schaltet die Audioausgabe der App temporär (z.B. für 1h oder 8h) stumm, ohne die globalen System-Benachrichtigungen zu blockieren.
* 🔍 **HiDPI & Ultrawide Zoom:** Stufenlose Skalierung (80% - 130%) für gestochen scharfe Darstellung auf 4K- oder 34-Zoll-Ultrawide-Monitoren.
* 📥 **Tray-Integration:** Schließen des Fensters minimiert die App elegant in den Systemabschnitt der Taskleiste. Inklusive unread-Nachrichten-Badge im App- und Tray-Icon!
* 🌙 **Erzwungenes Dark Theme:** Injiziert das dunkle WhatsApp-Design direkt beim Laden der Seite.

---

## 🇬🇧 Description (English)

**MatrixWhisper** is a tailored, native WhatsApp client for Linux desktops. By avoiding heavy Electron-based wrappers, it delivers a high-performance messaging experience utilizing the native Qt6 ecosystem.

### Key Features:
* 🚀 **Ultra Lightweight:** Minimal RAM and CPU footprint compared to standard Electron wrappers.
* 🌍 **On-The-Fly Internationalization:** Dynamic, instant UI translation supporting 8 languages (DE, EN, ES, FR, IT, NL, PT, PL).
* 🔋 **Power Saver Mode (GPU Throttle):** Completely disable hardware acceleration to preserve precious battery capacity while traveling or working remotely.
* 📢 **Silent Sentinel (Smart Mute):** Quick-mute audio output for 1 hour or 8 hours via the settings panel or system tray shortcut.
* 🔍 **HiDPI & Ultrawide Scaling:** Fine-tune your layout scale (80% - 130%) optimized for high-res screens and ultrawide setups.
* 📥 **Smart Tray Integration:** Minimizes to the system tray on close with a native unread message counter badge on both the window and tray icons.

---

## 🛠️ Installation & Setup

### Prerequisites (Anforderungen)
Make sure you have Python 3 and the required Qt6 libraries installed on your Linux system.

**For Fedora / RedHat:**
```bash
sudo dnf install python3-pyqt6 python3-pyqt6-webengine
