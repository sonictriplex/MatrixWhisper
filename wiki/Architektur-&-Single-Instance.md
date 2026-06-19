# 🖥️ Architektur & Single-Instance

## Übersicht

MatrixWhisper verwendet eine **Single-Instance-Architektur**, die sicherstellt, dass immer nur eine Instanz der App gleichzeitig läuft. Dies wird durch einen **QLocalServer** (IPC-Server) realisiert, der einen Unix-Socket im Runtime-Verzeichnis erstellt.

---

## Wie funktioniert die IPC-Sperre?

Beim Start der App wird in `init_single_instance_server()` ein `QLocalServer` erstellt, der auf dem Socket-Pfad lauscht:

```python
runtime_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.RuntimeLocation)
self.socket_path = os.path.join(runtime_dir, "matrixwhisper_socket")
QLocalServer.removeServer(self.socket_path)
self.instance_server.listen(self.socket_path)
self.instance_server.newConnection.connect(self.handle_remote_activation)
```

Wenn eine zweite Instanz gestartet wird, versucht sie, sich mit dem Socket zu verbinden. Gelingt dies, sendet sie einen Befehl (z. B. `toggle`, `mute`, `quit`, `show`) und beendet sich sofort.

---

## CLI-Controller

Der CLI-Controller wird im `__main__`-Block mit `argparse` definiert:

```python
parser = argparse.ArgumentParser(description="MatrixWhisper CLI Controller")
parser.add_argument("--minimized", action="store_true")
parser.add_argument("--toggle", action="store_true")
parser.add_argument("--mute", action="store_true")
parser.add_argument("--quit", action="store_true")
parser.add_argument("--show", action="store_true")
```

### Befehlsverarbeitung

1. **Socket-Verbindung** – Der Parser versucht, sich mit dem laufenden Server zu verbinden.
2. **Befehl senden** – Je nach Argument wird ein Befehl als Text gesendet:
   - `--toggle` → `"toggle"`
   - `--mute` → `"mute"`
   - `--quit` → `"quit"`
   - `--show` → `"show"`
3. **Server empfängt** – `handle_remote_activation()` liest den Befehl und ruft die entsprechende Methode auf:
   - `toggle` / `show` → Fenster ein-/ausblenden
   - `mute` → `activate_smart_mute(8)`
   - `quit` → `quit_application()`

### Beispiel

```bash
# Fenster ein-/ausblenden
python3 matrixwhisper.py --toggle

# Audio für 8 Stunden stummschalten
python3 matrixwhisper.py --mute

# App beenden
python3 matrixwhisper.py --quit

# Fenster anzeigen (falls minimiert)
python3 matrixwhisper.py --show
```

---

## Warum Single-Instance?

- **Ressourcenschonung** – Nur eine WebEngine-Instanz läuft.
- **Keine doppelten Login-Probleme** – WhatsApp erlaubt nur eine aktive Web-Session.
- **CLI-Steuerung** – Der Benutzer kann die laufende Instanz bequem von der Kommandozeile aus steuern.

---

## Verwandte Themen

- [[Einstellungen (Settings)]]
- [[Cache & Session-Reset Guide]]
- [[Roadmap & Known Issues]]
