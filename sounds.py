"""
SCARLI-MUSIC — procedural click sounds (no WAV files needed).
Генерирует короткие "щёлк" для нажатий через numpy + pygame.
"""

import numpy as np
import pygame

_sounds = {}
_enabled = True


def init():
    """Создаёт звуки. Сам инициализирует mixer если нужно."""
    global _sounds
    try:
        # Инициализация pygame mixer (если ещё не)
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        except pygame.error:
            # уже инициализирован — это ок
            pass

        _sounds["click"]    = _make_click(880, 0.04, 0.25)
        _sounds["toggle"]   = _make_click(1320, 0.06, 0.30)
        _sounds["reel"]     = _make_reel(0.20, 0.15)
        _sounds["error"]    = _make_click(220, 0.15, 0.35)
        _sounds["success"]  = _make_chord([523, 659, 784], 0.15, 0.20)
    except Exception as e:
        print("sounds init error:", e)
    try:
        _sounds["click"]    = _make_click(880, 0.04, 0.25)
        _sounds["toggle"]   = _make_click(1320, 0.06, 0.30)
        _sounds["reel"]     = _make_reel(0.20, 0.15)
        _sounds["error"]    = _make_click(220, 0.15, 0.35)
        _sounds["success"]  = _make_chord([523, 659, 784], 0.15, 0.20)
    except Exception as e:
        print("sounds init error:", e)

def _make_click(freq, dur, vol):
    sr = 22050
    t = np.linspace(0, dur, int(sr * dur), False)
    # короткий импульс с затуханием — щелчок
    wave = np.sin(2 * np.pi * freq * t) * np.exp(-t * 40)
    # немного шума для «аналоговости»
    noise = np.random.uniform(-0.3, 0.3, len(t)) * np.exp(-t * 80)
    samples = (wave + noise) * vol
    samples = np.clip(samples, -1.0, 1.0)
    arr = (samples * 32767).astype(np.int16)
    # stereo
    arr = np.column_stack([arr, arr])
    return pygame.sndarray.make_sound(arr)

def _make_reel(dur, vol):
    sr = 22050
    t = np.linspace(0, dur, int(sr * dur), False)
    # механический стрекот — шум модулированный
    noise = np.random.uniform(-1, 1, len(t))
    mod = (np.sin(2 * np.pi * 30 * t) + 1) / 2
    samples = noise * mod * vol * np.exp(-t * 3)
    samples = np.clip(samples, -1.0, 1.0)
    arr = (samples * 32767).astype(np.int16)
    arr = np.column_stack([arr, arr])
    return pygame.sndarray.make_sound(arr)

def _make_chord(freqs, dur, vol):
    sr = 22050
    t = np.linspace(0, dur, int(sr * dur), False)
    wave = np.zeros_like(t)
    for f in freqs:
        wave += np.sin(2 * np.pi * f * t)
    wave /= len(freqs)
    samples = wave * np.exp(-t * 8) * vol
    samples = np.clip(samples, -1.0, 1.0)
    arr = (samples * 32767).astype(np.int16)
    arr = np.column_stack([arr, arr])
    return pygame.sndarray.make_sound(arr)

def play(name):
    if not _enabled:
        return
    s = _sounds.get(name)
    if s:
        try:
            s.set_volume(0.4)
            s.play()
        except Exception:
            pass

def set_enabled(on):
    global _enabled
    _enabled = bool(on)

def is_available():
    return bool(_sounds)