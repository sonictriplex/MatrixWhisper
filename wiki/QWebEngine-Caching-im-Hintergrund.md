# 🧠 QWebEngine-Caching im Hintergrund

## Übersicht

Die Qt WebEngine (Chromium-Basis) verwendet ein mehrstufiges Caching-System, um die Ladezeiten zu verkürzen und den Login-Zustand zu erhalten.

---

## Cache-Pfade

MatrixWhisper speichert alle Daten in zwei dedizierten Ordnern:

| Pfad | Zweck |
|------|-------|
| `~/.local/share/MatrixWhisper/storage` | Persistente Speicherdaten (LocalStorage, IndexedDB, Service Worker) |
| `~/.cache/MatrixWhisper/cache` | Temporäre Cache-Daten (HTTP-Cache, Bild-Cache) |

---

## Caching-Ebenen

1. **HTTP-Cache** – Speichert heruntergeladene Ressourcen (HTML, CSS, JS, Bilder).
2. **LocalStorage** – Schlüssel-Wert-Datenbank für Webseiten (z. B. WhatsApp-Einstellungen).
3. **IndexedDB** – Strukturierte Datenbank für größere Datenmengen (z. B. Nachrichten-Cache).
4. **Service Worker** – Hintergrund-Skripte für Offline-Funktionalität und Push-Benachrichtigungen.

---

## Konfiguration im Code

```python
self.storage_path = os.path.expanduser("~/.local/share/MatrixWhisper/storage")
self.cache_path = os.path.expanduser("~/.cache/MatrixWhisper/cache")
os.makedirs(self.storage_path, exist_ok=True)
os.makedirs(self.cache_path, exist_ok=True)

self.profile = QWebEngineProfile("MatrixWhisperStorage", self)
self.profile.setPersistentStoragePath(self.storage_path)
self.profile.setCachePath(self.cache_path)
self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
```

---

## Session-Reset

Der **Session-Reset**-Button in den erweiterten Einstellungen löscht beide Ordner und alle Cookies. Siehe [[Cache & Session-Reset Guide]] für Details.

---

## Verwandte Themen

- [[Cache & Session-Reset Guide]]
- [[Einstellungen (Settings)]]
- [[Home]]
````
````

wiki/Smart-Mute-(Lautloser-Wächter).md
````
<<<<<<< SEARCH
# 🧠 QWebEngine-Caching im Hintergrund

## Übersicht

Die Qt WebEngine (Chromium-Basis) verwendet ein mehrstufiges Caching-System, um die Ladezeiten zu verkürzen und den Login-Zustand zu erhalten.

---

## Cache-Pfade

MatrixWhisper speichert alle Daten in zwei dedizierten Ordnern:

| Pfad | Zweck |
|------|-------|
| `~/.local/share/MatrixWhisper/storage` | Persistente Speicherdaten (LocalStorage, IndexedDB, Service Worker) |
| `~/.cache/MatrixWhisper/cache` | Temporäre Cache-Daten (HTTP-Cache, Bild-Cache) |

---

## Caching-Ebenen

1. **HTTP-Cache** – Speichert heruntergeladene Ressourcen (HTML, CSS, JS, Bilder).
2. **LocalStorage** – Schlüssel-Wert-Datenbank für Webseiten (z. B. WhatsApp-Einstellungen).
3. **IndexedDB** – Strukturierte Datenbank für größere Datenmengen (z. B. Nachrichten-Cache).
4. **Service Worker** – Hintergrund-Skripte für Offline-Funktionalität und Push-Benachrichtigungen.

---

## Konfiguration im Code

```python
self.storage_path = os.path.expanduser("~/.local/share/MatrixWhisper/storage")
self.cache_path = os.path.expanduser("~/.cache/MatrixWhisper/cache")
os.makedirs(self.storage_path, exist_ok=True)
os.makedirs(self.cache_path, exist_ok=True)

self.profile = QWebEngineProfile("MatrixWhisperStorage", self)
self.profile.setPersistentStoragePath(self.storage_path)
self.profile.setCachePath(self.cache_path)
self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
```

---

## Session-Reset

Der **Session-Reset**-Button in den erweiterten Einstellungen löscht beide Ordner und alle Cookies. Siehe [[Cache & Session-Reset Guide]] für Details.

---

## Verwandte Themen

- [[Cache & Session-Reset Guide]]
- [[Einstellungen (Settings)]]
- [[Home]]
