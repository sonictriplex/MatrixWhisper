import os
import sys
import re
import math
import time
import json
import locale
import shutil
import argparse
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QApplication, QMainWindow, QSystemTrayIcon, QMenu,
                             QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
                             QStackedWidget, QCheckBox, QLabel, QFrame, QSlider,
                             QComboBox, QScrollArea, QFileDialog, QListWidget)
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings, QWebEngineScript, QWebEnginePage, QWebEngineNotification
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QStandardPaths, Qt, QPoint, QSize, QRectF, QPointF, QTimer, QPropertyAnimation, pyqtProperty
from PyQt6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor, QFont, QPolygonF, QPen, QBrush, QDesktopServices
from PyQt6.QtNetwork import QLocalServer, QLocalSocket
from PyQt6.QtMultimedia import QMediaDevices, QAudioDevice

# --- TRANSLATION DICTIONARY (INTERNATIONALIZATION COMPLETE) ---
TRANSLATIONS = {
    "de": {
        "title": "Einstellungen",
        "tab_general": " Allgemein",
        "tab_media": " Audio & Medien",
        "tab_advanced": " Erweitert",
        "as_title": "Systemstart (Autostart)",
        "as_desc": "Startet MatrixWhisper automatisch mit dem Computer",
        "dm_title": "Erscheinungsbild (Dark Theme)",
        "dm_desc": "Erzwingt das dunkle WhatsApp-Theme in der Web-Oberfläche",
        "tb_title": "Schließen ins Tray (Hintergrund)",
        "tb_desc": "Fenster beim Schließen ('X') im Systemabschnitt verstecken",
        "nt_title": "Native Benachrichtigungen (Tray-Notifications)",
        "nt_desc": "Legt fest, ob Web-Notifications bei geschlossenem/verstecktem Fenster als native System-Benachrichtigungen aufpoppen",
        "gpu_title": "Stromsparmodus (GPU-Drossel)",
        "gpu_desc": "Hardware-Beschleunigung der WebEngine abschalten",
        "gpu_active": "Status: GPU deaktiviert (Stromsparmodus aktiv) ⚠️",
        "gpu_reboot_on": "Effekt nach Neustart: GPU wird abschaltet 🔋",
        "gpu_reboot_off": "Effekt nach Neustart: GPU wieder aktiv (Standard)",
        "mute_title": "Lautloser Wächter (Smart Mute)",
        "mute_active": "Audioausgabe: Aktiv",
        "mute_btn_1h": "1h Stumm",
        "mute_btn_8h": "8h Stumm",
        "mute_btn_reset": "Reset",
        "lang_title": "Anzeigesprache (Locale Profile)",
        "lang_header": "Aktueller Header:",
        "lang_reboot": "Sprache nach Neustart:",
        "zoom_title": "HiDPI / Ultrawide Zoom-Faktor",
        "zoom_desc": "Skalierung der WhatsApp Web-Oberfläche",
        "cache_title": "Bereinigung & Session-Reset",
        "cache_desc": "Einbau eines Buttons, der den lokalen storage-Ordner leert, um sich bei Bedarf mit neuem QR-Code anzumelden",
        "cache_btn": "Session & Cache zurücksetzen",
        "about_desc": "Ein nativer, hochoptimierter WhatsApp-Client mit IPC-Sperre und CLI-Steuerung für Linux.",
        "tray_whisper": "Flüstert im Hintergrund weiter...",
        "tray_open": "Öffnen",
        "tray_quit": "Beenden",
        "tray_mute_shortcut": "Stummschalten (8h Schnellwahl)",
        "dl_title": "Download-Verzeichnis",
        "dl_desc": "Dedizierten Ordner für WhatsApp-Downloads festlegen",
        "dl_btn": "Ordner wählen",
        "start_title": "Start-Modus (Tray-Start)",
        "start_desc": "MatrixWhisper beim Öffnen direkt in den Systemabschnitt minimieren",
        "audio_title": "Audio-Ausgabegerät",
        "audio_desc": "Standard-Audiokanal für WhatsApp-Töne und Sprachnachrichten festlegen",
        "cli_title": "Verfügbare CLI-Terminalbefehle:",
        "cli_hint": "• matrixwhisper.py --toggle  ➔  Fenster zeigen oder verstecken\n• matrixwhisper.py --mute    ➔  Audioausgabe für 8h stummschalten\n• matrixwhisper.py --quit    ➔  Hintergrund-Instanz sauber beenden"
    },
    "en": {
        "title": "Settings",
        "tab_general": " General",
        "tab_media": " Audio & Media",
        "tab_advanced": " Advanced",
        "as_title": "System Startup (Autostart)",
        "as_desc": "Launch MatrixWhisper automatically when starting the computer",
        "dm_title": "Appearance (Dark Theme)",
        "dm_desc": "Force the dark WhatsApp theme in the web interface",
        "tb_title": "Minimize to Tray on Close",
        "tb_desc": "Hide window in the system tray when clicking the close ('X') button",
        "nt_title": "Native Tray Notifications",
        "nt_desc": "Toggle whether web notifications pop up as native system notifications when window is closed or hidden",
        "gpu_title": "Power Saver Mode (GPU Throttle)",
        "gpu_desc": "Disable WebEngine hardware acceleration to save battery",
        "gpu_active": "Status: GPU disabled (Power saver active) ⚠️",
        "gpu_reboot_on": "Effect after restart: GPU will be disabled 🔋",
        "gpu_reboot_off": "Effect after restart: GPU active (Default)",
        "mute_title": "Silent Sentinel (Smart Mute)",
        "mute_active": "Audio output: Active",
        "mute_btn_1h": "1h Mute",
        "mute_btn_8h": "8h Mute",
        "mute_btn_reset": "Reset",
        "lang_title": "Display Language (Locale Profiles)",
        "lang_header": "Current Header:",
        "lang_reboot": "Language after restart:",
        "zoom_title": "HiDPI / Ultrawide Zoom Factor",
        "zoom_desc": "Scale the WhatsApp Web interface layout",
        "cache_title": "Session Reset & Cache Clear",
        "cache_desc": "Clear the local storage directories to enforce a clean logout and fresh QR code scan",
        "cache_btn": "Reset Session & Cache",
        "about_desc": "A native, highly optimized WhatsApp client featuring IPC-lock and CLI control for Linux.",
        "tray_whisper": "Whispering in the background...",
        "tray_open": "Open",
        "tray_quit": "Quit",
        "tray_mute_shortcut": "Mute Audio (8h Shortcut)",
        "dl_title": "Download Directory",
        "dl_desc": "Set a dedicated folder for WhatsApp downloads",
        "dl_btn": "Choose Folder",
        "start_title": "Startup Behavior (Tray Boot)",
        "start_desc": "Minimize MatrixWhisper directly to system tray on launch",
        "audio_title": "Audio Output Device",
        "audio_desc": "Set the default audio channel for WhatsApp tones and voice messages",
        "cli_title": "Available CLI Terminal Commands:",
        "cli_hint": "• matrixwhisper.py --toggle  ➔  Toggle window visibility\n• matrixwhisper.py --mute    ➔  Mute audio playback for 8h\n• matrixwhisper.py --quit    ➔  Cleanly terminate the running client"
    },
    "es": {
        "title": "Ajustes",
        "tab_general": " General",
        "tab_media": " Audio y Medios",
        "tab_advanced": " Avanzado",
        "as_title": "Inicio del sistema (Autostart)",
        "as_desc": "Iniciar MatrixWhisper automáticamente con el ordenador",
        "dm_title": "Apariencia (Tema oscuro)",
        "dm_desc": "Forzar el tema oscuro de WhatsApp en la interfaz web",
        "tb_title": "Cerrar a la bandeja (Segundo plano)",
        "tb_desc": "Ocultar la ventana en la bandeja del sistema al cerrar ('X')",
        "nt_title": "Notificaciones nativas del sistema",
        "nt_desc": "Establece si las notificaciones web devem aparecer como notificaciones del sistema quando la ventana está cerrada",
        "gpu_title": "Modo ahorro de energía (Drossel GPU)",
        "gpu_desc": "Desactivar la aceleración por hardware de WebEngine",
        "gpu_active": "Estado: GPU desactivada (Ahorro de energía activo) ⚠️",
        "gpu_reboot_on": "Efecto tras reiniciar: Se desactivará la GPU 🔋",
        "gpu_reboot_off": "Efecto tras reiniciar: GPU activa (Predeterminado)",
        "mute_title": "Guardián silencioso (Smart Mute)",
        "mute_active": "Salida de audio: Activa",
        "mute_btn_1h": "1h Silencio",
        "mute_btn_8h": "8h Silencio",
        "mute_btn_reset": "Reiniciar",
        "lang_title": "Idioma de visualización (Locales)",
        "lang_header": "Encabezado actual:",
        "lang_reboot": "Idioma tras reiniciar:",
        "zoom_title": "Factor de zoom HiDPI / Ultrawide",
        "zoom_desc": "Escalar la interfaz web de WhatsApp",
        "cache_title": "Restablecer sesión y borrar caché",
        "cache_desc": "Cierra la sesión, elimina las cookies y vacía la caché local",
        "cache_btn": "Restablecer sesión y caché",
        "about_desc": "Un cliente nativo de WhatsApp altamente optimizado para Linux.",
        "tray_whisper": "Susurrando in segundo plano...",
        "tray_open": "Abrir",
        "tray_quit": "Salir",
        "tray_mute_shortcut": "Silenciar (Acceso rápido 8h)",
        "dl_title": "Directorio de descargas",
        "dl_desc": "Establecer una carpeta dedicada para las descargas",
        "dl_btn": "Seleccionar carpeta",
        "start_title": "Comportamiento de inicio",
        "start_desc": "Minimizar directamente a la bandeja al iniciar",
        "audio_title": "Dispositivo de salida de audio",
        "audio_desc": "Establecer el canal de audio predeterminado para WhatsApp",
        "cli_title": "Comandos de terminal CLI disponibles:",
        "cli_hint": "• matrixwhisper.py --toggle  ➔  Mostrar/ocultar ventana\n• matrixwhisper.py --mute    ➔  Silenciar por 8h\n• matrixwhisper.py --quit    ➔  Cerrar la aplicación por completo"
    },
    "fr": {
        "title": "Paramètres",
        "tab_general": " Général",
        "tab_media": " Audio & Médias",
        "tab_advanced": " Avancé",
        "as_title": "Démarrage du système (Autostart)",
        "as_desc": "Lancer MatrixWhisper automatiquement avec l'ordinateur",
        "dm_title": "Apparence (Thème sombre)",
        "dm_desc": "Forcer le thème sombre de WhatsApp dans l'interface web",
        "tb_title": "Fermer dans la zone de notification",
        "tb_desc": "Masquer la fenêtre dans la barre des tâches lors de la fermeture ('X')",
        "nt_title": "Notifications natives du système",
        "nt_desc": "Détermine si les notifications web doivent s'afficher sous forme de notifications système lorsque la fenêtre est fermée",
        "gpu_title": "Mode économie d'énergie (Drossel GPU)",
        "gpu_desc": "Désactiver l'accélération matérielle de WebEngine",
        "gpu_active": "Statut: GPU désactivé (Économie d'énergie active) ⚠️",
        "gpu_reboot_on": "Effet après redémarrage: Le GPU sera désactivé 🔋",
        "gpu_reboot_off": "Effet après redémarrage: GPU actif (Par défaut)",
        "mute_title": "Gardien silencieux (Smart Mute)",
        "mute_active": "Sortie audio: Active",
        "mute_btn_1h": "1h Muet",
        "mute_btn_8h": "8h Muet",
        "mute_btn_reset": "Réinitialiser",
        "lang_title": "Langue d'affichage (Profils de langue)",
        "lang_header": "En-tête actuel:",
        "lang_reboot": "Langue après redémarrage:",
        "zoom_title": "Facteur de zoom HiDPI / Ultrawide",
        "zoom_desc": "Mettre à l'échelle l'interface web de WhatsApp",
        "cache_title": "Réinitialisation de la session & Vidage du cache",
        "cache_desc": "Vous déconnecte, supprime les cookies et vide le cache local",
        "cache_btn": "Réinitialiser la session & le cache",
        "about_desc": "Un client WhatsApp natif hautement optimisé pour les bureaux Linux.",
        "tray_whisper": "Chuchote en arrière-plan...",
        "tray_open": "Ouvrir",
        "tray_quit": "Quitter",
        "tray_mute_shortcut": "Mettre en muet (Raccourci 8h)",
        "dl_title": "Dossier de téléchargement",
        "dl_desc": "Définir un dossier dédié pour les téléchargements WhatsApp",
        "dl_btn": "Choisir un dossier",
        "start_title": "Comportement au démarrage",
        "start_desc": "Minimiser directement dans la zone de notification au lancement",
        "audio_title": "Périphérique de sortie audio",
        "audio_desc": "Définir le canal audio par défaut pour WhatsApp",
        "cli_title": "Commandes du terminal CLI disponibles:",
        "cli_hint": "• matrixwhisper.py --toggle  ➔  Afficher/masquer la fenêtre\n• matrixwhisper.py --mute    ➔  Rendre muet pour 8h\n• matrixwhisper.py --quit    ➔  Quitter proprement l'application"
    },
    "it": {
        "title": "Impostazioni",
        "tab_general": " Generale",
        "tab_media": " Audio & Media",
        "tab_advanced": " Avanzate",
        "as_title": "Avvio automatico",
        "as_desc": "Avvia automaticamente MatrixWhisper all'accensione del computer",
        "dm_title": "Aspetto (Tema scuro)",
        "dm_desc": "Forza il tema scuro di WhatsApp nell'interfaccia web",
        "tb_title": "Riduci nel vassoio di sistema",
        "tb_desc": "Nascondi la finestra nel vassoio di sistema quando si chiude ('X')",
        "nt_title": "Notifiche native di sistema",
        "nt_desc": "Stabilisce se le notifiche web devono apparire como notifiche di sistema quando la finestra è chiusa",
        "gpu_title": "Risparmio energetico (GPU)",
        "gpu_desc": "Disattiva l'accelerazione hardware della WebEngine",
        "gpu_active": "Stato: GPU disattivata (Risparmio energetico attivo) ⚠️",
        "gpu_reboot_on": "Effetto dopo il riavvio: la GPU verrà disattivata 🔋",
        "gpu_reboot_off": "Effetto dopo il riavvio: GPU attiva (Predefinito)",
        "mute_title": "Sentinella silenziosa (Smart Mute)",
        "mute_active": "Uscita audio: Attiva",
        "mute_btn_1h": "1h Silenzia",
        "mute_btn_8h": "8h Silenzia",
        "mute_btn_reset": "Ripristina",
        "lang_title": "Lingua di visualizzazione",
        "lang_header": "Intestazione attuale:",
        "lang_reboot": "Lingua dopo il riavvio:",
        "zoom_title": "Fattore di zoom HiDPI / Ultrawide",
        "zoom_desc": "Ridimensiona il layout dell'interfaccia web di WhatsApp",
        "cache_title": "Ripristino Sessione & Svuotamento Cache",
        "cache_desc": "Disconnette l'utente, elimina i cookie e svuota la cache locale",
        "cache_btn": "Ripristina Sessione & Cache",
        "about_desc": "Un client WhatsApp nativo e altamente optimizzato per desktop Linux.",
        "tray_whisper": "Sussurrando in background...",
        "tray_open": "Apri",
        "tray_quit": "Esci",
        "tray_mute_shortcut": "Disattiva audio (Scelta rapida 8h)",
        "dl_title": "Cartella di download",
        "dl_desc": "Imposta una cartella dedicata per i download di WhatsApp",
        "dl_btn": "Scegli cartella",
        "start_title": "Comportamento all'avvio",
        "start_desc": "Minimizza direttamente nel vassoio di sistema all'avvio",
        "audio_title": "Dispositivo di uscita audio",
        "audio_desc": "Imposta il canale audio predefinito per WhatsApp",
        "cli_title": "Comandi del terminale CLI disponibili:",
        "cli_hint": "• matrixwhisper.py --toggle  ➔  Mostra/nascondi finestra\n• matrixwhisper.py --mute    ➔  Silenzia per 8 ore\n• matrixwhisper.py --quit    ➔  Chiudi l'applicazione in background"
    },
    "nl": {
        "title": "Instellingen",
        "tab_general": " Algemeen",
        "tab_media": " Audio & Media",
        "tab_advanced": " Geavanceerd",
        "as_title": "Systeemstart (Autostart)",
        "as_desc": "MatrixWhisper automatisch starten bij het opstarten van de computer",
        "dm_title": "Uiterlijk (Donker thema)",
        "dm_desc": "Forceer het donkere WhatsApp-thema in de webinterface",
        "tb_title": "Sluiten naar systeemvak",
        "tb_desc": "Verberg het venster in het systeemvak bij het clicking op sluiten ('X')",
        "nt_title": "Native systeemnotificaties",
        "nt_desc": "Bepaalt of webnotificaties als native systeemnotificaties moeten verschijnen wanneer het venster is gesloten",
        "gpu_title": "Energiebesparingsmodus (GPU)",
        "gpu_desc": "Schakel WebEngine hardwareversnelling uit om batterij te sparen",
        "gpu_active": "Status: GPU uitgeschakeld (Energiebesparing actief) ⚠️",
        "gpu_reboot_on": "Effect na herstart: GPU wird uitgeschakeld 🔋",
        "gpu_reboot_off": "Effect na herstart: GPU actief (Standaard)",
        "mute_title": "Stille schildwacht (Smart Mute)",
        "mute_active": "Audio-uitvoer: Actief",
        "mute_btn_1h": "1u Dempen",
        "mute_btn_8h": "8u Dempen",
        "mute_btn_reset": "Reset",
        "lang_title": "Weergavetaal (Taalprofielen)",
        "lang_header": "Huidige header:",
        "lang_reboot": "Taal na herstart:",
        "zoom_title": "HiDPI / Ultrawide zoomfactor",
        "zoom_desc": "Schaal de WhatsApp Web interface-lay-out",
        "cache_title": "Sessiereset & Cache Wissen",
        "cache_desc": "Logt je uit, verwijdert cookies und leegt de lokale cache",
        "cache_btn": "Sessie & Cache herstellen",
        "about_desc": "Een sterk geoptimaliseerde, native WhatsApp-client voor Linux-desktops.",
        "tray_whisper": "Fluistert op de achtergrond...",
        "tray_open": "Openen",
        "tray_quit": "Afsluiten",
        "tray_mute_shortcut": "Audio dempen (8u snelkoppeling)",
        "dl_title": "Downloadmap",
        "dl_desc": "Stel een specifieke map in voor WhatsApp-downloads",
        "dl_btn": "Map kiezen",
        "start_title": "Opstartgedrag",
        "start_desc": "MatrixWhisper bij het opstarten direkt naar het systeemvak minimaliseren",
        "audio_title": "Audio-uitvoerapparaat",
        "audio_desc": "Stel het standaard audiokanaal in voor WhatsApp",
        "cli_title": "Beschikbare CLI-terminalcommando's:",
        "cli_hint": "• matrixwhisper.py --toggle  ➔  Venster tonen/verbergen\n• matrixwhisper.py --mute    ➔  8 uur dempen\n• matrixwhisper.py --quit    ➔  Applicatie netjes afsluiten"
    },
    "pt": {
        "title": "Configurações",
        "tab_general": " Geral",
        "tab_media": " Áudio e Mídia",
        "tab_advanced": " Avançado",
        "as_title": "Iniciar com o sistema",
        "as_desc": "Iniciar o MatrixWhisper automaticamente ao ligar o computador",
        "dm_title": "Aparência (Tema escuro)",
        "dm_desc": "Forçar o tema escuro do WhatsApp na interface web",
        "tb_title": "Fechar para a bandeja de sistema",
        "tb_desc": "Ocultar a janela na bandeja do sistema ao clicar no botão fechar ('X')",
        "gpu_title": "Modo de economia de energia (GPU)",
        "gpu_desc": "Desativar a aceleção de hardware do WebEngine",
        "gpu_active": "Status: GPU desativada (Economia de energia activa) ⚠️",
        "gpu_reboot_on": "Efeito após reiniciar: A GPU será desativada 🔋",
        "gpu_reboot_off": "Efecto após reiniciar: GPU activa (Padrão)",
        "mute_title": "Sentinela silenciosa (Smart Mute)",
        "mute_active": "Saída de áudio: Ativa",
        "mute_btn_1h": "1h Silenciar",
        "mute_btn_8h": "8h Silenciar",
        "mute_btn_reset": "Redefinir",
        "lang_title": "Idioma de exibição",
        "lang_header": "Cabeçalho atual:",
        "lang_reboot": "Idioma após reiniciar:",
        "zoom_title": "Fator de zoom HiDPI / Ultrawide",
        "zoom_desc": "Ajustar o tamanho da interface web do WhatsApp",
        "cache_title": "Redefinição de Sessão & Limpeza de Cache",
        "cache_desc": "Termina a sessão, apaga os cookies e limpa a cache local",
        "cache_btn": "Redefinir Sessão & Cache",
        "about_desc": "Um client WhatsApp nativo e altamente otimizado para desktops Linux.",
        "tray_whisper": "Sussurrando em segundo tempo...",
        "tray_open": "Abrir",
        "tray_quit": "Sair",
        "tray_mute_shortcut": "Silenciar áudio (Atalho 8h)",
        "dl_title": "Diretório de downloads",
        "dl_desc": "Definir uma pasta dedicada para downloads do WhatsApp",
        "dl_btn": "Escolher pasta",
        "start_title": "Comportamiento de inicialização",
        "start_desc": "Minimizar diretamente para a bandeja ao iniciar",
        "audio_title": "Dispositivo de saída de áudio",
        "audio_desc": "Definir o canal de áudio padrão para o WhatsApp",
        "cli_title": "Comandos de terminal CLI disponíveis:",
        "cli_hint": "• matrixwhisper.py --toggle  ➔  Alternar visibilidade da janela\n• matrixwhisper.py --mute    ➔  Silenciar por 8h\n• matrixwhisper.py --quit    ➔  Fechar o aplicativo em background"
    },
    "pl": {
        "title": "Ustawienia",
        "tab_general": " Ogólne",
        "tab_media": " Audio i Media",
        "tab_advanced": " Zaawansowane",
        "as_title": "Autostart systemu",
        "as_desc": "Uruchom MatrixWhisper automatisch przy starcie komputera",
        "dm_title": "Wygląd (Ciemny motyw)",
        "dm_desc": "Wymuś ciemny motyw WhatsApp w interfejsie webowym",
        "tb_title": "Zamknij do zasobnika systemowego",
        "tb_desc": "Ukryj okno w zasobnika systemowym przy kliknięciu zamknięcia ('X')",
        "nt_title": "Natywne powiadomienia systemowe",
        "nt_desc": "Określa, czy powiadomienia webowe powinny pojawiać się jako natywne powiadomienia systemowe, gdy okno jest zamknięte",
        "gpu_title": "Tryb oszczędzania energii (GPU)",
        "gpu_desc": "Wyłącz akcelerację sprzętową WebEngine",
        "gpu_active": "Status: GPU wyłączone (Oszczędzanie energii aktywne) ⚠️",
        "gpu_reboot_on": "Efekt po restarcie: GPU zostanie wyłączone 🔋",
        "gpu_reboot_off": "Efekt po restarcie: GPU aktywne (Domyślne)",
        "mute_title": "Cichy strażnik (Smart Mute)",
        "mute_active": "Wyjście audio: Aktywne",
        "mute_btn_1h": "1 godz. Wycisz",
        "mute_btn_8h": "8 godz. Wycisz",
        "mute_btn_reset": "Resetuj",
        "lang_title": "Język wyświetlania",
        "lang_header": "Aktualny nagłówek:",
        "lang_reboot": "Język po restarcie:",
        "zoom_title": "Współczynnik skalowania HiDPI / Ultrawide",
        "zoom_desc": "Skaluj układ interfejsu WhatsApp Web",
        "cache_title": "Resetowanie Sesji & Czyszczenie Pamięci Podręcznej",
        "cache_desc": "Wylogowuje użytkownika, usuwa pliki cookie i czyści pamięć cache",
        "cache_btn": "Resetuj Sesję & Pamięć Cache",
        "about_desc": "Wysoce zoptymalizowany, natywny klient WhatsApp dla pulpitów Linux.",
        "tray_whisper": "Szepta w tle...",
        "tray_open": "Otwórz",
        "tray_quit": "Zakończ",
        "tray_mute_shortcut": "Wycisz dźwięk (Skrót 8 godz.)",
        "dl_title": "Katalog pobierania",
        "dl_desc": "Ustaw dedykowany folder dla pobieranych plików WhatsApp",
        "dl_btn": "Wybierz folder",
        "start_title": "Zachowanie podczas uruchamiania",
        "start_desc": "Minimalizuj bezpośrednio do zasobnika systemowego przy uruchomieniu",
        "audio_title": "Urządzenie wyjściowe audio",
        "audio_desc": "Ustaw domyślny kanał audio dla WhatsApp",
        "cli_title": "Dostępne polecenia terminala CLI:",
        "cli_hint": "• matrixwhisper.py --toggle  ➔  Pokaż/ukryj okno\n• matrixwhisper.py --mute    ➔  Wycisz na 8 godz.\n• matrixwhisper.py --quit    ➔  Czyste zakończenie aplikacji w tle"
    }
}

