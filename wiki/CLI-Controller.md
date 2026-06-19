# 🖥️ CLI-Controller

## Übersicht

MatrixWhisper kann über die Kommandozeile gesteuert werden, ohne eine zweite Instanz zu starten. Der CLI-Controller verbindet sich mit der laufenden Instanz über einen Unix-Socket und sendet Befehle.

---

## Verfügbare Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `--toggle` | Fenster ein-/ausblenden |
| `--mute` | Audio für 8 Stunden stummschalten |
| `--quit` | App beenden |
| `--show` | Fenster anzeigen (falls minimiert) |
| `--minimized` | App minimiert starten (nur beim ersten Start) |

---

## Beispiele

```bash
# Fenster ein-/ausblenden
python3 matrixwhisper.py --toggle

# Audio für 8 Stunden stummschalten
python3 matrixwhisper.py --mute

# App beenden
python3 matrixwhisper.py --quit

# Fenster anzeigen (falls minimiert)
python3 matrixwhisper.py --show

# App minimiert starten
python3 matrixwhisper.py --minimized
```

---

## Technische Details

Der CLI-Controller verwendet `QLocalSocket`, um sich mit dem `QLocalServer` der laufenden Instanz zu verbinden. Der Socket-Pfad ist `~/.local/share/matrixwhisper_socket` (abhängig vom XDG-Runtime-Verzeichnis).

---

## Verwandte Themen

- [[Architektur & Single-Instance]]
- [[Home]]
- [[Einstellungen (Settings)]]
