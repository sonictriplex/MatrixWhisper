# ⚙️ Einstellungen (Settings)

## Übersicht

Die Einstellungsseite von MatrixWhisper v2.8.0 wurde komplett überarbeitet und verwendet jetzt ein **Modular Tabbed Design** mit einer **Sub-Sidebar** (linke Navigation). Die Seite ist in drei Tabs unterteilt:

| Tab | Inhalt |
|-----|--------|
| **Allgemein** | Autostart, Tray-Verhalten, Start-Modus, Sprache, Zoom |
| **Audio & Medien** | Audio-Ausgabegerät, Smart Mute, Download-Verzeichnis, Native Benachrichtigungen |
| **Erweitert** | Dark Theme, Zoom-Slider, GPU-Drosselung, Session-Reset |

---

## Sub-Sidebar (linke Navigation)

Die Sub-Sidebar wird im Code mit `QListWidget` erstellt und enthält drei Einträge:

```python
self.sub_sidebar.addItem("⚙️" + t["tab_general"])
self.sub_sidebar.addItem("🎧" + t["tab_media"])
self.sub_sidebar.addItem("🛠️" + t["tab_advanced"])
```

Die Auswahl eines Eintrags wechselt den sichtbaren Tab im `QStackedWidget` (`self.settings_tabs`). Die Verbindung erfolgt über `currentRowChanged.connect(self.switch_settings_tab)`.

---

## Live-Lokalisierung (On‑The‑Fly Übersetzung)

Alle UI-Texte werden aus dem `TRANSLATIONS`-Dictionary geladen. Die Methode `retranslate_ui()` aktualisiert alle Labels, Buttons und die Sub-Sidebar dynamisch, ohne die App neu starten zu müssen.

Die Sprachauswahl erfolgt über eine `QComboBox` im Tab **Allgemein**. Beim Wechsel wird `change_language_selection()` aufgerufen, die:

1. `self.selected_language` aktualisiert
2. `self.save_settings()` aufruft
3. `self.ui_lang = self.determine_ui_language_key()` neu berechnet
4. `self.retranslate_ui()` ausführt
5. `self.setup_tray_menu()` aktualisiert

---

## Smart Mute (Lautloser Wächter)

Im Tab **Audio & Medien** befindet sich die Smart-Mute-Sektion. Sie bietet drei Buttons:

- **1h Stumm** – Schaltet die Audioausgabe für eine Stunde stumm
- **8h Stumm** – Schaltet die Audioausgabe für acht Stunden stumm
- **Reset** – Hebt die Stummschaltung sofort auf

Die Methode `activate_smart_mute(hours)` verwendet einen `QTimer` mit `timeout.connect(self.deactivate_smart_mute)` und `start(milliseconds)`. Der Timer wird korrekt gestoppt, wenn ein neuer Befehl kommt.

---

## Zoom-Faktor

Im Tab **Erweitert** befindet sich ein `QSlider` (80 % – 130 %). Der Wert wird in `self.zoom_factor` gespeichert und auf den Browser angewendet:

```python
self.browser.setZoomFactor(self.zoom_factor)
```

Die Änderung wird sofort sichtbar und in der Konfigurationsdatei `config.json` gespeichert.

---

## Verwandte Themen

- [[Cache & Session-Reset Guide]]
- [[Architektur & Single-Instance]]
- [[Roadmap & Known Issues]]
