"""
SCARLI-MUSIC v0.2
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
from datetime import datetime
from collections import deque

from lang import t, set_lang, LANG, lang_display_name

APP_VERSION = "0.2"
APP_TITLE = "SCARLI-MUSIC"
APP_YEAR = "2026"
SETTINGS_FILE = "settings.json"
PLAYLIST_FILE = "playlist.json"

# ---------------------------------------------------------------------------
#  DEFAULT SETTINGS
# ---------------------------------------------------------------------------
DEFAULT_SETTINGS = {
    "volume": 0.5,
    "last_folder": "",
    "theme": "retro",
    "language": "en",
    "fade_in": True,
    "fade_in_ms": 500,
    "fade_out": True,
    "fade_out_ms": 300,
    "fade_between": False,
    "fade_between_ms": 1500,
    "gapless": True,
    "repeat_mode": "off",
    "shuffle_mode": "off",
    "shuffle_history": 5,
    "clock_on": True,
    "reels_animation": True,
    "crt_scanlines": False,
    "crt_flicker": False,
    "eco_mode": False,
    "ticker_on": True,
    "low_quality_render": False,
    "static_scrubber": False,
    "led_enabled": True,
    "window_animation": True,
}

DEFAULT_PLAYLIST = {
    "tracks": [],
    "favorites": [],
}

# ---------------------------------------------------------------------------
#  THEMES
# ---------------------------------------------------------------------------
THEMES = {
    "retro": {
        "label": "RETRO CRT",
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
        "btn_radius":   18,
        "btn_outline":  "#c9a227",
        "font_btn":     ("Courier New", 10, "bold"),
        "font_display": ("Courier New", 14, "bold"),
        "font_title":   ("Courier New", 13, "bold"),
        "font_small":   ("Courier New", 9, "bold"),
        "scanlines":    True,
    },
    "cassette": {
        "label": "CASSETTE",
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
        "btn_radius":   10,
        "btn_outline":  "#8a7a5a",
        "font_btn":     ("Arial", 10, "bold"),
        "font_display": ("Arial", 14, "bold"),
        "font_title":   ("Arial", 13, "bold"),
        "font_small":   ("Arial", 9, "bold"),
        "scanlines":    False,
    },
    "lamp": {
        "label": "LAMP AMP",
        "bg_body":      "#221608",
        "bg_panel":     "#2e1e0c",
        "bg_screen":    "#1a0f04",
        "bg_trough":    "#150c02",
        "fg_main":      "#ffcc66",
        "fg_dim":       "#8a6020",
        "fg_soft":      "#f0dba8",
        "btn_bg":       "#4a3016",
        "btn_fg":       "#ffe8b0",
        "btn_active":   "#6a4620",
        "led_on":       "#ff8a2a",
        "led_off":      "#3a220a",
        "led_pause":    "#ff5a1a",
        "led_off_p":    "#3a1508",
        "accent":       "#e0b060",
        "frame":        "#7a5525",
        "knob_bg":      "#3a2410",
        "knob_edge":    "#8a6535",
        "knob_line":    "#ffcc66",
        "knob_dot":     "#e0b060",
        "list_bg":      "#1a0f04",
        "list_sel":     "#4a3016",
        "list_fav":     "#ffcc66",
        "btn_radius":   22,
        "btn_outline":  "#ffcc66",
        "font_btn":     ("Georgia", 10, "bold"),
        "font_display": ("Georgia", 14, "bold"),
        "font_title":   ("Georgia", 13, "bold"),
        "font_small":   ("Georgia", 9, "bold"),
        "scanlines":    False,
    },
    "elektronika": {
        "label": "ELEKTRONIKA-302",
        "bg_body":      "#1e2226",
        "bg_panel":     "#2a2f34",
        "bg_screen":    "#0f1214",
        "bg_trough":    "#171a1c",
        "fg_main":      "#a8d4dc",
        "fg_dim":       "#5a7a82",
        "fg_soft":      "#d8e8ec",
        "btn_bg":       "#3a4046",
        "btn_fg":       "#d8e8ec",
        "btn_active":   "#505860",
        "led_on":       "#5affa0",
        "led_off":      "#1a3a28",
        "led_pause":    "#ff5a5a",
        "led_off_p":    "#3a1818",
        "accent":       "#7ab0c0",
        "frame":        "#4a5560",
        "knob_bg":      "#2a3038",
        "knob_edge":    "#5a6870",
        "knob_line":    "#a8d4dc",
        "knob_dot":     "#7ab0c0",
        "list_bg":      "#12161a",
        "list_sel":     "#2a3844",
        "list_fav":     "#a8d4dc",
        "btn_radius":   0,
        "btn_outline":  "#5a6870",
        "font_btn":     ("Consolas", 10, "bold"),
        "font_display": ("Consolas", 14, "bold"),
        "font_title":   ("Consolas", 13, "bold"),
        "font_small":   ("Consolas", 9, "bold"),
        "scanlines":    False,
    },
    "vinyl": {
        "label": "VINYL",
        "bg_body":      "#1a0a0e",
        "bg_panel":     "#2a1016",
        "bg_screen":    "#0f0508",
        "bg_trough":    "#150608",
        "fg_main":      "#ff8a9a",
        "fg_dim":       "#8a4050",
        "fg_soft":      "#f0c8d0",
        "btn_bg":       "#3a1820",
        "btn_fg":       "#f0c8d0",
        "btn_active":   "#552028",
        "led_on":       "#ff5a8a",
        "led_off":      "#3a0a14",
        "led_pause":    "#ffb060",
        "led_off_p":    "#3a2008",
        "accent":       "#e08a9a",
        "frame":        "#6a2a38",
        "knob_bg":      "#2e1218",
        "knob_edge":    "#7a3a48",
        "knob_line":    "#ff8a9a",
        "knob_dot":     "#e08a9a",
        "list_bg":      "#120508",
        "list_sel":     "#3a1820",
        "list_fav":     "#ff8a9a",
        "btn_radius":   28,
        "btn_outline":  "#ff8a9a",
        "font_btn":     ("Times New Roman", 10, "bold"),
        "font_display": ("Times New Roman", 14, "bold"),
        "font_title":   ("Times New Roman", 13, "bold"),
        "font_small":   ("Times New Roman", 9, "bold"),
        "scanlines":    False,
    },
}

C = dict(THEMES["retro"])

# ---------------------------------------------------------------------------
#  UTILS
# ---------------------------------------------------------------------------
def fmt_time(seconds):
    if seconds is None or seconds <= 0:
        return "--:--"
    s = int(seconds)
    return f"{s // 60:02d}:{s % 60:02d}"


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


def load_settings():
    return load_json(SETTINGS_FILE, DEFAULT_SETTINGS)


def load_playlist():
    p = load_json(PLAYLIST_FILE, DEFAULT_PLAYLIST)
    p["tracks"]    = [tt for tt in p.get("tracks", [])    if os.path.exists(tt)]
    p["favorites"] = [tt for tt in p.get("favorites", []) if os.path.exists(tt)]
    return p


def save_playlist(p):
    save_json(PLAYLIST_FILE, p)


def hex_to_rgb(h):
    """Поддерживает #RGB и #RRGGBB."""
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return f"#{max(0,min(255,int(r))):02x}{max(0,min(255,int(g))):02x}{max(0,min(255,int(b))):02x}"


