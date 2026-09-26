<div align="center">

# 🎵 SCARLI-MUSIC

**A modern, lightweight audio player for Windows**

![Version](https://img.shields.io/badge/version-0.3-blueviolet?style=flat-square)
![Python](https://img.shields.io/badge/python-3.14-blue?style=flat-square)
![Platform](https://img.shields.io/badge/platform-Windows-informational?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

[English](README.md) · [Русский](README.ru.md)

</div>

---

## ✨ About

SCARLI-MUSIC is a lightweight, modern audio player written in Python.
No hosting, no telemetry, no cloud — everything runs locally on your PC.

**Philosophy:**
- 🚀 **Fast** — starts in under 1 second
- 🪶 **Light** — works even on old hardware
- 🔒 **Private** — no tracking, no network calls
- 🎨 **Modern** — clean interface, purple accent theme

---

## 🎧 Features

### Player
- Modern rounded interface with purple accent theme
- Round transport buttons (⏮ ▶ ⏭) like Spotify / Apple Music
- Volume knob with arc indicator
- Modern scrubber with hover state
- Playlist with tabs: **All / Favorites / Recent**
- Search and sort tracks (by name, duration, date added)
- Drag & drop files or folders onto the player window
- Mini player (compact always-on-top window)
- System tray support *(optional)*

### Music library
- MP3, WAV, OGG, FLAC, M4A, AAC, WMA support
- **ID3 tag editor** — edit artist, title, album, year, genre
- Reading embedded metadata (artist, title, album, duration)
- Auto-detects track names from tags when available
- Favorites list
- Recent tracks history (last 100)

### Behavior
- Repeat modes: **Off / One / All**
- Shuffle modes: **Off / On / Smart** (no repeat of last N tracks)
- Gapless playback
- Fade in/out on play/pause

### Interface
- Single purple theme
- 8 languages: **English, Русский, Українська, Deutsch, Français, 中文, 日本語, Беларуская**
- Live theme switching (some settings apply instantly)
- Tooltips on hover
- Configurable card-based settings window
- Fast — no animations except where they matter

### Performance
- **Eco mode** — disable window animation and ticker
- **Static scrubber** — reduce CPU usage
- Works on old hardware (Windows 7+ compatible)

---

## ⬇️ Download

**Latest release:** [v0.3](https://github.com/ScarlLV/ScarliMusic/releases/latest)

- 🪟 **Windows:** download `ScarliMusic.exe` and run it. No Python required.
- 🐍 **From source:** see below.

[![Downloads](https://img.shields.io/github/downloads/ScarlLV/ScarliMusic/total?color=blueviolet&style=flat-square)](https://github.com/ScarlLV/ScarliMusic/releases)

---

## 🚀 From source

```bash
git clone https://github.com/ScarlLV/ScarliMusic.git
cd ScarliMusic
pip install -r requirements.txt
python main.py