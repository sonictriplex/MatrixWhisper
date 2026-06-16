# 🍏 MatrixWhisper v2.0

> **MatrixWhisper!** Ein hochoptimierter, schlanker und nativer WhatsApp-Web-Client für Linux-Desktops, geschrieben in purem Python 3 und PyQt6. Keine Electron-Ressourcenfresser, dafür maximale Performance und volle Kontrolle.

---

## 🚀 Key Features

* **📦 Pure PyQt6 Architecture:** Extrem ressourcensparend und blitzschnell im Vergleich zu herkömmlichen Electron-Wrappern.
* **🔍 HiDPI & Ultrawide Perfect Zoom:** Stufenlose Skalierung der Oberfläche von 80% bis 130% mit persistenter Speicherung – optimiert für 34-Zoll- und Ultrawide-Setups.
* **🔋 Battery-Saver (GPU Throttle):** Optionale Deaktivierung der Hardware-Beschleunigung der WebEngine, um unterwegs im Camper oder auf dem Laptop wertvolle Milliwatt Akku zu sparen.
* **📢 Smart Mute (Lautloser Wächter):** Temporäre Audio-Stummschaltung (1h / 8h) direkt aus der App oder dem System-Tray mit automatischer Restzeitberechnung bei App-Neustart.
* **🌐 Euro-Tour Ready (Dropdown-Locales):** Liest vollautomatisch deine Linux-Systemsprache aus, lässt sich aber flexibel im Menü auf Deutsch, Englisch, Spanisch, Französisch, Italienisch, Niederländisch, Portugiesisch oder Polnisch zwingen.
* **🎨 Custom UI Engine:** Schickes Dark-Theme, native Qt-Vektor-Icons und animierte Custom-Switch-Toggles mit mathematisch garantiert kreisrunden Punkten.
* **📥 Advanced Tray Integration:** Schließen-Verhalten konfigurierbar (Minimieren ins Tray vs. App killen), dynamischer Badge-Zähler für ungelesene Nachrichten im Systemabschnitt der Taskleiste.

---

## 🛠️ Installation & Start

### 1. Voraussetzungen (Beispiel für Arch/CachyOS/Fedora)
Stelle sicher, dass Python 3 und die Qt6-Bibliotheken auf deinem System installiert sind.

```bash
# Arch Linux / CachyOS
sudo pacman -S python-pyqt6 python-pyqt6-webengine

# Fedora
sudo dnf install python3-pyqt6 python3-pyqt6-webengine
