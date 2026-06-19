<p align="center">
  <img src="media/media-matrix-logo.png" alt="MatrixWhisper Logo" width="128" height="128">
</p>

<h1 align="center">MatrixWhisper v2.8.0</h1>

<p align="center">
  <strong>Ein hochoptimierter, nativer WhatsApp Web Client für Linux Desktops.</strong><br>
  <em>Gebaut mit Python 3, PyQt6 und QtWebEngine – komplett ohne schweren Electron-Bloat.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Linux-blue?style=flat-square&logo=linux" alt="Linux">
  <img src="https://img.shields.io/badge/Language-Python%203-green?style=flat-square&logo=python" alt="Python 3">
  <img src="https://img.shields.io/badge/Framework-PyQt6-darkbadge?style=flat-square&logo=qt" alt="PyQt6">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="MIT License">
</p>

---

## 🇩🇪 Beschreibung (Deutsch)

**MatrixWhisper** ist ein maßgeschneiderter, nativer WhatsApp-Client für Linux-Desktops (perfekt optimiert für KDE Plasma, Fedora, Arch und CachyOS). Im Gegensatz zu offiziellen Desktop-Apps oder generischen Wrappern verzichtet MatrixWhisper komplett auf das ressourcenfressende Electron-Framework und setzt stattdessen auf eine schlanke, native Qt6-Architektur. Version 2.8.0 bringt eine überarbeitete Einstellungsseite mit Sub-Sidebar, verbesserte GPU-Drosselung, eine neue Single-Instance-Architektur mit CLI-Controller, einstellbares Download-Verzeichnis, Start-Modus (Tray-Start), native Benachrichtigungen, Audio-Ausgabegerät-Auswahl und erweiterte Lokalisierung mit 8 Sprachen.

### Hauptmerkmale

- 🚀 **Extrem Leichtgewichtig** – Minimaler RAM- und CPU-Verbrauch dank nativem PyQt6 & QtWebEngine (kein Electron-Bloat).
- 🌍 **Echte Live-Lokalisierung** – Vollwertige, dynamische On‑The‑Fly‑Übersetzung der Benutzeroberfläche in **8 Sprachen** (DE, EN, ES, FR, IT, NL, PT, PL). Sowohl die App‑UI als auch das Tray‑Menü schalten sich in Echtzeit um.
- 🔋 **Stromsparmodus (GPU‑Drossel)** – Schaltet auf Wunsch die Hardware‑Beschleunigung der WebEngine komplett ab – ideal, um unterwegs im Camper‑Einsatz oder auf Laptops wertvolle Akkulaufzeit zu sparen.
- 📢 **Lautloser Wächter (Smart Mute)** – Schaltet die Audioausgabe der App temporär (1h / 8h / Reset) stumm, ohne die globalen System‑Benachrichtigungen zu blockieren. Direkt aus dem Einstellungs‑Panel oder dem System‑Tray steuerbar.
- 🔍 **HiDPI & Ultrawide Zoom** – Stufenlose Skalierung (80 % – 130 %) für gestochen scharfe Darstellung auf 4K‑ oder 34‑Zoll‑Ultrawide‑Monitoren.
- 📥 **Tray‑Integration** – Schließen des Fensters minimiert die App elegant in den Systemabschnitt der Taskleiste. Inklusive **Unread‑Nachrichten‑Badge** im App‑ und Tray‑Icon.
- 🌙 **Erzwungenes Dark Theme** – Injiziert das dunkle WhatsApp‑Design direkt beim Laden der Seite.
- 🧹 **Session-Reset & Cache-Bereinigung** – Ein Klick löscht alle lokalen Daten und ermöglicht eine saubere Neu-Anmeldung mit QR-Code.
- 🖥️ **Single-Instance-Architektur** – Nur eine Instanz der App kann gleichzeitig laufen; CLI-Befehle (--toggle, --mute, --quit) steuern die laufende Instanz.
- ⚙️ **Überarbeitete Einstellungsseite mit Sub-Sidebar** – Alle Optionen sind jetzt in drei Tabs (Allgemein, Audio & Medien, Erweitert) übersichtlich angeordnet.
- 📂 **Download-Verzeichnis** – Lege einen dedizierten Ordner für WhatsApp-Downloads fest.
- 🚀 **Start-Modus (Tray-Start)** – MatrixWhisper beim Öffnen direkt in den Systemabschnitt minimieren.
- 🔔 **Native Benachrichtigungen** – Web-Notifications bei geschlossenem Fenster als native System-Benachrichtigungen anzeigen.
- 🎧 **Audio-Ausgabegerät** – Wähle das Standard-Audiogerät für WhatsApp-Töne und Sprachnachrichten aus. *(Hinweis: Die Umleitung ist derzeit nicht implementiert – siehe Roadmap.)*