def lerp_color(c1, c2, t_):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex(r1 + (r2 - r1) * t_,
                      g1 + (g2 - g1) * t_,
                      b1 + (b2 - b1) * t_)


# ---------------------------------------------------------------------------
#  ROUNDED BUTTON
# ---------------------------------------------------------------------------
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text="", command=None, width=96, height=42,
                 radius=12, font=None, **kw):
        super().__init__(parent, width=width, height=height,
                         bg=parent["bg"], highlightthickness=0, bd=0, **kw)
        self.text = text
        self.command = command
        self.radius = radius
        self._btn_w = width
        self._btn_h = height
        self._state = "normal"
        self._hover = False
        self._pressed = False
        self._font = font

        self.bind("<Enter>",           self._on_enter)
        self.bind("<Leave>",           self._on_leave)
        self.bind("<Button-1>",        self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Configure>",       lambda e: self.redraw())

        self.redraw()

    def retheme(self):
        try:
            self.config(bg=self.master["bg"])
        except Exception:
            self.config(bg=C["bg_body"])
        self.redraw()

    def set_text(self, text):
        self.text = text
        self.redraw()

    def set_state(self, state):
        self._state = state
        self.redraw()

    def _on_enter(self, _e):
        self._hover = True
        self.redraw()

    def _on_leave(self, _e):
        self._hover = False
        self._pressed = False
        self.redraw()

    def _on_press(self, _e):
        if self._state == "disabled":
            return
        self._pressed = True
        self.redraw()

    def _on_release(self, _e):
        if self._state == "disabled":
            return
        if self._pressed:
            self._pressed = False
            self.redraw()
            if self.command:
                self.command()

    def _rounded_rect(self, x1, y1, x2, y2, r, **kw):
        r = min(r, (x2 - x1) / 2, (y2 - y1) / 2)
        if r <= 0:
            return self.create_rectangle(x1, y1, x2, y2, **kw)
        points = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kw)

    def _is_lowq(self):
        try:
            app = self.winfo_toplevel()._app
            return app.settings.get("low_quality_render", False)
        except Exception:
            return False

    def redraw(self):
        self.delete("all")
        w, h = self._btn_w, self._btn_h
        r = self.radius
        lq = self._is_lowq()

        if self._state == "disabled":
            bg = C["bg_panel"]
            fg = C["fg_dim"]
            outline = C["frame"]
        elif self._pressed:
            bg = lerp_color(C["btn_active"], "#000000", 0.25)
            fg = C["btn_fg"]
            outline = C["btn_outline"]
        elif self._hover:
            bg = C["btn_active"]
            fg = C["btn_fg"]
            outline = C["btn_outline"]
        else:
            bg = C["btn_bg"]
            fg = C["btn_fg"]
            outline = C["btn_outline"]

        if lq:
            self._rounded_rect(0, 0, w, h, r, fill=bg, outline="")
        else:
            self._rounded_rect(2, 3, w, h, r,
                               fill=lerp_color(C["bg_body"], "#000000", 0.4),
                               outline="")
            self._rounded_rect(0, 0, w - 1, h - 2, r,
                               fill=bg, outline=outline, width=1)

        if not lq and self._state != "disabled":
            self._rounded_rect(3, 2, w - 3, h * 0.42, max(2, r - 2),
                               fill=lerp_color(bg, "#ffffff", 0.10),
                               outline="")

        f = self._font or C["font_btn"]
        self.create_text(w / 2, h / 2, text=self.text, fill=fg, font=f)


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

    def retheme(self):
        self.config(bg=self.master["bg"] if self.master else C["bg_body"])
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
        self.create_line(cx, cy, x1, y1, fill=line_col, width=3, capstyle="round")
        self.create_oval(x1 - 4, y1 - 4, x1 + 4, y1 + 4,
                         fill=C["knob_dot"] if not self.disabled else C["fg_dim"],
                         outline="")

        for i in range(11):
            a = math.radians(-135 + i * 27)
            tx1 = cx + math.sin(a) * (r + 5)
            ty1 = cy - math.cos(a) * (r + 5)
            tx2 = cx + math.sin(a) * (r + 9)
            ty2 = cy - math.cos(a) * (r + 9)
            self.create_line(tx1, ty1, tx2, ty2, fill=C["fg_dim"], width=1)

        self.create_text(cx, s + 8, text=self.label,
                         fill=C["accent"], font=C["font_small"])

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
#  SCRUBBER
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

    def set_duration(self, d):
        self.duration = max(0.0, d)
        self._redraw()

    def set_position(self, p):
        if self._dragging:
            return
        self.position = max(0.0, p)
        self._redraw()

    def retheme(self):
        self.config(bg=C["bg_trough"])
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

        self.create_line(head_x, 2, head_x, h - 10, fill=C["fg_main"], width=3)
        self.create_rectangle(head_x - 4, 2, head_x + 4, 8,
                              fill=C["fg_main"], outline=C["knob_dot"])


