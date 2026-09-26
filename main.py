"""
SCARLI-MUSIC v0.3
Modern audio player.
Python 3.14+  /  pygame-ce
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import math
import random
import time
from datetime import datetime
from collections import deque

from lang import t, set_lang, LANG, lang_display_name, all_langs, faq_translated
from player import Player
from metadata import read_tags, write_tags, fmt_duration
from themes import THEMES
import sounds as sound_engine
import stats

APP_VERSION = "0.3"
APP_TITLE = "SCARLI-MUSIC"
SETTINGS_FILE = "settings.json"
PLAYLIST_FILE = "playlist.json"
RECENT_FILE = "recent.json"

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DND_OK = True
except Exception:
    DND_OK = False


DEFAULT_SETTINGS = {
    "volume": 0.5, "last_folder": "", "theme": "purple", "language": "en",
    "repeat_mode": "off", "shuffle_mode": "off", "shuffle_history": 5,
    "clock_on": True,
    "eco_mode": False, "ticker_on": True,
    "static_scrubber": False,
    "window_animation": True,
    "tooltips": True, "mini_mode": False,
    "stats_enabled": True,
}

DEFAULT_PLAYLIST = {"tracks": [], "favorites": []}
DEFAULT_RECENT = {"recent": []}

C = dict(THEMES["purple"])


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


def load_settings(): return load_json(SETTINGS_FILE, DEFAULT_SETTINGS)


def load_playlist():
    p = load_json(PLAYLIST_FILE, DEFAULT_PLAYLIST)
    p["tracks"] = [tt for tt in p.get("tracks", []) if os.path.exists(tt)]
    p["favorites"] = [tt for tt in p.get("favorites", []) if os.path.exists(tt)]
    return p


def load_recent(): return load_json(RECENT_FILE, DEFAULT_RECENT)
def save_playlist(p): save_json(PLAYLIST_FILE, p)
def save_recent(r): save_json(RECENT_FILE, r)


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return f"#{max(0,min(255,int(r))):02x}{max(0,min(255,int(g))):02x}{max(0,min(255,int(b))):02x}"


def lerp_color(c1, c2, t_):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex(r1 + (r2 - r1) * t_, g1 + (g2 - g1) * t_, b1 + (b2 - b1) * t_)


# ---------------------------------------------------------------------------
#  TOOLTIP
# ---------------------------------------------------------------------------
class Tooltip:
    def __init__(self, widget, text, delay=600):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip_window = None
        self._enter_id = None
        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")

    def _schedule(self, _e=None):
        self._cancel()
        self._enter_id = self.widget.after(self.delay, self._show)

    def _show(self):
        if self.tip_window: return
        try:
            x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 8
            self.tip_window = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            tk.Label(tw, text=self.text, justify="left",
                     bg=C["bg_panel"], fg=C["fg_soft"],
                     font=("Segoe UI", 9), relief="flat",
                     padx=10, pady=6).pack()
        except Exception:
            pass

    def _hide(self, _e=None):
        self._cancel()
        if self.tip_window:
            try: self.tip_window.destroy()
            except Exception: pass
            self.tip_window = None

    def _cancel(self):
        if self._enter_id:
            try: self.widget.after_cancel(self._enter_id)
            except Exception: pass
            self._enter_id = None

    def update_text(self, text):
        self.text = text


# ---------------------------------------------------------------------------
#  ROUNDED BUTTON
# ---------------------------------------------------------------------------
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text="", command=None, width=100, height=46,
                 radius=14, font=None, tooltip=None, accent=False, **kw):
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
        self._accent = accent
        self.tooltip = None
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Configure>", lambda e: self.redraw())
        self.redraw()
        if tooltip:
            self.tooltip = Tooltip(self, tooltip)

    def set_tooltip(self, text):
        if self.tooltip: self.tooltip.update_text(text)
        else: self.tooltip = Tooltip(self, text)

    def retheme(self):
        try: self.config(bg=self.master["bg"])
        except Exception: self.config(bg=C["bg_body"])
        self.redraw()

    def set_text(self, text):
        self.text = text
        self.redraw()

    def set_state(self, state):
        self._state = state
        self.redraw()

    def _on_enter(self, _e):
        if self._state == "disabled": return
        self._hover = True; self.redraw()
    def _on_leave(self, _e):
        self._hover = False; self._pressed = False; self.redraw()
    def _on_press(self, _e):
        if self._state == "disabled": return
        self._pressed = True; self.redraw()
    def _on_release(self, _e):
        if self._state == "disabled": return
        if self._pressed:
            self._pressed = False; self.redraw()
            try: sound_engine.play("click")
            except Exception: pass
            if self.command: self.command()

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

    def redraw(self):
        self.delete("all")
        w, h = self._btn_w, self._btn_h
        r = self.radius
        if self._state == "disabled":
            bg = C["bg_panel"]; fg = C["fg_dim"]; outline = C["frame"]
        elif self._pressed:
            bg = lerp_color(C["accent_dim"], "#000000", 0.20) if self._accent else \
                 lerp_color(C["btn_active"], "#000000", 0.20)
            fg = "#ffffff" if self._accent else C["btn_fg"]
            outline = C["accent_dim"] if self._accent else C["btn_outline"]
        elif self._hover:
            bg = C["accent_hover"] if self._accent else C["btn_active"]
            fg = "#ffffff" if self._accent else C["fg_main"]
            outline = C["accent_hover"] if self._accent else C["accent_dim"]
        else:
            bg = C["accent"] if self._accent else C["btn_bg"]
            fg = "#ffffff" if self._accent else C["btn_fg"]
            outline = C["accent"] if self._accent else C["btn_outline"]
        self._rounded_rect(0, 0, w - 1, h - 1, r, fill=bg, outline=outline, width=1)
        f = self._font or C["font_btn"]
        self.create_text(w / 2, h / 2, text=self.text, fill=fg, font=f)


# ---------------------------------------------------------------------------
#  KNOB
# ---------------------------------------------------------------------------
class Knob(tk.Canvas):
    def __init__(self, parent, label="", size=88, callback=None, value=0.5,
                 tooltip=None):
        super().__init__(parent, width=size, height=size + 22,
                         bg=parent["bg"], highlightthickness=0, bd=0)
        self.size = size; self.value = value; self.callback = callback
        self.label = label
        self._drag_start_y = None; self._drag_start_val = 0.0
        self.bind("<Button-1>", self._on_press)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<MouseWheel>", self._on_wheel)
        self._draw()
        if tooltip: self.tooltip = Tooltip(self, tooltip)

    def retheme(self):
        self.config(bg=self.master["bg"] if self.master else C["bg_body"])
        self._draw()

    def _draw(self):
        self.delete("all")
        s = self.size; cx, cy = s / 2, s / 2; r = s / 2 - 8
        self.create_oval(cx - r, cy - r, cx + r, cy + r,
                         fill=C["knob_bg"], outline=C["knob_edge"], width=2)
        start_angle = 90 + 135
        extent = -self.value * 270
        self.create_arc(cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6,
                        start=start_angle, extent=extent,
                        style="arc", outline=C["accent"], width=4)
        ir = r - 16
        self.create_oval(cx - ir, cy - ir, cx + ir, cy + ir,
                         fill=C["knob_bg"], outline="")
        ang = math.radians(-135 + self.value * 270)
        x1 = cx + math.sin(ang) * (ir - 6)
        y1 = cy - math.cos(ang) * (ir - 6)
        self.create_line(cx, cy, x1, y1, fill=C["accent"], width=3,
                         capstyle="round")
        self.create_oval(x1 - 4, y1 - 4, x1 + 4, y1 + 4,
                         fill=C["accent"], outline="")
        self.create_text(cx, s + 10, text=self.label,
                         fill=C["fg_dim"], font=("Segoe UI", 8, "bold"))

    def _on_press(self, e):
        self._drag_start_y = e.y_root; self._drag_start_val = self.value
    def _on_drag(self, e):
        if self._drag_start_y is None: return
        dy = self._drag_start_y - e.y_root
        delta = dy / 150.0
        v = max(0.0, min(1.0, self._drag_start_val + delta))
        if abs(v - self.value) > 1e-6:
            self.value = v; self._draw()
            if self.callback: self.callback(self.value)
    def _on_release(self, _e): self._drag_start_y = None
    def _on_wheel(self, e):
        step = 0.03 if e.delta > 0 else -0.03
        v = max(0.0, min(1.0, self.value + step))
        if abs(v - self.value) > 1e-6:
            self.value = v; self._draw()
            if self.callback: self.callback(self.value)
    def set(self, v):
        self.value = max(0.0, min(1.0, v)); self._draw()


# ---------------------------------------------------------------------------
#  SCRUBBER
# ---------------------------------------------------------------------------
class Scrubber(tk.Canvas):
    def __init__(self, parent, height=40, callback=None):
        super().__init__(parent, height=height, bg=C["bg_panel"],
                         highlightthickness=0, bd=0)
        self.callback = callback
        self.duration = 0.0
        self.position = 0.0
        self._dragging = False
        self._hover = False
        self.bind("<Configure>", lambda e: self._redraw())
        self.bind("<Button-1>", self._on_press)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", lambda e: self._set_hover(True))
        self.bind("<Leave>", lambda e: self._set_hover(False))
    def _set_hover(self, v):
        self._hover = v; self._redraw()
    def set_duration(self, d): self.duration = max(0.0, d); self._redraw()
    def set_position(self, p):
        if self._dragging: return
        self.position = max(0.0, p); self._redraw()
    def retheme(self): self.config(bg=C["bg_panel"]); self._redraw()
    def _on_press(self, e): self._dragging = True; self._seek_from_x(e.x)
    def _on_drag(self, e):
        if self._dragging: self._seek_from_x(e.x)
    def _on_release(self, _e): self._dragging = False
    def _seek_from_x(self, x):
        w = self.winfo_width()
        if w <= 2 or self.duration <= 0: return
        pad = 10
        x = max(pad, min(w - pad, x))
        ratio = (x - pad) / max(1, w - 2 * pad)
        target = ratio * self.duration
        self.position = target; self._redraw()
        if self.callback: self.callback(target)
    def _redraw(self):
        self.delete("all")
        w = self.winfo_width(); h = self.winfo_height()
        if w < 4 or h < 4: return
        pad = 10
        bar_h = 6 if self._hover or self._dragging else 4
        bar_y = h // 2 - bar_h // 2
        self.create_rectangle(pad, bar_y, w - pad, bar_y + bar_h,
                              fill=C["bg_trough"], outline="")
        if self.duration > 0:
            ratio = max(0.0, min(1.0, self.position / self.duration))
        else:
            ratio = 0.0
        head_x = pad + int(ratio * (w - 2 * pad))
        self.create_rectangle(pad, bar_y, head_x, bar_y + bar_h,
                              fill=C["accent"], outline="")
        if self._hover or self._dragging:
            r = 8
            self.create_oval(head_x - r, h // 2 - r,
                             head_x + r, h // 2 + r,
                             fill=C["accent"], outline=C["bg_panel"], width=2)


# ---------------------------------------------------------------------------
#  MINI PLAYER
# ---------------------------------------------------------------------------
class MiniPlayer(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        self.title("SCARLI-MUSIC MINI")
        self.configure(bg=C["bg_body"])
        self.resizable(False, False)
        self.geometry("420x160")
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self._restore)
        self._build()
        self._tick()
        try:
            self.lift(); self.focus_force()
        except Exception:
            pass

    def _build(self):
        top = tk.Frame(self, bg=C["bg_body"])
        top.pack(fill="x", padx=16, pady=(14, 6))
        self.title_lbl = tk.Label(top, text="—", bg=C["bg_body"],
                                  fg=C["fg_soft"], font=("Segoe UI", 11, "bold"),
                                  anchor="w")
        self.title_lbl.pack(side="left", fill="x", expand=True)
        self.time_lbl = tk.Label(top, text="--:-- / --:--", bg=C["bg_body"],
                                 fg=C["fg_dim"], font=("Segoe UI", 9))
        self.time_lbl.pack(side="right")

        self.progress = tk.Canvas(self, height=6, bg=C["bg_trough"],
                                  highlightthickness=0, bd=0)
        self.progress.pack(fill="x", padx=16, pady=(0, 12))
        self.progress.bind("<Configure>", lambda e: self._draw_progress())

        ctl = tk.Frame(self, bg=C["bg_body"])
        ctl.pack(pady=(0, 14))
        RoundedButton(ctl, text="⏮", command=self.app.play_prev,
                      width=56, height=38, radius=12,
                      font=("Segoe UI", 14)).pack(side="left", padx=3)
        self.btn_play = RoundedButton(ctl, text="▶", command=self.app._toggle_play,
                                       width=56, height=38, radius=12,
                                       font=("Segoe UI", 14), accent=True)
        self.btn_play.pack(side="left", padx=3)
        RoundedButton(ctl, text="⏭", command=self.app.play_next,
                      width=56, height=38, radius=12,
                      font=("Segoe UI", 14)).pack(side="left", padx=3)
        RoundedButton(ctl, text="✕", command=self._restore,
                      width=46, height=38, radius=12,
                      font=("Segoe UI", 12)).pack(side="left", padx=10)

    def _draw_progress(self):
        self.progress.delete("all")
        w = self.progress.winfo_width()
        h = self.progress.winfo_height()
        if w < 4 or h < 4: return
        self.progress.create_rectangle(0, 0, w, h, fill=C["bg_trough"], outline="")
        p = self.app.player
        if p.duration_s > 0:
            ratio = max(0.0, min(1.0, p.current_pos() / p.duration_s))
            self.progress.create_rectangle(0, 0, int(w * ratio), h,
                                           fill=C["accent"], outline="")

    def _tick(self):
        if not self.winfo_exists(): return
        p = self.app.player
        if hasattr(self.app, "_full_name"):
            self.title_lbl.config(text=self.app._full_name[:50])
        pos = p.current_pos(); dur = p.duration_s
        self.time_lbl.config(text=f"{fmt_time(pos)} / {fmt_time(dur)}")
        self.btn_play.set_text("❚❚" if p.state == "PLAYING" else "▶")
        self._draw_progress()
        self.after(500, self._tick)

    def _restore(self):
        try: self.destroy()
        except Exception: pass
        try:
            self.app.root.deiconify()
            self.app.root.lift()
        except Exception: pass
        self.app.settings["mini_mode"] = False
        save_json(SETTINGS_FILE, self.app.settings)
        self.app._mini_win = None


# ---------------------------------------------------------------------------
#  TAG EDITOR
# ---------------------------------------------------------------------------
class TagEditor(tk.Toplevel):
    def __init__(self, app, path):
        super().__init__(app.root)
        self.app = app
        self.path = path
        self.title(t("d_tags_title"))
        self.configure(bg=C["bg_body"])
        self.transient(app.root)
        self.grab_set()
        self.resizable(False, False)
        self._tags = read_tags(path)
        self._build()

    def _build(self):
        tk.Label(self, text=t("d_tags_title"), bg=C["bg_body"], fg=C["accent"],
                 font=("Segoe UI", 14, "bold")).pack(pady=(20, 8))
        tk.Label(self, text=os.path.basename(self.path), bg=C["bg_body"],
                 fg=C["fg_dim"], font=("Segoe UI", 9),
                 wraplength=440).pack(pady=(0, 14))
        form = tk.Frame(self, bg=C["bg_body"])
        form.pack(padx=24, pady=4, fill="x")

        def add_field(label_key, key):
            row = tk.Frame(form, bg=C["bg_body"])
            row.pack(fill="x", pady=5)
            tk.Label(row, text=t(label_key), bg=C["bg_body"], fg=C["fg_soft"],
                     font=("Segoe UI", 10), width=14, anchor="w").pack(side="left")
            var = tk.StringVar(value=str(self._tags.get(key, "") or ""))
            tk.Entry(row, textvariable=var, bg=C["btn_bg"], fg=C["fg_main"],
                     insertbackground=C["fg_main"], font=("Segoe UI", 10),
                     bd=0, relief="flat").pack(side="left", fill="x", expand=True,
                                                ipady=6, padx=(8, 0))
            return var

        v_artist = add_field("d_tags_artist", "artist")
        v_title = add_field("d_tags_title_f", "title")
        v_album = add_field("d_tags_album", "album")
        v_year = add_field("d_tags_year", "year")
        v_genre = add_field("d_tags_genre", "genre")

        btn_row = tk.Frame(self, bg=C["bg_body"])
        btn_row.pack(pady=20)

        def save():
            ok = write_tags(self.path, {
                "artist": v_artist.get().strip(), "title": v_title.get().strip(),
                "album": v_album.get().strip(), "year": v_year.get().strip(),
                "genre": v_genre.get().strip(),
            })
            if ok:
                if self.app._playlist_win is not None and self.app._playlist_win.winfo_exists():
                    self.app._playlist_win.refresh()
                if self.app.player.track_path == self.path:
                    self.app._refresh_now_playing_meta()
                self.destroy()
            else:
                messagebox.showerror(t("d_error"), "Failed to save tags")

        RoundedButton(btn_row, text=t("d_tags_save"), command=save,
                      width=120, height=40, radius=12, accent=True).pack(side="left", padx=6)
        RoundedButton(btn_row, text=t("d_tags_cancel"), command=self.destroy,
                      width=120, height=40, radius=12).pack(side="left", padx=6)


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
        self.geometry("720x600")
        self._sort_mode = "index"
        self._tab = "all"
        self._build()
        self.refresh()

    def _btn(self, parent, text, cmd, w=90, h=32):
        return RoundedButton(parent, text=text, command=cmd,
                             width=w, height=h, radius=C["btn_radius"])

    def _build(self):
        top = tk.Frame(self, bg=C["bg_body"])
        top.pack(fill="x", padx=16, pady=(16, 0))
        tk.Label(top, text=t("p_title"), bg=C["bg_body"], fg=C["accent"],
                 font=("Segoe UI", 16, "bold")).pack(side="left")
        self._btn(top, t("p_add"), self._add_files, w=88).pack(side="right", padx=3)
        self._btn(top, t("p_close"), self.destroy, w=88).pack(side="right", padx=3)

        tabs = tk.Frame(self, bg=C["bg_body"])
        tabs.pack(fill="x", padx=16, pady=(12, 0))
        for key, label in (("all", t("p_tab_all")),
                           ("fav", t("p_tab_fav")),
                           ("recent", t("p_tab_recent"))):
            self._btn(tabs, label, lambda k=key: self._set_tab(k),
                      w=120, h=32).pack(side="left", padx=3)

        sr = tk.Frame(self, bg=C["bg_body"])
        sr.pack(fill="x", padx=16, pady=(12, 0))
        tk.Label(sr, text=t("p_search"), bg=C["bg_body"], fg=C["fg_soft"],
                 font=("Segoe UI", 10)).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh())
        tk.Entry(sr, textvariable=self.search_var, bg=C["btn_bg"], fg=C["fg_main"],
                 insertbackground=C["fg_main"], font=("Segoe UI", 10),
                 bd=0, relief="flat").pack(side="left", fill="x", expand=True,
                                            padx=10, ipady=6)

        srt = tk.Frame(self, bg=C["bg_body"])
        srt.pack(fill="x", padx=16, pady=(8, 0))
        tk.Label(srt, text=t("p_sort"), bg=C["bg_body"], fg=C["fg_soft"],
                 font=("Segoe UI", 10)).pack(side="left")
        for label, mode in (("IDX", "index"), ("NAME", "name"),
                            ("DUR", "duration"), ("DATE", "date")):
            self._btn(srt, label, lambda m=mode: self._set_sort(m),
                      w=56, h=28).pack(side="left", padx=3)

        lw = tk.Frame(self, bg=C["frame"], bd=1)
        lw.pack(fill="both", expand=True, padx=16, pady=14)
        inner = tk.Frame(lw, bg=C["list_bg"])
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        self.listbox = tk.Listbox(inner, bg=C["list_bg"], fg=C["fg_main"],
                                  selectbackground=C["list_sel"],
                                  selectforeground=C["fg_main"],
                                  font=("Segoe UI", 10),
                                  bd=0, highlightthickness=0,
                                  activestyle="none")
        self.listbox.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        sb = tk.Scrollbar(inner, command=self.listbox.yview, bg=C["btn_bg"],
                          troughcolor=C["bg_trough"], activebackground=C["btn_active"],
                          bd=0, highlightthickness=0)
        sb.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=sb.set)
        self.listbox.bind("<Double-Button-1>", self._on_double)
        self.listbox.bind("<Button-3>", self._on_right_click)
        self.listbox.bind("<Button-2>", self._on_right_click)

        bot = tk.Frame(self, bg=C["bg_body"])
        bot.pack(fill="x", padx=16, pady=(0, 16))
        for key, cmd in (("p_fav", self._toggle_fav), ("p_remove", self._remove),
                         ("p_clear", self._clear)):
            self._btn(bot, t(key), cmd).pack(side="left", padx=3)
        for key, cmd in (("p_export", self._export_m3u), ("p_import", self._import_m3u)):
            self._btn(bot, t(key), cmd, w=110).pack(side="right", padx=3)

    def _set_tab(self, tab):
        self._tab = tab; self.refresh()

    def _set_sort(self, mode):
        self._sort_mode = mode; self.refresh()

    def _get_source_list(self):
        if self._tab == "fav": return list(self.app.playlist["favorites"])
        if self._tab == "recent": return list(self.app.recent.get("recent", []))
        return list(self.app.playlist["tracks"])

    def _get_sorted_tracks(self):
        tracks = self._get_source_list()
        if self._sort_mode == "name":
            tracks.sort(key=lambda p: os.path.basename(p).lower())
        elif self._sort_mode == "duration":
            tracks.sort(key=lambda p: read_tags(p).get("duration", 0.0))
        elif self._sort_mode == "date":
            tracks.sort(key=lambda p: os.path.getmtime(p) if os.path.exists(p) else 0)
        return tracks

    def refresh(self):
        self.listbox.delete(0, tk.END)
        query = (self.search_var.get() or "").lower().strip()
        self._visible = []
        for i, tt in enumerate(self._get_sorted_tracks()):
            tags = read_tags(tt)
            name = os.path.basename(tt)
            artist = tags.get("artist", ""); title = tags.get("title", "")
            display = f"{artist} — {title}" if (artist and title) else name
            if query and query not in display.lower(): continue
            dur_str = fmt_duration(tags.get("duration", 0.0))
            fav = tt in self.app.playlist["favorites"]
            mark = "★" if fav else " "
            self._visible.append(tt)
            self.listbox.insert(tk.END, f"{mark}  {i+1:02d}.  [{dur_str}]  {display}")
            if fav:
                self.listbox.itemconfig(tk.END, fg=C["list_fav"])

    def _add_files(self):
        paths = filedialog.askopenfilenames(
            title=t("m_open"),
            initialdir=self.app.settings.get("last_folder", "") or os.path.expanduser("~"),
            filetypes=[("Audio", "*.mp3 *.wav *.ogg *.flac *.m4a *.aac *.wma"),
                       ("All files", "*.*")])
        if not paths: return
        for p in paths:
            if p not in self.app.playlist["tracks"]:
                self.app.playlist["tracks"].append(p)
        if paths:
            self.app.settings["last_folder"] = os.path.dirname(paths[0])
        self.app.save_playlist(); self.refresh()

    def _on_double(self, _e):
        sel = self.listbox.curselection()
        if not sel: return
        self.app.load_track(self._visible[sel[0]])

    def _on_right_click(self, e):
        idx = self.listbox.nearest(e.y)
        if idx < 0 or idx >= len(self._visible): return
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(idx)
        path = self._visible[idx]
        menu = tk.Menu(self, tearoff=0, bg=C["btn_bg"], fg=C["fg_main"],
                       activebackground=C["accent"], activeforeground="#fff")
        menu.add_command(label=t("p_edit_tags"),
                         command=lambda p=path: TagEditor(self.app, p))
        menu.add_command(label=t("p_fav"), command=self._toggle_fav)
        menu.add_separator()
        menu.add_command(label=t("p_remove"), command=self._remove)
        try: menu.tk_popup(e.x_root, e.y_root)
        finally: menu.grab_release()

    def _toggle_fav(self):
        sel = self.listbox.curselection()
        if not sel: return
        path = self._visible[sel[0]]
        if path in self.app.playlist["favorites"]:
            self.app.playlist["favorites"].remove(path)
        else:
            self.app.playlist["favorites"].append(path)
        self.app.save_playlist(); self.refresh()
        try: self.listbox.selection_set(sel[0])
        except Exception: pass

    def _remove(self):
        sel = self.listbox.curselection()
        if not sel: return
        path = self._visible[sel[0]]
        if path in self.app.playlist["tracks"]: self.app.playlist["tracks"].remove(path)
        if path in self.app.playlist["favorites"]: self.app.playlist["favorites"].remove(path)
        self.app.save_playlist(); self.refresh()

    def _clear(self):
        if not messagebox.askyesno(t("p_clear"), t("d_clearq")): return
        if self._tab == "fav": self.app.playlist["favorites"] = []
        elif self._tab == "recent":
            self.app.recent["recent"] = []; save_recent(self.app.recent)
        else:
            self.app.playlist["tracks"] = []; self.app.playlist["favorites"] = []
        self.app.save_playlist(); self.refresh()

    def _export_m3u(self):
        path = filedialog.asksaveasfilename(title=t("d_exp"), defaultextension=".m3u",
                                            filetypes=[("M3U", "*.m3u"), ("All files", "*.*")])
        if not path: return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                for tt in self.app.playlist["tracks"]: f.write(tt + "\n")
            messagebox.showinfo(t("d_exp"), t("d_saved") + path)
        except Exception as e:
            messagebox.showerror(t("d_error"), str(e))

    def _import_m3u(self):
        path = filedialog.askopenfilename(title=t("d_imp"),
                                          filetypes=[("M3U", "*.m3u"), ("All files", "*.*")])
        if not path: return
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"): continue
                    if os.path.exists(line) and line not in self.app.playlist["tracks"]:
                        self.app.playlist["tracks"].append(line)
            self.app.save_playlist(); self.refresh()
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
        self.recent = load_recent()

        self.player = Player()

        self._end_check_id = None
        self._playlist_win = None
        self._mini_win = None
        self._ticker_job = None
        self._ticker_pos = 0
        self._clock_job = None
        self._smart_history = deque(maxlen=self.settings.get("shuffle_history", 5))
        self._all_buttons = []
        self._full_name = ""

        try:
            sound_engine.init()
            sound_engine.set_enabled(True)
        except Exception as e:
            print("sounds init failed:", e)

        self._session_started_at = time.time() if self.settings.get("stats_enabled", True) else None
        if self._session_started_at is not None:
            try: stats.session_start()
            except Exception as e: print("stats start error:", e)

        self._apply_theme_palette()
        self._setup_window()
        self._build_ui()
        self._bind_hotkeys()
        self._apply_settings_on_start()
        self._start_clock()
        self._tick_ui()

        if DND_OK:
            try:
                self.root.drop_target_register(DND_FILES)
                self.root.dnd_bind("<<Drop>>", self._on_drop)
            except Exception as e:
                print("DnD register error:", e)

        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        if self.settings.get("window_animation", True) \
                and not self.settings.get("eco_mode", False):
            self._animate_window_open()

    def _apply_theme_palette(self):
        global C
        key = self.settings.get("theme", "purple")
        if key not in THEMES: key = "purple"
        C.clear(); C.update(THEMES[key])

    def _setup_window(self):
        self.root.title(f"{APP_TITLE}  v{APP_VERSION}")
        self.root.configure(bg=C["bg_body"])
        self.root.resizable(False, False)
        w, h = 700, 660
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth(); sh = self.root.winfo_screenheight()
        x = (sw - w) // 2; y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _animate_window_open(self):
        try: self.root.attributes("-alpha", 0.0)
        except Exception: return
        total_ms = 300; steps = 15; dt = total_ms // steps
        def step(i=0):
            a = min(1.0, i / steps)
            try: self.root.attributes("-alpha", a)
            except Exception: return
            if i < steps: self.root.after(dt, step, i + 1)
        step()

    def _build_ui(self):
        self._all_buttons = []
        self._body = tk.Frame(self.root, bg=C["bg_body"])
        self._body.pack(fill="both", expand=True, padx=22, pady=20)

        # HEADER
        self._header = tk.Frame(self._body, bg=C["bg_body"])
        self._header.pack(fill="x", pady=(0, 16))

        logo = tk.Canvas(self._header, width=36, height=36,
                         bg=C["bg_body"], highlightthickness=0, bd=0)
        logo.create_oval(0, 0, 36, 36, fill=C["accent"], outline="")
        logo.create_text(18, 19, text="♪", fill="#ffffff",
                         font=("Segoe UI", 18, "bold"))
        logo.pack(side="left", padx=(0, 12))

        title_box = tk.Frame(self._header, bg=C["bg_body"])
        title_box.pack(side="left")
        self._title_lbl = tk.Label(title_box, text=APP_TITLE,
                                   bg=C["bg_body"], fg=C["fg_soft"],
                                   font=("Segoe UI", 18, "bold"), anchor="w")
        self._title_lbl.pack(anchor="w")
        self._ver_lbl = tk.Label(title_box, text=f"version {APP_VERSION}",
                                 bg=C["bg_body"], fg=C["fg_dim"],
                                 font=("Segoe UI", 9), anchor="w")
        self._ver_lbl.pack(anchor="w")

        self.clock_lbl = tk.Label(self._header, text="00:00",
                                  bg=C["bg_body"], fg=C["fg_dim"],
                                  font=("Segoe UI", 12), anchor="e")
        self.clock_lbl.pack(side="right")

        # PLAYER PANEL
        self._center = tk.Frame(self._body, bg=C["bg_body"])
        self._center.pack(fill="x", pady=(0, 16))

        self._panel = tk.Frame(self._center, bg=C["bg_panel"], bd=0,
                               highlightthickness=1, highlightbackground=C["frame"])
        self._panel.pack(side="left", fill="both", expand=True)

        self._screen = tk.Frame(self._panel, bg=C["bg_screen"])
        self._screen.pack(fill="both", expand=True, padx=20, pady=20)

        self.display = tk.Label(self._screen, text=t("no_track"), bg=C["bg_screen"],
                                fg=C["fg_soft"], font=("Segoe UI", 15, "bold"),
                                anchor="w", justify="left")
        self.display.pack(fill="x")

        self.meta_lbl = tk.Label(self._screen, text="", bg=C["bg_screen"],
                                 fg=C["fg_dim"], font=("Segoe UI", 10), anchor="w")
        self.meta_lbl.pack(fill="x", pady=(4, 0))

        self.status = tk.Label(self._screen, text=t("stopped"), bg=C["bg_screen"],
                               fg=C["accent"], font=("Segoe UI", 9, "bold"), anchor="w")
        self.status.pack(fill="x", pady=(10, 0))

        self.time_lbl = tk.Label(self._screen, text="--:-- / --:--", bg=C["bg_screen"],
                                 fg=C["fg_soft"], font=("Segoe UI", 11), anchor="w")
        self.time_lbl.pack(fill="x", pady=(4, 0))

        self._knobs = tk.Frame(self._center, bg=C["bg_body"])
        self._knobs.pack(side="right", padx=(20, 0))
        self.vol_knob = Knob(self._knobs, label=t("volume").upper(), size=100,
                             value=self.settings["volume"], callback=self.change_volume,
                             tooltip=t("volume"))
        self.vol_knob.pack()

        self.vol_label = tk.Label(self._knobs, text=f"{int(self.settings['volume']*100)}%",
                                  bg=C["bg_body"], fg=C["fg_main"],
                                  font=("Segoe UI", 10, "bold"))
        self.vol_label.pack(pady=(6, 0))

        # SCRUBBER
        self._scrub_frame = tk.Frame(self._body, bg=C["bg_body"])
        self._scrub_frame.pack(fill="x", pady=(0, 4))
        self.fav_indicator = tk.Label(self._scrub_frame, text="", bg=C["bg_body"],
                                      fg=C["list_fav"], font=("Segoe UI", 9, "bold"))
        self.fav_indicator.pack(side="right")
        self.scrubber = Scrubber(self._scrub_frame, height=40, callback=self.on_scrub)
        self.scrubber.pack(fill="x")

        # MAIN TRANSPORT
        self._btn_frame = tk.Frame(self._body, bg=C["bg_body"])
        self._btn_frame.pack(pady=22)

        self.btn_prev = self._mk_btn(self._btn_frame, "prev", self.play_prev,
                                     w=52, h=52, tip="P", round_icon="⏮")
        self.btn_play = self._mk_btn(self._btn_frame, "play", self.play_track,
                                     w=64, h=64, tip="Space", accent=True,
                                     state="disabled", round_icon="▶")
        self.btn_next = self._mk_btn(self._btn_frame, "next", self.play_next,
                                     w=52, h=52, tip="N", round_icon="⏭")

        self.btn_prev.pack(side="left", padx=6)
        self.btn_play.pack(side="left", padx=6)
        self.btn_next.pack(side="left", padx=6)

        # SECONDARY ROW
        self._btn2_frame = tk.Frame(self._body, bg=C["bg_body"])
        self._btn2_frame.pack()

        self.btn_open = self._mk_btn(self._btn2_frame, "open", self.open_file,
                                     w=110, h=42, tip="O")
        self.btn_pause = self._mk_btn(self._btn2_frame, "pause", self.pause_track,
                                      w=110, h=42, tip="Space", state="disabled")
        self.btn_stop = self._mk_btn(self._btn2_frame, "stop", self.stop_track,
                                     w=110, h=42, tip="S", state="disabled")
        self.btn_playlist = self._mk_btn(self._btn2_frame, "playlist", self.toggle_playlist,
                                         w=110, h=42, tip="L")
        self.btn_fav = self._mk_btn(self._btn2_frame, "fav", self.toggle_favorite,
                                     w=110, h=42, tip="F")

        self.btn_open.pack(side="left", padx=4)
        self.btn_pause.pack(side="left", padx=4)
        self.btn_stop.pack(side="left", padx=4)
        self.btn_playlist.pack(side="left", padx=4)
        self.btn_fav.pack(side="left", padx=4)

        self._build_menu()

    def _mk_btn(self, parent, text_key, cmd, w=100, h=46, tip=None,
                state="normal", accent=False, round_icon=None):
        text = round_icon if round_icon else t(text_key).upper()
        f = ("Segoe UI", 18) if round_icon else None
        b = RoundedButton(parent, text=text, command=cmd,
                          width=w, height=h, radius=w // 2 if round_icon else 14,
                          font=f, tooltip=tip, accent=accent)
        if state == "disabled": b.set_state("disabled")
        self._all_buttons.append(b)
        return b

    def _build_menu(self):
        menubar = tk.Menu(self.root, bg=C["bg_panel"], fg=C["fg_soft"],
                          activebackground=C["accent"], activeforeground="#ffffff",
                          bd=0, font=("Segoe UI", 10))
        fm = tk.Menu(menubar, tearoff=0, bg=C["bg_panel"], fg=C["fg_soft"],
                     activebackground=C["accent"], activeforeground="#ffffff")
        fm.add_command(label=t("m_open"), command=self.open_file)
        fm.add_separator()
        fm.add_command(label=t("m_screenshot"), command=self.take_screenshot)
        fm.add_separator()
        fm.add_command(label=t("m_exit"), command=self.on_closing)
        menubar.add_cascade(label=t("m_file"), menu=fm)

        vm = tk.Menu(menubar, tearoff=0, bg=C["bg_panel"], fg=C["fg_soft"],
                     activebackground=C["accent"], activeforeground="#ffffff")
        vm.add_command(label=t("m_mini"), command=self.toggle_mini)
        menubar.add_cascade(label="View", menu=vm)

        pm = tk.Menu(menubar, tearoff=0, bg=C["bg_panel"], fg=C["fg_soft"],
                     activebackground=C["accent"], activeforeground="#ffffff")
        pm.add_command(label=t("m_show_pl"), command=self.toggle_playlist)
        pm.add_command(label=t("m_add_pl"), command=self.add_current_to_playlist)
        pm.add_separator()
        pm.add_command(label=t("m_next"), command=self.play_next)
        pm.add_command(label=t("m_prev"), command=self.play_prev)
        menubar.add_cascade(label=t("m_playlist"), menu=pm)

        sm = tk.Menu(menubar, tearoff=0, bg=C["bg_panel"], fg=C["fg_soft"],
                     activebackground=C["accent"], activeforeground="#ffffff")
        sm.add_command(label=t("m_settings_w"), command=self.open_settings)
        sm.add_separator()
        sm.add_command(label=t("m_about"), command=self.show_about)
        menubar.add_cascade(label=t("m_settings"), menu=sm)
        self.root.config(menu=menubar)

    def _bind_hotkeys(self):
        self.root.bind("<space>", lambda e: self._toggle_play())
        self.root.bind("<KeyPress-o>", lambda e: self.open_file())
        self.root.bind("<KeyPress-s>", lambda e: self.stop_track())
        self.root.bind("<KeyPress-l>", lambda e: self.toggle_playlist())
        self.root.bind("<KeyPress-f>", lambda e: self.toggle_favorite())
        self.root.bind("<KeyPress-n>", lambda e: self.play_next())
        self.root.bind("<KeyPress-p>", lambda e: self.play_prev())
        self.root.bind("<KeyPress-m>", lambda e: self.toggle_mini())
        self.root.bind("<F12>", lambda e: self.take_screenshot())
        self.root.bind("<Left>", lambda e: self._seek_by(-5))
        self.root.bind("<Right>", lambda e: self._seek_by(5))
        self.root.bind("<Shift-Left>", lambda e: self._seek_by(-30))
        self.root.bind("<Shift-Right>", lambda e: self._seek_by(30))
        self.root.bind("<Escape>", lambda e: self.on_closing())

    def _seek_by(self, sec): self.player.seek_to(self.player.current_pos() + sec)

    def change_volume(self, v):
        self.player.set_volume(v)
        self._update_volume_label(v)
        self.settings["volume"] = v

    def _update_volume_label(self, v):
        self.vol_label.config(text=f"{int(v*100)}%")

    def on_scrub(self, target): self.player.seek_to(target)

    def _apply_settings_on_start(self):
        self.player.set_volume(self.settings["volume"])
        self.vol_knob.set(self.settings["volume"])
        self._update_volume_label(self.settings["volume"])
        self._update_fav_indicator()
        if not self.settings.get("clock_on", True):
            self.clock_lbl.pack_forget()
        if not self.settings.get("ticker_on", True):
            self._stop_ticker()

    def _toggle_play(self):
        if self.player.state == "PLAYING": self.pause_track()
        elif self.player.track_path: self.play_track()

    def open_file(self):
        path = filedialog.askopenfilename(
            title=t("m_open"),
            initialdir=self.settings.get("last_folder", "") or os.path.expanduser("~"),
            filetypes=[("Audio", "*.mp3 *.wav *.ogg *.flac *.m4a *.aac *.wma"),
                       ("All files", "*.*")])
        if not path: return
        self.settings["last_folder"] = os.path.dirname(path)
        save_json(SETTINGS_FILE, self.settings)
        self.load_track(path)

    def _on_drop(self, event):
        try: data = self.root.tk.splitlist(event.data)
        except Exception: return
        added = []
        for p in data:
            p = p.strip("{}")
            if os.path.isdir(p):
                for f in os.listdir(p):
                    fp = os.path.join(p, f)
                    if os.path.isfile(fp) and f.lower().endswith(
                            (".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac", ".wma")):
                        if fp not in self.playlist["tracks"]:
                            self.playlist["tracks"].append(fp); added.append(fp)
            elif os.path.isfile(p):
                if p not in self.playlist["tracks"]:
                    self.playlist["tracks"].append(p); added.append(p)
        if added:
            self.save_playlist()
            if self._playlist_win is not None and self._playlist_win.winfo_exists():
                self._playlist_win.refresh()
            self.load_track(added[0])

    def _add_to_recent(self, path):
        r = self.recent.get("recent", [])
        if path in r: r.remove(path)
        r.insert(0, path); r = r[:100]
        self.recent["recent"] = r
        save_recent(self.recent)

    def load_track(self, path, auto_play=True):
        if not os.path.exists(path):
            messagebox.showerror(t("d_error"), t("d_notfound") + path); return
        try: self.player.load(path)
        except Exception as e:
            messagebox.showerror(t("d_error"), t("d_loaderr") + str(e)); return
        self._full_name = os.path.basename(path)
        self._set_display_name(self._full_name)
        self._refresh_now_playing_meta()
        self._add_to_recent(path)
        self.status.config(text=t("ready"))
        self.btn_play.set_state("normal")
        self.btn_pause.set_state("normal")
        self.btn_stop.set_state("normal")
        self.scrubber.set_duration(self.player.duration_s)
        self.scrubber.set_position(0.0)
        self._update_fav_indicator()
        if auto_play: self.play_track()

    def _refresh_now_playing_meta(self):
        p = self.player.track_path
        if not p: return
        tags = read_tags(p)
        artist = tags.get("artist", ""); title = tags.get("title", "")
        album = tags.get("album", "")
        if artist and title:
            self.meta_lbl.config(text=f"{artist} — {title}" + (f"  ·  {album}" if album else ""))
        else:
            self.meta_lbl.config(text="")

    def _set_display_name(self, full_name):
        self._full_name = full_name
        if len(full_name) <= 36 or not self.settings.get("ticker_on", True) \
                or self.settings.get("eco_mode", False):
            self.display.config(text=full_name[:38]); self._stop_ticker()
        else:
            self._ticker_pos = 0; self._start_ticker()

    def _start_ticker(self):
        self._stop_ticker()
        def tick():
            if not self._full_name: return
            text = self._full_name + "   ·   "
            n = len(text); p = self._ticker_pos % n
            view = (text + text)[p:p + 34]
            self.display.config(text=view)
            self._ticker_pos = (self._ticker_pos + 1) % n
            self._ticker_job = self.root.after(250, tick)
        self._ticker_job = self.root.after(250, tick)

    def _stop_ticker(self):
        if self._ticker_job is not None:
            try: self.root.after_cancel(self._ticker_job)
            except Exception: pass
            self._ticker_job = None

    def play_track(self):
        if not self.player.track_path: return
        self.player.play()
        self.player.set_volume(self.player.target_volume)
        self.status.config(text=t("playing"))
        self.btn_play.set_state("disabled")
        self.btn_pause.set_state("normal")
        self._start_end_watch()
        if self.settings.get("stats_enabled", True):
            try:
                tags = read_tags(self.player.track_path) if self.player.track_path else {}
                stats.track_played(tags.get("artist", ""))
            except Exception: pass

    def pause_track(self):
        if self.player.state != "PLAYING": return
        self.player.pause()
        self.status.config(text=t("paused"))
        self.btn_play.set_state("normal")
        self.btn_pause.set_state("disabled")
        self._stop_end_watch()

    def stop_track(self):
        self.player.stop()
        self.player.set_volume(self.player.target_volume)
        self.status.config(text=t("stopped"))
        self.btn_play.set_state("normal")
        self.btn_pause.set_state("disabled")
        self.scrubber.set_position(0.0)
        self._stop_end_watch()

    def toggle_playlist(self):
        if self._playlist_win is not None and self._playlist_win.winfo_exists():
            self._playlist_win.lift(); self._playlist_win.focus_set(); return
        self._playlist_win = PlaylistWindow(self)

    def add_current_to_playlist(self):
        p = self.player.track_path
        if not p: return
        if p not in self.playlist["tracks"]:
            self.playlist["tracks"].append(p); self.save_playlist()
            if self._playlist_win is not None and self._playlist_win.winfo_exists():
                self._playlist_win.refresh()

    def toggle_favorite(self):
        p = self.player.track_path
        if not p: return
        if p not in self.playlist["tracks"]: self.playlist["tracks"].append(p)
        if p in self.playlist["favorites"]:
            self.playlist["favorites"].remove(p)
        else:
            self.playlist["favorites"].append(p)
        self.save_playlist(); self._update_fav_indicator()
        if self._playlist_win is not None and self._playlist_win.winfo_exists():
            self._playlist_win.refresh()

    def _update_fav_indicator(self):
        p = self.player.track_path
        if p and p in self.playlist["favorites"]:
            self.fav_indicator.config(text="★ " + t("favorite"))
        else: self.fav_indicator.config(text="")

    def _pick_next_track(self):
        tracks = self.playlist["tracks"]
        if not tracks: return None
        mode = self.settings.get("repeat_mode", "off")
        if mode == "one": return self.player.track_path
        cur = self.player.track_path
        if cur in tracks: idx = tracks.index(cur)
        else: idx = -1
        shuffle = self.settings.get("shuffle_mode", "off")
        if shuffle == "off":
            if mode == "all": nxt = (idx + 1) % len(tracks)
            else:
                nxt = idx + 1
                if nxt >= len(tracks): return None
        elif shuffle == "on": nxt = random.randrange(len(tracks))
        else:
            candidates = [i for i in range(len(tracks)) if tracks[i] not in self._smart_history]
            if not candidates: candidates = list(range(len(tracks)))
            nxt = random.choice(candidates)
        return tracks[nxt]

    def play_next(self):
        nxt = self._pick_next_track()
        if not nxt: self.stop_track(); return
        self._smart_history.append(nxt)
        self.load_track(nxt)

    def play_prev(self):
        tracks = self.playlist["tracks"]
        if not tracks: return
        cur = self.player.track_path
        if cur in tracks: idx = (tracks.index(cur) - 1) % len(tracks)
        else: idx = 0
        self.load_track(tracks[idx])

    def save_playlist(self): save_json(PLAYLIST_FILE, self.playlist)

    def toggle_mini(self):
        try:
            if self._mini_win is not None and self._mini_win.winfo_exists():
                try: self._mini_win.destroy()
                except Exception: pass
                self._mini_win = None
                try:
                    self.root.deiconify(); self.root.lift()
                except Exception: pass
                self.settings["mini_mode"] = False
                save_json(SETTINGS_FILE, self.settings)
                return
            self.settings["mini_mode"] = True
            save_json(SETTINGS_FILE, self.settings)
            self._mini_win = MiniPlayer(self)
            try:
                self.root.iconify()
            except Exception:
                pass
        except Exception as e:
            print("mini player error:", e)
            try:
                self.root.deiconify(); self.root.lift()
            except Exception:
                pass

    def take_screenshot(self):
        try:
            w = self.root.winfo_width(); h = self.root.winfo_height()
            x = self.root.winfo_rootx(); y = self.root.winfo_rooty()
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               f"scarli_screenshot_{ts}.png")
            try:
                from PIL import ImageGrab
                img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
                img.save(out)
                print("Screenshot saved:", out)
            except Exception as e:
                print("Screenshot requires Pillow:", e)
        except Exception as e:
            print("Screenshot error:", e)

    def _tick_ui(self):
        self._update_time_label()
        if not self.settings.get("static_scrubber", False):
            if self.player.duration_s > 0:
                self.scrubber.set_duration(self.player.duration_s)
                self.scrubber.set_position(self.player.current_pos())
        self.root.after(500, self._tick_ui)

    def _update_time_label(self):
        pos = self.player.current_pos(); dur = self.player.duration_s
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
                self.root.after(0, self._on_track_end); return
            self._end_check_id = self.root.after(300, watch)
        self._end_check_id = self.root.after(300, watch)

    def _stop_end_watch(self):
        if self._end_check_id is not None:
            try: self.root.after_cancel(self._end_check_id)
            except Exception: pass
            self._end_check_id = None

    def _on_track_end(self):
        self._stop_end_watch()
        mode = self.settings.get("repeat_mode", "off")
        if mode == "one":
            self.load_track(self.player.track_path); return
        nxt = self._pick_next_track()
        if nxt:
            self._smart_history.append(nxt); self.load_track(nxt)
        else: self.stop_track()

    # ---------------------------------------------------------------------
    #  SETTINGS — cards layout
    # ---------------------------------------------------------------------
    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title(t("s_title"))
        win.configure(bg=C["bg_body"])
        win.geometry("680x720")
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        head = tk.Frame(win, bg=C["bg_body"])
        head.pack(fill="x", padx=24, pady=(24, 8))
        tk.Label(head, text=t("s_title"), bg=C["bg_body"], fg=C["fg_soft"],
                 font=("Segoe UI", 22, "bold"), anchor="w").pack(side="left")
        tk.Label(head, text=f"v{APP_VERSION}", bg=C["bg_body"], fg=C["fg_dim"],
                 font=("Segoe UI", 10), anchor="e").pack(side="right", pady=(8, 0))

        outer = tk.Frame(win, bg=C["bg_body"])
        outer.pack(fill="both", expand=True, padx=24, pady=(4, 16))

        canvas = tk.Canvas(outer, bg=C["bg_body"], highlightthickness=0)
        sb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview,
                          bg=C["btn_bg"], troughcolor=C["bg_trough"],
                          bd=0, highlightthickness=0, width=8)
        scroll = tk.Frame(canvas, bg=C["bg_body"])
        scroll.bind("<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll, anchor="nw", width=608)
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        def _on_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_wheel)

        def make_card(title, subtitle=""):
            card = tk.Frame(scroll, bg=C["bg_panel"], bd=0,
                            highlightthickness=1, highlightbackground=C["frame"])
            card.pack(fill="x", pady=8)

            header = tk.Frame(card, bg=C["bg_panel"])
            header.pack(fill="x", padx=20, pady=(16, 4))
            tk.Label(header, text=title, bg=C["bg_panel"], fg=C["fg_soft"],
                     font=("Segoe UI", 13, "bold"), anchor="w").pack(side="left")
            if subtitle:
                tk.Label(card, text=subtitle, bg=C["bg_panel"], fg=C["fg_dim"],
                         font=("Segoe UI", 9), anchor="w").pack(fill="x", padx=20)

            body = tk.Frame(card, bg=C["bg_panel"])
            body.pack(fill="x", padx=20, pady=(8, 18))
            return body

        def add_switch(parent, label, key, cmd=None):
            row = tk.Frame(parent, bg=C["bg_panel"])
            row.pack(fill="x", pady=6)
            var = tk.BooleanVar(value=bool(self.settings.get(key, False)))

            sw = tk.Canvas(row, width=44, height=24, bg=C["bg_panel"],
                           highlightthickness=0, bd=0, cursor="hand2")

            def draw_sw():
                sw.delete("all")
                on = var.get()
                track_col = C["accent"] if on else C["bg_trough"]
                sw.create_oval(2, 2, 42, 22, fill=track_col, outline="")
                knob_x = 22 if on else 2
                sw.create_oval(knob_x + 2, 4, knob_x + 18, 20,
                               fill="#ffffff", outline="")

            def toggle(_e=None):
                var.set(not var.get())
                self.settings[key] = var.get()
                save_json(SETTINGS_FILE, self.settings)
                if cmd: cmd()
                draw_sw()

            sw.bind("<Button-1>", toggle)
            sw.pack(side="right")
            draw_sw()

            tk.Label(row, text=label, bg=C["bg_panel"], fg=C["fg_soft"],
                     font=("Segoe UI", 11), anchor="w").pack(side="left", fill="x",
                                                              expand=True)

        def add_radio_segmented(parent, label, key, options, labels=None):
            row = tk.Frame(parent, bg=C["bg_panel"])
            row.pack(fill="x", pady=8)
            tk.Label(row, text=label, bg=C["bg_panel"], fg=C["fg_soft"],
                     font=("Segoe UI", 11), anchor="w").pack(side="left")
            var = tk.StringVar(value=self.settings.get(key, options[0]))
            seg = tk.Frame(row, bg=C["bg_trough"], bd=0)
            seg.pack(side="right")
            btns = {}
            def update():
                for k, b in btns.items():
                    if k == var.get():
                        b.config(bg=C["accent"], fg="#ffffff")
                    else:
                        b.config(bg=C["bg_trough"], fg=C["fg_soft"])
            for i, opt in enumerate(options):
                label_txt = labels[i] if labels else opt.upper()
                b = tk.Button(seg, text=label_txt,
                              command=lambda o=opt: (var.set(o),
                                                     self._set_setting(key, o),
                                                     update()),
                              bg=C["bg_trough"], fg=C["fg_soft"],
                              activebackground=C["accent"],
                              activeforeground="#ffffff",
                              font=("Segoe UI", 9, "bold"),
                              bd=0, padx=14, pady=6, cursor="hand2",
                              relief="flat")
                b.pack(side="left")
                btns[opt] = b
            update()

        # CARD: PLAYBACK
        body = make_card(t("s_repeat"), "Repeat and shuffle behaviour")
        add_radio_segmented(body, t("s_repeat_l"), "repeat_mode",
                            ["off", "one", "all"],
                            ["OFF", "ONE", "ALL"])
        add_radio_segmented(body, t("s_shuffle_l"), "shuffle_mode",
                            ["off", "on", "smart"],
                            ["OFF", "ON", "SMART"])

        # CARD: INTERFACE
        body = make_card(t("s_visual"), "How the player looks and feels")
        add_switch(body, t("s_clock"), "clock_on", cmd=self._apply_clock_visibility)
        add_switch(body, t("s_ticker"), "ticker_on", cmd=self._apply_ticker_visibility)
        add_switch(body, t("s_tooltips"), "tooltips")

        # CARD: PERFORMANCE
        body = make_card(t("s_perf"), "For slower or older machines")
        add_switch(body, t("s_eco"), "eco_mode", cmd=self._apply_eco)
        add_switch(body, t("s_statscr"), "static_scrubber")
        add_switch(body, t("s_winanim"), "window_animation")

        # CARD: SYSTEM
        body = make_card(t("s_ui"), "Statistics")
        add_switch(body, t("s_stats"), "stats_enabled")

        # CARD: LANGUAGE
        body = make_card(t("s_lang"), "Choose your language")
        grid = tk.Frame(body, bg=C["bg_panel"])
        grid.pack(fill="x")
        langs = list(all_langs())

        def rebuild_langs():
            for w in grid.winfo_children():
                w.destroy()
            current = self.settings.get("language", "en")
            for i, code in enumerate(langs):
                is_active = (code == current)
                btn = tk.Button(grid, text=lang_display_name(code),
                                command=lambda c=code: (self._set_lang(c),
                                                        rebuild_langs()),
                                bg=C["accent"] if is_active else C["bg_trough"],
                                fg="#ffffff" if is_active else C["fg_soft"],
                                activebackground=C["accent_hover"],
                                activeforeground="#ffffff",
                                font=("Segoe UI", 10, "bold"),
                                bd=0, padx=18, pady=10, cursor="hand2",
                                relief="flat")
                btn.grid(row=i // 3, column=i % 3, padx=4, pady=4, sticky="ew")
        for c in range(3):
            grid.columnconfigure(c, weight=1)
        rebuild_langs()

        # FOOTER
        footer = tk.Frame(win, bg=C["bg_body"])
        footer.pack(fill="x", padx=24, pady=(0, 20))

        def reset_settings():
            if messagebox.askyesno(t("s_reset"), "Reset all settings?"):
                for k, v in DEFAULT_SETTINGS.items():
                    self.settings[k] = v
                save_json(SETTINGS_FILE, self.settings)
                win.destroy()
                self.open_settings()

        RoundedButton(footer, text=t("s_reset"), command=reset_settings,
                      width=130, height=42, radius=14).pack(side="left")
        RoundedButton(footer, text=t("s_close"), command=win.destroy,
                      width=140, height=42, radius=14, accent=True).pack(side="right")

    def _set_setting(self, key, val):
        self.settings[key] = val
        save_json(SETTINGS_FILE, self.settings)

    def _set_lang(self, code):
        self.settings["language"] = code
        save_json(SETTINGS_FILE, self.settings)
        set_lang(code)
        self._retranslate_ui()

    def _retranslate_ui(self):
        if self.player.state == "STOPPED": self.status.config(text=t("stopped"))
        elif self.player.state == "PLAYING": self.status.config(text=t("playing"))
        elif self.player.state == "PAUSED": self.status.config(text=t("paused"))
        self.vol_knob.label = t("volume").upper(); self.vol_knob._draw()
        if not self.player.track_path: self.display.config(text=t("no_track"))
        self._build_menu(); self._update_fav_indicator()

    def _apply_clock_visibility(self):
        if self.settings.get("clock_on", True): self.clock_lbl.pack(side="right")
        else: self.clock_lbl.pack_forget()

    def _apply_ticker_visibility(self):
        if not self.settings.get("ticker_on", True) or self.settings.get("eco_mode", False):
            self._stop_ticker()
            if self._full_name: self.display.config(text=self._full_name[:38])

    def _apply_eco(self):
        if self.settings.get("eco_mode", False):
            self.settings["window_animation"] = False
            self._stop_ticker()
        save_json(SETTINGS_FILE, self.settings)

    def show_about(self):
        win = tk.Toplevel(self.root)
        win.title(t("d_about"))
        win.configure(bg=C["bg_body"])
        win.geometry("700x580")
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text=f"SCARLI-MUSIC v{APP_VERSION}",
                 bg=C["bg_body"], fg=C["accent"],
                 font=("Segoe UI", 22, "bold")).pack(pady=(24, 4))
        tk.Label(win, text="github.com/ScarlLV/ScarliMusic",
                 bg=C["bg_body"], fg=C["fg_dim"],
                 font=("Segoe UI", 10)).pack(pady=(0, 16))

        tabs = tk.Frame(win, bg=C["bg_body"])
        tabs.pack(pady=(0, 12))
        content = tk.Frame(win, bg=C["bg_body"])
        content.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        pages = {}
        tab_btns = {}

        def show(page):
            for f in pages.values():
                f.pack_forget()
            pages[page].pack(fill="both", expand=True)
            for k, btn in tab_btns.items():
                if k == page:
                    btn.config(bg=C["accent"], fg="#ffffff")
                else:
                    btn.config(bg=C["btn_bg"], fg=C["fg_soft"])

        about_f = tk.Frame(content, bg=C["bg_body"])
        pages["about"] = about_f
        tk.Label(about_f, text=t("about_body"),
                 bg=C["bg_body"], fg=C["fg_soft"],
                 font=("Segoe UI", 10), justify="left", anchor="w",
                 wraplength=620).pack(fill="x", padx=8, pady=12)

        credits_f = tk.Frame(content, bg=C["bg_body"])
        pages["credits"] = credits_f
        tk.Label(credits_f, text=t("credits_body"),
                 bg=C["bg_body"], fg=C["fg_soft"],
                 font=("Segoe UI", 10), justify="left", anchor="w",
                 wraplength=620).pack(fill="x", padx=8, pady=12)

        faq_f = tk.Frame(content, bg=C["bg_body"])
        pages["faq"] = faq_f

        faq_items = faq_translated()
        if not faq_items:
            try:
                from faq import FAQ as _FAQ
                faq_items = _FAQ
            except Exception:
                faq_items = [("FAQ", "No FAQ available")]

        faq_canvas = tk.Canvas(faq_f, bg=C["bg_body"], highlightthickness=0)
        faq_sb = tk.Scrollbar(faq_f, orient="vertical", command=faq_canvas.yview,
                              bg=C["btn_bg"], troughcolor=C["bg_trough"], bd=0)
        faq_inner = tk.Frame(faq_canvas, bg=C["bg_body"])
        faq_inner.bind("<Configure>",
                       lambda e: faq_canvas.configure(scrollregion=faq_canvas.bbox("all")))
        faq_canvas.create_window((0, 0), window=faq_inner, anchor="nw")
        faq_canvas.configure(yscrollcommand=faq_sb.set)
        faq_canvas.pack(side="left", fill="both", expand=True)
        faq_sb.pack(side="right", fill="y")

        for q, a in faq_items:
            tk.Label(faq_inner, text="▸ " + q, bg=C["bg_body"], fg=C["fg_main"],
                     font=("Segoe UI", 10, "bold"), anchor="w", justify="left"
                     ).pack(fill="x", padx=10, pady=(10, 2))
            tk.Label(faq_inner, text=a, bg=C["bg_body"], fg=C["fg_soft"],
                     font=("Segoe UI", 9), anchor="w", justify="left",
                     wraplength=600).pack(fill="x", padx=22)

        def show_stats():
            s = stats.load()
            top = stats.top_artists(5)
            lines = [
                f"{t('stats_total')} {stats.fmt_hours(s.get('total_seconds', 0))}",
                f"{t('stats_tracks')} {s.get('tracks_played', 0)}",
                f"{t('stats_sessions')} {s.get('sessions', 0)}",
                "",
                t("stats_top_artists"),
            ]
            if top:
                for name, count in top:
                    lines.append(f"  · {name}: {count}")
            else:
                lines.append(t("stats_empty"))
            messagebox.showinfo(t("stats_title"), "\n".join(lines))

        for key, label in (
            ("about", t("ab_about")),
            ("credits", t("ab_credits")),
            ("faq", t("ab_faq")),
            ("stats", t("ab_stats")),
        ):
            if key == "stats":
                b = tk.Button(tabs, text=label, command=show_stats,
                              bg=C["btn_bg"], fg=C["fg_soft"],
                              activebackground=C["accent"], activeforeground="#fff",
                              font=("Segoe UI", 10, "bold"),
                              bd=0, padx=20, pady=8, cursor="hand2",
                              relief="flat")
            else:
                b = tk.Button(tabs, text=label,
                              command=lambda k=key: show(k),
                              bg=C["btn_bg"], fg=C["fg_soft"],
                              activebackground=C["accent"], activeforeground="#fff",
                              font=("Segoe UI", 10, "bold"),
                              bd=0, padx=20, pady=8, cursor="hand2",
                              relief="flat")
                tab_btns[key] = b
            b.pack(side="left", padx=4)

        tk.Button(win, text=t("s_close"), command=win.destroy,
                  bg=C["accent"], fg="#ffffff",
                  activebackground=C["accent_hover"], activeforeground="#ffffff",
                  font=("Segoe UI", 10, "bold"), bd=0, padx=28, pady=10,
                  cursor="hand2", relief="flat").pack(pady=12)

        show("about")

    def on_closing(self):
        if self._session_started_at is not None:
            try: stats.add_seconds(time.time() - self._session_started_at)
            except Exception: pass
        save_json(SETTINGS_FILE, self.settings)
        save_json(PLAYLIST_FILE, self.playlist)
        save_recent(self.recent)
        try: self.player.cleanup()
        except Exception: pass
        self.root.destroy()


def main():
    if DND_OK:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    try:
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "assets", "icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except Exception:
        pass
    ScarliMusic(root)
    root.mainloop()


if __name__ == "__main__":
    main()