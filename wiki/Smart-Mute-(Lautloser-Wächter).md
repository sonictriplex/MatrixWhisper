# 📢 Smart Mute (Lautloser Wächter)

## Übersicht

Der **Lautlose Wächter** (Smart Mute) schaltet die Audioausgabe von MatrixWhisper temporär stumm – ohne die globalen System-Benachrichtigungen zu blockieren.

---

## Funktionen

- **1h Stumm** – Audio für eine Stunde stummschalten
- **8h Stumm** – Audio für acht Stunden stummschalten
- **Reset** – Stummschaltung sofort aufheben

---

## Bedienung

### Über die Einstellungen

1. Öffne die **Einstellungen** (Tab **Audio & Medien**).
2. Klicke auf **1h Stumm** oder **8h Stumm**.
3. Der Status wird im Label angezeigt (z. B. „Stumm bis 14:30“).

### Über das Tray-Menü

- Rechtsklick auf das Tray-Icon → **Stummschalten (8h Schnellwahl)** aktivieren/deaktivieren.

### Über die Kommandozeile

```bash
python3 matrixwhisper.py --mute
```

---

## Technische Details

Die Methode `activate_smart_mute(hours)` verwendet einen `QTimer` mit `timeout.connect(self.deactivate_smart_mute)` und `start(milliseconds)`. Der Timer wird korrekt gestoppt, wenn ein neuer Befehl kommt.

```python
def activate_smart_mute(self, hours):
    self.web_page.setAudioMuted(True)
    self.mute_timer.stop()
    self.mute_timer.timeout.connect(self.deactivate_smart_mute)
    self.mute_timer.start(int(hours * 3600000))
```

---

## Verwandte Themen

- [[Einstellungen (Settings)]]
- [[CLI-Controller]]
- [[Home]]