# --- NATIV GEZEICHNETER SWITCH-TOGGLE ---
class SwitchToggle(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(46, 22)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._thumb_position = 3.0 if not self.isChecked() else 27.0

    def hitButton(self, pos: QPoint) -> bool:
        return self.rect().contains(pos)

    @pyqtProperty(float)
    def thumb_position(self):
        return self._thumb_position

    @thumb_position.setter
    def thumb_position(self, pos):
        self._thumb_position = pos
        self.update()

    def nextCheckState(self):
        super().nextCheckState()
        self.trigger_animation()

    def trigger_animation(self):
        end_val = 27.0 if self.isChecked() else 3.0
        self.anim = QPropertyAnimation(self, b"thumb_position")
        self.anim.setDuration(120)
        self.anim.setEndValue(end_val)
        self.anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        if self.isChecked(): track_color = QColor("#25D366")
        else: track_color = QColor("#2c313c")

        painter.setBrush(QBrush(track_color))
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 11, 11)

        if not self.isChecked():
            pen = QPen(QColor("#4c5264"), 1)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(0, 0, self.width() - 1, self.height() - 1, 11, 11)
            painter.setPen(Qt.PenStyle.NoPen)

        painter.setBrush(QBrush(QColor("#ffffff")))
        painter.drawEllipse(QRectF(self._thumb_position, 3.0, 16.0, 16.0))
        painter.end()


