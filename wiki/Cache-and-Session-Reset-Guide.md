# 🧹 Cache & Session-Reset Guide

## Übersicht

MatrixWhisper speichert alle WhatsApp-Web-Daten (Cookies, LocalStorage, IndexedDB, Service Worker) in zwei dedizierten Ordnern:

| Pfad | Zweck |
|------|-------|
| `~/.local/share/MatrixWhisper/storage` | Persistente Speicherdaten (LocalStorage, IndexedDB, Service Worker) |
| `~/.cache/MatrixWhisper/cache` | Temporäre Cache-Daten (HTTP-Cache, Bild-Cache) |

Diese Trennung folgt den **XDG Base Directory Specifications** und sorgt dafür, dass die App auch nach einem System-Neustart den Login-Zustand behält.

---

## Wie funktioniert das QWebEngine-Caching?

Die Qt WebEngine (Chromium-Basis) verwendet ein mehrstufiges Caching-System:

1. **HTTP-Cache** – Speichert heruntergeladene Ressourcen (HTML, CSS, JS, Bilder) für schnelleres Laden.
2. **LocalStorage** – Schlüssel-Wert-Datenbank für Webseiten (z. B. WhatsApp-Einstellungen).
3. **IndexedDB** – Strukturierte Datenbank für größere Datenmengen (z. B. Nachrichten-Cache).
4. **Service Worker** – Hintergrund-Skripte für Offline-Funktionalität und Push-Benachrichtigungen.

MatrixWhisper konfiguriert diese Pfade im Code:

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

## Der „Session-Reset“-Button

In den **Erweiterten Einstellungen** (Tab „Erweitert“) befindet sich der Button **„Session & Cache zurücksetzen“**.

### Was passiert beim Klick?

1. **Seite leeren** – Der Browser wird auf `about:blank` gesetzt.
2. **HTTP-Cache löschen** – `self.profile.clearHttpCache()` entfernt alle zwischengespeicherten Ressourcen.
3. **Cookies löschen** – `self.profile.cookieStore().deleteAllCookies()` entfernt alle gespeicherten Cookies.
4. **Ordner löschen** – Die beiden Ordner `storage` und `cache` werden rekursiv gelöscht und neu angelegt.
5. **Neu laden** – Die Seite wird erneut auf `https://web.whatsapp.com` geladen.

Der relevante Code:

```python
def reset_cache_and_session(self):
    self.browser.setUrl(QUrl("about:blank"))
    self.profile.clearHttpCache()
    self.profile.cookieStore().deleteAllCookies()
    try:
        if os.path.exists(self.storage_path):
            shutil.rmtree(self.storage_path)
        if os.path.exists(self.cache_path):
            shutil.rmtree(self.cache_path)
        os.makedirs(self.storage_path, exist_ok=True)
        os.makedirs(self.cache_path, exist_ok=True)
    except Exception:
        pass
    self.browser.setUrl(QUrl("https://web.whatsapp.com"))
    self.switch_view(0)
```

---

## Wann sollte man den Reset durchführen?

- **QR-Code abgelaufen** – Wenn WhatsApp einen neuen QR-Code verlangt, aber die Seite nicht richtig lädt.
- **Login-Probleme** – Nach einem Passwortwechsel oder bei „Gerät nicht erkannt“.
- **Performance-Probleme** – Wenn die App nach langer Nutzung träge wird.
- **Testzwecke** – Um einen frischen Zustand ohne gespeicherte Daten zu simulieren.

---

## Manuelles Löschen (ohne App)

Falls die App nicht startet, kannst du die Ordner auch manuell löschen:

```bash
rm -rf ~/.local/share/MatrixWhisper/storage
rm -rf ~/.cache/MatrixWhisper/cache
```

Danach startest du die App neu – sie erstellt die Ordner automatisch neu.

---

## Tipps & Hinweise

- **Keine Auswirkungen auf andere Apps** – Die Ordner sind exklusiv für MatrixWhisper.
- **Kein Datenverlust** – WhatsApp-Nachrichten werden auf den Servern von WhatsApp gespeichert, nicht lokal.
- **Nach dem Reset** – Du musst dich erneut mit dem QR-Code anmelden.
- **Automatische Bereinigung** – Der Cache wird nicht automatisch geleert; der Reset-Button ist die einzige Möglichkeit.

---

## Verwandte Themen

- [[Einstellungen (Settings)]]
- [[Architektur & Single-Instance]]
- [[Roadmap & Known Issues]]
