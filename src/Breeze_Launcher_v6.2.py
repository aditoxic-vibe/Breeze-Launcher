#!/usr/bin/env python3

import gi
import os
import json
import time
import shutil
import subprocess
import datetime

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")

from gi.repository import Gtk, Gdk, Gio, GLib, Pango


VERSION = "v6.2"

SETTINGS_FILE = os.path.expanduser(
    "~/.config/rofi/chapter3_settings.json"
)

ERROR_LOG_FILE = os.path.expanduser(
    "~/.config/rofi/chapter3_errors.log"
)


FEATURES = [
    (
        "🪟  Glass Interface",
        "Dark translucent panels designed to blend with the desktop wallpaper."
    ),
    (
        "🔎  Application Search",
        "Search installed desktop applications."
    ),
    (
        "📱  Application Selection",
        "Click an application to select it. Press Enter or Open to launch it."
    ),
    (
        "⌨  Keyboard Controls",
        "Escape and Super close the launcher. Enter launches the selected application."
    ),
    (
        "♫  Media Controls",
        "Basic playback controls using playerctl."
    ),
    (
        "🔒  System Controls",
        "Quick access to Lock, Restart and Shutdown."
    ),
    (
        "🗑  Flatpak Uninstall",
        "Provides an uninstall action for Flatpak applications."
    ),
    (
        "📜  Changelog",
        "Detailed version history."
    ),
    (
        "⚡  Fun Optimization",
        "Reduces unnecessary background refreshes."
    ),
    (
        "✨  High Quality",
        "Uses richer typography and more detailed application information without huge icons."
    ),
    (
        "🟢  Keep Launcher Alive",
        "Keeps the launcher open after launching an application."
    ),
    (
        "📜  Error Logs",
        "Stores launcher errors in a local log file."
    ),
]


CHANGELOG = [
    (
        "v5.1",
        "SETTINGS • BUGFIX",
        "🔧",
        [
            (
                "Working Settings",
                "Rebuilt settings persistence so every toggle uses the same settings system."
            ),
            (
                "Keep Launcher Alive",
                "Launcher can now remain open after launching an application."
            ),
            (
                "Error Logs",
                "Error logging can now be enabled or disabled from Settings."
            ),
            (
                "Normal High Quality",
                "High Quality no longer uses oversized application icons."
            ),
            (
                "No Super Bubbly Buttons",
                "Restart and Shutdown can be hidden while Lock remains available."
            ),
        ],
    ),
    (
        "v5.0",
        "MAJOR UPDATE",
        "⛏",
        [
            (
                "Quality Profiles",
                "Introduced Low Quality and High Quality rendering profiles."
            ),
            (
                "Fun Optimization",
                "Reduces unnecessary refreshes and background work."
            ),
            (
                "Statistics for Nerds",
                "Adds detailed application information and launcher diagnostics."
            ),
            (
                "Persistent Settings",
                "Launcher settings are saved between launches."
            ),
        ],
    ),
    (
        "v4.2.0",
        "SETTINGS • UX",
        "⚙",
        [
            (
                "Fun Optimization",
                "Added persistent optimization mode."
            ),
            (
                "High Quality",
                "Added persistent quality mode."
            ),
            (
                "Statistics for Nerds",
                "Added launcher diagnostics."
            ),
            (
                "Smart Notifications",
                "Added contextual launcher notifications."
            ),
        ],
    ),
    (
        "v4.1.3",
        "UI • BUGFIX",
        "✨",
        [
            (
                "Changelog",
                "Changelog is displayed in its own window."
            ),
            (
                "Glass",
                "Improved translucent glass appearance."
            ),
        ],
    ),
    (
        "v4.0",
        "MAJOR UPDATE",
        "🚀",
        [
            (
                "Glass Interface",
                "Introduced the redesigned dark glass launcher."
            ),
            (
                "Application Selection",
                "Applications can be selected before launching."
            ),
            (
                "System Controls",
                "Added quick system controls."
            ),
        ],
    ),
    (
        "v3.0",
        "MAJOR UPDATE",
        "🔥",
        [
            (
                "Chapter 3",
                "Complete visual redesign of Breeze Launcher."
            ),
            (
                "Dark Glass",
                "Introduced the dark glass visual style."
            ),
            (
                "Launcher Structure",
                "Separated applications, information and controls."
            ),
        ],
    ),
    (
        "v2.0",
        "MAJOR UPDATE",
        "🌑",
        [
            (
                "Chapter 2",
                "Introduced the dark launcher concept."
            ),
            (
                "Transparent Panels",
                "Added translucent interface panels."
            ),
        ],
    ),
    (
        "v1.0",
        "INITIAL RELEASE",
        "🌱",
        [
            (
                "Breeze Launcher",
                "Initial launcher release."
            ),
            (
                "Application Launcher",
                "Basic application launching functionality."
            ),
        ],
    ),
]


def load_settings():
    defaults = {
        "fun_optimization": False,
        "high_quality": False,
        "nerd_stats": False,
        "keep_launcher_alive": False,
        "error_logs_enabled": False,
        "no_super_bubbly_buttons": False,
        "unnamed_5": False,
    }

    try:
        if os.path.exists(SETTINGS_FILE):
            with open(
                SETTINGS_FILE,
                "r",
                encoding="utf-8"
            ) as f:
                data = json.load(f)

            if isinstance(data, dict):
                defaults.update(data)

    except Exception:
        pass

    return defaults


def save_settings(data):
    try:
        os.makedirs(
            os.path.dirname(SETTINGS_FILE),
            exist_ok=True
        )

        tmp = SETTINGS_FILE + ".tmp"

        with open(
            tmp,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                data,
                f,
                indent=2
            )

        os.replace(
            tmp,
            SETTINGS_FILE
        )

    except Exception:
        pass


