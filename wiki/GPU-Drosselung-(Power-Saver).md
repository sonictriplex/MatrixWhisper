# 🔋 GPU-Drosselung (Power Saver)

## Übersicht

Die GPU-Drosselung deaktiviert die Hardware-Beschleunigung der Qt WebEngine. Dies reduziert den Stromverbrauch und die Wärmeentwicklung – ideal für Laptops und mobile Einsätze.

---

## Aktivierung

1. Öffne die **Einstellungen** (Tab **Erweitert**).
2. Aktiviere den Schalter **Stromsparmodus (GPU-Drossel)**.
3. Die Änderung wird nach einem Neustart der App wirksam.

---

## Status-Anzeige

- **GPU deaktiviert (Stromsparmodus aktiv)** – Die Hardware-Beschleunigung ist ausgeschaltet.
- **GPU aktiv (Standard)** – Die Hardware-Beschleunigung ist eingeschaltet.

---

## Technische Details

Beim Start der App wird geprüft, ob die GPU-Drosselung in der Konfigurationsdatei `config.json` aktiviert ist. Falls ja, werden die Argumente `--disable-gpu` und `--disable-software-rasterizer` an die Qt WebEngine übergeben.

```python
if raw_cfg.get("disable_gpu_acceleration", False):
    sys.argv.extend(["--disable-gpu", "--disable-software-rasterizer"])
```

---

## Verwandte Themen

- [[Einstellungen (Settings)]]
- [[Home]]
- [[Roadmap & Known Issues]]
````
````

wiki/Sprachunterstützung-(i18n).md
````
<<<<<<< SEARCH
# 🔋 GPU-Drosselung (Power Saver)

## Übersicht

Die GPU-Drosselung deaktiviert die Hardware-Beschleunigung der Qt WebEngine. Dies reduziert den Stromverbrauch und die Wärmeentwicklung – ideal für Laptops und mobile Einsätze.

---

## Aktivierung

1. Öffne die **Einstellungen** (Tab **Erweitert**).
2. Aktiviere den Schalter **Stromsparmodus (GPU-Drossel)**.
3. Die Änderung wird nach einem Neustart der App wirksam.

---

## Status-Anzeige

- **GPU deaktiviert (Stromsparmodus aktiv)** – Die Hardware-Beschleunigung ist ausgeschaltet.
- **GPU aktiv (Standard)** – Die Hardware-Beschleunigung ist eingeschaltet.

---

## Technische Details

Beim Start der App wird geprüft, ob die GPU-Drosselung in der Konfigurationsdatei `config.json` aktiviert ist. Falls ja, werden die Argumente `--disable-gpu` und `--disable-software-rasterizer` an die Qt WebEngine übergeben.

```python
if raw_cfg.get("disable_gpu_acceleration", False):
    sys.argv.extend(["--disable-gpu", "--disable-software-rasterizer"])
```

---

## Verwandte Themen

- [[Einstellungen (Settings)]]
- [[Home]]
- [[Roadmap & Known Issues]]
