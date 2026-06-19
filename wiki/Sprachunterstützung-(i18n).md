# 🌍 Sprachunterstützung (i18n)

## Übersicht

MatrixWhisper unterstützt **8 Sprachen** mit dynamischer On‑The‑Fly‑Übersetzung. Die UI und das Tray-Menü schalten sich in Echtzeit um, ohne die App neu starten zu müssen.

---

## Verfügbare Sprachen

| Sprache | Kürzel |
|---------|--------|
| Deutsch | `de` |
| English | `en` |
| Español | `es` |
| Français | `fr` |
| Italiano | `it` |
| Nederlands | `nl` |
| Português | `pt` |
| Polski | `pl` |

---

## Sprachauswahl

1. Öffne die **Einstellungen** (Tab **Allgemein**).
2. Wähle die gewünschte Sprache aus der Dropdown-Liste.
3. Die UI wird sofort aktualisiert.

---

## Technische Details

Alle Übersetzungen sind im `TRANSLATIONS`-Dictionary in `matrixwhisper.py` gespeichert. Die Methode `retranslate_ui()` aktualisiert alle Labels, Buttons und die Sub-Sidebar dynamisch.

```python
def retranslate_ui(self):
    lang = self.ui_lang
    t = TRANSLATIONS[lang]
    # ... alle UI-Elemente aktualisieren
```

---

## Neue Sprache hinzufügen

1. Füge einen neuen Eintrag im `TRANSLATIONS`-Dictionary hinzu (z. B. `"ru"` für Russisch).
2. Füge die Sprache zur `QComboBox` in `__init__` hinzu.
3. Erstelle einen Pull Request im GitHub-Repository.

---

## Verwandte Themen

- [[Einstellungen (Settings)]]
- [[Home]]
- [[Contributing]]
