"""
SCARLI-MUSIC — listening statistics.
Хранит: время прослушивания, счётчик треков, топ исполнителей.
"""

import os
import json
from datetime import datetime, date
from collections import Counter

STATS_FILE = "stats.json"

DEFAULT_STATS = {
    "total_seconds": 0,
    "tracks_played": 0,
    "sessions": 0,
    "per_day": {},          # {"2026-09-26": 320.5}
    "top_artists": {},      # {"Кишлак": 42}
    "last_played": "",      # ISO date
}


def load():
    if not os.path.exists(STATS_FILE):
        save(DEFAULT_STATS)
        return dict(DEFAULT_STATS)
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        out = dict(DEFAULT_STATS)
        out.update(data)
        return out
    except Exception:
        return dict(DEFAULT_STATS)


def save(stats):
    try:
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("stats save error:", e)


def session_start():
    s = load()
    s["sessions"] = s.get("sessions", 0) + 1
    save(s)


def track_played(artist: str = ""):
    """Вызывается когда трек начинает играть."""
    s = load()
    s["tracks_played"] = s.get("tracks_played", 0) + 1
    s["last_played"] = datetime.now().isoformat()
    if artist:
        s.setdefault("top_artists", {})
        s["top_artists"][artist] = s["top_artists"].get(artist, 0) + 1
    save(s)


def add_seconds(seconds: float):
    """Вызывается при завершении сессии или периодически."""
    if seconds <= 0:
        return
    s = load()
    s["total_seconds"] = s.get("total_seconds", 0) + seconds
    today = date.today().isoformat()
    s.setdefault("per_day", {})
    s["per_day"][today] = s["per_day"].get(today, 0) + seconds
    save(s)


def fmt_hours(sec):
    if sec < 60:
        return f"{int(sec)} сек"
    if sec < 3600:
        return f"{int(sec // 60)} мин"
    h = sec / 3600
    if h < 24:
        return f"{h:.1f} ч"
    d = h / 24
    return f"{d:.1f} дн ({h:.0f} ч)"


def top_artists(n=5):
    s = load()
    ta = s.get("top_artists", {})
    return Counter(ta).most_common(n)