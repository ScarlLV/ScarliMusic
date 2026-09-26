"""
SCARLI-MUSIC — FAQ content (used in About window).
"""

FAQ = [
    ("Что такое SCARLI-MUSIC?",
     "SCARLI-MUSIC — ретро-плеер в стиле советской радиоэлектроники.\n"
     "Написан на Python + tkinter + pygame-ce + python-vlc.\n"
     "Полностью локальный, без телеметрии и хостинга."),
    ("Как переключить бэкенд VLC / pygame?",
     "Settings → BACKEND → выбери AUTO / VLC / PYGAME.\n"
     "AUTO: пробует VLC, откатывается на pygame.\n"
     "VLC даёт реальный SPEED, EQ, Mono, Balance.\n"
     "pygame — самый лёгкий, для слабых ПК."),
    ("Почему SPEED работает только в VLC?",
     "pygame.mixer не умеет менять скорость воспроизведения.\n"
     "VLC умеет через set_rate() с сохранением тона."),
    ("Что такое «Профиль слабого ПК»?",
     "Один клик — вырубает VLC, анимации, бобины, CRT-эффекты,\n"
     "включает low-quality render и static scrubber.\n"
     "Плеер начинает работать на чём угодно."),
    ("Где хранятся настройки?",
     "settings.json — настройки\n"
     "playlist.json — плейлист и избранное\n"
     "recent.json — история прослушивания\n"
     "stats.json — статистика\n"
     "Все файлы лежат рядом с main.py (.exe)."),
    ("Как загрузить обложку?",
     "Обложка читается из ID3-тега (APIC / covr / FLAC picture).\n"
     "Требуется Pillow (pip install pillow).\n"
     "Включить/выключить: Settings → VISUAL → Show covers."),
    ("Почему не работает Drag & drop?",
     "Нужен пакет tkinterdnd2: pip install tkinterdnd2.\n"
     "Без него DnD отключён, всё остальное работает."),
    ("Как переключить язык?",
     "Settings → LANGUAGE → выбери из 10 языков.\n"
     "EN / UA / SU / PL / DE / FR / ZH / JA / BE / KK."),
    ("Где взять исходники и обновления?",
     "GitHub: github.com/ScarlLV/ScarliMusic\n"
     "Релизы там же, включая .exe для Windows."),
    ("Плеер тормозит, что делать?",
     "1) Settings → PERFORMANCE → Eco mode (галочка).\n"
     "2) Settings → Low-quality render.\n"
     "3) Settings → Static scrubber.\n"
     "4) Выключи обложки, tooltips, бегущую строку."),
]