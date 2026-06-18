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
                             QComboBox, QScrollArea)
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings, QWebEngineScript, QWebEnginePage, QWebEngineNotification
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QStandardPaths, Qt, QPoint, QSize, QRectF, QPointF, QTimer, QPropertyAnimation, pyqtProperty
from PyQt6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor, QFont, QPolygonF, QPen, QBrush, QDesktopServices
from PyQt6.QtNetwork import QLocalServer, QLocalSocket

# --- TRANSLATION DICTIONARY (INTERNATIONALIZATION) ---
TRANSLATIONS = {
    "de": {
        "title": "Einstellungen",
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
        "about_desc": "Ein hochoptimierter, nativer WhatsApp-Client für Linux Desktops.",
        "tray_whisper": "Flüstert im Hintergrund weiter...",
        "tray_open": "Öffnen",
        "tray_quit": "Beenden",
        "tray_mute_shortcut": "Stummschalten (8h Schnellwahl)"
    },
    "en": {
        "title": "Settings",
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
        "about_desc": "A highly optimized, native WhatsApp client for Linux desktops.",
        "tray_whisper": "Whispering in the background...",
        "tray_open": "Open",
        "tray_quit": "Quit",
        "tray_mute_shortcut": "Mute Audio (8h Shortcut)"
    },
    "es": {
        "title": "Ajustes",
        "as_title": "Inicio del sistema (Autostart)",
        "as_desc": "Iniciar MatrixWhisper automáticamente con el ordenador",
        "dm_title": "Apariencia (Tema oscuro)",
        "dm_desc": "Forzar el tema oscuro de WhatsApp en la interfaz web",
        "tb_title": "Cerrar a la bandeja (Segundo plano)",
        "tb_desc": "Ocultar la ventana en la bandeja del sistema al cerrar ('X')",
        "nt_title": "Notificaciones nativas del sistema",
        "nt_desc": "Establece si las notificaciones web deben aparecer como notificaciones del sistema cuando la ventana está cerrada",
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
        "tray_whisper": "Susurrando en segundo plano...",
        "tray_open": "Abrir",
        "tray_quit": "Salir",
        "tray_mute_shortcut": "Silenciar (Acceso rápido 8h)"
    },
    "fr": {
        "title": "Paramètres",
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
        "tray_mute_shortcut": "Mettre en muet (Raccourci 8h)"
    },
    "it": {
        "title": "Impostazioni",
        "as_title": "Avvio automatico",
        "as_desc": "Avvia automaticamente MatrixWhisper all'accensione del computer",
        "dm_title": "Aspetto (Tema scuro)",
        "dm_desc": "Forza il tema scuro di WhatsApp nell'interfaccia web",
        "tb_title": "Riduci nel vassoio di sistema",
        "tb_desc": "Nascondi la finestra nel vassoio di sistema quando si chiude ('X')",
        "nt_title": "Notifiche native di sistema",
        "nt_desc": "Stabilisce se le notifiche web devono apparire come notifiche di sistema quando la finestra è chiusa",
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
        "tray_mute_shortcut": "Disattiva audio (Scelta rapida 8h)"
    },
    "nl": {
        "title": "Instellingen",
        "as_title": "Systeemstart (Autostart)",
        "as_desc": "MatrixWhisper automatisch starten bij het opstarten van de computer",
        "dm_title": "Uiterlijk (Donker thema)",
        "dm_desc": "Forceer het donkere WhatsApp-thema in de webinterface",
        "tb_title": "Sluiten naar systeemvak",
        "tb_desc": "Verberg het venster in het systeemvak bij het klikken op sluiten ('X')",
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
        "tray_mute_shortcut": "Audio dempen (8u snelkoppeling)"
    },
    "pt": {
        "title": "Configurações",
        "as_title": "Iniciar com o sistema",
        "as_desc": "Iniciar o MatrixWhisper automaticamente ao ligar o computador",
        "dm_title": "Aparência (Tema escuro)",
        "dm_desc": "Forçar o tema escuro do WhatsApp na interface web",
        "tb_title": "Fechar para a bandeja de sistema",
        "tb_desc": "Ocultar a janela na bandeja do sistema ao clicar no botão fechar ('X')",
        "gpu_title": "Modo de economia de energia (GPU)",
        "gpu_desc": "Desativar a aceleração de hardware do WebEngine",
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
        "tray_whisper": "Sussurrando em segundo plano...",
        "tray_open": "Abrir",
        "tray_quit": "Sair",
        "tray_mute_shortcut": "Silenciar áudio (Atalho 8h)"
    },
    "pl": {
        "title": "Ustawienia",
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
        "tray_mute_shortcut": "Wycisz dźwięk (Skrót 8 godz.)"
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


# --- CUSTOM PAGE-KLASSE FÜR HYPERLINKS ---
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
        self.app_version = "2.6.0"
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
        if self.selected_language == "system":
            try:
                sys_lang = locale.getdefaultlocale()[0].split("_")[0]
                self.profile.setSpellCheckLanguages([sys_lang, "en-US"])
            except Exception:
                self.profile.setSpellCheckLanguages(["de", "en-US"])
        else:
            lang_code = "en-US" if self.selected_language == "en" else self.selected_language
            self.profile.setSpellCheckLanguages([lang_code])

        self.profile.setNotificationPresenter(self.handle_web_notification)

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

        fake_storage_script = QWebEngineScript()
        fake_storage_script.setSourceCode("""
            if (navigator.storage && navigator.storage.persist) {
                navigator.storage.persist = function() { return Promise.resolve(true); };
            }
            if (navigator.storage && navigator.storage.persisted) {
                navigator.storage.persisted = function() { return Promise.resolve(true); };
            }
        """)
        fake_storage_script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        fake_storage_script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        fake_storage_script.setRunsOnSubFrames(True)
        self.profile.scripts().insert(fake_storage_script)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

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
        self.btn_chat.setToolTip("Chats")

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

        # --- EINSTELLUNGSSEITE ARCHITEKTUR ---
        self.settings_page = QWidget()
        self.settings_page.setStyleSheet("background-color: #1a1d24; color: #ffffff;")

        page_main_layout = QVBoxLayout(self.settings_page)
        page_main_layout.setContentsMargins(30, 30, 30, 30)
        page_main_layout.setSpacing(14)

        self.title_label = QLabel()
        self.title_label.setFont(QFont("sans-serif", 18, QFont.Weight.Bold))
        page_main_layout.addWidget(self.title_label)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #2c313c;")
        page_main_layout.addWidget(line)

        card_style = """
            QFrame { background-color: #1e222b; border-radius: 12px; border: 1px solid #2c313c; }
            QLabel { border: none; background: transparent; }
        """

        # --- SCROLL AREA ENGINE (Nimmt die dynamischen Karten auf) ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea { background-color: transparent; border: none; }
            QScrollBar:vertical {
                border: none;
                background: #1a1d24;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #2c313c;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #25D366;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: #1a1d24;")
        settings_layout = QVBoxLayout(scroll_content)
        settings_layout.setContentsMargins(0, 5, 10, 5)
        settings_layout.setSpacing(14)

        # --- CARD 1: SYSTEMSTART ---
        autostart_frame = QFrame()
        autostart_frame.setStyleSheet(card_style)
        autostart_layout = QHBoxLayout(autostart_frame)
        autostart_layout.setContentsMargins(15, 12, 15, 12)
        as_icon = QLabel("⚙️")
        as_icon.setFont(QFont("sans-serif", 20))
        autostart_layout.addWidget(as_icon)
        as_text_layout = QVBoxLayout()
        self.as_title = QLabel()
        self.as_title.setFont(QFont("sans-serif", 12, QFont.Weight.Bold))
        self.as_desc = QLabel()
        self.as_desc.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        as_text_layout.addWidget(self.as_title)
        as_text_layout.addWidget(self.as_desc)
        autostart_layout.addLayout(as_text_layout)
        autostart_layout.addStretch()
        self.cb_autostart = SwitchToggle()
        self.cb_autostart.setChecked(os.path.exists(self.autostart_file))
        self.cb_autostart.thumb_position = 27.0 if self.cb_autostart.isChecked() else 3.0
        self.cb_autostart.toggled.connect(self.toggle_autostart)
        autostart_layout.addWidget(self.cb_autostart)
        settings_layout.addWidget(autostart_frame)

        # --- CARD 2: DARK THEME ---
        darkmode_frame = QFrame()
        darkmode_frame.setStyleSheet(card_style)
        darkmode_layout = QHBoxLayout(darkmode_frame)
        darkmode_layout.setContentsMargins(15, 12, 15, 12)
        dm_icon = QLabel("🌙")
        dm_icon.setFont(QFont("sans-serif", 20))
        darkmode_layout.addWidget(dm_icon)
        dm_text_layout = QVBoxLayout()
        self.dm_title = QLabel()
        self.dm_title.setFont(QFont("sans-serif", 12, QFont.Weight.Bold))
        self.dm_desc = QLabel()
        self.dm_desc.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        dm_text_layout.addWidget(self.dm_title)
        dm_text_layout.addWidget(self.dm_desc)
        darkmode_layout.addLayout(dm_text_layout)
        darkmode_layout.addStretch()
        self.cb_darkmode = SwitchToggle()
        self.cb_darkmode.setChecked(True)
        self.cb_darkmode.thumb_position = 27.0 if self.cb_darkmode.isChecked() else 3.0
        self.cb_darkmode.toggled.connect(self.toggle_darkmode)
        darkmode_layout.addWidget(self.cb_darkmode)
        settings_layout.addWidget(darkmode_frame)

        # --- CARD 3: TRAY BEHAVIOR ---
        tray_behavior_frame = QFrame()
        tray_behavior_frame.setStyleSheet(card_style)
        tray_behavior_layout = QHBoxLayout(tray_behavior_frame)
        tray_behavior_layout.setContentsMargins(15, 12, 15, 12)
        tb_icon = QLabel("📥")
        tb_icon.setFont(QFont("sans-serif", 20))
        tray_behavior_layout.addWidget(tb_icon)
        tb_text_layout = QVBoxLayout()
        self.tb_title = QLabel()
        self.tb_title.setFont(QFont("sans-serif", 12, QFont.Weight.Bold))
        self.tb_desc = QLabel()
        self.tb_desc.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        tb_text_layout.addWidget(self.tb_title)
        tb_text_layout.addWidget(self.tb_desc)
        tray_behavior_layout.addLayout(tb_text_layout)
        tray_behavior_layout.addStretch()
        self.cb_tray_behavior = SwitchToggle()
        self.cb_tray_behavior.setChecked(self.minimize_to_tray)
        self.cb_tray_behavior.thumb_position = 27.0 if self.cb_tray_behavior.isChecked() else 3.0
        self.cb_tray_behavior.toggled.connect(self.toggle_tray_behavior)
        tray_behavior_layout.addWidget(self.cb_tray_behavior)
        settings_layout.addWidget(tray_behavior_frame)

        # --- CARD 3.5: NATIVE NOTIFICATIONS TOGGLE ---
        nt_frame = QFrame()
        nt_frame.setStyleSheet(card_style)
        nt_layout = QHBoxLayout(nt_frame)
        nt_layout.setContentsMargins(15, 12, 15, 12)
        nt_icon_lbl = QLabel("🔔")
        nt_icon_lbl.setFont(QFont("sans-serif", 20))
        nt_layout.addWidget(nt_icon_lbl)
        nt_text_layout = QVBoxLayout()
        self.nt_title = QLabel()
        self.nt_title.setFont(QFont("sans-serif", 12, QFont.Weight.Bold))
        self.nt_desc = QLabel()
        self.nt_desc.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        nt_text_layout.addWidget(self.nt_title)
        nt_text_layout.addWidget(self.nt_desc)
        nt_layout.addLayout(nt_text_layout)
        nt_layout.addStretch()
        self.cb_native_notifications = SwitchToggle()
        self.cb_native_notifications.setChecked(self.native_notifications)
        self.cb_native_notifications.thumb_position = 27.0 if self.cb_native_notifications.isChecked() else 3.0
        self.cb_native_notifications.toggled.connect(self.toggle_native_notifications)
        nt_layout.addWidget(self.cb_native_notifications)
        settings_layout.addWidget(nt_frame)

        # --- CARD 4: GPU THROTTLE ---
        gpu_frame = QFrame()
        gpu_frame.setStyleSheet(card_style)
        gpu_layout = QHBoxLayout(gpu_frame)
        gpu_layout.setContentsMargins(15, 12, 15, 12)
        gpu_icon = QLabel("🔋")
        gpu_icon.setFont(QFont("sans-serif", 20))
        gpu_layout.addWidget(gpu_icon)
        gpu_text_layout = QVBoxLayout()
        self.gpu_title = QLabel()
        self.gpu_title.setFont(QFont("sans-serif", 12, QFont.Weight.Bold))
        self.gpu_status_label = QLabel()
        self.gpu_status_label.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        gpu_text_layout.addWidget(self.gpu_title)
        gpu_text_layout.addWidget(self.gpu_status_label)
        gpu_layout.addLayout(gpu_text_layout)
        gpu_layout.addStretch()
        self.cb_gpu_accel = SwitchToggle()
        self.cb_gpu_accel.setChecked(self.disable_gpu_accel)
        self.cb_gpu_accel.thumb_position = 27.0 if self.cb_gpu_accel.isChecked() else 3.0
        self.cb_gpu_accel.toggled.connect(self.toggle_gpu_acceleration)
        gpu_layout.addWidget(self.cb_gpu_accel)
        settings_layout.addWidget(gpu_frame)

        # --- CARD 5: SMART MUTE ---
        mute_frame = QFrame()
        mute_frame.setStyleSheet(card_style + """
            QPushButton { background-color: #3e4451; color: #ffffff; border-radius: 6px; padding: 8px 16px; border: none; }
            QPushButton:hover { background-color: #4c5264; }
        """)
        mute_layout = QHBoxLayout(mute_frame)
        mute_layout.setContentsMargins(15, 12, 15, 12)
        mute_icon_label = QLabel("📢")
        mute_icon_label.setFont(QFont("sans-serif", 20))
        mute_layout.addWidget(mute_icon_label)
        mute_text_layout = QVBoxLayout()
        self.mute_title = QLabel()
        self.mute_title.setFont(QFont("sans-serif", 12, QFont.Weight.Bold))
        self.mute_status_label = QLabel()
        self.mute_status_label.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        mute_text_layout.addWidget(self.mute_title)
        mute_text_layout.addWidget(self.mute_status_label)
        mute_layout.addLayout(mute_text_layout)
        mute_layout.addStretch()
        self.btn_mute_1h = QPushButton()
        self.btn_mute_8h = QPushButton()
        self.btn_mute_reset = QPushButton()
        self.btn_mute_1h.clicked.connect(lambda: self.activate_smart_mute(1))
        self.btn_mute_8h.clicked.connect(lambda: self.activate_smart_mute(8))
        self.btn_mute_reset.clicked.connect(self.deactivate_smart_mute)
        mute_layout.addWidget(self.btn_mute_1h)
        mute_layout.addWidget(self.btn_mute_8h)
        mute_layout.addWidget(self.btn_mute_reset)
        settings_layout.addWidget(mute_frame)

        # --- CARD 6: SPRACHEINSTELLUNGEN ---
        lang_frame = QFrame()
        lang_frame.setStyleSheet(card_style + """
            QComboBox {
                background-color: #2c313c;
                color: #ffffff;
                border: 1px solid #4c5264;
                border-radius: 6px;
                padding: 5px 10px;
                min-width: 160px;
            }
            QComboBox:hover { background-color: #3e4451; }
            QComboBox QAbstractItemView {
                background-color: #1e222b;
                color: #ffffff;
                selection-background-color: #25D366;
                selection-color: #ffffff;
                border: 1px solid #4c5264;
            }
        """)
        lang_layout = QHBoxLayout(lang_frame)
        lang_layout.setContentsMargins(15, 12, 15, 12)
        lang_icon = QLabel("🌐")
        lang_icon.setFont(QFont("sans-serif", 20))
        lang_layout.addWidget(lang_icon)
        lang_text_layout = QVBoxLayout()
        self.lang_title = QLabel()
        self.lang_title.setFont(QFont("sans-serif", 12, QFont.Weight.Bold))
        self.lang_status_label = QLabel()
        self.lang_status_label.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        lang_text_layout.addWidget(self.lang_title)
        lang_text_layout.addWidget(self.lang_status_label)
        lang_layout.addLayout(lang_text_layout)
        lang_layout.addStretch()
        self.combo_lang = QComboBox()
        self.combo_lang.addItem("Systemstandard", "system")
        self.combo_lang.addItem("Deutsch (DE)", "de")
        self.combo_lang.addItem("English (US)", "en")
        self.combo_lang.addItem("Español (ES)", "es")
        self.combo_lang.addItem("Français (FR)", "fr")
        self.combo_lang.addItem("Italiano (IT)", "it")
        self.combo_lang.addItem("Nederlands (NL)", "nl")
        self.combo_lang.addItem("Português (PT)", "pt")
        self.combo_lang.addItem("Polski (PL)", "pl")
        index = self.combo_lang.findData(self.selected_language)
        if index != -1: self.combo_lang.setCurrentIndex(index)
        self.combo_lang.currentIndexChanged.connect(self.change_language_selection)
        lang_layout.addWidget(self.combo_lang)
        settings_layout.addWidget(lang_frame)

        # --- CARD 7: ZOOM FAKTOR BEREICH ---
        zoom_frame = QFrame()
        zoom_frame.setStyleSheet(card_style + """
            QSlider::groove:horizontal { border: 1px solid #3e4451; height: 6px; background: #1a1d24; border-radius: 3px; }
            QSlider::handle:horizontal { background: #25D366; border: 1px solid #25D366; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; }
            QSlider::handle:horizontal:hover { background: #40f081; border: 1px solid #40f081; }
        """)
        zoom_layout = QHBoxLayout(zoom_frame)
        zoom_layout.setContentsMargins(15, 12, 15, 12)
        zoom_icon_label = QLabel("🔍")
        zoom_icon_label.setFont(QFont("sans-serif", 20))
        zoom_layout.addWidget(zoom_icon_label)
        zoom_text_layout = QVBoxLayout()
        self.zoom_title = QLabel()
        self.zoom_title.setFont(QFont("sans-serif", 12, QFont.Weight.Bold))
        self.zoom_desc_label = QLabel()
        self.zoom_desc_label.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        zoom_text_layout.addWidget(self.zoom_title)
        zoom_text_layout.addWidget(self.zoom_desc_label)
        zoom_layout.addLayout(zoom_text_layout)
        zoom_layout.addStretch()
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setMinimum(80)
        self.zoom_slider.setMaximum(130)
        self.zoom_slider.setFixedWidth(200)
        self.zoom_slider.valueChanged.connect(self.update_zoom_factor)
        zoom_layout.addWidget(self.zoom_slider)
        self.lbl_percent = QLabel("")
        self.lbl_percent.setFont(QFont("sans-serif", 11, QFont.Weight.Bold))
        self.lbl_percent.setStyleSheet("color: #25D366; background: transparent; border: none;")
        self.lbl_percent.setFixedWidth(50)
        self.lbl_percent.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        zoom_layout.addWidget(self.lbl_percent)
        settings_layout.addWidget(zoom_frame)

        # --- CARD 8: CACHE RESET ENGINE ---
        cache_frame = QFrame()
        cache_frame.setStyleSheet(card_style + """
            QPushButton { background-color: #e03131; color: #ffffff; border-radius: 6px; padding: 8px 16px; border: none; font-weight: bold; }
            QPushButton:hover { background-color: #ff4a4a; }
        """)
        cache_layout = QHBoxLayout(cache_frame)
        cache_layout.setContentsMargins(15, 12, 15, 12)
        cache_icon = QLabel("🗑️")
        cache_icon.setFont(QFont("sans-serif", 20))
        cache_layout.addWidget(cache_icon)
        cache_text_layout = QVBoxLayout()
        self.cache_title = QLabel()
        self.cache_title.setFont(QFont("sans-serif", 12, QFont.Weight.Bold))
        self.cache_desc = QLabel()
        self.cache_desc.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        cache_text_layout.addWidget(self.cache_title)
        cache_text_layout.addWidget(self.cache_desc)
        cache_layout.addLayout(cache_text_layout)
        cache_layout.addStretch()
        self.btn_reset_cache = QPushButton()
        self.btn_reset_cache.clicked.connect(self.reset_cache_and_session)
        cache_layout.addWidget(self.btn_reset_cache)
        settings_layout.addWidget(cache_frame)

        # ScrollArea-Inhalt mappen
        scroll_area.setWidget(scroll_content)
        page_main_layout.addWidget(scroll_area)

        # --- CARD 9: FIXED FOOTER ("ÜBER DIESE APP") ---
        about_frame = QFrame()
        about_frame.setStyleSheet(card_style)
        about_layout = QHBoxLayout(about_frame)
        about_layout.setContentsMargins(20, 15, 20, 15)
        about_layout.setSpacing(20)
        logo_label = QLabel()
        if os.path.exists(self.icon_path):
            logo_pixmap = QPixmap(self.icon_path).scaled(54, 54, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        else:
            logo_label.setText("🤖")
            logo_label.setFont(QFont("sans-serif", 28))
        about_layout.addWidget(logo_label)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        app_title = QLabel(f"{self.app_name}")
        app_title.setFont(QFont("sans-serif", 13, QFont.Weight.Bold))
        app_title.setStyleSheet("color: #25D366;")
        self.app_version_lbl = QLabel(f"Version {self.app_version} (Single-Instance Build)")
        self.app_version_lbl.setFont(QFont("sans-serif", 10))
        self.app_version_lbl.setStyleSheet("color: #a0a0a0;")
        self.app_desc_lbl = QLabel()
        self.app_desc_lbl.setFont(QFont("sans-serif", 10))
        self.app_desc_lbl.setStyleSheet("color: #d1d5db;")
        app_specs = QLabel("Pure Python 3 & PyQt6 | Native Translation Dictionary Engines")
        specs_font = QFont("sans-serif", 9)
        specs_font.setItalic(True)
        app_specs.setFont(specs_font)
        app_specs.setStyleSheet("color: #71717a;")
        text_layout.addWidget(app_title)
        text_layout.addWidget(self.app_version_lbl)
        text_layout.addWidget(self.app_desc_lbl)
        text_layout.addWidget(app_specs)
        about_layout.addLayout(text_layout)
        about_layout.addStretch()

        page_main_layout.addWidget(about_frame)

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

    def init_single_instance_server(self):
        self.instance_server = QLocalServer(self)
        # Verhindert Überbleibsel von Abstürzen auf Unix-Sockets
        QLocalServer.removeServer("matrixwhisper_socket")
        self.instance_server.listen("matrixwhisper_socket")
        self.instance_server.newConnection.connect(self.handle_remote_activation)

    def handle_remote_activation(self):
        socket = self.instance_server.nextPendingConnection()
        if socket:
            socket.readyRead.connect(lambda: self.process_remote_command(socket))

    def process_remote_command(self, socket):
        cmd = socket.readAll().data().decode().strip()
        if cmd == "toggle":
            if self.isVisible() and not self.isMinimized():
                self.hide()
            else:
                self.show()
                self.raise_()
                self.activateWindow()
        elif cmd == "mute":
            self.activate_smart_mute(8)
        elif cmd == "quit":
            QApplication.instance().quit()
        elif cmd == "show":
            self.show()
            self.raise_()
            self.activateWindow()
        socket.close()

    def determine_ui_language_key(self):
        if self.selected_language != "system":
            return self.selected_language if self.selected_language in TRANSLATIONS else "en"
        try:
            sys_locale = locale.getdefaultlocale()[0]
            if sys_locale:
                lang_code = sys_locale.split("_")[0]
                if lang_code in TRANSLATIONS:
                    return lang_code
        except Exception:
            pass
        return "en"

    def retranslate_ui(self):
        lang = self.ui_lang
        t = TRANSLATIONS[lang]

        self.btn_settings.setToolTip(t["title"])
        self.title_label.setText(t["title"])
        self.as_title.setText(t["as_title"])
        self.as_desc.setText(t["as_desc"])
        self.dm_title.setText(t["dm_title"])
        self.dm_desc.setText(t["dm_desc"])
        self.tb_title.setText(t["tb_title"])
        self.tb_desc.setText(t["tb_desc"])
        self.nt_title.setText(t["nt_title"])
        self.nt_desc.setText(t["nt_desc"])
        self.gpu_title.setText(t["gpu_title"])
        self.mute_title.setText(t["mute_title"])
        self.btn_mute_1h.setText(t["mute_btn_1h"])
        self.btn_mute_8h.setText(t["mute_btn_8h"])
        self.btn_mute_reset.setText(t["mute_btn_reset"])
        self.lang_title.setText(t["lang_title"])
        self.zoom_title.setText(t["zoom_title"])
        self.zoom_desc_label.setText(t["zoom_desc"])
        self.cache_title.setText(t["cache_title"])
        self.cache_desc.setText(t["cache_desc"])
        self.btn_reset_cache.setText(t["cache_btn"])
        self.app_desc_lbl.setText(t["about_desc"])

        resolved = self.resolve_http_language_string().split(",")[0]
        self.lang_status_label.setText(f"{t['lang_header']} {resolved}")

    def setup_tray_menu(self):
        t = TRANSLATIONS[self.ui_lang]

        if hasattr(self, 'tray_menu') and self.tray_menu:
            self.tray_menu.clear()
        else:
            self.tray_menu = QMenu()

        show_action = QAction(t["tray_open"], self)
        quit_action = QAction(t["tray_quit"], self)

        self.mute_tray_action = QAction(t["tray_mute_shortcut"], self)
        self.mute_tray_action.setCheckable(True)

        if self.mute_until_time and self.mute_until_time > datetime.now():
            self.mute_tray_action.setChecked(True)

        self.mute_tray_action.toggled.connect(self.toggle_tray_mute_from_action)

        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(QApplication.instance().quit)

        self.tray_menu.addAction(show_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.mute_tray_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)

    def preload_config_metadata(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                self.zoom_factor = config.get("zoom_factor", 1.1)
                self.selected_language = config.get("language_selection", "system")
                self.minimize_to_tray = config.get("minimize_to_tray", True)
                self.native_notifications = config.get("native_notifications", True)
                self.disable_gpu_accel = config.get("disable_gpu_acceleration", False)
            except Exception as e:
                print(f"Fehler beim Preload der Config: {e}")

    def resolve_http_language_string(self):
        if self.selected_language == "system":
            try:
                sys_locale = locale.getdefaultlocale()[0]
                if sys_locale:
                    sys_lang = sys_locale.replace("_", "-")
                    return f"{sys_lang},{sys_lang[:2]};q=0.9,en-US;q=0.8,en;q=0.7"
            except Exception:
                pass
            return "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7"
        elif self.selected_language == "de": return "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7"
        elif self.selected_language == "en": return "en-US,en;q=0.9"
        elif self.selected_language == "es": return "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7"
        elif self.selected_language == "fr": return "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"
        elif self.selected_language == "it": return "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7"
        elif self.selected_language == "nl": return "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7"
        elif self.selected_language == "pt": return "pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7"
        elif self.selected_language == "pl": return "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"
        return "de-DE,de;q=0.9"

    def sync_loaded_settings_to_ui(self):
        t = TRANSLATIONS[self.ui_lang]
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                mute_until_str = config.get("mute_until", None)
                if mute_until_str:
                    mute_until = datetime.fromisoformat(mute_until_str)
                    if mute_until > datetime.now():
                        remaining_seconds = (mute_until - datetime.now()).total_seconds()
                        remaining_hours = max(1, math.ceil(remaining_seconds / 3600.0))
                        self.activate_smart_mute(remaining_hours)
                    else:
                        self.mute_status_label.setText(t["mute_active"])
                else:
                    self.mute_status_label.setText(t["mute_active"])
            except Exception as e:
                print(f"Fehler beim Sync der Config: {e}")
        else:
            self.mute_status_label.setText(t["mute_active"])

        self.zoom_slider.setValue(int(self.zoom_factor * 100))
        self.lbl_percent.setText(f"{int(self.zoom_factor * 100)}%")
        self.browser.setZoomFactor(self.zoom_factor)

        if self.disable_gpu_accel:
            self.gpu_status_label.setText(t["gpu_active"])
            self.gpu_status_label.setStyleSheet("color: #e03131; font-weight: bold; font-size: 10pt;")
        else:
            self.gpu_status_label.setText(t["gpu_reboot_off"])

    def save_settings(self):
        if self.is_initializing: return
        config = {
            "zoom_factor": self.zoom_factor,
            "language_selection": self.selected_language,
            "minimize_to_tray": self.minimize_to_tray,
            "native_notifications": self.native_notifications,
            "disable_gpu_acceleration": self.disable_gpu_accel,
            "mute_until": self.mute_until_time.isoformat() if self.mute_until_time else None
        }
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Fehler beim Speichern der Konfiguration: {e}")

    def toggle_tray_behavior(self, checked):
        self.minimize_to_tray = checked
        self.save_settings()

    def toggle_native_notifications(self, checked):
        self.native_notifications = checked
        self.save_settings()

    def handle_web_notification(self, notification: QWebEngineNotification):
        if self.native_notifications and (not self.isVisible() or self.isMinimized()):
            self.tray_icon.showMessage(
                notification.title(),
                notification.message(),
                QSystemTrayIcon.MessageIcon.Information,
                4000
            )
        notification.accept()

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
        except Exception as e:
            print(f"Fehler beim physischen Löschen des Caches: {e}")

        self.browser.setUrl(QUrl("https://web.whatsapp.com"))
        self.switch_view(0)

    def toggle_gpu_acceleration(self, checked):
        self.disable_gpu_accel = checked
        self.save_settings()
        t = TRANSLATIONS[self.ui_lang]
        if checked:
            self.gpu_status_label.setText(t["gpu_reboot_on"])
            self.gpu_status_label.setStyleSheet("color: #e03131; font-weight: bold; font-size: 10pt;")
        else:
            self.gpu_status_label.setText(t["gpu_reboot_off"])
            self.gpu_status_label.setStyleSheet("color: #a0a0a0; font-size: 10pt;")

    def change_language_selection(self, index):
        self.selected_language = self.combo_lang.itemData(index)
        self.save_settings()
        self.ui_lang = self.determine_ui_language_key()
        self.retranslate_ui()
        self.setup_tray_menu()

        t = TRANSLATIONS[self.ui_lang]
        resolved = self.resolve_http_language_string().split(",")[0]
        self.lang_status_label.setText(f"{t['lang_reboot']} {resolved} ⚠️")
        self.lang_status_label.setStyleSheet("color: #e03131; font-weight: bold; font-size: 10pt;")

    def activate_smart_mute(self, hours):
        if self.mute_timer: self.mute_timer.stop()
        self.browser.page().setAudioMuted(True)
        self.mute_until_time = datetime.now() + timedelta(hours=hours)
        formatted_time = self.mute_until_time.strftime("%H:%M")

        if self.ui_lang == "de": prefix = "Stumm bis"
        else: prefix = "Muted until"

        self.mute_status_label.setText(f"{prefix} {formatted_time}")
        self.mute_status_label.setStyleSheet("color: #e03131; font-weight: bold; font-size: 10pt;")
        if hours == 8:
            self.mute_tray_action.blockSignals(True)
            self.mute_tray_action.setChecked(True)
            self.mute_tray_action.blockSignals(False)
        self.save_settings()
        self.mute_timer = QTimer(self)
        self.mute_timer.singleShot(hours * 3600000, self.deactivate_smart_mute)

    def deactivate_smart_mute(self):
        self.browser.page().setAudioMuted(False)
        t = TRANSLATIONS[self.ui_lang]
        self.mute_status_label.setText(t["mute_active"])
        self.mute_status_label.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        self.mute_tray_action.blockSignals(True)
        self.mute_tray_action.setChecked(False)
        self.mute_tray_action.blockSignals(False)
        if self.mute_timer:
            self.mute_timer.stop()
            self.mute_timer = None
        self.mute_until_time = None
        self.save_settings()

    def toggle_tray_mute_from_action(self, checked):
        if checked: self.activate_smart_mute(8)
        else: self.deactivate_smart_mute()

    def update_zoom_factor(self, value):
        self.zoom_factor = value / 100.0
        self.browser.setZoomFactor(self.zoom_factor)
        self.lbl_percent.setText(f"{value}%")
        self.save_settings()

    def draw_vector_chat_icon(self):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor("#25D366"), 2)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)
        rect = QRectF(2, 4, 28, 19)
        painter.drawRoundedRect(rect, 5, 5)
        triangle = QPolygonF()
        triangle.append(QPointF(6.0, 23.0))
        triangle.append(QPointF(12.0, 23.0))
        triangle.append(QPointF(6.0, 28.0))
        painter.drawPolygon(triangle)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#1e222b"))
        painter.drawRect(QRectF(6.5, 22.0, 5.0, 2.0))
        painter.end()
        return QIcon(pixmap)

    def draw_vector_sliders_icon(self):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor("#25D366"), 2)
        painter.setPen(pen)
        y_positions = [8.0, 16.0, 24.0]
        knob_x_positions = [22.0, 10.0, 18.0]
        for i in range(3):
            y = y_positions[i]
            kx = knob_x_positions[i]
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawLine(QPointF(4.0, y), QPointF(28.0, y))
            painter.setBrush(QColor("#1e222b"))
            painter.drawEllipse(QPointF(kx, y), 3.0, 3.0)
        painter.end()
        return QIcon(pixmap)

    def switch_view(self, index):
        self.container.setCurrentIndex(index)
        self.btn_chat.setChecked(index == 0)
        self.btn_settings.setChecked(index == 1)

    def handle_permission_requested(self, request):
        request.grant()

    def toggle_autostart(self, checked):
        if checked:
            os.makedirs(self.autostart_dir, exist_ok=True)
            desktop_entry = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=MatrixWhisper
Comment=MatrixWhisper im Hintergrund starten
Exec=python3 {os.path.abspath(__file__)} --minimized
Icon={self.icon_path}
Terminal=false
Categories=Network;InstantMessaging;
StartupWMClass=matrixwhisper.py
"""
            try:
                with open(self.autostart_file, "w", encoding="utf-8") as f:
                    f.write(desktop_entry)
                os.chmod(self.autostart_file, 0o755)
            except Exception as e:
                print(f"Fehler beim Erstellen des Autostarts: {e}")
                self.cb_autostart.setChecked(False)
        else:
            if os.path.exists(self.autostart_file):
                try: os.remove(self.autostart_file)
                except Exception as e: print(f"Fehler beim Löschen des Autostarts: {e}")

    def toggle_darkmode(self, checked):
        if checked: self.browser.page().runJavaScript("document.body.classList.add('dark');")
        else: self.browser.page().runJavaScript("document.body.classList.remove('dark');")

    def apply_darkmode_on_load(self, success):
        if success and self.cb_darkmode.isChecked(): self.toggle_darkmode(True)

    def create_badge_icon(self, count):
        if not os.path.exists(self.icon_path): return QIcon.fromTheme("mail-message")
        base_pixmap = QPixmap(self.icon_path)
        if base_pixmap.isNull(): return QIcon.fromTheme("mail-message")
        if count > 0:
            badge_pixmap = base_pixmap.copy()
            painter = QPainter(badge_pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            w = badge_pixmap.width()
            radius = int(w * 0.28)
            center_x = w - radius - 1
            center_y = radius + 1
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(239, 68, 68))
            painter.drawEllipse(QPoint(center_x, center_y), radius, radius)
            text = str(count) if count < 10 else "9+"
            font = QFont("sans-serif", int(radius * 1.25), QFont.Weight.Bold)
            painter.setFont(font)
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(center_x - radius, center_y - radius, radius * 2, radius * 2, Qt.AlignmentFlag.AlignCenter, text)
            painter.end()
            return QIcon(badge_pixmap)
        return QIcon(base_pixmap)

    def update_app_icons(self, count):
        icon = self.create_badge_icon(count)
        self.setWindowIcon(icon)
        if hasattr(self, 'tray_icon'): self.tray_icon.setIcon(icon)

    def check_notifications(self, title):
        match = re.search(r'\((\d+)\)', title)
        if match:
            anzahl = int(match.group(1))
            self.setWindowTitle(f"{self.app_name} ({anzahl} ungelesen)")
            self.tray_icon.setToolTip(f"{self.app_name}: {anzahl} ungelesene Nachrichten")
            self.update_app_icons(anzahl)
            if self.cb_darkmode.isChecked(): self.toggle_darkmode(True)
        else:
            self.setWindowTitle(self.app_name)
            self.tray_icon.setToolTip(self.app_name)
            self.update_app_icons(0)

    def closeEvent(self, event):
        if self.minimize_to_tray:
            event.ignore()
            self.hide()
            t = TRANSLATIONS[self.ui_lang]
            self.tray_icon.showMessage(
                self.app_name, t["tray_whisper"],
                QSystemTrayIcon.MessageIcon.Information, 2000
            )
        else:
            QApplication.instance().quit()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible(): self.hide()
            else:
                self.show()
                self.raise_()
                self.activateWindow()

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # 1. Argument-Parser für CLI definieren
    parser = argparse.ArgumentParser(description="MatrixWhisper CLI Controller")
    parser.add_argument("--minimized", action="store_true", help="Startet die App direkt minimiert im System-Tray")
    parser.add_argument("--toggle", action="store_true", help="Blendet das Fenster der laufenden Instanz ein oder aus")
    parser.add_argument("--mute", action="store_true", help="Schaltet die laufende Instanz sofort für 8 Stunden lautlos")
    parser.add_argument("--quit", action="store_true", help="Beendet die im Hintergrund laufende Instanz sauber")
    args = parser.parse_args()

    # 2. IPC Socket-Check: Läuft bereits eine Instanz?
    socket = QLocalSocket()
    socket.connectToServer("matrixwhisper_socket")

    if socket.waitForConnected(500):
        # Nachricht an Hauptinstanz senden
        if args.toggle:
            socket.write(b"toggle")
        elif args.mute:
            socket.write(b"mute")
        elif args.quit:
            socket.write(b"quit")
        else:
            socket.write(b"show")

        socket.waitForBytesWritten()
        socket.close()
        sys.exit(0) # Sekundäre Instanz beendet sich sofort nach Signalübergabe

    # 3. Master-Instanz initialisieren, falls noch kein Server läuft
    gitignore_file = os.path.join(script_directory, ".gitignore")
    if not os.path.exists(gitignore_file):
        try:
            with open(gitignore_file, "w", encoding="utf-8") as f:
                f.write("config.json\n__pycache__/\n*.pyc\n")
        except Exception:
            pass

    cfg_file = os.path.join(script_directory, "config.json")
    if os.path.exists(cfg_file):
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                raw_cfg = json.load(f)
            if raw_cfg.get("disable_gpu_acceleration", False):
                sys.argv.append("--disable-gpu")
                sys.argv.append("--disable-software-rasterizer")
                print("[MatrixWhisper] Power saver active: Hardware acceleration throttle enabled.")
        except Exception:
            pass

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setOrganizationName("the-media-matrix")
    app.setApplicationName("MatrixWhisper")

    window = MatrixWhisper()

    # Auswertung des Initialstarts (--minimized)
    if not args.minimized:
        window.show()

    sys.exit(app.exec())
