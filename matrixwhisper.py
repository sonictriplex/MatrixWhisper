import os
import sys
import re
import math
import time
import json
import locale
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QApplication, QMainWindow, QSystemTrayIcon, QMenu,
                             QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
                             QStackedWidget, QCheckBox, QLabel, QFrame, QSlider,
                             QComboBox)
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings, QWebEngineScript, QWebEnginePage
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QStandardPaths, Qt, QPoint, QSize, QRectF, QPointF, QTimer, QPropertyAnimation, pyqtProperty
from PyQt6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor, QFont, QPolygonF, QPen, QBrush

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

        if self.isChecked():
            track_color = QColor("#25D366")
        else:
            track_color = QColor("#2c313c")

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


class MatrixWhisper(QMainWindow):
    def __init__(self):
        super().__init__()

        self.app_name = "MatrixWhisper"
        self.setWindowTitle(self.app_name)
        self.resize(1150, 750)

        # Pfade ermitteln
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.icon_path = os.path.join(self.script_dir, "media-matrix-logo.png")
        self.config_path = os.path.join(self.script_dir, "config.json")

        self.autostart_dir = os.path.join(os.path.expanduser("~"), ".config", "autostart")
        self.autostart_file = os.path.join(self.autostart_dir, "matrixwhisper.desktop")

        # --- VARIABLEN MIT STANDARDWERTEN ---
        self.zoom_factor = 1.1
        self.mute_timer = None
        self.mute_until_time = None
        self.selected_language = "system"
        self.minimize_to_tray = True          # NEU: Standardmäßig minimieren anstatt schließen
        self.disable_gpu_accel = False         # NEU: Standardmäßig GPU anlassen

        self.is_initializing = True

        # --- CONFIGURATION PRELOAD ---
        self.preload_config_metadata()

        # Session-Profil & Browser laden
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)

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

        # JS-Injektion für Speicher-Persistenz
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

        # --- HAUPTLAYOUT MIT SEITENLEISTE ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Die linke Seitenleiste bauen
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
        self.btn_settings.setToolTip("Einstellungen")

        self.btn_chat.clicked.connect(lambda: self.switch_view(0))
        self.btn_settings.clicked.connect(lambda: self.switch_view(1))

        sidebar_layout.addWidget(self.btn_chat)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btn_settings)

        # Den Hauptbereich (Stapel-Karten) bauen
        self.container = QStackedWidget()

        # Karte 0: WhatsApp Browser
        self.browser = QWebEngineView()
        self.web_page = QWebEnginePage(self.profile, self.browser)
        self.browser.setPage(self.web_page)
        self.browser.setUrl(QUrl("https://web.whatsapp.com"))
        self.container.addWidget(self.browser)

        # Karte 1: Einstellungs-Ansicht
        self.settings_page = QWidget()
        self.settings_page.setStyleSheet("background-color: #1a1d24; color: #ffffff;")
        settings_layout = QVBoxLayout(self.settings_page)
        settings_layout.setContentsMargins(30, 30, 30, 30)
        settings_layout.setSpacing(14) # Minimal kompakter für die neuen Karten

        title_label = QLabel("Einstellungen")
        title_label.setFont(QFont("sans-serif", 18, QFont.Weight.Bold))
        settings_layout.addWidget(title_label)

        # Trennlinie
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #2c313c;")
        settings_layout.addWidget(line)

        # Gemeinsames Stylesheet für alle Einstellungs-Karten
        card_style = """
            QFrame { background-color: #1e222b; border-radius: 12px; border: 1px solid #2c313c; }
            QLabel { border: none; background: transparent; }
        """

        # --- CARD 1: SYSTEMSTART ---
        autostart_frame = QFrame()
        autostart_frame.setStyleSheet(card_style)
        autostart_layout = QHBoxLayout(autostart_frame)
        autostart_layout.setContentsMargins(15, 12, 15, 12)

        as_icon = QLabel("⚙️")
        as_icon.setFont(QFont("sans-serif", 20))
        autostart_layout.addWidget(as_icon)

        as_text_layout = QVBoxLayout()
        as_title = QLabel("Systemstart (Autostart)")
        as_title.setFont(QFont("sans-serif", 12, QFont.Weight.Bold))
        as_desc = QLabel("Startet MatrixWhisper automatisch mit dem Computer")
        as_desc.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        as_text_layout.addWidget(as_title)
        as_text_layout.addWidget(as_desc)
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
        dm_title = QLabel("Erscheinungsbild (Dark Theme)")
        dm_title.setFont(QFont("sans-serif", 12, QFont.Weight.Bold))
        dm_desc = QLabel("Erzwingt das dunkle WhatsApp-Theme in der Web-Oberfläche")
        dm_desc.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        dm_text_layout.addWidget(dm_title)
        dm_text_layout.addWidget(dm_desc)
        darkmode_layout.addLayout(dm_text_layout)

        darkmode_layout.addStretch()

        self.cb_darkmode = SwitchToggle()
        self.cb_darkmode.setChecked(True)
        self.cb_darkmode.thumb_position = 27.0 if self.cb_darkmode.isChecked() else 3.0
        self.cb_darkmode.toggled.connect(self.toggle_darkmode)
        darkmode_layout.addWidget(self.cb_darkmode)
        settings_layout.addWidget(darkmode_frame)

        # --- NEU - CARD 6: TRAY BEHAVIOR ---
        tray_behavior_frame = QFrame()
        tray_behavior_frame.setStyleSheet(card_style)
        tray_behavior_layout = QHBoxLayout(tray_behavior_frame)
        tray_behavior_layout.setContentsMargins(15, 12, 15, 12)

        tb_icon = QLabel("📥")
        tb_icon.setFont(QFont("sans-serif", 20))
        tray_behavior_layout.addWidget(tb_icon)

        tb_text_layout = QVBoxLayout()
        tb_title = QLabel("Schließen ins Tray (Hintergrund)")
        tb_title.setFont(QFont("sans-serif", 12, QFont.Weight.Bold))
        tb_desc = QLabel("Fenster beim Schließen ('X') im Systemabschnitt verstecken")
        tb_desc.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        tb_text_layout.addWidget(tb_title)
        tb_text_layout.addWidget(tb_desc)
        tray_behavior_layout.addLayout(tb_text_layout)

        tray_behavior_layout.addStretch()

        self.cb_tray_behavior = SwitchToggle()
        self.cb_tray_behavior.setChecked(self.minimize_to_tray)
        self.cb_tray_behavior.thumb_position = 27.0 if self.cb_tray_behavior.isChecked() else 3.0
        self.cb_tray_behavior.toggled.connect(self.toggle_tray_behavior)
        tray_behavior_layout.addWidget(self.cb_tray_behavior)
        settings_layout.addWidget(tray_behavior_frame)

        # --- NEU - CARD 7: HARDWARE ACCELERATION CONTROL ---
        gpu_frame = QFrame()
        gpu_frame.setStyleSheet(card_style)
        gpu_layout = QHBoxLayout(gpu_frame)
        gpu_layout.setContentsMargins(15, 12, 15, 12)

        gpu_icon = QLabel("🔋")
        gpu_icon.setFont(QFont("sans-serif", 20))
        gpu_layout.addWidget(gpu_icon)

        gpu_text_layout = QVBoxLayout()
        gpu_title = QLabel("Stromsparmodus (GPU-Drossel)")
        gpu_title.setFont(QFont("sans-serif", 12, QFont.Weight.Bold))
        self.gpu_status_label = QLabel("Hardware-Beschleunigung der WebEngine abschalten")
        self.gpu_status_label.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        gpu_text_layout.addWidget(gpu_title)
        gpu_text_layout.addWidget(self.gpu_status_label)
        gpu_layout.addLayout(gpu_text_layout)

        gpu_layout.addStretch()

        self.cb_gpu_accel = SwitchToggle()
        self.cb_gpu_accel.setChecked(self.disable_gpu_accel)
        self.cb_gpu_accel.thumb_position = 27.0 if self.cb_gpu_accel.isChecked() else 3.0
        self.cb_gpu_accel.toggled.connect(self.toggle_gpu_acceleration)
        gpu_layout.addWidget(self.cb_gpu_accel)
        settings_layout.addWidget(gpu_frame)

        # --- CARD 3: SMART MUTE BEREICH ---
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
        mute_title = QLabel("Lautloser Wächter (Smart Mute)")
        mute_title.setFont(QFont("sans-serif", 12, QFont.Weight.Bold))
        self.mute_status_label = QLabel("Audioausgabe: Aktiv")
        self.mute_status_label.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        mute_text_layout.addWidget(mute_title)
        mute_text_layout.addWidget(self.mute_status_label)
        mute_layout.addLayout(mute_text_layout)

        mute_layout.addStretch()

        btn_mute_1h = QPushButton("1h Stumm")
        btn_mute_8h = QPushButton("8h Stumm")
        btn_mute_reset = QPushButton("Reset")

        btn_mute_1h.clicked.connect(lambda: self.activate_smart_mute(1))
        btn_mute_8h.clicked.connect(lambda: self.activate_smart_mute(8))
        btn_mute_reset.clicked.connect(self.deactivate_smart_mute)

        mute_layout.addWidget(btn_mute_1h)
        mute_layout.addWidget(btn_mute_8h)
        mute_layout.addWidget(btn_mute_reset)
        settings_layout.addWidget(mute_frame)

        # --- CARD 5: SPRACHEINSTELLUNGEN ---
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
        lang_title = QLabel("Anzeigesprache (Locale Profile)")
        lang_title.setFont(QFont("sans-serif", 12, QFont.Weight.Bold))
        self.lang_status_label = QLabel(f"Aktueller Header: {resolved_lang.split(',')[0]}")
        self.lang_status_label.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        lang_text_layout.addWidget(lang_title)
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
        if index != -1:
            self.combo_lang.setCurrentIndex(index)

        self.combo_lang.currentIndexChanged.connect(self.change_language_selection)
        lang_layout.addWidget(self.combo_lang)
        settings_layout.addWidget(lang_frame)

        # --- CARD 4: ZOOM FAKTOR BEREICH ---
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
        zoom_title = QLabel("HiDPI / Ultrawide Zoom-Faktor")
        zoom_title.setFont(QFont("sans-serif", 12, QFont.Weight.Bold))
        self.zoom_status_label = QLabel("Skalierung der WhatsApp Web-Oberfläche")
        self.zoom_status_label.setStyleSheet("color: #a0a0a0; font-size: 10pt;")
        zoom_text_layout.addWidget(zoom_title)
        zoom_text_layout.addWidget(self.zoom_status_label)
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

        # --- ELEGANTES "ÜBER DIESE APP" MODUL ---
        about_frame = QFrame()
        about_frame.setStyleSheet("""
            QFrame { background-color: #1e222b; border-radius: 12px; border: 1px solid #2c313c; }
            QLabel { border: none; background: transparent; }
        """)
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

        app_version = QLabel("Version 2.0 (Ultimate Feature-Complete Brett)")
        app_version.setFont(QFont("sans-serif", 10))
        app_version.setStyleSheet("color: #a0a0a0;")

        app_desc = QLabel("Ein hochoptimierter, nativer WhatsApp-Client für Linux Desktops.")
        app_desc.setFont(QFont("sans-serif", 10))
        app_desc.setStyleSheet("color: #d1d5db;")

        app_specs = QLabel("Pure Python 3 & PyQt6 | Hardware-Throttle & Custom Vector Engines")
        specs_font = QFont("sans-serif", 9)
        specs_font.setItalic(True)
        app_specs.setFont(specs_font)
        app_specs.setStyleSheet("color: #71717a;")

        text_layout.addWidget(app_title)
        text_layout.addWidget(app_version)
        text_layout.addWidget(app_desc)
        text_layout.addWidget(app_specs)

        about_layout.addLayout(text_layout)
        about_layout.addStretch()
        settings_layout.addWidget(about_frame)

        self.container.addWidget(self.settings_page)
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.container)

        self.browser.page().permissionRequested.connect(self.handle_permission_requested)
        self.browser.titleChanged.connect(self.check_notifications)
        self.browser.loadFinished.connect(self.apply_darkmode_on_load)

        # System-Tray-Icon einrichten
        self.tray_icon = QSystemTrayIcon(self)
        self.update_app_icons(0)

        tray_menu = QMenu()
        show_action = QAction("Öffnen", self)
        quit_action = QAction("Beenden", self)

        self.mute_tray_action = QAction("Stummschalten (8h Schnellwahl)", self)
        self.mute_tray_action.setCheckable(True)
        self.mute_tray_action.toggled.connect(self.toggle_tray_mute_from_action)

        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(QApplication.instance().quit)

        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(self.mute_tray_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_icon_activated)

        self.sync_loaded_settings_to_ui()
        self.is_initializing = False

    # --- CONFIGURATION (JSON PERSISTENZ) ---
    def preload_config_metadata(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                self.zoom_factor = config.get("zoom_factor", 1.1)
                self.selected_language = config.get("language_selection", "system")
                self.minimize_to_tray = config.get("minimize_to_tray", True)
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
            except Exception as e:
                print(f"Fehler beim Sync der Config: {e}")

        self.zoom_slider.setValue(int(self.zoom_factor * 100))
        self.lbl_percent.setText(f"{int(self.zoom_factor * 100)}%")
        self.browser.setZoomFactor(self.zoom_factor)

        # GPU Statusanzeige initialisieren
        if self.disable_gpu_accel:
            self.gpu_status_label.setText("Status: GPU deaktiviert (Stromsparmodus aktiv) ⚠️")
            self.gpu_status_label.setStyleSheet("color: #e03131; font-weight: bold; font-size: 10pt;")

    def save_settings(self):
        if self.is_initializing:
            return

        config = {
            "zoom_factor": self.zoom_factor,
            "language_selection": self.selected_language,
            "minimize_to_tray": self.minimize_to_tray,
            "disable_gpu_acceleration": self.disable_gpu_accel,
            "mute_until": self.mute_until_time.isoformat() if self.mute_until_time else None
        }
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Fehler beim Speichern der Konfiguration: {e}")

    # --- TOGGLE SLIDER LOGIKEN ---
    def toggle_tray_behavior(self, checked):
        """ Toggelt, ob das Schließen ('X') die App killt oder ins Tray schiebt """
        self.minimize_to_tray = checked
        self.save_settings()

    def toggle_gpu_acceleration(self, checked):
        """ Schaltet die GPU-Beschleunigung um (erfordert Neustart) """
        self.disable_gpu_accel = checked
        self.save_settings()
        if checked:
            self.gpu_status_label.setText("Effekt nach Neustart: GPU wird abgeschaltet 🔋")
            self.gpu_status_label.setStyleSheet("color: #e03131; font-weight: bold; font-size: 10pt;")
        else:
            self.gpu_status_label.setText("Effekt nach Neustart: GPU wieder aktiv (Standard)")
            self.gpu_status_label.setStyleSheet("color: #a0a0a0; font-size: 10pt;")

    def change_language_selection(self, index):
        self.selected_language = self.combo_lang.itemData(index)
        self.save_settings()
        resolved = self.resolve_http_language_string().split(",")[0]
        self.lang_status_label.setText(f"Sprache nach Neustart: {resolved} ⚠️")
        self.lang_status_label.setStyleSheet("color: #e03131; font-weight: bold; font-size: 10pt;")

    # --- FUNKTIONEN FÜR SMART MUTE ---
    def activate_smart_mute(self, hours):
        if self.mute_timer: self.mute_timer.stop()
        self.browser.page().setAudioMuted(True)
        self.mute_until_time = datetime.now() + timedelta(hours=hours)
        formatted_time = self.mute_until_time.strftime("%H:%M")
        self.mute_status_label.setText(f"Audioausgabe: Stumm (bis {formatted_time})")
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
        self.mute_status_label.setText("Audioausgabe: Aktiv")
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
        """ Reagiert dynamisch auf das eingestellte Schließ-Verhalten """
        if self.minimize_to_tray:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                self.app_name, "Flüstert im Hintergrund weiter...",
                QSystemTrayIcon.MessageIcon.Information, 2000
            )
        else:
            # Wenn Schalter aus ist, App ganz normal beenden
            QApplication.instance().quit()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible(): self.hide()
            else:
                self.show()
                self.raise_()
                self.activateWindow()

if __name__ == "__main__":
    # --- FRÜHE PRÜFUNG DER HARDWARE-BESCHLEUNIGUNG ---
    # Wir müssen die config.json auslesen, BEVOR Qt irgendetwas anderes macht!
    script_directory = os.path.dirname(os.path.abspath(__file__))
    cfg_file = os.path.join(script_directory, "config.json")
    if os.path.exists(cfg_file):
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                raw_cfg = json.load(f)
            if raw_cfg.get("disable_gpu_acceleration", False):
                # Übergibt die Chromium-Flags direkt an das Backend, um die GPU schlafen zu legen
                sys.argv.append("--disable-gpu")
                sys.argv.append("--disable-software-rasterizer")
                print("[MatrixWhisper] Akkusparmodus aktiv: Hardware-Beschleunigung wurde gedrosselt.")
        except Exception:
            pass

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setOrganizationName("the-media-matrix")
    app.setApplicationName("MatrixWhisper")
    window = MatrixWhisper()
    if "--minimized" not in sys.argv:
        window.show()
    sys.exit(app.exec())