class StartMenu(Gtk.Window):

    def __init__(self):

        super().__init__(
            title="Breeze Launcher"
        )

        self.set_default_size(
            820,
            650
        )

        self.set_position(
            Gtk.WindowPosition.CENTER
        )

        self.set_decorated(False)
        self.set_resizable(False)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)

        # Breeze Launcher icon
        icon_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "assets",
                "breeze.png"
            )
        )
        if os.path.exists(icon_path):
            try:
                self.set_icon_from_file(icon_path)
            except Exception as error:
                self.log_error("Launcher icon error: " + str(error))

        visual = self.get_screen().get_rgba_visual()

        if visual:
            self.set_visual(visual)

        self.settings_data = load_settings()

        self.fun_optimization = bool(
            self.settings_data["fun_optimization"]
        )

        self.high_quality = bool(
            self.settings_data["high_quality"]
        )

        self.nerd_stats = bool(
            self.settings_data["nerd_stats"]
        )

        self.keep_launcher_alive = bool(
            self.settings_data["keep_launcher_alive"]
        )

        self.error_logs_enabled = bool(
            self.settings_data["error_logs_enabled"]
        )

        self.no_super_bubbly_buttons = bool(
            self.settings_data["no_super_bubbly_buttons"]
        )

        self.unnamed_5 = bool(
            self.settings_data["unnamed_5"]
        )

        self.apps = []
        self.selected = None
        self.selected_name = ""

        self.notice_timer = None
        self.media_timer = None

        self._system_action_buttons = []

        self.setup_css()
        self.build_ui()

        self.load_apps()
        self.update_media()
        self.update_clock()

        self.connect(
            "key-press-event",
            self.key_press
        )

        GLib.timeout_add_seconds(
            1,
            self.update_clock
        )

        self.start_media_timer()

        GLib.timeout_add(
            250,
            self.startup_notification
        )

    # ---------------------------------------------------------
    # SETTINGS
    # ---------------------------------------------------------

    def write_settings(self):

        self.settings_data = {
            "fun_optimization":
                self.fun_optimization,

            "high_quality":
                self.high_quality,

            "nerd_stats":
                self.nerd_stats,

            "keep_launcher_alive":
                self.keep_launcher_alive,

            "error_logs_enabled":
                self.error_logs_enabled,

            "no_super_bubbly_buttons":
                self.no_super_bubbly_buttons,

            "unnamed_5":
                self.unnamed_5,
        }

        save_settings(
            self.settings_data
        )

    def save_settings(self):
        self.write_settings()

    def apply_settings(self):

        self.write_settings()

        self.apply_quality()

        self.start_media_timer()

        self.update_bubbly_buttons()

        self.update_info()

    def toggle_setting(self, button, key):

        # GTK zawsze przekazuje button jako pierwszy argument,
        # a key jako argument z connect().
        if not isinstance(key, str):
            return

        if not hasattr(self, key):
            return

        value = not bool(
            getattr(
                self,
                key
            )
        )

        setattr(
            self,
            key,
            value
        )

        ctx = button.get_style_context()

        if value:
            ctx.add_class("on")
        else:
            ctx.remove_class("on")

        button.set_tooltip_text(
            "TRUE"
            if value
            else "FALSE"
        )

        self.apply_settings()

        if key == "no_super_bubbly_buttons":
            self.update_bubbly_buttons()

    def refresh_ui_animation(self):

        widgets = []

        if hasattr(self, "list"):
            widgets.append(self.list)
        if hasattr(self, "info"):
            widgets.append(self.info)

        for widget in widgets:
            widget.set_opacity(0.0)

        def refresh():
            self.apply_settings()

            animation = {"step": 0}

            def fade_in():
                animation["step"] += 1
                t = min(animation["step"] / 10.0, 1.0)
                eased = 1.0 - (1.0 - t) ** 3

                for widget in widgets:
                    widget.set_opacity(eased)

                return t < 1.0

            GLib.timeout_add(16, fade_in)
            return False

        GLib.timeout_add(80, refresh)

    def apply_quality(self):

        self.set_name(
            "quality_high"
            if self.high_quality
            else "quality_low"
        )

        if hasattr(self, "list"):
            self.populate(
                self.filtered_apps()
            )

        if hasattr(self, "info"):
            self.update_info()

    # ---------------------------------------------------------
    # NOTIFICATIONS / LOGS
    # ---------------------------------------------------------

    def startup_notification(self):

        self.show_notification(
            "SUCCESS",
            "Breeze Launcher loaded successfully."
        )

        return False

    def log_error(
        self,
        message
    ):

        message = str(
            message
        )

        if self.error_logs_enabled:

            try:

                os.makedirs(
                    os.path.dirname(
                        ERROR_LOG_FILE
                    ),
                    exist_ok=True
                )

                stamp = datetime.datetime.now().isoformat(
                    timespec="seconds"
                )

                with open(
                    ERROR_LOG_FILE,
                    "a",
                    encoding="utf-8"
                ) as f:

                    f.write(
                        f"[{stamp}] {message}\n"
                    )

            except Exception:
                pass

        self.show_notification(
            "ERROR",
            message
        )

    def show_notification(
        self,
        kind,
        message
    ):

        if not hasattr(self, "notification_box"):
            return

        for child in self.notification_box.get_children():
            self.notification_box.remove(child)

        card = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10
        )

        card.set_name("notification_card")
        card.set_opacity(0.0)
        card.set_margin_top(0)

        icon_map = {
            "SUCCESS": "✓",
            "INFO": "ⓘ",
            "ERROR": "!"
        }

        icon = Gtk.Label(
            label=icon_map.get(kind, "ⓘ")
        )
        icon.set_name("notification_icon")

        text_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=1
        )

        title = Gtk.Label(label=kind)
        title.set_name("notification_title")
        title.set_xalign(0)

        body = Gtk.Label(label=message)
        body.set_name("notification_text")
        body.set_xalign(0)
        body.set_line_wrap(True)

        text_box.pack_start(
            title,
            False,
            False,
            0
        )

        text_box.pack_start(
            body,
            False,
            False,
            0
        )

        card.pack_start(
            icon,
            False,
            False,
            0
        )

        card.pack_start(
            text_box,
            True,
            True,
            0
        )

        if (
            kind == "ERROR"
            and self.error_logs_enabled
            and os.path.exists(ERROR_LOG_FILE)
        ):

            copy_button = Gtk.Button(
                label="Copy Logs"
            )

            copy_button.set_name("notification_copy")

            copy_button.connect(
                "clicked",
                self.copy_logs
            )

            card.pack_end(
                copy_button,
                False,
                False,
                0
            )

        self.notification_box.pack_start(
            card,
            False,
            False,
            0
        )

        self.notification_box.show_all()

        # Smooth entrance animation
        animation = {
            "opacity": 0.0,
            "offset": -12.0,
            "step": 0
        }

        def animate_in():

            animation["step"] += 1

            t = min(
                animation["step"] / 12.0,
                1.0
            )

            # smooth ease-out
            eased = 1.0 - (1.0 - t) ** 3

            card.set_opacity(eased)


            if t >= 1.0:
                return False

            return True

        GLib.timeout_add(
            16,
            animate_in
        )

        if self.notice_timer:

            try:
                GLib.source_remove(
                    self.notice_timer
                )
            except Exception:
                pass

        self.notice_timer = GLib.timeout_add(
            3000,
            self.clear_notification
        )

    def clear_notification(self):

        if not hasattr(self, "notification_box"):
            return False

        children = self.notification_box.get_children()

        if not children:
            self.notice_timer = None
            return False

        card = children[0]

        animation = {
            "step": 0
        }

        def animate_out():

            animation["step"] += 1

            t = min(
                animation["step"] / 10.0,
                1.0
            )

            # smooth ease-in
            eased = t * t

            card.set_opacity(
                1.0 - eased
            )


            if t >= 1.0:

                try:
                    self.notification_box.remove(card)
                except Exception:
                    pass

                self.notice_timer = None

                return False

            return True

        GLib.timeout_add(
            16,
            animate_out
        )

        return False

    def copy_logs(
        self,
        button
    ):

        try:

            if not os.path.exists(
                ERROR_LOG_FILE
            ):
                return

            clipboard = Gtk.Clipboard.get(
                Gdk.SELECTION_CLIPBOARD
            )

            with open(
                ERROR_LOG_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                clipboard.set_text(
                    f.read(),
                    -1
                )

            self.show_notification(
                "SUCCESS",
                "Logs copied to clipboard."
            )

        except Exception as error:

            self.log_error(
                "Copy logs error: "
                + str(error)
            )

    # ---------------------------------------------------------
    # CSS
    # ---------------------------------------------------------

    def setup_css(self):

        css = """

        window {
            background-color: transparent;
        }

        * {
            font-family: Sans;
            color: #ffffff;
        }

        #top {
            background-color: rgba(25,31,43,0.68);
            border: 1px solid rgba(255,255,255,0.16);
            border-radius: 20px;
            padding: 10px 14px;
        }

        #brand {
            font-size: 14px;
            font-weight: 900;
        }

        #version {
            font-size: 10px;
            color: rgba(255,255,255,0.45);
            font-weight: 800;
        }

        #clock {
            font-size: 13px;
            font-weight: 900;
        }

        #panel {
            background-color: rgba(18,23,33,0.72);
            border: 1px solid rgba(255,255,255,0.13);
            border-radius: 22px;
            padding: 14px;
        }

        #search {
            background-color: rgba(8,12,19,0.54);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 15px;
            padding: 9px 12px;
            font-size: 13px;
            font-weight: 800;
        }

        #search:focus {
            border: 1px solid rgba(170,220,255,0.30);
        }

        #section {
            color: rgba(255,255,255,0.42);
            font-size: 9px;
            font-weight: 900;
            padding: 3px;
        }

        row {
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 11px;
            padding: 7px 9px;
        }

        row:hover {
            background-color: rgba(150,205,255,0.085);
            border: 1px solid rgba(255,255,255,0.075);
        }

        row:selected {
            background-color: rgba(125,190,245,0.13);
            border: 1px solid rgba(185,225,255,0.20);
        }

        row label {
            font-size: 13px;
            font-weight: 800;
        }

        #button {
            background-color: rgba(90,105,125,0.38);
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 13px;
            padding: 6px 10px;
            min-height: 30px;
            font-size: 11px;
            font-weight: 900;
        }

        #button:hover {
            background-color: rgba(125,160,190,0.42);
            border: 1px solid rgba(210,235,255,0.18);
        }

        #button:active {
            background-color: rgba(70,90,110,0.52);
            border: 1px solid rgba(255,255,255,0.12);
        }

        #button:focus {
            border: 0;
            outline: none;
            box-shadow: none;
        }

        #info {
            background-color: rgba(35,45,58,0.44);
            border: 1px solid rgba(255,255,255,0.09);
            border-radius: 14px;
            padding: 9px;
            font-size: 9px;
            font-weight: 700;
        }

        #media {
            background-color: rgba(17,23,33,0.48);
            border: 1px solid rgba(255,255,255,0.09);
            border-radius: 15px;
            padding: 9px;
        }

        #changelog_button {
            background-color: rgba(70,165,225,0.48);
            border: 1px solid rgba(170,225,255,0.30);
            border-radius: 11px;
            padding: 6px 11px;
            min-height: 30px;
            font-size: 11px;
            font-weight: 900;
            color: #e7f7ff;
        }

        #changelog_button:hover {
            background-color: rgba(90,185,240,0.62);
            border-color: rgba(205,240,255,0.45);
        }

        #changelog_button:focus,
        #changelog_button:active {
            background-color: rgba(65,155,215,0.56);
            border-color: rgba(180,230,255,0.36);
            box-shadow: none;
            outline: none;
        }

        #bottom {
            background-color: rgba(25,31,42,0.62);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 18px;
            padding: 5px;
        }

        #mac_close {
            background-color: #ff5f57;
            border: 0;
            border-radius: 50%;
            min-width: 14px;
            min-height: 14px;
            padding: 0;
            margin: 0;
            color: transparent;
        }

        #mac_close > * {
            min-width: 0;
            min-height: 0;
        }

        #mac_close:hover {
            background-color: #ff3b30;
        }

        #settings_button {
            background-color: rgba(90,110,135,0.36);
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 12px;
            min-width: 38px;
            min-height: 30px;
            padding: 0;
        }

        #settings_button:hover {
            background-color: rgba(105,105,105,0.70);
        }

        #settings_panel {
            background-color: rgba(19,24,35,0.84);
            border: 1px solid rgba(255,255,255,0.13);
            border-radius: 22px;
            padding: 18px;
        }

        #settings_title {
            font-family: "Noto Sans";
            font-size: 20px;
            font-weight: 900;
        }

        #setting_row {
            background-color: rgba(255,255,255,0.048);
            border: 1px solid rgba(255,255,255,0.055);
            border-radius: 15px;
            padding: 9px 13px;
            min-height: 42px;
        }

        #setting_row:hover {
            background-color: rgba(150,205,255,0.075);
            border: 1px solid rgba(255,255,255,0.10);
        }

        #setting_name {
            font-family: "Noto Sans";
            font-size: 13px;
            font-weight: 900;
        }

        #setting_desc {
            font-family: Sans;
            font-size: 10px;
            color: rgba(255,255,255,0.52);
        }

        /* SMALL ROUND TOGGLES */

        #toggle_dot {
            min-width: 10px;
            min-height: 10px;
            padding: 0;
            margin: 0;
            border: 0;
            border-radius: 999px;
            background-color: #ff5f57;
        }

        #toggle_dot.on {
            background-color: #34c759;
        }

        #toggle_dot:hover {
            background-color: #ff756e;
        }

        #toggle_dot.on:hover {
            background-color: #5ddd7b;
        }

        #toggle_dot:focus,
        #toggle_dot:active {
            border: 0;
            box-shadow: none;
            outline: none;
        }

        /* CHANGELOG TABS */

        #changelog_tab {
            background-color: rgba(125,195,240,0.20);
            border: 1px solid rgba(180,225,255,0.22);
            border-radius: 10px;
            padding: 7px 14px;
            min-width: 120px;
            min-height: 30px;
            font-size: 11px;
            font-weight: 900;
            color: #dff3ff;
        }

        #changelog_tab:hover {
            background-color: rgba(125,195,240,0.34);
            border-color: rgba(200,235,255,0.32);
        }

        #changelog_tab:focus,
        #changelog_tab:active {
            border: 0;
            box-shadow: none;
            outline: none;
        }

        #notification_card {
            background-color: rgba(55,165,225,0.46);
            border: 1px solid rgba(175,230,255,0.34);
            border-radius: 13px;
            padding: 8px 11px;
        }

        #notification_icon {
            font-size: 16px;
            font-weight: 900;
            color: #bfe8ff;
        }

        #notification_title {
            font-size: 10px;
            font-weight: 900;
            color: #dff4ff;
        }

        #notification_text {
            color: rgba(225,245,255,0.82);
            font-size: 10px;
        }

        #notification_copy {
            background: transparent;
            border: 0;
            color: #e2f6ff;
            font-size: 10px;
            font-weight: 800;
        }

        #dialog {
            background-color: rgba(19,24,35,0.84);
            border: 1px solid rgba(255,255,255,0.13);
            border-radius: 22px;
            padding: 13px;
        }

        #head {
            background-color: rgba(90,110,135,0.25);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 15px;
            padding: 10px;
        }

        #title {
            font-size: 18px;
            font-weight: 900;
        }

        #sub {
            font-size: 10px;
            color: rgba(255,255,255,0.52);
        }

        #entry {
            background-color: rgba(78,76,85,0.56);
            border-radius: 12px;
            padding: 10px;
        }

        #topic {
            color: #c9a7ff;
            font-size: 12px;
            font-weight: 900;
        }

        #desc {
            color: rgba(255,255,255,0.70);
            font-size: 10px;
        }

        #feature {
            background-color: rgba(78,76,85,0.56);
            border-radius: 12px;
            padding: 10px;
        }

        #featuretitle {
            color: #c9a7ff;
            font-size: 12px;
            font-weight: 900;
        }

        #featuredesc {
            color: rgba(255,255,255,0.70);
            font-size: 10px;
        }

        #forge_refresh {
            background-color: rgba(35,35,40,0.96);
            border-radius: 18px;
            padding: 18px;
        }

        #forge_icon {
            font-size: 42px;
            font-weight: 900;
        }

        #forge_text {
            font-family: "Noto Sans";
            font-size: 11px;
            font-weight: 800;
        }
        """

        provider = Gtk.CssProvider()

        provider.load_from_data(
            css.encode("utf-8")
        )

        Gtk.StyleContext.add_provider_for_screen(
            self.get_screen(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def build_ui(self):

        root = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8
        )

        root.set_border_width(
            10
        )

        self.main_box = root

        self.add(
            root
        )

        # TOP

        top = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL
        )

        top.set_name(
            "top"
        )

        brand = Gtk.Label(
            label="--Breeze Launcher"
        )

        brand.set_name(
            "brand"
        )

        version = Gtk.Label(
            label=VERSION
        )

        version.set_name(
            "version"
        )

        self.clock = Gtk.Label()

        self.clock.set_name(
            "clock"
        )

        top.pack_start(
            brand,
            False,
            False,
            0
        )

        top.pack_start(
            version,
            False,
            False,
            8
        )

        top.pack_end(
            self.clock,
            False,
            False,
            0
        )

        root.pack_start(
            top,
            False,
            False,
            0
        )

        # NOTIFICATIONS

        self.notification_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL
        )

        root.pack_start(
            self.notification_box,
            False,
            False,
            0
        )

        # MAIN

        main = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8
        )

        root.pack_start(
            main,
            True,
            True,
            0
        )

        # SIDE

        side = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=6
        )

        side.set_name(
            "panel"
        )

        side.set_size_request(
            210,
            -1
        )

        self.icon = Gtk.Image.new_from_icon_name(
            "application-x-executable-symbolic",
            Gtk.IconSize.LARGE_TOOLBAR
        )

        self.icon.set_pixel_size(
            40
        )

        side.pack_start(
            self.icon,
            False,
            False,
            6
        )

        self.name = Gtk.Label(
            label="Select an application"
        )

        self.name.set_xalign(
            0.5
        )

        self.name.set_ellipsize(
            Pango.EllipsizeMode.END
        )

        side.pack_start(
            self.name,
            False,
            False,
            2
        )

        side.pack_start(
            self.make_button(
                "↗  Open",
                self.open_app
            ),
            False,
            False,
            0
        )

        side.pack_start(
            self.make_button(
                "🗑  Uninstall",
                self.uninstall
            ),
            False,
            False,
            0
        )

        self.info = Gtk.Label(
            label="APPLICATION INFO\nSelect an application"
        )

        self.info.set_name(
            "info"
        )

        self.info.set_xalign(
            0
        )

        self.info.set_line_wrap(
            True
        )

        side.pack_start(
            self.info,
            False,
            False,
            0
        )

        # MEDIA

        media = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=2
        )

        media.set_name(
            "media"
        )

        self.media_player = Gtk.Label(
            label="NO PLAYER"
        )
        self.media_player.set_xalign(0)

        self.media_title = Gtk.Label(
            label="♫  No media playing"
        )
        self.media_title.set_xalign(0)
        self.media_title.set_line_wrap(False)

        self.media_artist = Gtk.Label(
            label=""
        )
        self.media_artist.set_xalign(0)

        self.media_status = Gtk.Label(
            label=""
        )
        self.media_status.set_xalign(0)

        media.pack_start(
            self.media_player,
            False,
            False,
            0
        )

        media.pack_start(
            self.media_title,
            False,
            False,
            0
        )

        media.pack_start(
            self.media_artist,
            False,
            False,
            0
        )

        media.pack_start(
            self.media_status,
            False,
            False,
            0
        )

        controls = Gtk.Box(
            spacing=3
        )

        self.media_buttons = {}

        for icon_name, command in [
            (
                "media-skip-backward-symbolic",
                "previous"
            ),
            (
                "media-playback-start-symbolic",
                "play-pause"
            ),
            (
                "media-skip-forward-symbolic",
                "next"
            ),
        ]:

            button = Gtk.Button()

            button.set_name(
                "button"
            )

            button.set_tooltip_text(
                {
                    "previous": "Previous track",
                    "play-pause": "Play / Pause",
                    "next": "Next track",
                }[command]
            )

            button.set_image(
                Gtk.Image.new_from_icon_name(
                    icon_name,
                    Gtk.IconSize.BUTTON
                )
            )

            button.connect(
                "clicked",
                self.media_command,
                command
            )

            self.media_buttons[command] = button

            controls.pack_start(
                button,
                True,
                True,
                0
            )

        media.pack_start(
            controls,
            False,
            False,
            0
        )

        side.pack_end(
            media,
            False,
            False,
            0
        )

        main.pack_start(
            side,
            False,
            False,
            0
        )

        # APPS

        apps = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=6
        )

        apps.set_name(
            "panel"
        )

        self.search = Gtk.SearchEntry()

        self.search.set_name(
            "search"
        )

        self.search.set_placeholder_text(
            "Search applications..."
        )

        self.search.connect(
            "search-changed",
            self.search_changed
        )

        apps.pack_start(
            self.search,
            False,
            False,
            0
        )

        section = Gtk.Label(
            label="APPLICATIONS"
        )

        section.set_name(
            "section"
        )

        section.set_xalign(
            0
        )

        apps.pack_start(
            section,
            False,
            False,
            0
        )

        scroll = Gtk.ScrolledWindow()

        scroll.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC
        )

        self.list = Gtk.ListBox()

        self.list.set_selection_mode(
            Gtk.SelectionMode.SINGLE
        )

        self.list.set_activate_on_single_click(
            False
        )

        self.list.connect(
            "row-selected",
            self.select
        )

        self.list.connect(
            "row-activated",
            self.activate
        )

        scroll.add(
            self.list
        )

        apps.pack_start(
            scroll,
            True,
            True,
            0
        )

        main.pack_start(
            apps,
            True,
            True,
            0
        )

        # LOWER

        lower = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=6
        )

        changelog_button = Gtk.Button(
            label="📜  Changelog"
        )

        changelog_button.set_name(
            "changelog_button"
        )

        changelog_button.connect(
            "clicked",
            self.changelog
        )

        settings_button = Gtk.Button()

        settings_button.set_name(
            "settings_button"
        )

        settings_button.set_relief(
            Gtk.ReliefStyle.NONE
        )

        settings_button.set_image(
            Gtk.Image.new_from_icon_name(
                "preferences-system-symbolic",
                Gtk.IconSize.BUTTON
            )
        )

        settings_button.set_tooltip_text(
            "Settings"
        )

        settings_button.connect(
            "clicked",
            self.settings
        )

        lower.pack_start(
            changelog_button,
            False,
            False,
            0
        )

        lower.pack_start(
            settings_button,
            False,
            False,
            0
        )

        # SYSTEM BUTTONS

        bottom = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=4
        )

        bottom.set_name(
            "bottom"
        )

        system_buttons = [
            (
                "system-lock-screen-symbolic",
                "Lock",
                self.lock
            ),
            (
                "system-reboot-symbolic",
                "Restart",
                self.restart
            ),
            (
                "system-shutdown-symbolic",
                "Shutdown",
                self.shutdown
            ),
        ]

        for icon_name, tooltip, callback in system_buttons:

            button = Gtk.Button()

            button.set_name(
                "button"
            )

            button.set_tooltip_text(
                tooltip
            )

            button.set_image(
                Gtk.Image.new_from_icon_name(
                    icon_name,
                    Gtk.IconSize.BUTTON
                )
            )

            button.connect(
                "clicked",
                callback
            )

            bottom.pack_start(
                button,
                True,
                True,
                0
            )

            self._system_action_buttons.append(
                button
            )

        lower.pack_start(
            bottom,
            True,
            True,
            0
        )

        root.pack_start(
            lower,
            False,
            False,
            0
        )

        self.update_bubbly_buttons()

    # ---------------------------------------------------------
    # BUTTONS
    # ---------------------------------------------------------

    def make_button(
        self,
        text,
        callback
    ):

        button = Gtk.Button(
            label=text
        )

        button.set_name(
            "button"
        )

        if callback:
            button.connect(
                "clicked",
                callback
            )

        return button

    def update_bubbly_buttons(
        self
    ):

        hidden = bool(
            self.no_super_bubbly_buttons
        )

        for button in self._system_action_buttons:

            button.set_visible(
                not hidden
            )

    # ---------------------------------------------------------
    # APPLICATIONS
    # ---------------------------------------------------------

    def load_apps(self):

        self.apps = []

        for app in Gio.AppInfo.get_all():

            try:

                if not app.should_show():
                    continue

                name = app.get_display_name()

                if name:
                    self.apps.append(
                        (
                            name,
                            app
                        )
                    )

            except Exception as error:

                self.log_error(
                    "Application loading error: "
                    + str(error)
                )

        self.apps.sort(
            key=lambda item:
            item[0].lower()
        )

        self.populate(
            self.apps
        )

    def filtered_apps(self):

        query = self.search.get_text().strip().lower()

        if not query:
            return self.apps

        return [
            item
            for item in self.apps
            if query in item[0].lower()
        ]

    def populate(
        self,
        data
    ):

        for row in self.list.get_children():

            self.list.remove(
                row
            )

        for name, app in data:

            row = Gtk.ListBoxRow()

            box = Gtk.Box(
                spacing=9
            )

            icon = app.get_icon()

            if icon:

                image = Gtk.Image.new_from_gicon(
                    icon,
                    Gtk.IconSize.LARGE_TOOLBAR
                )

            else:

                image = Gtk.Image.new_from_icon_name(
                    "application-x-executable-symbolic",
                    Gtk.IconSize.LARGE_TOOLBAR
                )

            image.set_pixel_size(
                32
            )

            label = Gtk.Label(
                label=name
            )

            label.set_xalign(
                0
            )

            label.set_ellipsize(
                Pango.EllipsizeMode.END
            )

            box.pack_start(
                image,
                False,
                False,
                0
            )

            box.pack_start(
                label,
                True,
                True,
                0
            )

            row.add(
                box
            )

            row.app = app
            row.app_name = name

            self.list.add(
                row
            )

        self.list.show_all()

        self.update_bubbly_buttons()

    def search_changed(
        self,
        entry
    ):

        self.populate(
            self.filtered_apps()
        )

    def select(
        self,
        box,
        row
    ):

        if not row:
            return

        self.selected = row.app
        self.selected_name = row.app_name

        self.name.set_text(
            row.app_name
        )

        icon = row.app.get_icon()

        if icon:

            self.icon.set_from_gicon(
                icon,
                Gtk.IconSize.LARGE_TOOLBAR
            )

            self.icon.set_pixel_size(
                40
            )

        self.update_info()

    def activate(
        self,
        box,
        row
    ):

        if not row:
            return

        self.selected = row.app
        self.selected_name = row.app_name

        self.open_app(
            None
        )

    def update_info(self):

        if not self.selected:

            if self.nerd_stats:

                try:
                    with open(
                        "/proc/self/status",
                        "r",
                        encoding="utf-8"
                    ) as f:

                        memory = next(
                            (
                                x.split(":", 1)[1].strip()
                                for x in f
                                if x.startswith("VmRSS:")
                            ),
                            "Unknown"
                        )

                except Exception:
                    memory = "Unknown"

                self.info.set_markup(
                    "<b>Statistics for Nerds</b>\\n"
                    "Applications: "
                    + str(len(self.apps))
                    + "\\n"
                    "Launcher RAM: "
                    + GLib.markup_escape_text(memory)
                )

            else:
                self.info.set_text(
                    "APPLICATION INFO\\nSelect an application"
                )

            return

        name = (
            self.selected.get_display_name()
            or "Unknown"
        )

        app_id = (
            self.selected.get_id()
            or "Unknown"
        )

        lines = [
            "<b>"
            + GLib.markup_escape_text(name)
            + "</b>",
            "ID: "
            + GLib.markup_escape_text(app_id)
        ]

        if self.high_quality:

            description = (
                self.selected.get_description()
                or "No description available"
            )

            executable = (
                self.selected.get_executable()
                or "Unknown"
            )

            lines += [
                "",
                "<b>High Quality Information</b>",
                "Description: "
                + GLib.markup_escape_text(
                    description
                ),
                "Executable: "
                + GLib.markup_escape_text(
                    executable
                ),
            ]

        if self.nerd_stats:

            try:

                with open(
                    "/proc/self/status",
                    "r",
                    encoding="utf-8"
                ) as f:

                    memory = next(
                        (
                            x.split(
                                ":",
                                1
                            )[1].strip()
                            for x in f
                            if x.startswith(
                                "VmRSS:"
                            )
                        ),
                        "Unknown"
                    )

            except Exception:

                memory = "Unknown"

            lines += [
                "",
                "<b>Statistics for Nerds</b>",
                "Applications: "
                + str(
                    len(self.apps)
                ),
                "Launcher RAM: "
                + GLib.markup_escape_text(
                    memory
                ),
            ]

        self.info.set_markup(
            "\n".join(lines)
        )

    # ---------------------------------------------------------
    # LAUNCHING
    # ---------------------------------------------------------

    def open_app(
        self,
        button
    ):

        if not self.selected:
            return

        try:

            self.selected.launch(
                [],
                None
            )

            self.show_notification(
                "SUCCESS",
                self.selected_name
                + " launched successfully."
            )

            if self.keep_launcher_alive:
                # Pozwól aplikacji znaleźć się nad launcherem.
                self.set_keep_above(False)

            else:
                GLib.timeout_add(
                    450,
                    self.destroy
                )

        except Exception as error:

            self.log_error(
                "Launch error: "
                + str(error)
            )

    # ---------------------------------------------------------
    # UNINSTALL
    # ---------------------------------------------------------

    def uninstall(
        self,
        button
    ):

        if not self.selected:
            return

        app_id = self.selected.get_id()

        if not app_id:
            return

        if not shutil.which(
            "flatpak"
        ):

            self.show_notification(
                "ERROR",
                "Flatpak is not installed."
            )

            return

        try:

            result = subprocess.run(
                [
                    "flatpak",
                    "info",
                    app_id
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2
            )

            if result.returncode != 0:

                dialog = Gtk.MessageDialog(
                    transient_for=self,
                    modal=True,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text="Not a Flatpak application"
                )

                dialog.format_secondary_text(
                    "The selected application is not detected as a Flatpak."
                )

                dialog.run()
                dialog.destroy()

                return

            confirm = Gtk.MessageDialog(
                transient_for=self,
                modal=True,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.YES_NO,
                text="Uninstall application?"
            )

            confirm.format_secondary_text(
                self.selected_name
            )

            response = confirm.run()

            confirm.destroy()

            if response == Gtk.ResponseType.YES:

                subprocess.Popen(
                    [
                        "flatpak",
                        "uninstall",
                        "--user",
                        "-y",
                        app_id
                    ],
                    start_new_session=True
                )

                self.destroy()

        except Exception as error:

            self.log_error(
                "Uninstall error: "
                + str(error)
            )

    # ---------------------------------------------------------
    # MEDIA
    # ---------------------------------------------------------

    def start_media_timer(self):

        if self.media_timer:

            try:
                GLib.source_remove(
                    self.media_timer
                )
            except Exception:
                pass

        interval = (
            30
            if self.fun_optimization
            else 10
        )

        self.media_timer = GLib.timeout_add_seconds(
            interval,
            self.update_media
        )

    def media_command(
        self,
        button,
        command
    ):

        if not shutil.which(
            "playerctl"
        ):
            return

        try:

            subprocess.Popen(
                [
                    "playerctl",
                    command
                ],
                start_new_session=True
            )

            GLib.timeout_add(
                120,
                self.update_media
            )

        except Exception as error:

            self.log_error(
                "Media command error: "
                + str(error)
            )

    def update_media(self):

        if not shutil.which(
            "playerctl"
        ):

            self.media_player.set_text("♫  playerctl not installed")
            self.media_title.set_text("No media controls available")
            self.media_artist.set_text("")
            self.media_status.set_text("")

            for button in self.media_buttons.values():
                button.set_sensitive(False)

            return True

        try:

            raw = subprocess.check_output(
                [
                    "playerctl",
                    "metadata",
                    "--format",
                    "{{ playerName }}\t{{ status }}\t{{ title }}\t{{ artist }}\t{{ album }}"
                ],
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=0.6
            ).strip()

            if not raw:
                raise RuntimeError("No active player")

            parts = raw.split("\t", 4)
            while len(parts) < 5:
                parts.append("")

            player, status, title, artist, album = parts

            title = title.strip()
            artist = artist.strip()
            album = album.strip()
            status = status.strip().lower()
            player = player.strip()

            self.media_player.set_text(
                "♫  " + (player or "Media player")
            )

            if title:
                self.media_title.set_text(
                    title
                )
            else:
                self.media_title.set_text(
                    "No title"
                )

            details = " • ".join(
                item for item in (artist, album) if item
            )

            self.media_artist.set_text(
                details
            )

            status_text = {
                "playing": "▶ Playing",
                "paused": "Ⅱ Paused",
                "stopped": "■ Stopped",
            }.get(
                status,
                status.title() if status else "Ready"
            )

            self.media_status.set_text(
                status_text
            )

            for button in self.media_buttons.values():
                button.set_sensitive(True)

            play_button = self.media_buttons.get(
                "play-pause"
            )

            if play_button:
                icon = (
                    "media-playback-pause-symbolic"
                    if status == "playing"
                    else "media-playback-start-symbolic"
                )

                play_button.set_image(
                    Gtk.Image.new_from_icon_name(
                        icon,
                        Gtk.IconSize.BUTTON
                    )
                )

                play_button.set_tooltip_text(
                    "Pause"
                    if status == "playing"
                    else "Play"
                )

        except Exception:

            self.media_player.set_text(
                "♫  No media player"
            )

            self.media_title.set_text(
                "Nothing is playing"
            )

            self.media_artist.set_text(
                ""
            )

            self.media_status.set_text(
                ""
            )

            for button in self.media_buttons.values():
                button.set_sensitive(False)

        return True

    # ---------------------------------------------------------
    # CLOCK
    # ---------------------------------------------------------

    def update_clock(self):

        self.clock.set_text(
            time.strftime(
                "%H:%M"
            )
        )

        return True

    # ---------------------------------------------------------
    # SYSTEM
    # ---------------------------------------------------------

    def lock(
        self,
        button
    ):

        try:

            subprocess.Popen(
                [
                    "cinnamon-screensaver-command",
                    "--lock"
                ],
                start_new_session=True
            )

        except Exception as error:

            self.log_error(
                "Lock error: "
                + str(error)
            )

        self.destroy()

    def restart(
        self,
        button
    ):

        try:

            subprocess.Popen(
                [
                    "systemctl",
                    "reboot"
                ],
                start_new_session=True
            )

        except Exception as error:

            self.log_error(
                "Restart error: "
                + str(error)
            )

    def shutdown(
        self,
        button
    ):

        try:

            subprocess.Popen(
                [
                    "systemctl",
                    "poweroff"
                ],
                start_new_session=True
            )

        except Exception as error:

            self.log_error(
                "Shutdown error: "
                + str(error)
            )

    # ---------------------------------------------------------
    # SETTINGS WINDOW
    # ---------------------------------------------------------

    def mac_close_button(
        self,
        dialog
    ):

        button = Gtk.Button()

        button.set_name(
            "mac_close"
        )

        button.set_relief(
            Gtk.ReliefStyle.NONE
        )

        button.set_size_request(
            14,
            14
        )

        button.set_hexpand(False)
        button.set_vexpand(False)
        button.set_halign(Gtk.Align.END)
        button.set_valign(Gtk.Align.CENTER)
        button.set_can_focus(False)

        button.set_tooltip_text(
            "Close"
        )

        button.connect(
            "clicked",
            lambda b:
            dialog.destroy()
        )

        return button

    def settings(
        self,
        button
    ):

        dialog = Gtk.Window(
            title="Breeze Launcher Settings"
        )

        dialog.set_default_size(
            580,
            560
        )

        dialog.set_position(
            Gtk.WindowPosition.CENTER
        )

        dialog.set_transient_for(
            self
        )

        dialog.set_modal(
            True
        )

        dialog.set_decorated(
            False
        )

        dialog.set_resizable(
            False
        )

        panel = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )

        panel.set_name(
            "settings_panel"
        )

        header = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL
        )

        title = Gtk.Label(
            label="⚙  Settings"
        )

        title.set_name(
            "settings_title"
        )

        title.set_xalign(
            0
        )

        close = self.mac_close_button(
            dialog
        )

        header.pack_start(
            title,
            True,
            True,
            0
        )

        header.pack_end(
            close,
            False,
            False,
            0
        )

        panel.pack_start(
            header,
            False,
            False,
            0
        )

        def add_setting(
            name,
            description,
            key
        ):

            row = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=12
            )

            row.set_name(
                "setting_row"
            )

            texts = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,
                spacing=2
            )

            label = Gtk.Label(
                label=name
            )

            label.set_name(
                "setting_name"
            )

            label.set_xalign(
                0
            )

            desc = Gtk.Label(
                label=description
            )

            desc.set_name(
                "setting_desc"
            )

            desc.set_xalign(
                0
            )

            desc.set_line_wrap(
                True
            )

            texts.pack_start(
                label,
                False,
                False,
                0
            )

            texts.pack_start(
                desc,
                False,
                False,
                0
            )

            toggle = Gtk.Button()

            toggle.set_name(
                "toggle_dot"
            )

            toggle.set_relief(
                Gtk.ReliefStyle.NONE
            )

            # FORCE tiny fixed toggle size
            toggle.set_size_request(
                10,
                10
            )

            toggle.set_hexpand(False)
            toggle.set_vexpand(False)
            toggle.set_halign(Gtk.Align.END)
            toggle.set_valign(Gtk.Align.CENTER)
            toggle.set_can_focus(False)
            toggle.set_focus_on_click(False)
            toggle.set_margin_start(4)
            toggle.set_margin_end(2)

            state = bool(
                getattr(
                    self,
                    key
                )
            )

            if state:
                toggle.get_style_context().add_class(
                    "on"
                )

            toggle.set_tooltip_text(
                "TRUE"
                if state
                else "FALSE"
            )

            toggle.connect(
                "clicked",
                self.toggle_setting,
                key
            )

            row.pack_start(
                texts,
                True,
                True,
                0
            )

            row.pack_end(
                toggle,
                False,
                False,
                0
            )

            panel.pack_start(
                row,
                False,
                False,
                0
            )

            return toggle

        # =====================================================
        # TOGGLES
        # =====================================================

        add_setting(
            "⚡  Fun Optimization",
            "Reduce unnecessary work, refreshes and visual overhead.",
            "fun_optimization"
        )

        add_setting(
            "✨  High Quality",
            "WIP",
            "high_quality"
        )

        add_setting(
            "🧠  Statistics for Nerds",
            "Show advanced application information and launcher diagnostics.",
            "nerd_stats"
        )

        add_setting(
            "🟢  Keep Launcher Alive",
            "Keep Breeze Launcher open after launching an application.",
            "keep_launcher_alive"
        )

        add_setting(
            "📜  Error Logs",
            "WIP",
            "error_logs_enabled"
        )

        add_setting(
            "🫧  NO SUPER BUBBLY BUTTONS",
            "Hides the bottom distracting bottom buttons",
            "no_super_bubbly_buttons"
        )

        add_setting(
            "Unnamed 5",
            "Placeholder setting.",
            "unnamed_5"
        )

        dialog.add(
            panel
        )

        dialog.show_all()

    # ---------------------------------------------------------
    # CHANGELOG
    # ---------------------------------------------------------

    def changelog(
        self,
        button
    ):

        dialog = Gtk.Window(
            title="Breeze Launcher Changelog"
        )

        dialog.set_default_size(
            680,
            610
        )

        dialog.set_position(
            Gtk.WindowPosition.CENTER
        )

        dialog.set_transient_for(
            self
        )

        dialog.set_modal(
            True
        )

        dialog.set_decorated(
            False
        )

        dialog.set_resizable(
            False
        )

        root = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8
        )

        root.set_name(
            "dialog"
        )

        header = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8
        )

        header.set_name(
            "head"
        )

        left = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=2
        )

        title = Gtk.Label(
            label="📜  Breeze Launcher"
        )

        title.set_name(
            "title"
        )

        title.set_xalign(
            0
        )

        subtitle = Gtk.Label(
            label="Detailed version history  •  "
            + VERSION
        )

        subtitle.set_name(
            "sub"
        )

        subtitle.set_xalign(
            0
        )

        left.pack_start(
            title,
            False,
            False,
            0
        )

        left.pack_start(
            subtitle,
            False,
            False,
            0
        )

        close = self.mac_close_button(
            dialog
        )

        header.pack_start(
            left,
            True,
            True,
            0
        )

        header.pack_end(
            close,
            False,
            False,
            0
        )

        root.pack_start(
            header,
            False,
            False,
            0
        )

        tabs = Gtk.Box(
            spacing=4
        )

        changes_button = Gtk.Button(
            label="📜  Changelog"
        )

        changes_button.set_name(
            "changelog_tab"
        )

        features_button = Gtk.Button(
            label="✦  Features"
        )

        features_button.set_name(
            "changelog_tab"
        )

        tabs.pack_start(
            changes_button,
            False,
            False,
            0
        )

        tabs.pack_start(
            features_button,
            False,
            False,
            0
        )

        root.pack_start(
            tabs,
            False,
            False,
            0
        )

        stack = Gtk.Stack()

        # CHANGELOG PAGE

        change_scroll = Gtk.ScrolledWindow()

        change_scroll.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC
        )

        change_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=6
        )

        for version, update_type, emoji, entries in CHANGELOG:

            version_label = Gtk.Label(
                label=(
                    f"{emoji}  {version}"
                    f"  •  {update_type}"
                )
            )

            version_label.set_name(
                "topic"
            )

            version_label.set_xalign(
                0
            )

            change_box.pack_start(
                version_label,
                False,
                False,
                5
            )

            for topic, description in entries:

                entry = Gtk.Box(
                    orientation=Gtk.Orientation.VERTICAL,
                    spacing=3
                )

                entry.set_name(
                    "entry"
                )

                topic_label = Gtk.Label()

                topic_label.set_markup(
                    "<u><span foreground='#c9a7ff'>"
                    + GLib.markup_escape_text(
                        topic
                    )
                    + "</span></u>"
                )

                topic_label.set_xalign(
                    0
                )

                description_label = Gtk.Label(
                    label=description
                )

                description_label.set_name(
                    "desc"
                )

                description_label.set_xalign(
                    0
                )

                description_label.set_line_wrap(
                    True
                )

                entry.pack_start(
                    topic_label,
                    False,
                    False,
                    0
                )

                entry.pack_start(
                    description_label,
                    False,
                    False,
                    0
                )

                change_box.pack_start(
                    entry,
                    False,
                    False,
                    0
                )

        change_scroll.add(
            change_box
        )

        stack.add_named(
            change_scroll,
            "changes"
        )

        # FEATURES PAGE

        feature_scroll = Gtk.ScrolledWindow()

        feature_scroll.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC
        )

        feature_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=6
        )

        for feature_title, feature_description in FEATURES:

            feature = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,
                spacing=3
            )

            feature.set_name(
                "feature"
            )

            feature_title_label = Gtk.Label(
                label=feature_title
            )

            feature_title_label.set_name(
                "featuretitle"
            )

            feature_title_label.set_xalign(
                0
            )

            feature_description_label = Gtk.Label(
                label=feature_description
            )

            feature_description_label.set_name(
                "featuredesc"
            )

            feature_description_label.set_xalign(
                0
            )

            feature_description_label.set_line_wrap(
                True
            )

            feature.pack_start(
                feature_title_label,
                False,
                False,
                0
            )

            feature.pack_start(
                feature_description_label,
                False,
                False,
                0
            )

            feature_box.pack_start(
                feature,
                False,
                False,
                0
            )

        feature_scroll.add(
            feature_box
        )

        stack.add_named(
            feature_scroll,
            "features"
        )

        root.pack_start(
            stack,
            True,
            True,
            0
        )

        changes_button.connect(
            "clicked",
            lambda b:
            stack.set_visible_child_name(
                "changes"
            )
        )

        features_button.connect(
            "clicked",
            lambda b:
            stack.set_visible_child_name(
                "features"
            )
        )

        dialog.add(
            root
        )

        dialog.show_all()

    # ---------------------------------------------------------
    # KEYBOARD
    # ---------------------------------------------------------

    def key_press(
        self,
        widget,
        event
    ):

        if event.keyval in (
            Gdk.KEY_Escape,
            Gdk.KEY_Super_L,
            Gdk.KEY_Super_R
        ):

            self.destroy()

            return True

        if event.keyval in (
            Gdk.KEY_Return,
            Gdk.KEY_KP_Enter
        ):

            self.open_app(
                None
            )

            return True

        return False


# =============================================================
# START
# =============================================================

menu = StartMenu()

menu.show_all()

menu.update_bubbly_buttons()

menu.present()

menu.search.grab_focus()

Gtk.main()
