# 🐛 Roadmap & Known Issues

## Übersicht

Diese Seite dokumentiert bekannte Probleme und zukünftige Pläne für MatrixWhisper v2.8.0.

---

## Bekannte Probleme

### 1. YouTube-Cookie-Eigenheit

**Problem:** Wenn ein YouTube-Video in WhatsApp geteilt wird, kann es vorkommen, dass die Vorschau nicht geladen wird oder ein Cookie-Fehler auftritt. Dies liegt daran, dass die Qt WebEngine standardmäßig keine YouTube-Cookies speichert.

**Status:** Unter Beobachtung. Eine mögliche Lösung wäre, die Cookie-Policy auf `ForcePersistentCookies` zu setzen (bereits implementiert). Falls das Problem weiterhin besteht, könnte ein separater Cookie-Container für YouTube nötig sein.

---

### 2. Audio-Ausgabegerät-Umleitung nicht implementiert

**Problem:** Die Methode `change_audio_device` gibt nur eine Print-Anweisung aus, leitet den Audio-Stream aber nicht tatsächlich um. Die Auswahl in den Einstellungen hat derzeit keine Wirkung.

**Lösung:** Eine echte Qt-Multimedia-Routing-Implementierung einbauen (z. B. `QAudioSink` mit dem gewählten Gerät).

**Status:** Offen – siehe Roadmap in der README.

---

### 3. `--show`-Argument (behoben)

**Problem:** Der Parser kannte `--show` nicht. **Behoben** in v2.8.0.

---

### 4. Smart-Mute-Timer (behoben)

**Problem:** Der Timer wurde nie gestartet. **Behoben** in v2.8.0.

---

## Zukünftige Pläne

### Flatpak-Veröffentlichung

**Ziel:** MatrixWhisper als Flatpak im Flathub bereitstellen, um eine einfache Installation auf allen Linux-Distributionen zu ermöglichen.

**Status:** In Planung. Dazu muss ein Flatpak-Manifest erstellt werden, das die Abhängigkeiten (PyQt6, QtWebEngine) bündelt.

### Weitere Sprachen

**Ziel:** Unterstützung für weitere Sprachen (z. B. Russisch, Chinesisch, Japanisch).

**Status:** Offen – Übersetzungen können über Pull Requests beigesteuert werden.

### Verbesserte Audio-Umleitung

**Ziel:** Echte Qt-Multimedia-Routing-Implementierung (siehe Punkt 2).

**Status:** Offen.

---

## Mitwirken

Wenn du einen Bug findest oder eine neue Funktion vorschlagen möchtest, erstelle bitte ein Issue im GitHub-Repository.

---

## Verwandte Themen

- [[Einstellungen (Settings)]]
- [[Architektur & Single-Instance]]
- [[Cache & Session-Reset Guide]]