class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self._link_interceptors = []

    def acceptNavigationRequest(self, url, nav_type, is_main_frame):
        if "whatsapp.com" not in url.toString() and url.toString() != "about:blank":
            QDesktopServices.openUrl(url)
            return False
        return super().acceptNavigationRequest(url, nav_type, is_main_frame)

    def createWindow(self, window_type):
        interceptor_view = QWebEngineView()
        interceptor_page = QWebEnginePage(self.profile(), interceptor_view)
        interceptor_view.setPage(interceptor_page)
        interceptor_page.urlChanged.connect(lambda url: QDesktopServices.openUrl(url))
        self._link_interceptors.append(interceptor_view)
        QTimer.singleShot(1000, lambda: self._clean_interceptor(interceptor_view))
        return interceptor_page

    def _clean_interceptor(self, view):
        if view in self._link_interceptors:
            self._link_interceptors.remove(view)


class MatrixWhisper(QMainWindow):
    def __init__(self):
        super().__init__()

        self.app_name = "MatrixWhisper"
        self.app_version = "2.8.0"
        self.setWindowTitle(self.app_name)
        self.resize(1150, 750)

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.icon_path = os.path.join(self.script_dir, "media", "media-matrix-logo.png")
        self.config_path = os.path.join(self.script_dir, "config.json")

        self.autostart_dir = os.path.join(os.path.expanduser("~"), ".config", "autostart")
        self.autostart_file = os.path.join(self.autostart_dir, "matrixwhisper.desktop")

        self.zoom_factor = 1.1
        self.mute_timer = None
        self.mute_until_time = None
        self.selected_language = "system"
        self.minimize_to_tray = True
        self.native_notifications = True
        self.disable_gpu_accel = False
        self.download_dir = os.path.expanduser("~/Downloads")
        self.start_minimized = False
        self.exiting = False
        self.is_initializing = True

        self.preload_config_metadata()
        self.ui_lang = self.determine_ui_language_key()

        self.storage_path = os.path.expanduser("~/.local/share/MatrixWhisper/storage")
        self.cache_path = os.path.expanduser("~/.cache/MatrixWhisper/cache")
        os.makedirs(self.storage_path, exist_ok=True)
        os.makedirs(self.cache_path, exist_ok=True)

        self.profile = QWebEngineProfile("MatrixWhisperStorage", self)
        self.profile.setPersistentStoragePath(self.storage_path)
        self.profile.setCachePath(self.cache_path)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)

        self.profile.setSpellCheckEnabled(True)
        try:
            sys_lang = (locale.getlocale()[0] or "de").split("_")[0]
            self.profile.setSpellCheckLanguages([sys_lang, "en-US"])
        except Exception:
            self.profile.setSpellCheckLanguages(["de", "en-US"])

        self.profile.setNotificationPresenter(self.handle_web_notification)
        self.profile.downloadRequested.connect(self.handle_download_requested)

        resolved_lang = self.resolve_http_language_string()
        self.profile.setHttpAcceptLanguage(resolved_lang)

        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)

        chrome_user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
        self.profile.setHttpUserAgent(chrome_user_agent)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- SIDEBAR MAIN ---
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(60)
        self.sidebar.setStyleSheet("""
            QFrame { background-color: #1e222b; border: none; }
            QPushButton { border: none; border-radius: 8px; padding: 10px; margin: 5px; background-color: transparent; }
            QPushButton:hover { background-color: #2c313c; }
            QPushButton:checked { background-color: #3e4451; }
        """)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 10, 0, 10)
        sidebar_layout.setSpacing(10)

        self.btn_chat = QPushButton()
        self.btn_chat.setIcon(self.draw_vector_chat_icon())
        self.btn_chat.setIconSize(QSize(24, 24))
        self.btn_chat.setCheckable(True)
        self.btn_chat.setChecked(True)

        self.btn_settings = QPushButton()
        self.btn_settings.setIcon(self.draw_vector_sliders_icon())
        self.btn_settings.setIconSize(QSize(24, 24))
        self.btn_settings.setCheckable(True)

        self.btn_chat.clicked.connect(lambda: self.switch_view(0))
        self.btn_settings.clicked.connect(lambda: self.switch_view(1))

        sidebar_layout.addWidget(self.btn_chat)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btn_settings)

        self.container = QStackedWidget()

        self.browser = QWebEngineView()
        self.web_page = CustomWebEnginePage(self.profile, self.browser)
        self.browser.setPage(self.web_page)
        self.browser.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.browser.setUrl(QUrl("https://web.whatsapp.com"))
        self.container.addWidget(self.browser)

        # --- OPTION B: SETTINGS INTERFACE WITH SUB-SIDEBAR ---
        self.settings_page = QWidget()
        self.settings_page.setStyleSheet("background-color: #1a1d24; color: #ffffff;")
        settings_main_layout = QHBoxLayout(self.settings_page)
        settings_main_layout.setContentsMargins(0, 0, 0, 0)
        settings_main_layout.setSpacing(0)

        # Sub-Sidebar für Einstellungen
        self.sub_sidebar = QListWidget()
        self.sub_sidebar.setFixedWidth(180)
        self.sub_sidebar.setStyleSheet("""
            QListWidget {
                background-color: #1e222b;
                border: none;
                border-right: 1px solid #2c313c;
                padding-top: 20px;
            }
            QListWidget::item {
                color: #a0a0a0;
                padding: 12px 15px;
                margin: 4px 8px;
                border-radius: 6px;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background-color: #2c313c;
                color: #ffffff;
            }
            QListWidget::item:selected {
                background-color: #25D366;
                color: #ffffff;
            }
        """)
        self.sub_sidebar.currentRowChanged.connect(self.switch_settings_tab)
        settings_main_layout.addWidget(self.sub_sidebar)

        # Rechter Content-Bereich für Tabs
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(30, 25, 30, 25)
        right_layout.setSpacing(15)

        self.title_label = QLabel()
        self.title_label.setFont(QFont("sans-serif", 16, QFont.Weight.Bold))
        right_layout.addWidget(self.title_label)

        self.settings_tabs = QStackedWidget()
        card_style = "QFrame { background-color: #1e222b; border-radius: 12px; border: 1px solid #2c313c; } QLabel { border: none; background: transparent; }"

        # --- TAB 1: ALLGEMEIN ---
        tab_gen_widget = QScrollArea()
        tab_gen_widget.setWidgetResizable(True)
        tab_gen_widget.setFrameShape(QFrame.Shape.NoFrame)
        tab_gen_content = QWidget()
        tab_gen_layout = QVBoxLayout(tab_gen_content)
        tab_gen_layout.setSpacing(12)

        # Autostart Card
        f1 = QFrame(); f1.setStyleSheet(card_style); l1 = QHBoxLayout(f1)
        self.as_title = QLabel(); self.as_title.setFont(QFont("sans-serif", 11, QFont.Weight.Bold))
        self.as_desc = QLabel(); self.as_desc.setStyleSheet("color: #a0a0a0; font-size: 9.5pt;")
        v1 = QVBoxLayout(); v1.addWidget(self.as_title); v1.addWidget(self.as_desc); l1.addLayout(v1); l1.addStretch()
        self.cb_autostart = SwitchToggle(); self.cb_autostart.setChecked(os.path.exists(self.autostart_file)); self.cb_autostart.toggled.connect(self.toggle_autostart); l1.addWidget(self.cb_autostart)
        tab_gen_layout.addWidget(f1)

        # Tray Behavior Card
        f2 = QFrame(); f2.setStyleSheet(card_style); l2 = QHBoxLayout(f2)
        self.tb_title = QLabel(); self.tb_title.setFont(QFont("sans-serif", 11, QFont.Weight.Bold))
        self.tb_desc = QLabel(); self.tb_desc.setStyleSheet("color: #a0a0a0; font-size: 9.5pt;")
        v2 = QVBoxLayout(); v2.addWidget(self.tb_title); v2.addWidget(self.tb_desc); l2.addLayout(v2); l2.addStretch()
        self.cb_tray_behavior = SwitchToggle(); self.cb_tray_behavior.setChecked(self.minimize_to_tray); self.cb_tray_behavior.toggled.connect(self.toggle_tray_behavior); l2.addWidget(self.cb_tray_behavior)
        tab_gen_layout.addWidget(f2)

        # Tray Start Card
        f3 = QFrame(); f3.setStyleSheet(card_style); l3 = QHBoxLayout(f3)
        self.start_title = QLabel(); self.start_title.setFont(QFont("sans-serif", 11, QFont.Weight.Bold))
        self.start_desc = QLabel(); self.start_desc.setStyleSheet("color: #a0a0a0; font-size: 9.5pt;")
        v3 = QVBoxLayout(); v3.addWidget(self.start_title); v3.addWidget(self.start_desc); l3.addLayout(v3); l3.addStretch()
        self.cb_start_minimized = SwitchToggle(); self.cb_start_minimized.setChecked(self.start_minimized); self.cb_start_minimized.toggled.connect(self.toggle_start_minimized); l3.addWidget(self.cb_start_minimized)
        tab_gen_layout.addWidget(f3)

        # Language Profile Card
        f4 = QFrame(); f4.setStyleSheet(card_style + "QComboBox { background-color: #2c313c; color: #ffffff; border: 1px solid #4c5264; border-radius: 6px; padding: 5px; min-width: 150px; }")
        l4 = QHBoxLayout(f4); v4 = QVBoxLayout()
        self.lang_title = QLabel(); self.lang_title.setFont(QFont("sans-serif", 11, QFont.Weight.Bold))
        self.lang_status_label = QLabel(); self.lang_status_label.setStyleSheet("color: #a0a0a0; font-size: 9.5pt;")
        v4.addWidget(self.lang_title); v4.addWidget(self.lang_status_label); l4.addLayout(v4); l4.addStretch()
        self.combo_lang = QComboBox(); self.combo_lang.addItem("Systemstandard", "system"); self.combo_lang.addItem("Deutsch (DE)", "de"); self.combo_lang.addItem("English (US)", "en"); self.combo_lang.addItem("Español (ES)", "es"); self.combo_lang.addItem("Français (FR)", "fr"); self.combo_lang.addItem("Italiano (IT)", "it"); self.combo_lang.addItem("Nederlands (NL)", "nl"); self.combo_lang.addItem("Português (PT)", "pt"); self.combo_lang.addItem("Polski (PL)", "pl")
        self.combo_lang.currentIndexChanged.connect(self.change_language_selection); l4.addWidget(self.combo_lang)
        tab_gen_layout.addWidget(f4)

        tab_gen_layout.addStretch()
        tab_gen_widget.setWidget(tab_gen_content)
        self.settings_tabs.addWidget(tab_gen_widget)

        # --- TAB 2: AUDIO & MEDIEN ---
        tab_med_widget = QScrollArea()
        tab_med_widget.setWidgetResizable(True)
        tab_med_widget.setFrameShape(QFrame.Shape.NoFrame)
        tab_med_content = QWidget()
        tab_med_layout = QVBoxLayout(tab_med_content)
        tab_med_layout.setSpacing(12)

        # Audio Output Card
        f5 = QFrame(); f5.setStyleSheet(card_style + "QComboBox { background-color: #2c313c; color: #ffffff; border: 1px solid #4c5264; border-radius: 6px; padding: 5px; min-width: 200px; }")
        l5 = QHBoxLayout(f5); v5 = QVBoxLayout()
        self.audio_title = QLabel(); self.audio_title.setFont(QFont("sans-serif", 11, QFont.Weight.Bold))
        self.audio_desc = QLabel(); self.audio_desc.setStyleSheet("color: #a0a0a0; font-size: 9.5pt;")
        v5.addWidget(self.audio_title); v5.addWidget(self.audio_desc); l5.addLayout(v5); l5.addStretch()
        self.combo_audio = QComboBox(); self.populate_audio_devices(); self.combo_audio.currentIndexChanged.connect(self.change_audio_device); l5.addWidget(self.combo_audio)
        tab_med_layout.addWidget(f5)

        # Smart Mute Card
        f6 = QFrame(); f6.setStyleSheet(card_style + "QPushButton { background-color: #3e4451; color: #ffffff; border-radius: 6px; padding: 6px 12px; border: none; } QPushButton:hover { background-color: #4c5264; }")
        l6 = QHBoxLayout(f6); v6 = QVBoxLayout()
        self.mute_title = QLabel(); self.mute_title.setFont(QFont("sans-serif", 11, QFont.Weight.Bold))
        self.mute_status_label = QLabel(); self.mute_status_label.setStyleSheet("color: #a0a0a0; font-size: 9.5pt;")
        v6.addWidget(self.mute_title); v6.addWidget(self.mute_status_label); l6.addLayout(v6); l6.addStretch()
        self.btn_mute_1h = QPushButton(); self.btn_mute_8h = QPushButton(); self.btn_mute_reset = QPushButton()
        self.btn_mute_1h.clicked.connect(lambda: self.activate_smart_mute(1)); self.btn_mute_8h.clicked.connect(lambda: self.activate_smart_mute(8)); self.btn_mute_reset.clicked.connect(self.deactivate_smart_mute)
        l6.addWidget(self.btn_mute_1h); l6.addWidget(self.btn_mute_8h); l6.addWidget(self.btn_mute_reset)
        tab_med_layout.addWidget(f6)

        # Download Directory Card
        f7 = QFrame(); f7.setStyleSheet(card_style + "QPushButton { background-color: #3e4451; color: #ffffff; border-radius: 6px; padding: 6px 12px; border: none; }")
        l7 = QHBoxLayout(f7); v7 = QVBoxLayout()
        self.dl_title = QLabel(); self.dl_title.setFont(QFont("sans-serif", 11, QFont.Weight.Bold))
        self.dl_path_label = QLabel(); self.dl_path_label.setStyleSheet("color: #25D366; font-size: 9.5pt; font-family: monospace;")
        v7.addWidget(self.dl_title); v7.addWidget(self.dl_path_label); l7.addLayout(v7); l7.addStretch()
        self.btn_choose_dl = QPushButton(); self.btn_choose_dl.clicked.connect(self.select_download_directory); l7.addWidget(self.btn_choose_dl)
        tab_med_layout.addWidget(f7)

        # Native Notifications Card
        f8 = QFrame(); f8.setStyleSheet(card_style); l8 = QHBoxLayout(f8)
        self.nt_title = QLabel(); self.nt_title.setFont(QFont("sans-serif", 11, QFont.Weight.Bold))
        self.nt_desc = QLabel(); self.nt_desc.setStyleSheet("color: #a0a0a0; font-size: 9.5pt;")
        v8 = QVBoxLayout(); v8.addWidget(self.nt_title); v8.addWidget(self.nt_desc); l8.addLayout(v8); l8.addStretch()
        self.cb_native_notifications = SwitchToggle(); self.cb_native_notifications.setChecked(self.native_notifications); self.cb_native_notifications.toggled.connect(self.toggle_native_notifications); l8.addWidget(self.cb_native_notifications)
        tab_med_layout.addWidget(f8)

        tab_med_layout.addStretch()
        tab_med_widget.setWidget(tab_med_content)
        self.settings_tabs.addWidget(tab_med_widget)

        # --- TAB 3: ERWEITERT ---
        tab_adv_widget = QScrollArea()
        tab_adv_widget.setWidgetResizable(True)
        tab_adv_widget.setFrameShape(QFrame.Shape.NoFrame)
        tab_adv_content = QWidget()
        tab_adv_layout = QVBoxLayout(tab_adv_content)
        tab_adv_layout.setSpacing(12)

        # Dark Theme Card
        f9 = QFrame(); f9.setStyleSheet(card_style); l9 = QHBoxLayout(f9)
        self.dm_title = QLabel(); self.dm_title.setFont(QFont("sans-serif", 11, QFont.Weight.Bold))
        self.dm_desc = QLabel(); self.dm_desc.setStyleSheet("color: #a0a0a0; font-size: 9.5pt;")
        v9 = QVBoxLayout(); v9.addWidget(self.dm_title); v9.addWidget(self.dm_desc); l9.addLayout(v9); l9.addStretch()
        self.cb_darkmode = SwitchToggle(); self.cb_darkmode.setChecked(True); self.cb_darkmode.toggled.connect(self.toggle_darkmode); l9.addWidget(self.cb_darkmode)
        tab_adv_layout.addWidget(f9)

        # Zoom Slider Card
        f10 = QFrame(); f10.setStyleSheet(card_style + "QSlider::groove:horizontal { border: 1px solid #3e4451; height: 6px; background: #1a1d24; border-radius: 3px; } QSlider::handle:horizontal { background: #25D366; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; }")
        l10 = QHBoxLayout(f10); v10 = QVBoxLayout()
        self.zoom_title = QLabel(); self.zoom_title.setFont(QFont("sans-serif", 11, QFont.Weight.Bold))
        self.zoom_desc_label = QLabel(); self.zoom_desc_label.setStyleSheet("color: #a0a0a0; font-size: 9.5pt;")
        v10.addWidget(self.zoom_title); v10.addWidget(self.zoom_desc_label); l10.addLayout(v10); l10.addStretch()
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal); self.zoom_slider.setMinimum(80); self.zoom_slider.setMaximum(130); self.zoom_slider.setFixedWidth(150); self.zoom_slider.valueChanged.connect(self.update_zoom_factor); l10.addWidget(self.zoom_slider)
        self.lbl_percent = QLabel(); self.lbl_percent.setFont(QFont("sans-serif", 11, QFont.Weight.Bold)); self.lbl_percent.setStyleSheet("color: #25D366;"); self.lbl_percent.setFixedWidth(45); self.lbl_percent.setAlignment(Qt.AlignmentFlag.AlignRight); l10.addWidget(self.lbl_percent)
        tab_adv_layout.addWidget(f10)

        # GPU Throttle Card
        f11 = QFrame(); f11.setStyleSheet(card_style); l11 = QHBoxLayout(f11)
        self.gpu_title = QLabel(); self.gpu_title.setFont(QFont("sans-serif", 11, QFont.Weight.Bold))
        self.gpu_status_label = QLabel(); self.gpu_status_label.setStyleSheet("color: #a0a0a0; font-size: 9.5pt;")
        v11 = QVBoxLayout(); v11.addWidget(self.gpu_title); v11.addWidget(self.gpu_status_label); l11.addLayout(v11); l11.addStretch()
        self.cb_gpu_accel = SwitchToggle(); self.cb_gpu_accel.setChecked(self.disable_gpu_accel); self.cb_gpu_accel.toggled.connect(self.toggle_gpu_acceleration); l11.addWidget(self.cb_gpu_accel)
        tab_adv_layout.addWidget(f11)

        # Cache Clean Card
        f12 = QFrame(); f12.setStyleSheet(card_style + "QPushButton { background-color: #e03131; color: #ffffff; border-radius: 6px; padding: 6px 12px; border: none; font-weight: bold; } QPushButton:hover { background-color: #ff4a4a; }")
        l12 = QHBoxLayout(f12); v12 = QVBoxLayout()
        self.cache_title = QLabel(); self.cache_title.setFont(QFont("sans-serif", 11, QFont.Weight.Bold))
        self.cache_desc = QLabel(); self.cache_desc.setStyleSheet("color: #a0a0a0; font-size: 9.5pt;")
        v12.addWidget(self.cache_title); v12.addWidget(self.cache_desc); l12.addLayout(v12); l12.addStretch()
        self.btn_reset_cache = QPushButton(); self.btn_reset_cache.clicked.connect(self.reset_cache_and_session); l12.addWidget(self.btn_reset_cache)
        tab_adv_layout.addWidget(f12)

        tab_adv_layout.addStretch()
        tab_adv_widget.setWidget(tab_adv_content)
        self.settings_tabs.addWidget(tab_adv_widget)

        right_layout.addWidget(self.settings_tabs)

        # --- UNBEWEGLICHER INLINE FOOTER ---
        about_frame = QFrame(); about_frame.setStyleSheet(card_style); about_layout = QHBoxLayout(about_frame)
        logo_label = QLabel()
        if os.path.exists(self.icon_path): logo_label.setPixmap(QPixmap(self.icon_path).scaled(42, 42, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else: logo_label.setText("🤖")
        about_layout.addWidget(logo_label)
        text_layout = QVBoxLayout()
        app_title = QLabel(self.app_name); app_title.setFont(QFont("sans-serif", 11, QFont.Weight.Bold)); app_title.setStyleSheet("color: #25D366;")
        self.app_version_lbl = QLabel(f"Version {self.app_version} (Modular Tabbed Design)")
        self.app_version_lbl.setStyleSheet("color: #a0a0a0; font-size: 9pt;")
        self.app_desc_lbl = QLabel(); self.app_desc_lbl.setStyleSheet("color: #d1d5db; font-size: 9pt;")
        self.lbl_cli_title = QLabel(); self.lbl_cli_title.setFont(QFont("sans-serif", 9, QFont.Weight.Bold)); self.lbl_cli_title.setStyleSheet("color: #25D366;")
        self.lbl_cli_hint = QLabel(); self.lbl_cli_hint.setFont(QFont("monospace", 8)); self.lbl_cli_hint.setStyleSheet("color: #a0a0a0;")
        text_layout.addWidget(app_title); text_layout.addWidget(self.app_version_lbl); text_layout.addWidget(self.app_desc_lbl); text_layout.addWidget(self.lbl_cli_title); text_layout.addWidget(self.lbl_cli_hint)
        about_layout.addLayout(text_layout); about_layout.addStretch()
        right_layout.addWidget(about_frame)

        settings_main_layout.addWidget(right_panel)
        self.container.addWidget(self.settings_page)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.container)

        self.browser.page().permissionRequested.connect(self.handle_permission_requested)
        self.browser.titleChanged.connect(self.check_notifications)
        self.browser.loadFinished.connect(self.apply_darkmode_on_load)

        self.retranslate_ui()
        self.tray_icon = QSystemTrayIcon(self)
        self.update_app_icons(0)
        self.setup_tray_menu()
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_icon_activated)

        self.sync_loaded_settings_to_ui()
        self.init_single_instance_server()
        self.is_initializing = False

    def populate_audio_devices(self):
        self.combo_audio.blockSignals(True); self.combo_audio.clear()
        default_device = QMediaDevices.defaultAudioOutput()
        self.combo_audio.addItem(f"Systemstandard ({default_device.description()})", "default")
        for device in QMediaDevices.audioOutputs():
            if device.id() != default_device.id():
                self.combo_audio.addItem(device.description(), device.id().data().decode('utf-8', errors='ignore'))
        self.combo_audio.blockSignals(False)

    def change_audio_device(self, index):
        device_id_str = self.combo_audio.itemData(index)
        if device_id_str != "default": print(f"[MatrixWhisper] Routing Audio Stream to Device-ID: {device_id_str}")

    def init_single_instance_server(self):
        self.instance_server = QLocalServer(self)
        runtime_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.RuntimeLocation)
        self.socket_path = os.path.join(runtime_dir, "matrixwhisper_socket")
        QLocalServer.removeServer(self.socket_path)
        self.instance_server.listen(self.socket_path)
        self.instance_server.newConnection.connect(self.handle_remote_activation)

    def handle_remote_activation(self):
        socket = self.instance_server.nextPendingConnection()
        if socket and socket.waitForReadyRead(500): self.process_remote_command(socket)

    def process_remote_command(self, socket):
        cmd = socket.readAll().data().decode().strip()
        if cmd in ["toggle", "show"]:
            if cmd == "toggle" and self.isVisible() and not self.isMinimized(): self.hide()
            else:
                self.showNormal() if self.isMinimized() else self.show()
                self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
                self.raise_(); self.activateWindow()
        elif cmd == "mute": self.activate_smart_mute(8)
        elif cmd == "quit": self.quit_application()
        socket.close()

    def select_download_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Download Ordner wählen", self.download_dir)
        if dir_path: self.download_dir = dir_path; self.dl_path_label.setText(self.download_dir); self.save_settings()

    def toggle_start_minimized(self, checked): self.start_minimized = checked; self.save_settings()

    def handle_download_requested(self, download_item):
        filename = download_item.downloadFileName() if hasattr(download_item, 'downloadFileName') else os.path.basename(download_item.suggestedFileName())
        download_item.setDownloadDirectory(self.download_dir); download_item.setDownloadFileName(filename); download_item.accept()

    def quit_application(self): self.exiting = True; QApplication.instance().quit()

    def determine_ui_language_key(self):
        if self.selected_language != "system": return self.selected_language if self.selected_language in TRANSLATIONS else "en"
        try:
            sys_locale = locale.getlocale()[0]
            if sys_locale and sys_locale.split("_")[0] in TRANSLATIONS: return sys_locale.split("_")[0]
        except Exception: pass
        return "en"

    def retranslate_ui(self):
        lang = self.ui_lang; t = TRANSLATIONS[lang]
        self.btn_settings.setToolTip(t["title"]); self.title_label.setText(t["title"])

        # Sub-Sidebar Items füllen
        self.sub_sidebar.blockSignals(True); self.sub_sidebar.clear()
        self.sub_sidebar.addItem("⚙️" + t["tab_general"])
        self.sub_sidebar.addItem("🎧" + t["tab_media"])
        self.sub_sidebar.addItem("🛠️" + t["tab_advanced"])
        self.sub_sidebar.setCurrentRow(self.settings_tabs.currentIndex())
        self.sub_sidebar.blockSignals(False)

        self.as_title.setText(t["as_title"]); self.as_desc.setText(t["as_desc"])
        self.dm_title.setText(t["dm_title"]); self.dm_desc.setText(t["dm_desc"])
        self.tb_title.setText(t["tb_title"]); self.tb_desc.setText(t["tb_desc"])
        self.nt_title.setText(t["nt_title"]); self.nt_desc.setText(t["nt_desc"])
        self.gpu_title.setText(t["gpu_title"]); self.mute_title.setText(t["mute_title"])
        self.btn_mute_1h.setText(t["mute_btn_1h"]); self.btn_mute_8h.setText(t["mute_btn_8h"]); self.btn_mute_reset.setText(t["mute_btn_reset"])
        self.lang_title.setText(t["lang_title"]); self.zoom_title.setText(t["zoom_title"]); self.zoom_desc_label.setText(t["zoom_desc"])
        self.cache_title.setText(t["cache_title"]); self.cache_desc.setText(t["cache_desc"]); self.btn_reset_cache.setText(t["cache_btn"])
        self.app_desc_lbl.setText(t["about_desc"]); self.dl_title.setText(t["dl_title"]); self.btn_choose_dl.setText(t["dl_btn"])
        self.start_title.setText(t["start_title"]); self.start_desc.setText(t["start_desc"])
        self.audio_title.setText(t["audio_title"]); self.audio_desc.setText(t["audio_desc"])
        self.lbl_cli_title.setText(t["cli_title"]); self.lbl_cli_hint.setText(t["cli_hint"])
        self.lang_status_label.setText(f"{t['lang_header']} {self.resolve_http_language_string().split(',')[0]}")

    def switch_settings_tab(self, index): self.settings_tabs.setCurrentIndex(index)

    def setup_tray_menu(self):
        t = TRANSLATIONS[self.ui_lang]; self.tray_menu = QMenu()
        show_action = QAction(t["tray_open"], self); quit_action = QAction(t["tray_quit"], self)
        self.mute_tray_action = QAction(t["tray_mute_shortcut"], self); self.mute_tray_action.setCheckable(True)
        if self.mute_until_time and self.mute_until_time > datetime.now(): self.mute_tray_action.setChecked(True)
        self.mute_tray_action.toggled.connect(self.toggle_tray_mute_from_action)
        show_action.triggered.connect(self.show); quit_action.triggered.connect(self.quit_application)
        self.tray_menu.addAction(show_action); self.tray_menu.addSeparator(); self.tray_menu.addAction(self.mute_tray_action); self.tray_menu.addSeparator(); self.tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)

    def preload_config_metadata(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f: config = json.load(f)
                self.zoom_factor = config.get("zoom_factor", 1.1)
                self.selected_language = config.get("language_selection", "system")
                self.minimize_to_tray = config.get("minimize_to_tray", True)
                self.native_notifications = config.get("native_notifications", True)
                self.disable_gpu_accel = config.get("disable_gpu_acceleration", False)
                self.download_dir = config.get("download_directory", os.path.expanduser("~/Downloads"))
                self.start_minimized = config.get("start_minimized", False)
            except Exception: pass

    def resolve_http_language_string(self):
        if self.selected_language != "system": return f"{self.selected_language}-{self.selected_language.upper()},{self.selected_language};q=0.9"
        return "de-DE,de;q=0.9,en-US;q=0.8"

    def sync_loaded_settings_to_ui(self):
        t = TRANSLATIONS[self.ui_lang]
        self.mute_status_label.setText(t["mute_active"])
        self.zoom_slider.setValue(int(self.zoom_factor * 100)); self.lbl_percent.setText(f"{int(self.zoom_factor * 100)}%"); self.browser.setZoomFactor(self.zoom_factor)
        if self.disable_gpu_accel: self.gpu_status_label.setText(t["gpu_active"]); self.gpu_status_label.setStyleSheet("color: #e03131; font-weight: bold;")
        else: self.gpu_status_label.setText(t["gpu_reboot_off"])
        self.dl_path_label.setText(self.download_dir); index = self.combo_lang.findData(self.selected_language)
        if index != -1: self.combo_lang.setCurrentIndex(index)

    def save_settings(self):
        if self.is_initializing: return
        config = {"zoom_factor": self.zoom_factor, "language_selection": self.selected_language, "minimize_to_tray": self.minimize_to_tray, "native_notifications": self.native_notifications, "disable_gpu_acceleration": self.disable_gpu_accel, "download_directory": self.download_dir, "start_minimized": self.start_minimized}
        try:
            with open(self.config_path, "w", encoding="utf-8") as f: json.dump(config, f, indent=4)
        except Exception: pass

    def toggle_tray_behavior(self, checked): self.minimize_to_tray = checked; self.save_settings()
    def toggle_native_notifications(self, checked): self.native_notifications = checked; self.save_settings()

    def handle_web_notification(self, notification: QWebEngineNotification):
        if self.native_notifications and (not self.isVisible() or self.isMinimized()):
            self.tray_icon.showMessage(notification.title(), notification.message(), QSystemTrayIcon.MessageIcon.Information, 4000)
        notification.accept()

    def reset_cache_and_session(self):
        self.browser.setUrl(QUrl("about:blank")); self.profile.clearHttpCache(); self.profile.cookieStore().deleteAllCookies()
        try:
            if os.path.exists(self.storage_path): shutil.rmtree(self.storage_path)
            if os.path.exists(self.cache_path): shutil.rmtree(self.cache_path)
            os.makedirs(self.storage_path, exist_ok=True); os.makedirs(self.cache_path, exist_ok=True)
        except Exception: pass
        self.browser.setUrl(QUrl("https://web.whatsapp.com")); self.switch_view(0)

    def toggle_gpu_acceleration(self, checked):
        self.disable_gpu_accel = checked; self.save_settings(); t = TRANSLATIONS[self.ui_lang]
        self.gpu_status_label.setText(t["gpu_reboot_on"] if checked else t["gpu_reboot_off"])

    def change_language_selection(self, index):
        self.selected_language = self.combo_lang.itemData(index); self.save_settings(); self.ui_lang = self.determine_ui_language_key(); self.retranslate_ui(); self.setup_tray_menu()

    def activate_smart_mute(self, hours):
        if self.mute_timer: self.mute_timer.stop()
        self.browser.page().setAudioMuted(True); self.mute_until_time = datetime.now() + timedelta(hours=hours)
        self.mute_status_label.setText(f"Stumm bis {self.mute_until_time.strftime('%H:%M')}"); self.save_settings()
        self.mute_timer = QTimer(self); self.mute_timer.singleShot(hours * 3600000, self.deactivate_smart_mute)

    def deactivate_smart_mute(self):
        self.browser.page().setAudioMuted(False); t = TRANSLATIONS[self.ui_lang]; self.mute_status_label.setText(t["mute_active"])
        if self.mute_timer: self.mute_timer.stop(); self.mute_timer = None
        self.mute_until_time = None; self.save_settings()

    def toggle_tray_mute_from_action(self, checked): self.activate_smart_mute(8) if checked else self.deactivate_smart_mute()
    def update_zoom_factor(self, value): self.zoom_factor = value / 100.0; self.browser.setZoomFactor(self.zoom_factor); self.lbl_percent.setText(f"{value}%"); self.save_settings()

    def draw_vector_chat_icon(self):
        p = QPixmap(32, 32); p.fill(Qt.GlobalColor.transparent); painter = QPainter(p); painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor("#25D366"), 2); pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin); painter.setPen(pen); painter.drawRoundedRect(QRectF(2, 4, 28, 19), 5, 5)
        t = QPolygonF([QPointF(6.0, 23.0), QPointF(12.0, 23.0), QPointF(6.0, 28.0)]); painter.drawPolygon(t); painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(QColor("#1e222b")); painter.drawRect(QRectF(6.5, 22.0, 5.0, 2.0)); painter.end()
        return QIcon(p)

    def draw_vector_sliders_icon(self):
        p = QPixmap(32, 32); p.fill(Qt.GlobalColor.transparent); painter = QPainter(p); painter.setRenderHint(QPainter.RenderHint.Antialiasing); painter.setPen(QPen(QColor("#25D366"), 2))
        for y, kx in [(8.0, 22.0), (16.0, 10.0), (24.0, 18.0)]: painter.setBrush(Qt.BrushStyle.NoBrush); painter.drawLine(QPointF(4.0, y), QPointF(28.0, y)); painter.setBrush(QColor("#1e222b")); painter.drawEllipse(QPointF(kx, y), 3.0, 3.0)
        painter.end()
        return QIcon(p)

    def switch_view(self, index): self.container.setCurrentIndex(index); self.btn_chat.setChecked(index == 0); self.btn_settings.setChecked(index == 1)
    def handle_permission_requested(self, request): request.grant()
    def toggle_darkmode(self, checked): self.browser.page().runJavaScript(f"document.body.classList.{'add' if checked else 'remove'}('dark');")

    def apply_darkmode_on_load(self, success):
        if success and self.cb_darkmode.isChecked():
            self.toggle_darkmode(True)

    def toggle_autostart(self, checked):
        if checked:
            os.makedirs(self.autostart_dir, exist_ok=True)
            desktop_entry = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=MatrixWhisper