---

## 🇬🇧 Description (English)

**MatrixWhisper** is a tailored, native WhatsApp client for Linux desktops. By avoiding heavy Electron‑based wrappers, it delivers a high‑performance messaging experience utilizing the native Qt6 ecosystem. Version 2.8.0 introduces a redesigned settings page with sub‑sidebar, improved GPU throttling, a new single‑instance architecture with CLI controller, configurable download directory, startup behavior (tray boot), native notifications, audio output device selection, and enhanced localization with 8 languages.

### Key Features

- 🚀 **Ultra Lightweight** – Minimal RAM and CPU footprint compared to standard Electron wrappers.
- 🌍 **On‑The‑Fly Internationalization** – Dynamic, instant UI translation supporting **8 languages** (DE, EN, ES, FR, IT, NL, PT, PL). Both the app UI and the tray menu switch in real time.
- 🔋 **Power Saver Mode (GPU Throttle)** – Completely disable hardware acceleration to preserve precious battery capacity while traveling or working remotely.
- 📢 **Silent Sentinel (Smart Mute)** – Quick‑mute audio output for 1 hour or 8 hours via the settings panel or system tray shortcut.
- 🔍 **HiDPI & Ultrawide Scaling** – Fine‑tune your layout scale (80 % – 130 %) optimized for high‑res screens and ultrawide setups.
- 📥 **Smart Tray Integration** – Minimizes to the system tray on close with a native unread message counter badge on both the window and tray icons.
- 🌙 **Forced Dark Theme** – Injects the dark WhatsApp design directly when the page loads.
- 🧹 **Session Reset & Cache Clear** – One click wipes all local data, enabling a clean re‑login with a fresh QR code.
- 🖥️ **Single‑Instance Architecture** – Only one instance of the app can run at a time; CLI commands (--toggle, --mute, --quit) control the running instance.
- ⚙️ **Redesigned Settings Page with Sub‑Sidebar** – All options are now neatly arranged in three tabs (General, Audio & Media, Advanced).
- 📂 **Download Directory** – Set a dedicated folder for WhatsApp downloads.
- 🚀 **Startup Behavior (Tray Boot)** – Minimize MatrixWhisper directly to system tray on launch.
- 🔔 **Native Notifications** – Show web notifications as native system notifications when the window is closed.
- 🎧 **Audio Output Device** – Select the default audio device for WhatsApp tones and voice messages. *(Note: The routing is not yet implemented – see Roadmap.)*

---

## 🛠️ Installation & Setup

### Voraussetzungen / Prerequisites

Stelle sicher, dass Python 3 und die benötigten Qt6‑Bibliotheken auf deinem Linux‑System installiert sind.

Make sure you have Python 3 and the required Qt6 libraries installed on your Linux system.

**Fedora / RedHat:**
```bash
sudo dnf install python3-pyqt6 python3-pyqt6-webengine
```

**Arch Linux / CachyOS / Manjaro:**
```bash
sudo pacman -S python-pyqt6 python-pyqt6-webengine
```

### Schnellstart / Quick Start

1. Repository klonen / Clone the repository:
   ```bash
   git clone https://github.com/sonictriplex/MatrixWhisper.git
   cd MatrixWhisper
   ```

2. Anwendung starten / Run the application:
   ```bash
   python3 matrixwhisper.py
   ```

### CLI-Controller (ab Version 2.8.0)

Die App kann über die Kommandozeile gesteuert werden, ohne eine zweite Instanz zu starten:

```bash
# Fenster ein-/ausblenden
python3 matrixwhisper.py --toggle

# Audio für 8 Stunden stummschalten
python3 matrixwhisper.py --mute

# App beenden
python3 matrixwhisper.py --quit

# Fenster anzeigen (falls minimiert) – Achtung: noch nicht implementiert (siehe Roadmap)
python3 matrixwhisper.py --show
```

### CLI Controller (since v2.8.0)

You can control the app from the command line without launching a second instance:

```bash
# Toggle window visibility
python3 matrixwhisper.py --toggle

# Mute audio for 8 hours
python3 matrixwhisper.py --mute

# Quit the app
python3 matrixwhisper.py --quit

# Show the window (if hidden) – Note: not yet implemented (see Roadmap)
python3 matrixwhisper.py --show
```

---

## 🗺️ Roadmap / Bekannte Probleme / Known Issues

### 1. `--show`-Argument fehlt im Parser / `--show` argument missing in parser

**🇩🇪** Die README erwähnt den Befehl `python3 matrixwhisper.py --show`, aber der Argument-Parser in `matrixwhisper.py` kennt dieses Argument nicht. Ein Aufruf mit `--show` führt zu einem Fehler.  
**Lösung:** `parser.add_argument("--show", action="store_true")` im `__main__`-Block ergänzen.

**🇬🇧** The README mentions the command `python3 matrixwhisper.py --show`, but the argument parser in `matrixwhisper.py` does not know this argument. Calling `--show` results in an error.  
**Solution:** Add `parser.add_argument("--show", action="store_true")` in the `__main__` block.

---

### 2. Smart-Mute-Timer funktioniert nicht / Smart Mute timer not working

**🇩🇪** In `activate_smart_mute` wird `self.mute_timer.singleShot(...)` verwendet. `singleShot` ist eine statische Methode, die keinen Timer zurückgibt. Der erstellte `QTimer` wird nie gestartet, sodass die Stummschaltung nie automatisch aufgehoben wird.  
**Lösung:** Stattdessen `self.mute_timer.timeout.connect(self.deactivate_smart_mute)` und `self.mute_timer.start(hours * 3600000)` verwenden.

**🇬🇧** In `activate_smart_mute`, `self.mute_timer.singleShot(...)` is used. `singleShot` is a static method that does not return a timer. The created `QTimer` is never started, so the mute is never automatically deactivated.  
**Solution:** Use `self.mute_timer.timeout.connect(self.deactivate_smart_mute)` and `self.mute_timer.start(hours * 3600000)` instead.

---

### 3. Sub-Sidebar in den Einstellungen (bereits implementiert) / Sub‑Sidebar in settings (already implemented)

**🇩🇪** Die Einstellungsseite verwendet eine Sub-Sidebar mit drei Tabs (Allgemein, Audio & Medien, Erweitert). Dieses Feature ist voll funktionsfähig und erfordert keine Änderungen.

**🇬🇧** The settings page uses a sub‑sidebar with three tabs (General, Audio & Media, Advanced). This feature is fully functional and requires no changes.

---

### 4. Audio-Ausgabegerät-Umleitung nicht implementiert / Audio output device routing not implemented

**🇩🇪** Die Methode `change_audio_device` gibt nur eine Print-Anweisung aus, leitet den Audio-Stream aber nicht tatsächlich um. Die Auswahl in den Einstellungen hat derzeit keine Wirkung.  
**Lösung:** Eine echte Qt-Multimedia-Routing-Implementierung einbauen (z. B. `QAudioSink` mit dem gewählten Gerät).

**🇬🇧** The `change_audio_device` method only prints a message; it does not actually route the audio stream. The selection in the settings currently has no effect.  
**Solution:** Implement a proper Qt Multimedia routing (e.g., `QAudioSink` with the selected device).

---

## 📄 Lizenz / License

Dieses Projekt ist unter der **MIT License** lizenziert – siehe die Datei `LICENSE` für Details.

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

<p align="center">
  <sub>Entwickelt mit ❤️ von <strong>sonictriplex</strong></sub>
</p>