# ---------------------------------------------------------------------------
#  REELS
# ---------------------------------------------------------------------------
class ReelsCanvas(tk.Canvas):
    def __init__(self, parent, size=80):
        super().__init__(parent, width=size, height=size,
                         bg=parent["bg"], highlightthickness=0, bd=0)
        self.size = size
        self.angle = 0.0
        self.playing = False
        self._draw()

    def retheme(self):
        self.config(bg=self.master["bg"] if self.master else C["bg_body"])
        self._draw()

    def set_playing(self, playing):
        self.playing = playing

    def tick(self, animate, speed=8):
        if self.playing and animate:
            self.angle = (self.angle + speed) % 360
            self._draw()

    def _draw(self):
        self.delete("all")
        s = self.size
        cx = s / 2
        r = s / 2 - 6

        self.create_rectangle(2, 2, s - 2, s - 2,
                              fill=C["bg_panel"], outline=C["frame"], width=2)

        for kx in (cx - r * 0.55, cx + r * 0.55):
            ky = cx
            kr = r * 0.4
            self.create_oval(kx - kr, ky - kr, kx + kr, ky + kr,
                             fill=C["bg_trough"], outline=C["knob_edge"], width=2)
            for i in range(6):
                a = math.radians(self.angle + i * 60)
                mx1 = kx + math.cos(a) * (kr * 0.35)
                my1 = ky + math.sin(a) * (kr * 0.35)
                mx2 = kx + math.cos(a) * (kr * 0.85)
                my2 = ky + math.sin(a) * (kr * 0.85)
                self.create_line(mx1, my1, mx2, my2,
                                 fill=C["knob_line"], width=2)
            self.create_oval(kx - 3, ky - 3, kx + 3, ky + 3,
                             fill=C["knob_dot"], outline="")


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
        self.target_volume = 0.5

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

    def play(self, start_at=None):
        if self.state == "PAUSED":
            pygame.mixer.music.unpause()
        else:
            s = self.seek_base if start_at is None else max(0.0, start_at)
            pygame.mixer.music.play(start=s)
            self.seek_base = s
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
        self.target_volume = max(0.0, min(1.0, v))
        pygame.mixer.music.set_volume(self.target_volume)

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
#  PLAYLIST WINDOW
# ---------------------------------------------------------------------------
class PlaylistWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        self.title(t("p_title"))
        self.configure(bg=C["bg_body"])
        self.transient(app.root)
        self.geometry("620x520")
        self._sort_mode = "index"
        self._buttons = []
        self._build()
        self.refresh()

    def _rbtn(self, parent, key, cmd, w=96, h=32, text_override=None):
        label = text_override if text_override is not None else (t(key) if key else "")
        b = RoundedButton(parent, text=label, command=cmd,
                          width=w, height=h, radius=C["btn_radius"])
        self._buttons.append(b)
        return b

    def _build(self):
        top = tk.Frame(self, bg=C["bg_body"])
        top.pack(fill="x", padx=10, pady=(10, 0))
        tk.Label(top, text=t("p_title"), bg=C["bg_body"], fg=C["accent"],
                 font=C["font_title"]).pack(side="left")
        self._rbtn(top, "p_add",   self._add_files, w=88).pack(side="right", padx=2)
        self._rbtn(top, "p_close", self.destroy,     w=88).pack(side="right", padx=2)

        sr = tk.Frame(self, bg=C["bg_body"])
        sr.pack(fill="x", padx=10, pady=(8, 0))
        tk.Label(sr, text=t("p_search"), bg=C["bg_body"], fg=C["fg_soft"],
                 font=C["font_btn"]).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh())
        tk.Entry(sr, textvariable=self.search_var,
                 bg=C["bg_trough"], fg=C["fg_main"], insertbackground=C["fg_main"],
                 font=C["font_btn"], bd=1, relief="flat").pack(
                     side="left", fill="x", expand=True, padx=6)

        srt = tk.Frame(self, bg=C["bg_body"])
        srt.pack(fill="x", padx=10, pady=(6, 0))
        tk.Label(srt, text=t("p_sort"), bg=C["bg_body"], fg=C["fg_soft"],
                 font=C["font_btn"]).pack(side="left")
        for label, mode in (("IDX", "index"), ("NAME", "name"),
                            ("DUR", "duration"), ("DATE", "date")):
            self._rbtn(srt, None, lambda m=mode: self._set_sort(m),
                       w=54, h=26, text_override=label).pack(side="left", padx=2)

        lw = tk.Frame(self, bg=C["accent"], bd=1)
        lw.pack(fill="both", expand=True, padx=10, pady=10)
        inner = tk.Frame(lw, bg=C["list_bg"])
        inner.pack(fill="both", expand=True, padx=2, pady=2)

        self.listbox = tk.Listbox(
            inner, bg=C["list_bg"], fg=C["fg_main"],
            selectbackground=C["list_sel"], selectforeground=C["fg_main"],
            font=C["font_btn"], bd=0, highlightthickness=0,
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

        bot = tk.Frame(self, bg=C["bg_body"])
        bot.pack(fill="x", padx=10, pady=(0, 10))
        for key, cmd in (("p_fav", self._toggle_fav),
                         ("p_remove", self._remove),
                         ("p_clear", self._clear)):
            self._rbtn(bot, key, cmd).pack(side="left", padx=2)
        for key, cmd in (("p_export", self._export_m3u),
                         ("p_import", self._import_m3u)):
            self._rbtn(bot, key, cmd, w=110).pack(side="right", padx=2)

    def _set_sort(self, mode):
        self._sort_mode = mode
        self.refresh()

    def _get_sorted_tracks(self):
        tracks = list(self.app.playlist["tracks"])
        if self._sort_mode == "name":
            tracks.sort(key=lambda p: os.path.basename(p).lower())
        elif self._sort_mode == "duration":
            def dur(p):
                try:
                    from mutagen import File as MFile
                    f = MFile(p)
                    if f is not None and f.info is not None:
                        return float(f.info.length)
                except Exception:
                    pass
                return 0.0
            tracks.sort(key=dur)
        elif self._sort_mode == "date":
            tracks.sort(key=lambda p: os.path.getmtime(p) if os.path.exists(p) else 0)
        return tracks

    def refresh(self):
        self.listbox.delete(0, tk.END)
        query = (self.search_var.get() or "").lower().strip()
        self._visible = []
        for i, tt in enumerate(self._get_sorted_tracks()):
            name = os.path.basename(tt)
            if query and query not in name.lower():
                continue
            self._visible.append(tt)
            fav = tt in self.app.playlist["favorites"]
            mark = "★ " if fav else "  "
            self.listbox.insert(tk.END, f"{mark}{i+1:02d}. {name}")
            if fav:
                self.listbox.itemconfig(tk.END, fg=C["list_fav"])

    def _add_files(self):
        paths = filedialog.askopenfilenames(
            title=t("m_open"),
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
        self.app.load_track(self._visible[sel[0]])

    def _toggle_fav(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        path = self._visible[sel[0]]
        if path in self.app.playlist["favorites"]:
            self.app.playlist["favorites"].remove(path)
        else:
            self.app.playlist["favorites"].append(path)
        self.app.save_playlist()
        self.refresh()
        self.listbox.selection_set(sel[0])

    def _remove(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        path = self._visible[sel[0]]
        if path in self.app.playlist["tracks"]:
            self.app.playlist["tracks"].remove(path)
        if path in self.app.playlist["favorites"]:
            self.app.playlist["favorites"].remove(path)
        self.app.save_playlist()
        self.refresh()

    def _clear(self):
        if not messagebox.askyesno(t("p_clear"), t("d_clearq")):
            return
        self.app.playlist["tracks"] = []
        self.app.playlist["favorites"] = []
        self.app.save_playlist()
        self.refresh()

    def _export_m3u(self):
        path = filedialog.asksaveasfilename(
            title=t("d_exp"), defaultextension=".m3u",
            filetypes=[("M3U", "*.m3u"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                for tt in self.app.playlist["tracks"]:
                    f.write(tt + "\n")
            messagebox.showinfo(t("d_exp"), t("d_saved") + path)
        except Exception as e:
            messagebox.showerror(t("d_error"), str(e))

    def _import_m3u(self):
        path = filedialog.askopenfilename(
            title=t("d_imp"),
            filetypes=[("M3U", "*.m3u"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if os.path.exists(line) and line not in self.app.playlist["tracks"]:
                        self.app.playlist["tracks"].append(line)
            self.app.save_playlist()
            self.refresh()
        except Exception as e:
            messagebox.showerror(t("d_error"), str(e))


# ---------------------------------------------------------------------------
#  MAIN APP
# ---------------------------------------------------------------------------
class ScarliMusic:
    def __init__(self, root):
        self.root = root
        root._app = self
        self.settings = load_settings()
        set_lang(self.settings.get("language", "en"))
        self.playlist = load_playlist()
        self.player = Player()
        self._end_check_id = None
        self._playlist_win = None
        self._ticker_job = None
        self._ticker_pos = 0
        self._clock_job = None
        self._fade_job = None
        self._fading = False
        self._smart_history = deque(maxlen=self.settings.get("shuffle_history", 5))
        self._all_buttons = []

        self._apply_theme_palette()
        self._setup_window()
        self._build_ui()
        self._bind_hotkeys()
        self._apply_settings_on_start()
        self._start_clock()
        self._tick_ui()

        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        if self.settings.get("window_animation", True) \
                and not self.settings.get("eco_mode", False):
            self._animate_window_open()

    # -- theme ------------------------------------------------------------
    def _apply_theme_palette(self):
        global C
        key = self.settings.get("theme", "retro")
        if key not in THEMES:
            key = "retro"
        C.clear()
        C.update(THEMES[key])

    def change_theme(self, key):
        if key not in THEMES:
            return
        self.settings["theme"] = key
        save_json(SETTINGS_FILE, self.settings)
        self._apply_theme_palette()
        self._retheme_all()
        self._build_menu()

    def _retheme_all(self):
        for name, col in (
            ("_body", "bg_body"), ("_header", "bg_body"), ("_center", "bg_body"),
            ("_knobs", "bg_body"), ("_pl_row", "bg_body"),
            ("_scrub_frame", "bg_panel"), ("_panel", "bg_panel"),
            ("_screen", "bg_screen"), ("_screen_top", "bg_screen"),
        ):
            w = getattr(self, name, None)
            if w is not None:
                try:
                    w.config(bg=C[col])
                except Exception:
                    pass
        for w, col in (
            (getattr(self, "_title_lbl", None), "accent"),
            (getattr(self, "_ver_lbl", None), "fg_dim"),
            (getattr(self, "display", None), "fg_main"),
            (getattr(self, "status", None), "fg_dim"),
            (getattr(self, "time_lbl", None), "fg_soft"),
            (getattr(self, "clock_lbl", None), "fg_dim"),
            (getattr(self, "vol_label", None), "fg_main"),
        ):
            if w is not None:
                try:
                    screen = w in (self.display, self.status, self.time_lbl, self.clock_lbl)
                    w.config(bg=C["bg_screen"] if screen else C["bg_body"], fg=C[col])
                except Exception:
                    pass
        for k in ("vol_knob", "speed_knob", "scrubber", "reels"):
            w = getattr(self, k, None)
            if w is not None:
                w.retheme()
        for btn in self._all_buttons:
            btn.retheme()

        if self._playlist_win is not None and self._playlist_win.winfo_exists():
            try:
                self._playlist_win.destroy()
            except Exception:
                pass
            self._playlist_win = None

    # -- window -----------------------------------------------------------
    def _setup_window(self):
        self.root.title(f"{APP_TITLE}  v{APP_VERSION}")
        self.root.configure(bg=C["bg_body"])
        self.root.resizable(False, False)
        w, h = 660, 640
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _animate_window_open(self):
        try:
            self.root.attributes("-alpha", 0.0)
        except Exception:
            return
        total_ms = 280
        steps = 14
        dt = total_ms // steps
        def step(i=0):
            a = min(1.0, i / steps)
            try:
                self.root.attributes("-alpha", a)
            except Exception:
                return
            if i < steps:
                self.root.after(dt, step, i + 1)
        step()

    # -- UI ---------------------------------------------------------------
    def _build_ui(self):
        self._all_buttons = []

        self._body = tk.Frame(self.root, bg=C["bg_body"])
        self._body.pack(fill="both", expand=True, padx=10, pady=10)

        self._header = tk.Frame(self._body, bg=C["bg_body"])
        self._header.pack(fill="x", pady=(0, 8))
        self._title_lbl = tk.Label(self._header, text=f"◉ {APP_TITLE}",
                                   bg=C["bg_body"], fg=C["accent"],
                                   font=C["font_title"], anchor="w")
        self._title_lbl.pack(side="left", padx=4)
        self._ver_lbl = tk.Label(self._header, text=f"v{APP_VERSION}",
                                 bg=C["bg_body"], fg=C["fg_dim"],
                                 font=C["font_small"], anchor="e")
        self._ver_lbl.pack(side="right", padx=4)

        self._center = tk.Frame(self._body, bg=C["bg_body"])
        self._center.pack(fill="x", pady=4)

        self._panel = tk.Frame(self._center, bg=C["bg_panel"], bd=2, relief="ridge")
        self._panel.pack(side="left", fill="both", expand=True)

        self._led_frame = tk.Frame(self._panel, bg=C["bg_panel"])
        self._led_frame.pack(side="left", padx=(10, 4), pady=10)

        self.led_play = tk.Canvas(self._led_frame, width=14, height=14,
                                  bg=C["bg_panel"], highlightthickness=0)
        self.led_play.pack(pady=3)
        self._draw_led(self.led_play, False)

        self.led_pause = tk.Canvas(self._led_frame, width=14, height=14,
                                   bg=C["bg_panel"], highlightthickness=0)
        self.led_pause.pack(pady=3)
        self._draw_led(self.led_pause, False,
                       color_off=C["led_off_p"], color_on=C["led_pause"])

        screen_wrap = tk.Frame(self._panel, bg=C["accent"], bd=1)
        screen_wrap.pack(side="left", padx=(4, 10), pady=10, fill="both", expand=True)
        self._screen_wrap = screen_wrap

        self._screen = tk.Frame(screen_wrap, bg=C["bg_screen"])
        self._screen.pack(fill="both", expand=True, padx=2, pady=2)

        self._screen_top = tk.Frame(self._screen, bg=C["bg_screen"])
        self._screen_top.pack(fill="x", padx=10, pady=(8, 0))

        self.display = tk.Label(self._screen_top, text=t("no_track"),
                                bg=C["bg_screen"], fg=C["fg_main"],
                                font=C["font_display"], anchor="w", justify="left")
        self.display.pack(side="left", fill="x", expand=True)

        self.clock_lbl = tk.Label(self._screen_top, text="00:00",
                                  bg=C["bg_screen"], fg=C["fg_dim"],
                                  font=C["font_small"], anchor="e")
        self.clock_lbl.pack(side="right")

        self.status = tk.Label(self._screen, text=t("stopped"),
                               bg=C["bg_screen"], fg=C["fg_dim"],
                               font=C["font_small"], anchor="w")
        self.status.pack(fill="x", padx=10)

        self.time_lbl = tk.Label(self._screen, text="--:-- / --:--",
                                 bg=C["bg_screen"], fg=C["fg_soft"],
                                 font=C["font_small"], anchor="w")
        self.time_lbl.pack(fill="x", padx=10, pady=(2, 8))

        self._knobs = tk.Frame(self._center, bg=C["bg_body"])
        self._knobs.pack(side="right", padx=(10, 0))

        self.vol_knob = Knob(self._knobs, label=t("volume"), size=74,
                             value=self.settings["volume"],
                             callback=self.change_volume)
        self.vol_knob.pack(side="top", pady=(0, 6))

        self.speed_knob = Knob(self._knobs, label=t("speed"), size=74,
                               value=0.5, disabled=True)
        self.speed_knob.pack(side="top", pady=(0, 6))

        self._soon_lbl = tk.Label(self._knobs, text=t("coming_soon"),
                                  bg=C["bg_body"], fg=C["fg_dim"],
                                  font=("Courier New", 8))
        self._soon_lbl.pack()

        self.reels = ReelsCanvas(self._knobs, size=80)
        if self.settings.get("theme") == "cassette":
            self.reels.pack(pady=(8, 0))

        self._scrub_frame = tk.Frame(self._body, bg=C["bg_panel"], bd=2, relief="ridge")
        self._scrub_frame.pack(fill="x", pady=(12, 0))

        row = tk.Frame(self._scrub_frame, bg=C["bg_panel"])
        row.pack(fill="x", padx=8, pady=(4, 0))
        self._scrub_row = row
        self._scrub_lbl = tk.Label(row, text=t("tape"), bg=C["bg_panel"],
                                   fg=C["accent"], font=C["font_small"])
        self._scrub_lbl.pack(side="left")
        self.fav_indicator = tk.Label(row, text="", bg=C["bg_panel"],
                                      fg=C["list_fav"], font=C["font_small"])
        self.fav_indicator.pack(side="right")

        self.scrubber = Scrubber(self._scrub_frame, height=38,
                                 callback=self.on_scrub)
        self.scrubber.pack(fill="x", padx=8, pady=(0, 6))

        self._btn_frame = tk.Frame(self._body, bg=C["bg_body"])
        self._btn_frame.pack(pady=14)

        self.btn_open  = self._mk_btn(self._btn_frame, "open",  self.open_file)
        self.btn_play  = self._mk_btn(self._btn_frame, "play",  self.play_track, state="disabled")
        self.btn_pause = self._mk_btn(self._btn_frame, "pause", self.pause_track, state="disabled")
        self.btn_stop  = self._mk_btn(self._btn_frame, "stop",  self.stop_track, state="disabled")

        self.btn_open .grid(row=0, column=0, padx=3)
        self.btn_play .grid(row=0, column=1, padx=3)
        self.btn_pause.grid(row=0, column=2, padx=3)
        self.btn_stop .grid(row=0, column=3, padx=3)

        self._pl_row = tk.Frame(self._body, bg=C["bg_body"])
        self._pl_row.pack(pady=(4, 0))

        self.btn_prev     = self._mk_btn(self._pl_row, "prev",     self.play_prev)
        self.btn_playlist = self._mk_btn(self._pl_row, "playlist", self.toggle_playlist)
        self.btn_fav      = self._mk_btn(self._pl_row, "fav",      self.toggle_favorite)
        self.btn_next     = self._mk_btn(self._pl_row, "next",     self.play_next)

        self.btn_prev.grid(row=0, column=0, padx=3)
        self.btn_playlist.grid(row=0, column=1, padx=3)
        self.btn_fav.grid(row=0, column=2, padx=3)
        self.btn_next.grid(row=0, column=3, padx=3)

        self.vol_label = tk.Label(self._body, text="50%", bg=C["bg_body"],
                                  fg=C["fg_main"], font=C["font_small"])
        self.vol_label.pack(pady=(6, 0))

        self._build_menu()

    def _mk_btn(self, parent, text_key, cmd, state="normal"):
        b = RoundedButton(parent, text=t(text_key), command=cmd,
                          width=96, height=44, radius=C["btn_radius"])
        if state == "disabled":
            b.set_state("disabled")
        self._all_buttons.append(b)
        return b

    def _draw_led(self, canvas, on, color_on=None, color_off=None):
        canvas.delete("all")
        c_on  = color_on  or C["led_on"]
        c_off = color_off or C["led_off"]
        color = c_on if on else c_off
        canvas.create_oval(2, 2, 12, 12, fill=color, outline=C["frame"], width=1)

    def _build_menu(self):
        menubar = tk.Menu(self.root, bg=C["bg_panel"], fg=C["btn_fg"],
                          activebackground=C["accent"], activeforeground="#000", bd=0)
        fm = tk.Menu(menubar, tearoff=0, bg=C["bg_panel"], fg=C["btn_fg"],
                     activebackground=C["accent"], activeforeground="#000")
        fm.add_command(label=t("m_open"), command=self.open_file)
        fm.add_separator()
        fm.add_command(label=t("m_exit"), command=self.on_closing)
        menubar.add_cascade(label=t("m_file"), menu=fm)

        pm = tk.Menu(menubar, tearoff=0, bg=C["bg_panel"], fg=C["btn_fg"],
                     activebackground=C["accent"], activeforeground="#000")
        pm.add_command(label=t("m_show_pl"), command=self.toggle_playlist)
        pm.add_command(label=t("m_add_pl"), command=self.add_current_to_playlist)
        pm.add_separator()
        pm.add_command(label=t("m_next"), command=self.play_next)
        pm.add_command(label=t("m_prev"), command=self.play_prev)
        menubar.add_cascade(label=t("m_playlist"), menu=pm)

        tm = tk.Menu(menubar, tearoff=0, bg=C["bg_panel"], fg=C["btn_fg"],
                     activebackground=C["accent"], activeforeground="#000")
        for key, th in THEMES.items():
            tm.add_command(label=th["label"],
                           command=lambda k=key: self.change_theme(k))
        menubar.add_cascade(label=t("m_theme"), menu=tm)

        sm = tk.Menu(menubar, tearoff=0, bg=C["bg_panel"], fg=C["btn_fg"],
                     activebackground=C["accent"], activeforeground="#000")
        sm.add_command(label=t("m_settings_w"), command=self.open_settings)
        sm.add_separator()
        sm.add_command(label=t("m_about"), command=self.show_about)
        menubar.add_cascade(label=t("m_settings"), menu=sm)

        self.root.config(menu=menubar)

    # -- hotkeys ----------------------------------------------------------
    def _bind_hotkeys(self):
        self.root.bind("<space>", lambda e: self._toggle_play())
        self.root.bind("<KeyPress-o>", lambda e: self.open_file())
        self.root.bind("<KeyPress-s>", lambda e: self.stop_track())
        self.root.bind("<KeyPress-l>", lambda e: self.toggle_playlist())
        self.root.bind("<KeyPress-f>", lambda e: self.toggle_favorite())
        self.root.bind("<KeyPress-n>", lambda e: self.play_next())
        self.root.bind("<KeyPress-p>", lambda e: self.play_prev())
        self.root.bind("<Left>",  lambda e: self._seek_by(-5))
        self.root.bind("<Right>", lambda e: self._seek_by(5))
        self.root.bind("<Shift-Left>",  lambda e: self._seek_by(-30))
        self.root.bind("<Shift-Right>", lambda e: self._seek_by(30))
        self.root.bind("<Escape>", lambda e: self.on_closing())

    def _seek_by(self, sec):
        self.player.seek_to(self.player.current_pos() + sec)

    # -- apply settings on start ------------------------------------------
    def _apply_settings_on_start(self):
        self.player.set_volume(self.settings["volume"])
        self.vol_knob.set(self.settings["volume"])
        self._update_volume_label(self.settings["volume"])
        self._update_fav_indicator()
        if not self.settings.get("clock_on", True):
            self.clock_lbl.pack_forget()
        if not self.settings.get("ticker_on", True):
            self._stop_ticker()
        if not self.settings.get("led_enabled", True):
            self.led_play.pack_forget()
            self.led_pause.pack_forget()

    # -- fade -------------------------------------------------------------
    def _cancel_fade(self):
        if self._fade_job is not None:
            try:
                self.root.after_cancel(self._fade_job)
            except Exception:
                pass
            self._fade_job = None
        self._fading = False

    def _start_fade(self, from_v, to_v, duration_ms, on_done=None):
        self._cancel_fade()
        if duration_ms <= 0:
            pygame.mixer.music.set_volume(to_v)
            if on_done:
                on_done()
            return
        self._fading = True
        steps = max(2, int(duration_ms / 30))
        dt = duration_ms / steps
        delta = (to_v - from_v) / steps

        def step(i=0, current=from_v):
            if not self._fading:
                return
            current = from_v + delta * (i + 1)
            current = max(0.0, min(1.0, current))
            target_now = self.player.target_volume
            if i >= steps or abs(current - target_now) < 0.005:
                pygame.mixer.music.set_volume(target_now)
                self._fading = False
                self._fade_job = None
                if on_done:
                    on_done()
                return
            pygame.mixer.music.set_volume(current)
            self._fade_job = self.root.after(int(dt), step, i + 1, current)

        step()

    # -- player logic -----------------------------------------------------
    def _toggle_play(self):
        if self.player.state == "PLAYING":
            self.pause_track()
        elif self.player.track_path:
            self.play_track()

    def open_file(self):
        path = filedialog.askopenfilename(
            title=t("m_open"),
            initialdir=self.settings.get("last_folder", "") or os.path.expanduser("~"),
            filetypes=[("Audio", "*.mp3 *.wav *.ogg *.flac"), ("All files", "*.*")]
        )
        if not path:
            return
        self.settings["last_folder"] = os.path.dirname(path)
        save_json(SETTINGS_FILE, self.settings)
        self.load_track(path)

    def load_track(self, path, auto_play=True):
        if not os.path.exists(path):
            messagebox.showerror(t("d_error"), t("d_notfound") + path)
            return
        try:
            self.player.load(path)
        except Exception as e:
            messagebox.showerror(t("d_error"), t("d_loaderr") + str(e))
            return

        self._set_display_name(os.path.basename(path))
        self.status.config(text=t("ready"))
        self.btn_play.set_state("normal")
        self.btn_play.set_text(t("play"))
        self.btn_pause.set_state("normal")
        self.btn_stop.set_state("normal")
        self._set_leds(False, False)
        self.scrubber.set_duration(self.player.duration_s)
        self.scrubber.set_position(0.0)
        self._update_fav_indicator()

        if auto_play:
            self.play_track()

    def _set_display_name(self, full_name):
        self._full_name = full_name
        if len(full_name) <= 28 or not self.settings.get("ticker_on", True) \
                or self.settings.get("eco_mode", False):
            self.display.config(text=full_name[:30])
            self._stop_ticker()
        else:
            self._ticker_pos = 0
            self._start_ticker()

    def _start_ticker(self):
        self._stop_ticker()
        def tick():
            if not self._full_name:
                return
            text = self._full_name + "   ·   "
            n = len(text)
            p = self._ticker_pos % n
            view = (text + text)[p:p + 28]
            self.display.config(text=view)
            self._ticker_pos = (self._ticker_pos + 1) % n
            self._ticker_job = self.root.after(250, tick)
        self._ticker_job = self.root.after(250, tick)

    def _stop_ticker(self):
        if self._ticker_job is not None:
            try:
                self.root.after_cancel(self._ticker_job)
            except Exception:
                pass
            self._ticker_job = None

    def play_track(self):
        if not self.player.track_path:
            return
        self._cancel_fade()
        if self.settings.get("fade_in", True) and self.player.state != "PAUSED":
            pygame.mixer.music.set_volume(0.0)
            self.player.play()
            self._start_fade(0.0, self.player.target_volume,
                             self.settings.get("fade_in_ms", 500))
        else:
            self.player.play()
            pygame.mixer.music.set_volume(self.player.target_volume)

        self.status.config(text=t("playing"))
        self.btn_play.set_state("disabled")
        self.btn_play.set_text(t("playing"))
        self.btn_pause.set_state("normal")
        self._set_leds(True, False)
        self._start_end_watch()
        self.reels.set_playing(True)

    def pause_track(self):
        if self.player.state != "PLAYING":
            return
        self._cancel_fade()
        if self.settings.get("fade_out", True):
            cur = self.player.target_volume
            pygame.mixer.music.set_volume(cur)
            def after():
                self.player.pause()
                pygame.mixer.music.set_volume(self.player.target_volume)
                self._set_leds(False, True)
            self._start_fade(cur, 0.0, self.settings.get("fade_out_ms", 300), after)
        else:
            self.player.pause()
            self._set_leds(False, True)
        self.status.config(text=t("paused"))
        self.btn_play.set_state("normal")
        self.btn_play.set_text(t("resume"))
        self.btn_pause.set_state("disabled")
        self._stop_end_watch()
        self.reels.set_playing(False)

    def stop_track(self):
        self._cancel_fade()
        def do_stop():
            self.player.stop()
            pygame.mixer.music.set_volume(self.player.target_volume)
        if self.settings.get("fade_out", True) and self.player.state == "PLAYING":
            cur = self.player.target_volume
            pygame.mixer.music.set_volume(cur)
            self._start_fade(cur, 0.0, self.settings.get("fade_out_ms", 300), do_stop)
        else:
            do_stop()
        self.status.config(text=t("stopped"))
        self.btn_play.set_state("normal")
        self.btn_play.set_text(t("play"))
        self.btn_pause.set_state("disabled")
        self._set_leds(False, False)
        self.scrubber.set_position(0.0)
        self._stop_end_watch()
        self.reels.set_playing(False)

    def change_volume(self, v):
        self.player.set_volume(v)
        self._update_volume_label(v)
        self.settings["volume"] = v

    def _update_volume_label(self, v):
        self.vol_label.config(text=f"{int(v*100)}%")

    def on_scrub(self, target):
        self.player.seek_to(target)

    def _set_leds(self, play_on, pause_on):
        if not self.settings.get("led_enabled", True):
            return
        self._draw_led(self.led_play, play_on)
        self._draw_led(self.led_pause, pause_on,
                       color_off=C["led_off_p"], color_on=C["led_pause"])

    # -- playlist ---------------------------------------------------------
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
            self.fav_indicator.config(text="★ " + t("favorite"))
        else:
            self.fav_indicator.config(text="")

    def _pick_next_track(self):
        tracks = self.playlist["tracks"]
        if not tracks:
            return None
        mode = self.settings.get("repeat_mode", "off")
        if mode == "one":
            return self.player.track_path
        cur = self.player.track_path
        if cur in tracks:
            idx = tracks.index(cur)
        else:
            idx = -1
        shuffle = self.settings.get("shuffle_mode", "off")
        if shuffle == "off":
            if mode == "all":
                nxt = (idx + 1) % len(tracks)
            else:
                nxt = idx + 1
                if nxt >= len(tracks):
                    return None
        elif shuffle == "on":
            nxt = random.randrange(len(tracks))
        else:
            candidates = [i for i in range(len(tracks))
                          if tracks[i] not in self._smart_history]
            if not candidates:
                candidates = list(range(len(tracks)))
            nxt = random.choice(candidates)
        return tracks[nxt]

    def play_next(self):
        nxt = self._pick_next_track()
        if not nxt:
            self.stop_track()
            return
        self._smart_history.append(nxt)
        self.load_track(nxt)

    def play_prev(self):
        tracks = self.playlist["tracks"]
        if not tracks:
            return
        cur = self.player.track_path
        if cur in tracks:
            idx = (tracks.index(cur) - 1) % len(tracks)
        else:
            idx = 0
        self.load_track(tracks[idx])

    def save_playlist(self):
        save_json(PLAYLIST_FILE, self.playlist)

    # -- periodic ---------------------------------------------------------
    def _tick_ui(self):
        self._update_time_label()
        if not self.settings.get("static_scrubber", False):
            if self.player.duration_s > 0:
                self.scrubber.set_duration(self.player.duration_s)
                self.scrubber.set_position(self.player.current_pos())
        animate = (self.settings.get("reels_animation", True)
                   and not self.settings.get("eco_mode", False))
        self.reels.tick(animate)
        self.root.after(500, self._tick_ui)

    def _update_time_label(self):
        pos = self.player.current_pos()
        dur = self.player.duration_s
        self.time_lbl.config(text=f"{fmt_time(pos)} / {fmt_time(dur)}")

    def _start_clock(self):
        def tick():
            now = datetime.now()
            self.clock_lbl.config(text=now.strftime("%H:%M"))
            self._clock_job = self.root.after(15000, tick)
        tick()

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
        mode = self.settings.get("repeat_mode", "off")
        if mode == "one":
            self.load_track(self.player.track_path)
            return
        nxt = self._pick_next_track()
        if nxt:
            self._smart_history.append(nxt)
            self.load_track(nxt)
        else:
            self.stop_track()

    # -- settings ---------------------------------------------------------
    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title(t("s_title"))
        win.configure(bg=C["bg_body"])
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text=t("s_title"), bg=C["bg_body"],
                 fg=C["accent"], font=C["font_title"]).pack(pady=(14, 10))

        body = tk.Frame(win, bg=C["bg_body"])
        body.pack(fill="both", expand=True, padx=16, pady=4)

        def add_section(title_key):
            tk.Label(body, text=t(title_key), bg=C["bg_body"], fg=C["accent"],
                     font=C["font_small"], anchor="w").pack(fill="x", pady=(10, 2))
            tk.Frame(body, bg=C["frame"], height=1).pack(fill="x", pady=(0, 6))

        def add_check(label_key, key, cmd=None):
            var = tk.BooleanVar(value=bool(self.settings.get(key, False)))
            def _on():
                self.settings[key] = var.get()
                save_json(SETTINGS_FILE, self.settings)
                if cmd:
                    cmd()
            tk.Checkbutton(body, text=t(label_key), variable=var, command=_on,
                           bg=C["bg_body"], fg=C["fg_soft"],
                           activebackground=C["bg_body"],
                           activeforeground=C["accent"],
                           selectcolor=C["bg_trough"],
                           font=C["font_small"], anchor="w",
                           highlightthickness=0, bd=0).pack(fill="x")

        add_section("s_sound")
        add_check("s_fadein",  "fade_in")
        add_check("s_fadeout", "fade_out")
        add_check("s_fadebet", "fade_between")
        add_check("s_gapless", "gapless")

        add_section("s_repeat")
        repeat_var = tk.StringVar(value=self.settings.get("repeat_mode", "off"))
        rrow = tk.Frame(body, bg=C["bg_body"])
        rrow.pack(fill="x")
        tk.Label(rrow, text=t("s_repeat_l"), bg=C["bg_body"], fg=C["fg_soft"],
                 font=C["font_small"], width=12, anchor="w").pack(side="left")
        for val in ("off", "one", "all"):
            tk.Radiobutton(rrow, text=val.upper(), value=val, variable=repeat_var,
                           command=lambda: self._set_setting("repeat_mode", repeat_var.get()),
                           bg=C["bg_body"], fg=C["fg_soft"],
                           activebackground=C["bg_body"],
                           selectcolor=C["bg_trough"],
                           font=C["font_small"],
                           highlightthickness=0, bd=0).pack(side="left", padx=4)

        shuffle_var = tk.StringVar(value=self.settings.get("shuffle_mode", "off"))
        srow = tk.Frame(body, bg=C["bg_body"])
        srow.pack(fill="x", pady=(4, 0))
        tk.Label(srow, text=t("s_shuffle_l"), bg=C["bg_body"], fg=C["fg_soft"],
                 font=C["font_small"], width=12, anchor="w").pack(side="left")
        for val in ("off", "on", "smart"):
            tk.Radiobutton(srow, text=val.upper(), value=val, variable=shuffle_var,
                           command=lambda: self._set_setting("shuffle_mode", shuffle_var.get()),
                           bg=C["bg_body"], fg=C["fg_soft"],
                           activebackground=C["bg_body"],
                           selectcolor=C["bg_trough"],
                           font=C["font_small"],
                           highlightthickness=0, bd=0).pack(side="left", padx=4)

        add_section("s_visual")
        add_check("s_clock",   "clock_on",  cmd=self._apply_clock_visibility)
        add_check("s_reels",   "reels_animation")
        add_check("s_ticker",  "ticker_on", cmd=self._apply_ticker_visibility)
        add_check("s_scan",    "crt_scanlines")
        add_check("s_flicker", "crt_flicker")

        add_section("s_perf")
        add_check("s_eco",     "eco_mode", cmd=self._apply_eco)
        add_check("s_lowq",    "low_quality_render")
        add_check("s_statscr", "static_scrubber")
        add_check("s_led",     "led_enabled", cmd=self._apply_led)
        add_check("s_winanim", "window_animation")

        add_section("s_theme")
        theme_var = tk.StringVar(value=self.settings.get("theme", "retro"))
        trow = tk.Frame(body, bg=C["bg_body"])
        trow.pack(fill="x")
        for key, th in THEMES.items():
            tk.Radiobutton(trow, text=th["label"], value=key, variable=theme_var,
                           command=lambda: self.change_theme(theme_var.get()),
                           bg=C["bg_body"], fg=C["fg_soft"],
                           activebackground=C["bg_body"],
                           selectcolor=C["bg_trough"],
                           font=C["font_small"],
                           highlightthickness=0, bd=0).pack(side="left", padx=2)

        add_section("s_lang")
        lang_var = tk.StringVar(value=self.settings.get("language", "en"))
        lrow = tk.Frame(body, bg=C["bg_body"])
        lrow.pack(fill="x")
        for code in ("en", "ua", "su"):
            tk.Radiobutton(lrow, text=lang_display_name(code),
                           value=code, variable=lang_var,
                           command=lambda: self._set_lang(lang_var.get()),
                           bg=C["bg_body"], fg=C["fg_soft"],
                           activebackground=C["bg_body"],
                           selectcolor=C["bg_trough"],
                           font=C["font_small"],
                           highlightthickness=0, bd=0).pack(side="left", padx=4)

        RoundedButton(win, text=t("s_close"), command=win.destroy,
                      width=120, height=38,
                      radius=C["btn_radius"]).pack(pady=16)

    def _set_setting(self, key, val):
        self.settings[key] = val
        save_json(SETTINGS_FILE, self.settings)

    def _set_lang(self, code):
        self.settings["language"] = code
        save_json(SETTINGS_FILE, self.settings)
        set_lang(code)
        self._retranslate_ui()

    def _retranslate_ui(self):
        self.btn_open.set_text(t("open"))
        if self.player.state == "PLAYING":
            self.btn_play.set_text(t("playing"))
        elif self.player.state == "PAUSED":
            self.btn_play.set_text(t("resume"))
        else:
            self.btn_play.set_text(t("play"))
        self.btn_pause.set_text(t("pause"))
        self.btn_stop.set_text(t("stop"))
        self.btn_playlist.set_text(t("playlist"))
        self.btn_fav.set_text(t("fav"))
        self.btn_next.set_text(t("next"))
        self.btn_prev.set_text(t("prev"))
        self.vol_knob.label = t("volume")
        self.vol_knob._draw()
        self.speed_knob.label = t("speed")
        self.speed_knob._draw()
        self._soon_lbl.config(text=t("coming_soon"))
        if self.player.state == "STOPPED":
            self.status.config(text=t("stopped"))
        elif self.player.state == "PLAYING":
            self.status.config(text=t("playing"))
        elif self.player.state == "PAUSED":
            self.status.config(text=t("paused"))
        self._scrub_lbl.config(text=t("tape"))
        if not self.player.track_path:
            self.display.config(text=t("no_track"))
        self._build_menu()
        self._update_fav_indicator()

    def _apply_clock_visibility(self):
        if self.settings.get("clock_on", True):
            self.clock_lbl.pack(side="right")
        else:
            self.clock_lbl.pack_forget()

    def _apply_ticker_visibility(self):
        if not self.settings.get("ticker_on", True) or self.settings.get("eco_mode", False):
            self._stop_ticker()
            if hasattr(self, "_full_name") and self._full_name:
                self.display.config(text=self._full_name[:30])

    def _apply_eco(self):
        if self.settings.get("eco_mode", False):
            self.settings["reels_animation"] = False
            self.settings["crt_scanlines"] = False
            self.settings["crt_flicker"] = False
            self.settings["window_animation"] = False
            self._stop_ticker()
            self.reels.set_playing(False)
        save_json(SETTINGS_FILE, self.settings)

    def _apply_led(self):
        if self.settings.get("led_enabled", True):
            self.led_play.pack(pady=3)
            self.led_pause.pack(pady=3)
        else:
            self.led_play.pack_forget()
            self.led_pause.pack_forget()

    def show_about(self):
        messagebox.showinfo(t("d_about"),
                            f"SCARLI-MUSIC v{APP_VERSION}\n\n{t('d_abouttxt')}")

    def on_closing(self):
        self._cancel_fade()
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