Comment=MatrixWhisper im Hintergrund starten (v{self.app_version})
Exec=python3 {os.path.abspath(__file__)} --minimized
Icon={self.icon_path}
Terminal=false
Categories=Network;InstantMessaging;
StartupWMClass=matrixwhisper.py
X-GNOME-Autostart-enabled=true
"""
            try:
                with open(self.autostart_file, "w", encoding="utf-8") as f: f.write(desktop_entry)
                os.chmod(self.autostart_file, 0o755)
            except Exception: self.cb_autostart.setChecked(False)
        else:
            if os.path.exists(self.autostart_file):
                try: os.remove(self.autostart_file)
                except Exception: pass

    def check_notifications(self, title):
        m = re.search(r'\((\d+)\)', title)
        if m:
            a = int(m.group(1)); self.setWindowTitle(f"{self.app_name} ({a} ungelesen)"); self.tray_icon.setToolTip(f"{self.app_name}: {a} ungelesene Nachrichten"); self.update_app_icons(a)
        else: self.setWindowTitle(self.app_name); self.tray_icon.setToolTip(self.app_name); self.update_app_icons(0)

    def update_app_icons(self, count):
        if not os.path.exists(self.icon_path): return
        bp = QPixmap(self.icon_path)
        if count > 0:
            badge = bp.copy(); painter = QPainter(badge); painter.setRenderHint(QPainter.RenderHint.Antialiasing); w = badge.width(); r = int(w * 0.28); cx, cy = w - r - 1, r + 1
            painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(QColor(239, 68, 68)); painter.drawEllipse(QPoint(cx, cy), r, r)
            painter.setFont(QFont("sans-serif", int(r * 1.25), QFont.Weight.Bold)); painter.setPen(QColor(255, 255, 255)); painter.drawText(cx - r, cy - r, r * 2, r * 2, Qt.AlignmentFlag.AlignCenter, str(count) if count < 10 else "9+"); painter.end()
            self.setWindowIcon(QIcon(badge)); self.tray_icon.setIcon(QIcon(badge))
        else: self.setWindowIcon(QIcon(bp)); self.tray_icon.setIcon(QIcon(bp))

    def closeEvent(self, event):
        if self.exiting: event.accept()
        elif self.minimize_to_tray: event.ignore(); self.hide()
        else: self.quit_application()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible(): self.hide()
            else:
                self.show()
                self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
                self.raise_(); self.activateWindow()


if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="MatrixWhisper CLI Controller")
    parser.add_argument("--minimized", action="store_true")
    parser.add_argument("--toggle", action="store_true")
    parser.add_argument("--mute", action="store_true")
    parser.add_argument("--quit", action="store_true")
    args = parser.parse_args()

    runtime_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.RuntimeLocation)
    socket_path = os.path.join(runtime_dir, "matrixwhisper_socket")
    socket = QLocalSocket()
    socket.connectToServer(socket_path)

    if socket.waitForConnected(500):
        cmd = "show"
        if args.toggle: cmd = "toggle"
        elif args.mute: cmd = "mute"
        elif args.quit: cmd = "quit"
        socket.write(cmd.encode()); socket.flush(); socket.waitForBytesWritten(500); socket.disconnectFromServer()
        sys.exit(0)

    cfg_file = os.path.join(script_directory, "config.json")
    if os.path.exists(cfg_file):
        try:
            with open(cfg_file, "r", encoding="utf-8") as f: raw_cfg = json.load(f)
            if raw_cfg.get("disable_gpu_acceleration", False):
                sys.argv.extend(["--disable-gpu", "--disable-software-rasterizer"])
        except Exception: pass

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setOrganizationName("the-media-matrix")
    app.setApplicationName("MatrixWhisper")

    window = MatrixWhisper()
    if not (args.minimized or window.start_minimized): window.show()
    sys.exit(app.exec())
