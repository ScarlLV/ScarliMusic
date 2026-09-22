"""
SCARLI-MUSIC v0.1
Retro player inspired by Soviet radio electronics.
Python 3.14+  /  pygame-ce
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import json
import os
import math
import random

APP_VERSION = "0.1"
APP_TITLE = "SCARLI-MUSIC"
SETTINGS_FILE = "settings.json"
PLAYLIST_FILE = "playlist.json"

DEFAULT_SETTINGS = {
    "volume": 0.5,
    "last_folder": "",
    "theme": "retro",       # "retro" | "cassette"
    "language": "en",
}

DEFAULT_PLAYLIST = {
    "tracks": [],       # list of absolute paths
    "favorites": [],    # list of absolute paths
}

# ---------------------------------------------------------------------------
#  THEMES
# ---------------------------------------------------------------------------
THEMES = {
    "retro": {
        "name": "RETRO  CRT",
        "bg_body":      "#1a1614",
        "bg_panel":     "#24201c",
        "bg_screen":    "#0d0a06",
        "bg_trough":    "#100d0a",
        "fg_main":      "#ffb000",
        "fg_dim":       "#8a5f00",
        "fg_soft":      "#e8d9b0",
        "btn_bg":       "#3a322a",
        "btn_fg":       "#f0e2c0",
        "btn_active":   "#524636",
        "btn_red":      "#7a1f1f",
        "btn_red_act":  "#a02828",
        "led_on":       "#ffb000",
        "led_off":      "#3a2a0a",
        "led_pause":    "#ff5a1a",
        "led_off_p":    "#3a1408",
        "accent":       "#c9a227",
        "frame":        "#5a4a30",
        "knob_bg":      "#2e2820",
        "knob_edge":    "#6a5a3a",
        "knob_line":    "#ffb000",
        "knob_dot":     "#c9a227",
        "list_bg":      "#161210",
        "list_sel":     "#3a2a0a",
        "list_fav":     "#ffb000",
    },
    "cassette": {
        "name": "CASSETTE",
        "bg_body":      "#2b2620",
        "bg_panel":     "#3a332a",
        "bg_screen":    "#141210",
        "bg_trough":    "#1e1a15",
        "fg_main":      "#ffd98a",
        "fg_dim":       "#9a7a44",
        "fg_soft":      "#f5e6c8",
        "btn_bg":       "#4a3f30",
        "btn_fg":       "#f5e6c8",
        "btn_active":   "#6a5a44",
        "btn_red":      "#8a3a2a",
        "btn_red_act":  "#b04a36",
        "led_on":       "#ffd98a",
        "led_off":      "#3a2f1c",
        "led_pause":    "#ff8a3a",
        "led_off_p":    "#3a1c0a",
        "accent":       "#d9b46a",
        "frame":        "#6a5a44",
        "knob_bg":      "#3a332a",
        "knob_edge":    "#8a7a5a",
        "knob_line":    "#ffd98a",
        "knob_dot":     "#d9b46a",
        "list_bg":      "#1c1813",
        "list_sel":     "#4a3a1a",
        "list_fav":     "#ffd98a",
    },
}

C = dict(THEMES["retro"])   # current palette, updated on theme change


FONT_MONO      = ("Courier New", 11, "bold")
FONT_MONO_SM   = ("Courier New", 9,  "bold")
FONT_DISPLAY   = ("Courier New", 14, "bold")
FONT_TITLE     = ("Courier New", 13, "bold")
FONT_LABEL     = ("Courier New", 8,  "bold")
FONT_TINY      = ("Courier New", 8,  "normal")


def fmt_time(seconds: float) -> str:
    if seconds is None or seconds <= 0:
        return "--:--"
    s = int(seconds)
    return f"{s // 60:02d}:{s % 60:02d}"


# ---------------------------------------------------------------------------
#  SETTINGS / PLAYLIST
# ---------------------------------------------------------------------------
def load_json(path, default):
    if not os.path.exists(path):
        save_json(path, default)
        return dict(default)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        out = dict(default)
        out.update(data)
        return out
    except Exception:
        return dict(default)


def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"save {path} error:", e)


def load_settings() -> dict:
    return load_json(SETTINGS_FILE, DEFAULT_SETTINGS)


def load_playlist() -> dict:
    p = load_json(PLAYLIST_FILE, DEFAULT_PLAYLIST)
    # filter out missing files
    p["tracks"]    = [t for t in p.get("tracks", [])    if os.path.exists(t)]
    p["favorites"] = [t for t in p.get("favorites", []) if os.path.exists(t)]
    return p


def save_playlist(p: dict):
    save_json(PLAYLIST_FILE, p)


# ---------------------------------------------------------------------------
#  KNOB
# ---------------------------------------------------------------------------
class Knob(tk.Canvas):
    def __init__(self, parent, label="", size=78, callback=None, value=0.5,
                 disabled=False):
        super().__init__(parent, width=size, height=size + 18,
                         bg=parent["bg"], highlightthickness=0, bd=0)
        self.size = size
        self.value = value
        self.callback = callback
        self.label = label
        self.disabled = disabled
        self._drag_start_y = None
        self._drag_start_val = 0.0

        if not disabled:
            self.bind("<Button-1>",        self._on_press)
            self.bind("<B1-Motion>",       self._on_drag)
            self.bind("<ButtonRelease-1>", self._on_release)
            self.bind("<MouseWheel>",      self._on_wheel)

        self._draw()

    def _draw(self):
        self.delete("all")
        s = self.size
        cx, cy = s / 2, s / 2
        r = s / 2 - 6

        line_col = C["fg_dim"] if self.disabled else C["knob_line"]
        edge_col = C["fg_dim"] if self.disabled else C["knob_edge"]

        self.create_oval(cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3,
                         fill=C["knob_bg"], outline=C["frame"], width=2)
        self.create_oval(cx - r, cy - r, cx + r, cy + r,
                         fill=C["knob_bg"], outline=edge_col, width=2)
        self.create_oval(cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6,
                         fill=C["knob_bg"], outline=edge_col, width=1)

        ang = math.radians(-135 + self.value * 270)
        x1 = cx + math.sin(ang) * (r - 8)
        y1 = cy - math.cos(ang) * (r - 8)
        self.create_line(cx, cy, x1, y1, fill=line_col, width=3,
                         capstyle="round")
        self.create_oval(x1 - 4, y1 - 4, x1 + 4, y1 + 4,
                         fill=C["knob_dot"] if not self.disabled else C["fg_dim"],
                         outline="")

        for i in range(11):
            a = math.radians(-135 + i * 27)
            tx1 = cx + math.sin(a) * (r + 5)
            ty1 = cy - math.cos(a) * (r + 5)
            tx2 = cx + math.sin(a) * (r + 9)
            ty2 = cy - math.cos(a) * (r + 9)
            self.create_line(tx1, ty1, tx2, ty2,
                             fill=C["fg_dim"], width=1)

        self.create_text(cx, s + 8, text=self.label,
                         fill=C["accent"], font=FONT_LABEL)

    def _on_press(self, e):
        self._drag_start_y = e.y_root
        self._drag_start_val = self.value

    def _on_drag(self, e):
        if self._drag_start_y is None:
            return
        dy = self._drag_start_y - e.y_root
        delta = dy / 150.0
        v = max(0.0, min(1.0, self._drag_start_val + delta))
        if abs(v - self.value) > 1e-6:
            self.value = v
            self._draw()
            if self.callback:
                self.callback(self.value)

    def _on_release(self, _e):
        self._drag_start_y = None

    def _on_wheel(self, e):
        step = 0.03 if e.delta > 0 else -0.03
        v = max(0.0, min(1.0, self.value + step))
        if abs(v - self.value) > 1e-6:
            self.value = v
            self._draw()
            if self.callback:
                self.callback(self.value)

    def set(self, v):
        self.value = max(0.0, min(1.0, v))
        self._draw()


# ---------------------------------------------------------------------------
#  SCRUBBER  (tape ruler)
# ---------------------------------------------------------------------------
class Scrubber(tk.Canvas):
    def __init__(self, parent, height=36, callback=None):
        super().__init__(parent, height=height, bg=C["bg_trough"],
                         highlightthickness=0, bd=0)
        self.callback = callback
        self.duration = 0.0
        self.position = 0.0
        self._dragging = False

        self.bind("<Configure>",       lambda e: self._redraw())
        self.bind("<Button-1>",        self._on_press)
        self.bind("<B1-Motion>",       self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)

    def set_duration(self, d: float):
        self.duration = max(0.0, d)
        self._redraw()

    def set_position(self, p: float):
        if self._dragging:
            return
        self.position = max(0.0, p)
        self._redraw()

    def _on_press(self, e):
        self._dragging = True
        self._seek_from_x(e.x)

    def _on_drag(self, e):
        if self._dragging:
            self._seek_from_x(e.x)

    def _on_release(self, _e):
        self._dragging = False

    def _seek_from_x(self, x):
        w = self.winfo_width()
        if w <= 2 or self.duration <= 0:
            return
        ratio = max(0.0, min(1.0, x / w))
        target = ratio * self.duration
        self.position = target
        self._redraw()
        if self.callback:
            self.callback(target)

    def _redraw(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 4 or h < 4:
            return

        pad = 8
        y0 = h - 8
        y1 = h - 2

        self.create_rectangle(0, 0, w, h, fill=C["bg_trough"], outline="")

        if self.duration > 0:
            ratio = max(0.0, min(1.0, self.position / self.duration))
        else:
            ratio = 0.0
        head_x = pad + ratio * (w - 2 * pad)
        self.create_rectangle(0, 0, head_x, h, fill=C["list_sel"], outline="")

        n_minor = 50
        for i in range(n_minor + 1):
            x = pad + (w - 2 * pad) * (i / n_minor)
            is_major = (i % 5 == 0)
            length = 10 if is_major else 5
            self.create_line(x, y0 - length, x, y1,
                             fill=C["fg_dim"] if not is_major else C["accent"],
                             width=1)

        self.create_line(head_x, 2, head_x, h - 10,
                         fill=C["fg_main"], width=3)
        self.create_rectangle(head_x - 4, 2, head_x + 4, 8,
                              fill=C["fg_main"], outline=C["knob_dot"])

    def retheme(self):
        self.config(bg=C["bg_trough"])
        self._redraw()


# ---------------------------------------------------------------------------
#  PLAYLIST WINDOW
# ---------------------------------------------------------------------------
class PlaylistWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        self.title("PLAYLIST")
        self.configure(bg=C["bg_body"])
        self.transient(app.root)
        self.geometry("520x420")
        self._build()
        self.refresh()

    def _build(self):
        top = tk.Frame(self, bg=C["bg_body"])
        top.pack(fill="x", padx=10, pady=(10, 0))

        tk.Label(top, text="PLAYLIST", bg=C["bg_body"], fg=C["accent"],
                 font=FONT_TITLE).pack(side="left")

        tk.Button(top, text="+ ADD", command=self._add_files,
                  bg=C["btn_bg"], fg=C["btn_fg"], activebackground=C["btn_active"],
                  font=FONT_MONO_SM, bd=2, relief="raised",
                  highlightthickness=0, cursor="hand2").pack(side="right", padx=2)
        tk.Button(top, text="CLOSE", command=self.destroy,
                  bg=C["btn_bg"], fg=C["btn_fg"], activebackground=C["btn_active"],
                  font=FONT_MONO_SM, bd=2, relief="raised",
                  highlightthickness=0, cursor="hand2").pack(side="right", padx=2)

        # list
        list_wrap = tk.Frame(self, bg=C["accent"], bd=1)
        list_wrap.pack(fill="both", expand=True, padx=10, pady=10)

        inner = tk.Frame(list_wrap, bg=C["list_bg"])
        inner.pack(fill="both", expand=True, padx=2, pady=2)

        self.listbox = tk.Listbox(
            inner, bg=C["list_bg"], fg=C["fg_main"],
            selectbackground=C["list_sel"], selectforeground=C["fg_main"],
            font=FONT_MONO_SM, bd=0, highlightthickness=0,
            activestyle="none"
        )
        self.listbox.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(inner, command=self.listbox.yview,
                          bg=C["btn_bg"], troughcolor=C["bg_trough"],
                          activebackground=C["btn_active"], bd=0,
                          highlightthickness=0)
        sb.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=sb.set)

        self.listbox.bind("<Double-Button-1>", self._on_double)

        # bottom buttons
        bot = tk.Frame(self, bg=C["bg_body"])
        bot.pack(fill="x", padx=10, pady=(0, 10))

        tk.Button(bot, text="FAVORITE", command=self._toggle_fav,
                  bg=C["btn_bg"], fg=C["btn_fg"], activebackground=C["btn_active"],
                  font=FONT_MONO_SM, bd=2, relief="raised",
                  highlightthickness=0, cursor="hand2").pack(side="left", padx=2)
        tk.Button(bot, text="REMOVE", command=self._remove,
                  bg=C["btn_bg"], fg=C["btn_fg"], activebackground=C["btn_active"],
                  font=FONT_MONO_SM, bd=2, relief="raised",
                  highlightthickness=0, cursor="hand2").pack(side="left", padx=2)
        tk.Button(bot, text="CLEAR", command=self._clear,
                  bg=C["btn_red"], fg=C["btn_fg"], activebackground=C["btn_red_act"],
                  font=FONT_MONO_SM, bd=2, relief="raised",
                  highlightthickness=0, cursor="hand2").pack(side="left", padx=2)

    def refresh(self):
        self.listbox.delete(0, tk.END)
        p = self.app.playlist
        for i, t in enumerate(p["tracks"]):
            name = os.path.basename(t)
            fav = t in p["favorites"]
            mark = "★ " if fav else "  "
            self.listbox.insert(tk.END, f"{mark}{i+1:02d}. {name}")
            if fav:
                self.listbox.itemconfig(i, fg=C["list_fav"])

    def _add_files(self):
        paths = filedialog.askopenfilenames(
            title="Add to playlist",
            initialdir=self.app.settings.get("last_folder", "") or os.path.expanduser("~"),
            filetypes=[("Audio", "*.mp3 *.wav *.ogg *.flac"), ("All files", "*.*")]
        )
        if not paths:
            return
        for p in paths:
            if p not in self.app.playlist["tracks"]:
                self.app.playlist["tracks"].append(p)
        if paths:
            self.app.settings["last_folder"] = os.path.dirname(paths[0])
        self.app.save_playlist()
        self.refresh()

    def _on_double(self, _e):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        path = self.app.playlist["tracks"][idx]
        self.app.load_track(path)

    def _toggle_fav(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        path = self.app.playlist["tracks"][idx]
        if path in self.app.playlist["favorites"]:
            self.app.playlist["favorites"].remove(path)
        else:
            self.app.playlist["favorites"].append(path)
        self.app.save_playlist()
        self.refresh()
        self.listbox.selection_set(idx)

    def _remove(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        path = self.app.playlist["tracks"][idx]
        self.app.playlist["tracks"].pop(idx)
        if path in self.app.playlist["favorites"]:
            self.app.playlist["favorites"].remove(path)
        self.app.save_playlist()
        self.refresh()

    def _clear(self):
        if not messagebox.askyesno("Clear", "Remove all tracks?"):
            return
        self.app.playlist["tracks"] = []
        self.app.playlist["favorites"] = []
        self.app.save_playlist()
        self.refresh()


# ---------------------------------------------------------------------------
#  PLAYER
# ---------------------------------------------------------------------------
class Player:
    def __init__(self):
        pygame.mixer.init()
        self.track_path = None
        self.state = "STOPPED"
        self.duration_s = 0.0
        self.seek_base = 0.0

    def load(self, path):
        pygame.mixer.music.load(path)
        self.track_path = path
        self.state = "STOPPED"
        self.duration_s = self._probe_duration(path)
        self.seek_base = 0.0

    def _probe_duration(self, path):
        try:
            from mutagen import File as MFile
            f = MFile(path)
            if f is not None and f.info is not None:
                return float(f.info.length)
        except Exception:
            pass
        return 0.0

    def play(self):
        if self.state == "PAUSED":
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.play(start=self.seek_base)
        self.state = "PLAYING"

    def pause(self):
        if self.state == "PLAYING":
            pygame.mixer.music.pause()
            self.state = "PAUSED"

    def stop(self):
        pygame.mixer.music.stop()
        self.state = "STOPPED"
        self.seek_base = 0.0

    def set_volume(self, v):
        pygame.mixer.music.set_volume(v)

    def is_busy(self):
        return pygame.mixer.music.get_busy()

    def current_pos(self):
        if self.state == "STOPPED":
            return 0.0
        try:
            ms = pygame.mixer.music.get_pos()
        except Exception:
            ms = -1
        if ms < 0:
            return self.seek_base
        return self.seek_base + ms / 1000.0

    def seek_to(self, target):
        if self.duration_s > 0:
            target = max(0.0, min(self.duration_s - 0.5, target))
        else:
            target = max(0.0, target)

        was_playing = self.state == "PLAYING"
        try:
            if was_playing:
                pygame.mixer.music.play(start=target)
            else:
                self.seek_base = target
                return
        except Exception:
            return
        self.seek_base = target


# ---------------------------------------------------------------------------
#  MAIN APP
# ---------------------------------------------------------------------------
class ScarliMusic:
    def __init__(self, root):
        self.root = root
        self.settings = load_settings()
        self.playlist = load_playlist()
        self.player = Player()
        self._end_check_id = None
        self._playlist_win = None

        # apply theme before UI build
        self._apply_theme_palette()

        self._setup_window()
        self._build_ui()
        self._bind_hotkeys()

        self.player.set_volume(self.settings["volume"])
        self.vol_knob.set(self.settings["volume"])
        self._update_volume_label(self.settings["volume"])
        self._update_fav_indicator()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # --- theme -----------------------------------------------------------
    def _apply_theme_palette(self):
        global C
        key = self.settings.get("theme", "retro")
        if key not in THEMES:
            key = "retro"
        C.clear()
        C.update(THEMES[key])

    # --- window ----------------------------------------------------------
    def _setup_window(self):
        self.root.title(f"{APP_TITLE}  v{APP_VERSION}")
        self.root.configure(bg=C["bg_body"])
        self.root.resizable(False, False)

        w, h = 620, 580
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # --- UI --------------------------------------------------------------
    def _build_ui(self):
        body = tk.Frame(self.root, bg=C["bg_body"])
        body.pack(fill="both", expand=True, padx=10, pady=10)

        # header
        header = tk.Frame(body, bg=C["bg_body"])
        header.pack(fill="x", pady=(0, 8))
        tk.Label(header, text=f"◉ {APP_TITLE}", bg=C["bg_body"],
                 fg=C["accent"], font=FONT_TITLE, anchor="w").pack(side="left", padx=4)
        tk.Label(header, text=f"v{APP_VERSION}", bg=C["bg_body"],
                 fg=C["fg_dim"], font=FONT_MONO_SM,
                 anchor="e").pack(side="right", padx=4)

        # center: screen + knobs
        center = tk.Frame(body, bg=C["bg_body"])
        center.pack(fill="x", pady=4)

        # --- screen ------------------------------------------------------
        panel = tk.Frame(center, bg=C["bg_panel"], bd=2, relief="ridge")
        panel.pack(side="left", fill="both", expand=True)

        led_frame = tk.Frame(panel, bg=C["bg_panel"])
        led_frame.pack(side="left", padx=(10, 4), pady=10)

        self.led_play = tk.Canvas(led_frame, width=14, height=14,
                                  bg=C["bg_panel"], highlightthickness=0)
        self.led_play.pack(pady=3)
        self._draw_led(self.led_play, False)

        self.led_pause = tk.Canvas(led_frame, width=14, height=14,
                                   bg=C["bg_panel"], highlightthickness=0)
        self.led_pause.pack(pady=3)
        self._draw_led(self.led_pause, False,
                       color_off=C["led_off_p"], color_on=C["led_pause"])

        screen_wrap = tk.Frame(panel, bg=C["accent"], bd=1)
        screen_wrap.pack(side="left", padx=(4, 10), pady=10, fill="both", expand=True)

        screen = tk.Frame(screen_wrap, bg=C["bg_screen"])
        screen.pack(fill="both", expand=True, padx=2, pady=2)

        self.display = tk.Label(screen, text="NO TRACK",
                                bg=C["bg_screen"], fg=C["fg_main"],
                                font=FONT_DISPLAY, anchor="w", justify="left")
        self.display.pack(fill="x", padx=10, pady=(8, 0))

        self.status = tk.Label(screen, text="STOPPED",
                               bg=C["bg_screen"], fg=C["fg_dim"],
                               font=FONT_MONO_SM, anchor="w")
        self.status.pack(fill="x", padx=10)

        self.time_lbl = tk.Label(screen, text="--:-- / --:--",
                                 bg=C["bg_screen"], fg=C["fg_soft"],
                                 font=FONT_MONO_SM, anchor="w")
        self.time_lbl.pack(fill="x", padx=10, pady=(2, 8))

        # --- knobs -------------------------------------------------------
        knobs = tk.Frame(center, bg=C["bg_body"])
        knobs.pack(side="right", padx=(10, 0))

        self.vol_knob = Knob(knobs, label="VOLUME", size=74,
                             value=self.settings["volume"],
                             callback=self.change_volume)
        self.vol_knob.pack(side="top", pady=(0, 6))

        self.speed_knob = Knob(knobs, label="SPEED", size=74,
                               value=0.5, disabled=True)
        self.speed_knob.pack(side="top", pady=(0, 6))

        # small "coming soon" tag
        tk.Label(knobs, text="COMING SOON", bg=C["bg_body"],
                 fg=C["fg_dim"], font=FONT_TINY).pack()

        # --- scrubber ----------------------------------------------------
        scrub_frame = tk.Frame(body, bg=C["bg_panel"], bd=2, relief="ridge")
        scrub_frame.pack(fill="x", pady=(12, 0))

        row = tk.Frame(scrub_frame, bg=C["bg_panel"])
        row.pack(fill="x", padx=8, pady=(4, 0))
        tk.Label(row, text="TAPE POSITION", bg=C["bg_panel"],
                 fg=C["accent"], font=FONT_LABEL).pack(side="left")
        self.fav_indicator = tk.Label(row, text="", bg=C["bg_panel"],
                                      fg=C["list_fav"], font=FONT_LABEL)
        self.fav_indicator.pack(side="right")

        self.scrubber = Scrubber(scrub_frame, height=38,
                                 callback=self.on_scrub)
        self.scrubber.pack(fill="x", padx=8, pady=(0, 6))

        # --- transport buttons ------------------------------------------
        btn_frame = tk.Frame(body, bg=C["bg_body"])
        btn_frame.pack(pady=14)

        self.btn_open  = self._make_button(btn_frame, "OPEN",  self.open_file)
        self.btn_play  = self._make_button(btn_frame, "PLAY",  self.play_track, state="disabled")
        self.btn_pause = self._make_button(btn_frame, "PAUSE", self.pause_track, state="disabled")
        self.btn_stop  = self._make_button(btn_frame, "STOP",  self.stop_track, state="disabled")

        self.btn_open .grid(row=0, column=0, padx=3)
        self.btn_play .grid(row=0, column=1, padx=3)
        self.btn_pause.grid(row=0, column=2, padx=3)
        self.btn_stop .grid(row=0, column=3, padx=3)

        # --- playlist row -----------------------------------------------
        pl_row = tk.Frame(body, bg=C["bg_body"])
        pl_row.pack(pady=(4, 0))

        self.btn_playlist = self._make_button(pl_row, "PLAYLIST", self.toggle_playlist)
        self.btn_fav      = self._make_button(pl_row, "★ FAV",     self.toggle_favorite)
        self.btn_next     = self._make_button(pl_row, "NEXT >",    self.play_next)

        self.btn_playlist.grid(row=0, column=0, padx=3)
        self.btn_fav.grid(row=0, column=1, padx=3)
        self.btn_next.grid(row=0, column=2, padx=3)

        self.vol_label = tk.Label(body, text="50%", bg=C["bg_body"],
                                  fg=C["fg_main"], font=FONT_MONO_SM)
        self.vol_label.pack(pady=(6, 0))

        self._build_menu()
        self._tick_ui()

    def _make_button(self, parent, text, cmd, state="normal"):
        return tk.Button(
            parent, text=text, command=cmd, state=state,
            bg=C["btn_bg"], fg=C["btn_fg"], activebackground=C["btn_active"],
            activeforeground="#ffffff",
            font=FONT_MONO_SM, width=8, height=2,
            relief="raised", bd=2, highlightthickness=0,
            cursor="hand2"
        )

    def _draw_led(self, canvas, on, color_on=None, color_off=None):
        canvas.delete("all")
        c_on  = color_on  or C["led_on"]
        c_off = color_off or C["led_off"]
        color = c_on if on else c_off
        canvas.create_oval(2, 2, 12, 12, fill=color, outline=C["frame"], width=1)

    def _build_menu(self):
        menubar = tk.Menu(self.root, bg=C["bg_panel"], fg=C["btn_fg"],
                          activebackground=C["accent"], activeforeground="#000", bd=0)

        file_menu = tk.Menu(menubar, tearoff=0, bg=C["bg_panel"], fg=C["btn_fg"],
                            activebackground=C["accent"], activeforeground="#000")
        file_menu.add_command(label="Open...", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        menubar.add_cascade(label="File", menu=file_menu)

        pl_menu = tk.Menu(menubar, tearoff=0, bg=C["bg_panel"], fg=C["btn_fg"],
                          activebackground=C["accent"], activeforeground="#000")
        pl_menu.add_command(label="Show playlist", command=self.toggle_playlist)
        pl_menu.add_command(label="Add current to playlist", command=self.add_current_to_playlist)
        pl_menu.add_separator()
        pl_menu.add_command(label="Next track", command=self.play_next)
        menubar.add_cascade(label="Playlist", menu=pl_menu)

        settings_menu = tk.Menu(menubar, tearoff=0, bg=C["bg_panel"], fg=C["btn_fg"],
                                activebackground=C["accent"], activeforeground="#000")
        settings_menu.add_command(label="Settings", command=self.open_settings)
        settings_menu.add_separator()
        settings_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        self.root.config(menu=menubar)

    # --- hotkeys ---------------------------------------------------------
    def _bind_hotkeys(self):
        self.root.bind("<space>", lambda e: self._toggle_play())
        self.root.bind("<KeyPress-o>", lambda e: self.open_file())
        self.root.bind("<KeyPress-s>", lambda e: self.stop_track())
        self.root.bind("<KeyPress-l>", lambda e: self.toggle_playlist())
        self.root.bind("<KeyPress-f>", lambda e: self.toggle_favorite())
        self.root.bind("<KeyPress-n>", lambda e: self.play_next())
        self.root.bind("<Left>",  lambda e: self._seek_by(-5))
        self.root.bind("<Right>", lambda e: self._seek_by(5))
        self.root.bind("<Shift-Left>",  lambda e: self._seek_by(-30))
        self.root.bind("<Shift-Right>", lambda e: self._seek_by(30))
        self.root.bind("<Escape>", lambda e: self.on_closing())

    def _seek_by(self, sec):
        self.player.seek_to(self.player.current_pos() + sec)

    # --- player logic ----------------------------------------------------
    def _toggle_play(self):
        if self.player.state == "PLAYING":
            self.pause_track()
        elif self.player.track_path:
            self.play_track()

    def open_file(self):
        path = filedialog.askopenfilename(
            title="Select Audio File",
            initialdir=self.settings.get("last_folder", "") or os.path.expanduser("~"),
            filetypes=[("Audio", "*.mp3 *.wav *.ogg *.flac"),
                       ("All files", "*.*")]
        )
        if not path:
            return
        self.settings["last_folder"] = os.path.dirname(path)
        save_json(SETTINGS_FILE, self.settings)
        self.load_track(path)

    def load_track(self, path):
        if not os.path.exists(path):
            messagebox.showerror("Error", "File not found:\n" + path)
            return
        try:
            self.player.load(path)
        except Exception as e:
            messagebox.showerror("Error", "Failed to load:\n" + str(e))
            return

        name = os.path.basename(path)
        if len(name) > 30:
            name = name[:27] + "..."
        self.display.config(text=name)
        self.status.config(text="READY")

        self.btn_play.config(state="normal", text="PLAY")
        self.btn_pause.config(state="normal")
        self.btn_stop.config(state="normal")
        self._set_leds(False, False)

        self.scrubber.set_duration(self.player.duration_s)
        self.scrubber.set_position(0.0)
        self._update_fav_indicator()

        self.play_track()

    def play_track(self):
        if not self.player.track_path:
            return
        self.player.play()
        self.status.config(text="PLAYING")
        self.btn_play.config(state="disabled", text="PLAYING")
        self.btn_pause.config(state="normal")
        self._set_leds(True, False)
        self._start_end_watch()

    def pause_track(self):
        if self.player.state != "PLAYING":
            return
        self.player.pause()
        self.status.config(text="PAUSED")
        self.btn_play.config(state="normal", text="RESUME")
        self.btn_pause.config(state="disabled")
        self._set_leds(False, True)
        self._stop_end_watch()

    def stop_track(self):
        self.player.stop()
        self.status.config(text="STOPPED")
        self.btn_play.config(state="normal", text="PLAY")
        self.btn_pause.config(state="disabled")
        self._set_leds(False, False)
        self.scrubber.set_position(0.0)
        self._stop_end_watch()

    def change_volume(self, v):
        self.player.set_volume(v)
        self._update_volume_label(v)
        self.settings["volume"] = v

    def _update_volume_label(self, v):
        self.vol_label.config(text=f"{int(v*100)}%")

    def on_scrub(self, target):
        self.player.seek_to(target)

    def _set_leds(self, play_on, pause_on):
        self._draw_led(self.led_play, play_on)
        self._draw_led(self.led_pause, pause_on,
                       color_off=C["led_off_p"], color_on=C["led_pause"])

    # --- playlist actions ------------------------------------------------
    def toggle_playlist(self):
        if self._playlist_win is not None and self._playlist_win.winfo_exists():
            self._playlist_win.lift()
            self._playlist_win.focus_set()
            return
        self._playlist_win = PlaylistWindow(self)

    def add_current_to_playlist(self):
        p = self.player.track_path
        if not p:
            return
        if p not in self.playlist["tracks"]:
            self.playlist["tracks"].append(p)
            self.save_playlist()
            if self._playlist_win is not None and self._playlist_win.winfo_exists():
                self._playlist_win.refresh()

    def toggle_favorite(self):
        p = self.player.track_path
        if not p:
            return
        # also ensure it's in playlist
        if p not in self.playlist["tracks"]:
            self.playlist["tracks"].append(p)
        if p in self.playlist["favorites"]:
            self.playlist["favorites"].remove(p)
        else:
            self.playlist["favorites"].append(p)
        self.save_playlist()
        self._update_fav_indicator()
        if self._playlist_win is not None and self._playlist_win.winfo_exists():
            self._playlist_win.refresh()

    def _update_fav_indicator(self):
        p = self.player.track_path
        if p and p in self.playlist["favorites"]:
            self.fav_indicator.config(text="★ FAVORITE")
        else:
            self.fav_indicator.config(text="")

    def play_next(self):
        tracks = self.playlist["tracks"]
        if not tracks:
            return
        cur = self.player.track_path
        if cur in tracks:
            idx = (tracks.index(cur) + 1) % len(tracks)
        else:
            idx = 0
        self.load_track(tracks[idx])

    def save_playlist(self):
        save_json(PLAYLIST_FILE, self.playlist)

    # --- periodic UI update ---------------------------------------------
    def _tick_ui(self):
        self._update_time_label()
        if self.player.duration_s > 0:
            self.scrubber.set_duration(self.player.duration_s)
            self.scrubber.set_position(self.player.current_pos())
        self.root.after(500, self._tick_ui)

    def _update_time_label(self):
        pos = self.player.current_pos()
        dur = self.player.duration_s
        self.time_lbl.config(text=f"{fmt_time(pos)} / {fmt_time(dur)}")

    def _start_end_watch(self):
        self._stop_end_watch()

        def watch():
            if self.player.state == "PLAYING" and not self.player.is_busy():
                self.root.after(0, self._on_track_end)
                return
            self._end_check_id = self.root.after(300, watch)

        self._end_check_id = self.root.after(300, watch)

    def _stop_end_watch(self):
        if self._end_check_id is not None:
            try:
                self.root.after_cancel(self._end_check_id)
            except Exception:
                pass
            self._end_check_id = None

    def _on_track_end(self):
        self._stop_end_watch()
        self.stop_track()

    # --- dialogs ---------------------------------------------------------
    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title("SETTINGS")
        win.configure(bg=C["bg_body"])
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text="SETTINGS", bg=C["bg_body"],
                 fg=C["accent"], font=FONT_TITLE).pack(pady=(14, 10))

        theme_frame = tk.Frame(win, bg=C["bg_body"])
        theme_frame.pack(fill="x", padx=16, pady=8)
        tk.Label(theme_frame, text="Theme:", bg=C["bg_body"],
                 fg=C["btn_fg"], font=FONT_MONO_SM, width=10, anchor="w").pack(side="left")

        theme_var = tk.StringVar(value=self.settings.get("theme", "retro"))
        theme_menu = tk.OptionMenu(theme_frame, theme_var, "retro", "cassette")
        theme_menu.config(bg=C["btn_bg"], fg=C["btn_fg"], activebackground=C["accent"],
                          font=FONT_MONO_SM, highlightthickness=0, bd=0, width=10)
        theme_menu["menu"].config(bg=C["bg_panel"], fg=C["btn_fg"],
                                  activebackground=C["accent"])
        theme_menu.pack(side="left")

        tk.Label(win, text="(Theme applies after restart)",
                 bg=C["bg_body"], fg=C["fg_dim"],
                 font=FONT_TINY).pack(pady=(0, 4))

        def apply_and_close():
            self.settings["theme"] = theme_var.get()
            save_json(SETTINGS_FILE, self.settings)
            win.destroy()

        btn_row = tk.Frame(win, bg=C["bg_body"])
        btn_row.pack(pady=16)
        tk.Button(btn_row, text="OK", command=apply_and_close,
                  bg=C["btn_bg"], fg=C["btn_fg"], activebackground=C["btn_active"],
                  font=FONT_MONO_SM, width=10, bd=2, relief="raised",
                  highlightthickness=0).pack(side="left", padx=6)
        tk.Button(btn_row, text="Close", command=win.destroy,
                  bg=C["btn_bg"], fg=C["btn_fg"], activebackground=C["btn_active"],
                  font=FONT_MONO_SM, width=10, bd=2, relief="raised",
                  highlightthickness=0).pack(side="left", padx=6)

    def show_about(self):
        messagebox.showinfo(
            "About",
            f"SCARLI-MUSIC (BETA) v{APP_VERSION}\n\n"
            "Retro player inspired by\n"
            "Soviet radio electronics.\n\n"
            "Python 3.14 + pygame-ce + tkinter\n"
            "© 2026"
        )

    # --- exit ------------------------------------------------------------
    def on_closing(self):
        save_json(SETTINGS_FILE, self.settings)
        save_json(PLAYLIST_FILE, self.playlist)
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception:
            pass
        self.root.destroy()


def main():
    root = tk.Tk()
    ScarliMusic(root)
    root.mainloop()


if __name__ == "__main__":
    main()