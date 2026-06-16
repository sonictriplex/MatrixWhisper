import os
from PIL import Image, ImageDraw

def create_circular_logo(input_path, output_path, size=512):
    # 1. Ein neues, quadratisches Bild mit transparentem Hintergrund erstellen (RGBA)
    # Wir bauen es in doppelter Größe (1024x1024) für perfektes Antialiasing beim Skalieren
    working_size = size * 2
    img = Image.new("RGBA", (working_size, working_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Farben definieren (WhatsApp-Grün)
    green_color = (37, 211, 102, 255)
    white_color = (255, 255, 255, 255)

    # Dimensionen für die Kreise festlegen
    padding = 10
    outer_thick = 12
    gap = 8
    inner_thick = 6

    # Äußerer Rahmen
    out_start = padding
    out_end = working_size - padding
    draw.ellipse([out_start, out_start, out_end, out_end], fill=green_color)

    # Der Zwischenraum (Lücke)
    gap_start = out_start + outer_thick
    gap_end = out_end - outer_thick
    draw.ellipse([gap_start, gap_start, gap_end, gap_end], fill=(0, 0, 0, 0))

    # Innerer Rahmen
    in_start = gap_start + gap
    in_end = gap_end - gap
    draw.ellipse([in_start, in_start, in_end, in_end], fill=green_color)

    # Weißer Hintergrund-Kreis
    bg_start = in_start + inner_thick
    bg_end = in_end - inner_thick
    draw.ellipse([bg_start, bg_start, bg_end, bg_end], fill=white_color)

    # 2. Das originale Logo laden und vorbereiten
    if not os.path.exists(input_path):
        print(f"Fehler: {input_path} wurde nicht gefunden!")
        return

    logo = Image.open(input_path).convert("RGBA")

    # Wir berechnen die optimale Größe für das "m", damit es sauber im inneren Kreis sitzt
    # Der weiße Bereich hat einen Durchmesser von (bg_end - bg_start)
    inner_diameter = bg_end - bg_start
    target_width = int(inner_diameter * 0.65) # 65% des Platzes ausnutzen, damit es nicht gequetscht wirkt

    # Proportionen beibehalten beim Skalieren
    aspect_ratio = logo.height / logo.width
    target_height = int(target_width * aspect_ratio)

    logo_resized = logo.resize((target_width, target_height), Image.Resampling.LANCZOS)

    # Position berechnen, um das Logo exakt in die Mitte zu setzen
    paste_x = (working_size - target_width) // 2
    paste_y = (working_size - target_height) // 2

    # Das Logo auf den weißen Hintergrund klatschen (Alpha-Kanal als Maske nutzen!)
    img.paste(logo_resized, (paste_x, paste_y), logo_resized)

    # 3. Das fertige Bild auf die gewünschte Zielgröße herunterskalieren (glättet die Kanten)
    final_img = img.resize((size, size), Image.Resampling.LANCZOS)

    # Speichern
    final_img.save(output_path, "PNG")
    print(f"Erfolg! Das neue App-Icon wurde unter '{output_path}' gespeichert.")

if __name__ == "__main__":
    # Pfade anpassen falls nötig
    create_circular_logo("media-matrix-logo.png", "media-matrix-logo.png")
