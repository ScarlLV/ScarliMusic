"""
SCARLI-MUSIC — localization
EN / RU / UA / DE / FR / ZH / JA / BE
"""

LANG = {
    "en": {
        "no_track": "NO TRACK", "stopped": "STOPPED", "playing": "PLAYING",
        "paused": "PAUSED", "ready": "READY",
        "open": "OPEN", "play": "PLAY", "pause": "PAUSE", "stop": "STOP", "resume": "RESUME",
        "volume": "VOLUME", "speed": "SPEED", "tape": "POSITION",
        "playlist": "PLAYLIST", "fav": "FAV", "next": "NEXT", "prev": "PREV",
        "coming_soon": "SOON", "favorite": "FAVORITE",
        "m_file": "File", "m_open": "Open...", "m_exit": "Exit",
        "m_playlist": "Playlist", "m_show_pl": "Show playlist",
        "m_add_pl": "Add current to playlist", "m_next": "Next track",
        "m_prev": "Previous track", "m_theme": "Theme",
        "m_settings": "Settings", "m_settings_w": "Settings", "m_about": "About",
        "m_mini": "Mini player", "m_screenshot": "Screenshot (F12)",
        "s_title": "SETTINGS", "s_sound": "SOUND",
        "s_fadein": "Fade in on play", "s_fadeout": "Fade out on pause",
        "s_gapless": "Gapless playback",
        "s_repeat": "REPEAT & SHUFFLE", "s_repeat_l": "Repeat:", "s_shuffle_l": "Shuffle:",
        "s_visual": "VISUAL", "s_clock": "Show clock",
        "s_ticker": "Scrolling title",
        "s_perf": "PERFORMANCE", "s_eco": "Eco mode",
        "s_statscr": "Static scrubber",
        "s_winanim": "Window open animation",
        "s_ui": "INTERFACE", "s_ui_sounds": "UI click sounds",
        "s_stats": "Collect statistics",
        "s_theme": "THEME", "s_lang": "LANGUAGE", "s_close": "CLOSE",
        "s_tooltips": "Tooltips",
        "s_apply": "Apply",
        "s_reset": "Reset",
        "p_title": "PLAYLIST", "p_add": "+ ADD", "p_close": "CLOSE",
        "p_search": "Search:", "p_sort": "Sort:",
        "p_fav": "FAVORITE", "p_remove": "REMOVE", "p_clear": "CLEAR",
        "p_export": "EXPORT .m3u", "p_import": "IMPORT .m3u",
        "p_tab_all": "All", "p_tab_fav": "Favorites", "p_tab_recent": "Recent",
        "p_edit_tags": "Edit tags",
        "d_about": "About",
        "d_error": "Error", "d_notfound": "File not found:\n",
        "d_loaderr": "Failed to load:\n", "d_clearq": "Remove all tracks?",
        "d_exp": "Export", "d_imp": "Import", "d_saved": "Saved: ",
        "d_tags_title": "EDIT TAGS",
        "d_tags_artist": "Artist:", "d_tags_title_f": "Title:", "d_tags_album": "Album:",
        "d_tags_year": "Year:", "d_tags_genre": "Genre:", "d_tags_save": "SAVE",
        "d_tags_cancel": "CANCEL",
        "ab_about": "ABOUT", "ab_credits": "THANKS", "ab_faq": "FAQ", "ab_stats": "STATS",
        "about_body": (
            "SCARLI-MUSIC — a lightweight audio player.\n\n"
            "Written in Python 3.14 with tkinter and pygame-ce.\n\n"
            "Philosophy:\n"
            "  · 100% local — no hosting, no cloud\n"
            "  · No telemetry, no tracking\n"
            "  · Lightweight and fast\n\n"
            "© 2026 · SCARLI-MUSIC"
        ),
        "credits_body": (
            "Thank you to everyone who supported the project:\n\n"
            "· The Python and pygame communities\n"
            "· Authors of mutagen, Pillow, tkinterdnd2\n"
            "· Everyone who reported bugs and suggested ideas\n"
            "· You — for using SCARLI-MUSIC\n\n"
            "github.com/ScarlLV/ScarliMusic"
        ),
        "stats_title": "STATISTICS",
        "stats_total": "Total listened:",
        "stats_tracks": "Tracks played:",
        "stats_sessions": "Sessions:",
        "stats_top_artists": "Top artists:",
        "stats_empty": "  (empty yet)",
    },
    "ru": {
        "no_track": "НЕТ ТРЕКА", "stopped": "ОСТАНОВЛЕНО", "playing": "ИГРАЕТ",
        "paused": "ПАУЗА", "ready": "ГОТОВ",
        "open": "ОТКРЫТЬ", "play": "ИГРАТЬ", "pause": "ПАУЗА", "stop": "СТОП", "resume": "ПРОДОЛЖИТЬ",
        "volume": "ГРОМКОСТЬ", "speed": "СКОРОСТЬ", "tape": "ПОЗИЦИЯ",
        "playlist": "ПЛЕЙЛИСТ", "fav": "ИЗБРАННОЕ", "next": "СЛЕДУЮЩИЙ", "prev": "ПРЕДЫДУЩИЙ",
        "coming_soon": "СКОРО", "favorite": "В ИЗБРАННОМ",
        "m_file": "Файл", "m_open": "Открыть...", "m_exit": "Выход",
        "m_playlist": "Плейлист", "m_show_pl": "Показать плейлист",
        "m_add_pl": "Добавить в плейлист", "m_next": "Следующий трек",
        "m_prev": "Предыдущий трек", "m_theme": "Тема",
        "m_settings": "Настройки", "m_settings_w": "Настройки", "m_about": "О программе",
        "m_mini": "Мини-плеер", "m_screenshot": "Скриншот (F12)",
        "s_title": "НАСТРОЙКИ", "s_sound": "ЗВУК",
        "s_fadein": "Плавное появление при старте", "s_fadeout": "Плавное затухание при паузе",
        "s_gapless": "Без паузы между треками",
        "s_repeat": "ПОВТОР И ПЕРЕМЕШИВАНИЕ", "s_repeat_l": "Повтор:", "s_shuffle_l": "Перемешивание:",
        "s_visual": "ВНЕШНИЙ ВИД", "s_clock": "Показывать часы",
        "s_ticker": "Бегущая строка",
        "s_perf": "ПРОИЗВОДИТЕЛЬНОСТЬ", "s_eco": "Экономный режим",
        "s_statscr": "Статичная шкала",
        "s_winanim": "Анимация открытия окна",
        "s_ui": "ИНТЕРФЕЙС", "s_ui_sounds": "Звуки нажатия кнопок",
        "s_stats": "Собирать статистику",
        "s_theme": "ТЕМА", "s_lang": "ЯЗЫК", "s_close": "ЗАКРЫТЬ",
        "s_tooltips": "Всплывающие подсказки",
        "s_apply": "Применить",
        "s_reset": "Сбросить",
        "p_title": "ПЛЕЙЛИСТ", "p_add": "+ ДОБАВИТЬ", "p_close": "ЗАКРЫТЬ",
        "p_search": "Поиск:", "p_sort": "Сортировка:",
        "p_fav": "В ИЗБРАННОЕ", "p_remove": "УДАЛИТЬ", "p_clear": "ОЧИСТИТЬ",
        "p_export": "ЭКСПОРТ .m3u", "p_import": "ИМПОРТ .m3u",
        "p_tab_all": "Все", "p_tab_fav": "Избранное", "p_tab_recent": "Недавние",
        "p_edit_tags": "Правка тегов",
        "d_about": "О программе",
        "d_error": "Ошибка", "d_notfound": "Файл не найден:\n",
        "d_loaderr": "Не удалось загрузить:\n", "d_clearq": "Удалить все записи?",
        "d_exp": "Экспорт", "d_imp": "Импорт", "d_saved": "Сохранено: ",
        "d_tags_title": "ПРАВКА ТЕГОВ",
        "d_tags_artist": "Исполнитель:", "d_tags_title_f": "Название:", "d_tags_album": "Альбом:",
        "d_tags_year": "Год:", "d_tags_genre": "Жанр:", "d_tags_save": "СОХРАНИТЬ",
        "d_tags_cancel": "ОТМЕНА",
        "ab_about": "О ПРОГРАММЕ", "ab_credits": "БЛАГОДАРНОСТИ", "ab_faq": "FAQ", "ab_stats": "СТАТИСТИКА",
        "about_body": (
            "SCARLI-MUSIC — лёгкий музыкальный плеер.\n\n"
            "Написан на Python 3.14 с tkinter и pygame-ce.\n\n"
            "Философия:\n"
            "  · 100% локально — без хостинга и облака\n"
            "  · Без телеметрии и слежки\n"
            "  · Лёгкий и быстрый\n\n"
            "© 2026 · SCARLI-MUSIC"
        ),
        "credits_body": (
            "Спасибо всем, кто поддерживал проект:\n\n"
            "· Сообществу Python и pygame\n"
            "· Авторам mutagen, Pillow, tkinterdnd2\n"
            "· Всем, кто присылал баг-репорты и идеи\n"
            "· Тебе — за то, что пользуешься SCARLI-MUSIC\n\n"
            "github.com/ScarlLV/ScarliMusic"
        ),
        "stats_title": "СТАТИСТИКА",
        "stats_total": "Всего прослушано:",
        "stats_tracks": "Треков воспроизведено:",
        "stats_sessions": "Сессий:",
        "stats_top_artists": "Топ исполнителей:",
        "stats_empty": "  (пока пусто)",
    },
    "ua": {
        "no_track": "НЕМАЄ ТРЕКУ", "stopped": "ЗУПИНЕНО", "playing": "ГРАЄ",
        "paused": "ПАУЗА", "ready": "ГОТОВО",
        "open": "ВІДКРИТИ", "play": "ГРАТИ", "pause": "ПАУЗА", "stop": "СТОП", "resume": "ДАЛІ",
        "volume": "ГУЧНІСТЬ", "speed": "ШВИДКІСТЬ", "tape": "ПОЗИЦІЯ",
        "playlist": "ПЛЕЙЛИСТ", "fav": "УЛЮБЛЕНЕ", "next": "ДАЛІ", "prev": "НАЗАД",
        "coming_soon": "СКОРО", "favorite": "В ОБРАНЕ",
        "m_file": "Файл", "m_open": "Відкрити...", "m_exit": "Вихід",
        "m_playlist": "Плейлист", "m_show_pl": "Показати плейлист",
        "m_add_pl": "Додати трек до плейлиста", "m_next": "Наступний трек",
        "m_prev": "Попередній трек", "m_theme": "Тема",
        "m_settings": "Налаштування", "m_settings_w": "Налаштування", "m_about": "Про програму",
        "m_mini": "Міні-плеєр", "m_screenshot": "Скріншот (F12)",
        "s_title": "НАЛАШТУВАННЯ", "s_sound": "ЗВУК",
        "s_fadein": "Плавний вхід", "s_fadeout": "Плавне затухання",
        "s_gapless": "Без пауз між треками",
        "s_repeat": "ПОВТОР І ПЕРЕМІШУВАННЯ", "s_repeat_l": "Повтор:", "s_shuffle_l": "Перемішування:",
        "s_visual": "ВИГЛЯД", "s_clock": "Показувати годинник",
        "s_ticker": "Рядок, що біжить",
        "s_perf": "ПРОДУКТИВНІСТЬ", "s_eco": "Економний режим",
        "s_statscr": "Статичний скраббер",
        "s_winanim": "Анімація відкриття вікна",
        "s_ui": "ІНТЕРФЕЙС", "s_ui_sounds": "Звуки натискання",
        "s_stats": "Збирати статистику",
        "s_theme": "ТЕМА", "s_lang": "МОВА", "s_close": "ЗАКРИТИ",
        "s_tooltips": "Спливаючі підказки",
        "s_apply": "Застосувати",
        "s_reset": "Скинути",
        "p_title": "ПЛЕЙЛИСТ", "p_add": "+ ДОДАТИ", "p_close": "ЗАКРИТИ",
        "p_search": "Пошук:", "p_sort": "Сортування:",
        "p_fav": "В ОБРАНЕ", "p_remove": "ВИДАЛИТИ", "p_clear": "ОЧИСТИТИ",
        "p_export": "ЕКСПОРТ .m3u", "p_import": "ІМПОРТ .m3u",
        "p_tab_all": "Усі", "p_tab_fav": "Обране", "p_tab_recent": "Недавні",
        "p_edit_tags": "Редагувати теги",
        "d_about": "Про програму",
        "d_error": "Помилка", "d_notfound": "Файл не знайдено:\n",
        "d_loaderr": "Не вдалося завантажити:\n", "d_clearq": "Видалити всі треки?",
        "d_exp": "Експорт", "d_imp": "Імпорт", "d_saved": "Збережено: ",
        "d_tags_title": "РЕДАГУВАТИ ТЕГИ",
        "d_tags_artist": "Виконавець:", "d_tags_title_f": "Назва:", "d_tags_album": "Альбом:",
        "d_tags_year": "Рік:", "d_tags_genre": "Жанр:", "d_tags_save": "ЗБЕРЕГТИ",
        "d_tags_cancel": "СКАСУВАТИ",
        "ab_about": "ПРО ПРОГРАМУ", "ab_credits": "ПОДЯКИ", "ab_faq": "FAQ", "ab_stats": "СТАТИСТИКА",
        "about_body": (
            "SCARLI-MUSIC — легкий музичний плеєр.\n\n"
            "Написаний на Python 3.14 з tkinter та pygame-ce.\n\n"
            "Філософія:\n"
            "  · 100% локально — без хостингу та хмари\n"
            "  · Без телеметрії та стеження\n"
            "  · Легкий та швидкий\n\n"
            "© 2026 · SCARLI-MUSIC"
        ),
        "credits_body": (
            "Дякую всім, хто підтримував проект:\n\n"
            "· Спільноті Python та pygame\n"
            "· Авторам mutagen, Pillow, tkinterdnd2\n"
            "· Усім, хто надсилав баг-репорти та ідеї\n"
            "· Тобі — за те, що користуєшся SCARLI-MUSIC\n\n"
            "github.com/ScarlLV/ScarliMusic"
        ),
        "stats_title": "СТАТИСТИКА",
        "stats_total": "Всього прослухано:",
        "stats_tracks": "Треків відтворено:",
        "stats_sessions": "Сесій:",
        "stats_top_artists": "Топ виконавців:",
        "stats_empty": "  (поки порожньо)",
    },
    "de": {
        "no_track": "KEIN TITEL", "stopped": "GESTOPPT", "playing": "WIEDERGABE",
        "paused": "PAUSE", "ready": "BEREIT",
        "open": "ÖFFNEN", "play": "SPIELEN", "pause": "PAUSE", "stop": "STOP", "resume": "WEITER",
        "volume": "LAUTSTÄRKE", "speed": "GESCHW.", "tape": "POSITION",
        "playlist": "PLAYLISTE", "fav": "FAV", "next": "WEITER", "prev": "ZURÜCK",
        "coming_soon": "BALD", "favorite": "FAVORIT",
        "m_file": "Datei", "m_open": "Öffnen...", "m_exit": "Beenden",
        "m_playlist": "Playliste", "m_show_pl": "Playliste zeigen",
        "m_add_pl": "Zur Playliste", "m_next": "Nächster Titel",
        "m_prev": "Vorheriger Titel", "m_theme": "Thema",
        "m_settings": "Einstellungen", "m_settings_w": "Einstellungen", "m_about": "Über",
        "m_mini": "Mini-Player", "m_screenshot": "Screenshot (F12)",
        "s_title": "EINSTELLUNGEN", "s_sound": "TON",
        "s_fadein": "Einblenden", "s_fadeout": "Ausblenden",
        "s_gapless": "Ohne Pausen",
        "s_repeat": "WIEDERHOLEN & ZUFALL", "s_repeat_l": "Wiederholen:", "s_shuffle_l": "Zufall:",
        "s_visual": "AUSSEHEN", "s_clock": "Uhr zeigen",
        "s_ticker": "Laufschrift",
        "s_perf": "LEISTUNG", "s_eco": "Öko-Modus",
        "s_statscr": "Statischer Scrubber",
        "s_winanim": "Fensteranimation",
        "s_ui": "OBERFLÄCHE", "s_ui_sounds": "Klick-Töne",
        "s_stats": "Statistiken sammeln",
        "s_theme": "THEMA", "s_lang": "SPRACHE", "s_close": "SCHLIESSEN",
        "s_tooltips": "Tooltips",
        "s_apply": "Anwenden",
        "s_reset": "Zurücksetzen",
        "p_title": "PLAYLISTE", "p_add": "+ HINZU", "p_close": "SCHLIESSEN",
        "p_search": "Suche:", "p_sort": "Sortieren:",
        "p_fav": "FAVORIT", "p_remove": "LÖSCHEN", "p_clear": "LEEREN",
        "p_export": "EXPORT .m3u", "p_import": "IMPORT .m3u",
        "p_tab_all": "Alle", "p_tab_fav": "Favoriten", "p_tab_recent": "Zuletzt",
        "p_edit_tags": "Tags bearbeiten",
        "d_about": "Über",
        "d_error": "Fehler", "d_notfound": "Datei nicht gefunden:\n",
        "d_loaderr": "Laden fehlgeschlagen:\n", "d_clearq": "Alle Titel entfernen?",
        "d_exp": "Export", "d_imp": "Import", "d_saved": "Gespeichert: ",
        "d_tags_title": "TAGS BEARBEITEN",
        "d_tags_artist": "Künstler:", "d_tags_title_f": "Titel:", "d_tags_album": "Album:",
        "d_tags_year": "Jahr:", "d_tags_genre": "Genre:", "d_tags_save": "SPEICHERN",
        "d_tags_cancel": "ABBRECHEN",
        "ab_about": "ÜBER", "ab_credits": "DANKSAGUNG", "ab_faq": "FAQ", "ab_stats": "STATISTIK",
        "about_body": (
            "SCARLI-MUSIC — ein schlanker Audioplayer.\n\n"
            "Geschrieben in Python 3.14 mit tkinter und pygame-ce.\n\n"
            "Philosophie:\n"
            "  · 100% lokal — kein Hosting, keine Cloud\n"
            "  · Keine Telemetrie, kein Tracking\n"
            "  · Leicht und schnell\n\n"
            "© 2026 · SCARLI-MUSIC"
        ),
        "credits_body": (
            "Danke an alle, die das Projekt unterstützt haben:\n\n"
            "· Der Python- und pygame-Community\n"
            "· Den Autoren von mutagen, Pillow, tkinterdnd2\n"
            "· Allen, die Bugs gemeldet und Ideen geteilt haben\n"
            "· Dir — für die Nutzung von SCARLI-MUSIC\n\n"
            "github.com/ScarlLV/ScarliMusic"
        ),
        "stats_title": "STATISTIK",
        "stats_total": "Insgesamt gehört:",
        "stats_tracks": "Titel gespielt:",
        "stats_sessions": "Sitzungen:",
        "stats_top_artists": "Top-Künstler:",
        "stats_empty": "  (noch leer)",
    },
    "fr": {
        "no_track": "AUCUNE PISTE", "stopped": "ARRÊTÉ", "playing": "LECTURE",
        "paused": "PAUSE", "ready": "PRÊT",
        "open": "OUVRIR", "play": "JOUER", "pause": "PAUSE", "stop": "STOP", "resume": "REPRENDRE",
        "volume": "VOLUME", "speed": "VITESSE", "tape": "POSITION",
        "playlist": "PLAYLIST", "fav": "FAV", "next": "SUIV", "prev": "PRÉC",
        "coming_soon": "BIENTÔT", "favorite": "FAVORI",
        "m_file": "Fichier", "m_open": "Ouvrir...", "m_exit": "Quitter",
        "m_playlist": "Playlist", "m_show_pl": "Voir la playlist",
        "m_add_pl": "Ajouter à la playlist", "m_next": "Piste suivante",
        "m_prev": "Piste précédente", "m_theme": "Thème",
        "m_settings": "Paramètres", "m_settings_w": "Paramètres", "m_about": "À propos",
        "m_mini": "Mini lecteur", "m_screenshot": "Capture (F12)",
        "s_title": "PARAMÈTRES", "s_sound": "SON",
        "s_fadein": "Fondu entrant", "s_fadeout": "Fondu sortant",
        "s_gapless": "Sans coupures",
        "s_repeat": "RÉPÉTER & ALÉATOIRE", "s_repeat_l": "Répéter:", "s_shuffle_l": "Aléatoire:",
        "s_visual": "APPARENCE", "s_clock": "Afficher l'horloge",
        "s_ticker": "Titre défilant",
        "s_perf": "PERFORMANCE", "s_eco": "Mode éco",
        "s_statscr": "Curseur statique",
        "s_winanim": "Animation d'ouverture",
        "s_ui": "INTERFACE", "s_ui_sounds": "Sons de clic",
        "s_stats": "Collecter des stats",
        "s_theme": "THÈME", "s_lang": "LANGUE", "s_close": "FERMER",
        "s_tooltips": "Infobulles",
        "s_apply": "Appliquer",
        "s_reset": "Réinitialiser",
        "p_title": "PLAYLIST", "p_add": "+ AJOUTER", "p_close": "FERMER",
        "p_search": "Chercher:", "p_sort": "Trier:",
        "p_fav": "FAVORI", "p_remove": "RETIRER", "p_clear": "VIDER",
        "p_export": "EXPORT .m3u", "p_import": "IMPORT .m3u",
        "p_tab_all": "Tout", "p_tab_fav": "Favoris", "p_tab_recent": "Récents",
        "p_edit_tags": "Éditer tags",
        "d_about": "À propos",
        "d_error": "Erreur", "d_notfound": "Fichier introuvable:\n",
        "d_loaderr": "Échec du chargement:\n", "d_clearq": "Supprimer toutes les pistes?",
        "d_exp": "Export", "d_imp": "Import", "d_saved": "Enregistré: ",
        "d_tags_title": "ÉDITER LES TAGS",
        "d_tags_artist": "Artiste:", "d_tags_title_f": "Titre:", "d_tags_album": "Album:",
        "d_tags_year": "Année:", "d_tags_genre": "Genre:", "d_tags_save": "ENREGISTRER",
        "d_tags_cancel": "ANNULER",
        "ab_about": "À PROPOS", "ab_credits": "REMERCIEMENTS", "ab_faq": "FAQ", "ab_stats": "STATS",
        "about_body": (
            "SCARLI-MUSIC — un lecteur audio léger.\n\n"
            "Écrit en Python 3.14 avec tkinter et pygame-ce.\n\n"
            "Philosophie:\n"
            "  · 100% local — pas d'hébergement, pas de cloud\n"
            "  · Aucune télémétrie, aucun suivi\n"
            "  · Léger et rapide\n\n"
            "© 2026 · SCARLI-MUSIC"
        ),
        "credits_body": (
            "Merci à tous ceux qui ont soutenu le projet:\n\n"
            "· La communauté Python et pygame\n"
            "· Les auteurs de mutagen, Pillow, tkinterdnd2\n"
            "· Tous ceux qui ont signalé des bugs et proposé des idées\n"
            "· Toi — pour utiliser SCARLI-MUSIC\n\n"
            "github.com/ScarlLV/ScarliMusic"
        ),
        "stats_title": "STATISTIQUES",
        "stats_total": "Total écouté:",
        "stats_tracks": "Pistes jouées:",
        "stats_sessions": "Sessions:",
        "stats_top_artists": "Top artistes:",
        "stats_empty": "  (vide)",
    },
    "zh": {
        "no_track": "无曲目", "stopped": "已停止", "playing": "播放中",
        "paused": "暂停", "ready": "就绪",
        "open": "打开", "play": "播放", "pause": "暂停", "stop": "停止", "resume": "继续",
        "volume": "音量", "speed": "速度", "tape": "位置",
        "playlist": "播放列表", "fav": "收藏", "next": "下一首", "prev": "上一首",
        "coming_soon": "即将推出", "favorite": "已收藏",
        "m_file": "文件", "m_open": "打开...", "m_exit": "退出",
        "m_playlist": "播放列表", "m_show_pl": "显示播放列表",
        "m_add_pl": "添加到播放列表", "m_next": "下一首",
        "m_prev": "上一首", "m_theme": "主题",
        "m_settings": "设置", "m_settings_w": "设置", "m_about": "关于",
        "m_mini": "迷你播放器", "m_screenshot": "截图 (F12)",
        "s_title": "设置", "s_sound": "声音",
        "s_fadein": "淡入", "s_fadeout": "淡出",
        "s_gapless": "无间隙播放",
        "s_repeat": "循环与随机", "s_repeat_l": "循环:", "s_shuffle_l": "随机:",
        "s_visual": "外观", "s_clock": "显示时钟",
        "s_ticker": "滚动标题",
        "s_perf": "性能", "s_eco": "节能模式",
        "s_statscr": "静态滚动条",
        "s_winanim": "窗口打开动画",
        "s_ui": "界面", "s_ui_sounds": "点击音效",
        "s_stats": "收集统计",
        "s_theme": "主题", "s_lang": "语言", "s_close": "关闭",
        "s_tooltips": "提示",
        "s_apply": "应用",
        "s_reset": "重置",
        "p_title": "播放列表", "p_add": "+ 添加", "p_close": "关闭",
        "p_search": "搜索:", "p_sort": "排序:",
        "p_fav": "收藏", "p_remove": "移除", "p_clear": "清空",
        "p_export": "导出 .m3u", "p_import": "导入 .m3u",
        "p_tab_all": "全部", "p_tab_fav": "收藏", "p_tab_recent": "最近",
        "p_edit_tags": "编辑标签",
        "d_about": "关于",
        "d_error": "错误", "d_notfound": "未找到文件:\n",
        "d_loaderr": "加载失败:\n", "d_clearq": "删除所有曲目？",
        "d_exp": "导出", "d_imp": "导入", "d_saved": "已保存: ",
        "d_tags_title": "编辑标签",
        "d_tags_artist": "艺术家:", "d_tags_title_f": "标题:", "d_tags_album": "专辑:",
        "d_tags_year": "年份:", "d_tags_genre": "流派:", "d_tags_save": "保存",
        "d_tags_cancel": "取消",
        "ab_about": "关于", "ab_credits": "鸣谢", "ab_faq": "FAQ", "ab_stats": "统计",
        "about_body": (
            "SCARLI-MUSIC — 轻量级音频播放器。\n\n"
            "使用 Python 3.14 和 tkinter、pygame-ce 编写。\n\n"
            "理念：\n"
            "  · 100% 本地 — 无托管，无云\n"
            "  · 无遥测，无跟踪\n"
            "  · 轻巧快速\n\n"
            "© 2026 · SCARLI-MUSIC"
        ),
        "credits_body": (
            "感谢所有支持项目的人：\n\n"
            "· Python 和 pygame 社区\n"
            "· mutagen、Pillow、tkinterdnd2 的作者\n"
            "· 所有报告错误和提出建议的人\n"
            "· 你 — 使用 SCARLI-MUSIC\n\n"
            "github.com/ScarlLV/ScarliMusic"
        ),
        "stats_title": "统计", "stats_total": "总时长:",
        "stats_tracks": "播放曲目:", "stats_sessions": "会话:",
        "stats_top_artists": "热门艺术家:", "stats_empty": "  (空)",
    },
    "ja": {
        "no_track": "トラックなし", "stopped": "停止中", "playing": "再生中",
        "paused": "一時停止", "ready": "準備完了",
        "open": "開く", "play": "再生", "pause": "一時停止", "stop": "停止", "resume": "再開",
        "volume": "音量", "speed": "速度", "tape": "位置",
        "playlist": "プレイリスト", "fav": "お気に入り", "next": "次へ", "prev": "前へ",
        "coming_soon": "近日公開", "favorite": "お気に入り",
        "m_file": "ファイル", "m_open": "開く...", "m_exit": "終了",
        "m_playlist": "プレイリスト", "m_show_pl": "プレイリストを表示",
        "m_add_pl": "プレイリストに追加", "m_next": "次のトラック",
        "m_prev": "前のトラック", "m_theme": "テーマ",
        "m_settings": "設定", "m_settings_w": "設定", "m_about": "情報",
        "m_mini": "ミニプレーヤー", "m_screenshot": "スクリーンショット (F12)",
        "s_title": "設定", "s_sound": "サウンド",
        "s_fadein": "フェードイン", "s_fadeout": "フェードアウト",
        "s_gapless": "ギャップレス再生",
        "s_repeat": "リピート＆シャッフル", "s_repeat_l": "リピート:", "s_shuffle_l": "シャッフル:",
        "s_visual": "外観", "s_clock": "時計を表示",
        "s_ticker": "スクロールタイトル",
        "s_perf": "パフォーマンス", "s_eco": "エコモード",
        "s_statscr": "静的スクラバー",
        "s_winanim": "ウィンドウアニメ",
        "s_ui": "インターフェース", "s_ui_sounds": "クリック音",
        "s_stats": "統計を収集",
        "s_theme": "テーマ", "s_lang": "言語", "s_close": "閉じる",
        "s_tooltips": "ツールチップ",
        "s_apply": "適用",
        "s_reset": "リセット",
        "p_title": "プレイリスト", "p_add": "+ 追加", "p_close": "閉じる",
        "p_search": "検索:", "p_sort": "並び替え:",
        "p_fav": "お気に入り", "p_remove": "削除", "p_clear": "クリア",
        "p_export": "エクスポート .m3u", "p_import": "インポート .m3u",
        "p_tab_all": "すべて", "p_tab_fav": "お気に入り", "p_tab_recent": "最近",
        "p_edit_tags": "タグを編集",
        "d_about": "情報",
        "d_error": "エラー", "d_notfound": "ファイルが見つかりません:\n",
        "d_loaderr": "読み込みに失敗:\n", "d_clearq": "すべてのトラックを削除しますか？",
        "d_exp": "エクスポート", "d_imp": "インポート", "d_saved": "保存先: ",
        "d_tags_title": "タグを編集",
        "d_tags_artist": "アーティスト:", "d_tags_title_f": "タイトル:", "d_tags_album": "アルバム:",
        "d_tags_year": "年:", "d_tags_genre": "ジャンル:", "d_tags_save": "保存",
        "d_tags_cancel": "キャンセル",
        "ab_about": "情報", "ab_credits": "謝辞", "ab_faq": "FAQ", "ab_stats": "統計",
        "about_body": (
            "SCARLI-MUSIC — 軽量なオーディオプレーヤー。\n\n"
            "Python 3.14 と tkinter、pygame-ce で作成。\n\n"
            "哲学：\n"
            "  · 100% ローカル — ホスティングもクラウドもなし\n"
            "  · テレメトリもトラッキングもなし\n"
            "  · 軽くて速い\n\n"
            "© 2026 · SCARLI-MUSIC"
        ),
        "credits_body": (
            "プロジェクトを支援してくれたすべての人に感謝：\n\n"
            "· Python と pygame コミュニティ\n"
            "· mutagen、Pillow、tkinterdnd2 の作者\n"
            "· バグ報告やアイデアを送ってくれた皆さん\n"
            "· あなた — SCARLI-MUSIC を使ってくれてありがとう\n\n"
            "github.com/ScarlLV/ScarliMusic"
        ),
        "stats_title": "統計", "stats_total": "合計:",
        "stats_tracks": "再生したトラック:", "stats_sessions": "セッション:",
        "stats_top_artists": "トップアーティスト:", "stats_empty": "  (空)",
    },
    "be": {
        "no_track": "НЯМА ТРЭКА", "stopped": "СПЫНЕНА", "playing": "ПРАЙГРАВАННЕ",
        "paused": "ПАУЗА", "ready": "ГАТОВА",
        "open": "АДКРЫЦЬ", "play": "ГУЛЯЦЬ", "pause": "ПАУЗА", "stop": "СТОП", "resume": "ПРАЦЯГНУЦЬ",
        "volume": "ГУЧНАСЦЬ", "speed": "ХУТКАСЦЬ", "tape": "ПАЛАЖЭННЕ",
        "playlist": "ФАНАТЭКА", "fav": "АБРАНАЕ", "next": "ДАЛЕЙ", "prev": "НАЗАД",
        "coming_soon": "ХУТКА", "favorite": "У АБРАНЫМ",
        "m_file": "Файл", "m_open": "Адкрыць...", "m_exit": "Выхад",
        "m_playlist": "Фанатэка", "m_show_pl": "Паказаць фанатэку",
        "m_add_pl": "Занесці ў фанатэку", "m_next": "Наступны запіс",
        "m_prev": "Папярэдні запіс", "m_theme": "Афармленне",
        "m_settings": "Налады", "m_settings_w": "Налады", "m_about": "Аб праграме",
        "m_mini": "Міні-плэер", "m_screenshot": "Здымак (F12)",
        "s_title": "НАЛАДЫ", "s_sound": "ГУК",
        "s_fadein": "Плыўны пачатак", "s_fadeout": "Плыўнае затуханне",
        "s_gapless": "Без паўз",
        "s_repeat": "ПАЎТОР І ПЕРАМЯШВАННЕ", "s_repeat_l": "Паўтор:", "s_shuffle_l": "Перамяшванне:",
        "s_visual": "АФАРМЛЕННЕ", "s_clock": "Паказваць гадзіннік",
        "s_ticker": "Бягучы радок",
        "s_perf": "ПРАДУКЦЫЙНАСЦЬ", "s_eco": "Эканомны рэжым",
        "s_statscr": "Статычная шкала",
        "s_winanim": "Анімацыя адкрыцця",
        "s_ui": "ІНТЭРФЕЙС", "s_ui_sounds": "Гукі націску",
        "s_stats": "Збіраць статыстыку",
        "s_theme": "АФАРМЛЕННЕ", "s_lang": "МОВА", "s_close": "ЗАКРЫЦЬ",
        "s_tooltips": "Падказкі",
        "s_apply": "Ужыць",
        "s_reset": "Скінуць",
        "p_title": "ФАНАТЭКА", "p_add": "+ ДАДАЦЬ", "p_close": "ЗАКРЫЦЬ",
        "p_search": "Пошук:", "p_sort": "Сартаванне:",
        "p_fav": "У АБРАНАЕ", "p_remove": "ВЫДАЛІЦЬ", "p_clear": "АЧЫСЦІЦЬ",
        "p_export": "ЭКСПАРТ .m3u", "p_import": "ІМПАРТ .m3u",
        "p_tab_all": "Усе", "p_tab_fav": "Абранае", "p_tab_recent": "Нядаўнія",
        "p_edit_tags": "Правіць тэгі",
        "d_about": "Аб праграме",
        "d_error": "Памылка", "d_notfound": "Файл не знойдзены:\n",
        "d_loaderr": "Не ўдалося загрузіць:\n", "d_clearq": "Выдаліць усе запісы?",
        "d_exp": "Экспарт", "d_imp": "Імпарт", "d_saved": "Захавана: ",
        "d_tags_title": "ПРАЎКА ТЭГАЎ",
        "d_tags_artist": "Выканаўца:", "d_tags_title_f": "Назва:", "d_tags_album": "Альбом:",
        "d_tags_year": "Год:", "d_tags_genre": "Жанр:", "d_tags_save": "ЗАХАВАЦЬ",
        "d_tags_cancel": "СКАСАВАЦЬ",
        "ab_about": "АБ ПРАГРАМЕ", "ab_credits": "ПАДЗЯКІ", "ab_faq": "FAQ", "ab_stats": "СТАТЫСТЫКА",
        "about_body": (
            "SCARLI-MUSIC — лёгкі музычны плэер.\n\n"
            "Напісаны на Python 3.14 з tkinter і pygame-ce.\n\n"
            "Філасофія:\n"
            "  · 100% лакальна — без хосцінгу і воблака\n"
            "  · Без тэлеметрыі і сачэння\n"
            "  · Лёгкі і хуткі\n\n"
            "© 2026 · SCARLI-MUSIC"
        ),
        "credits_body": (
            "Дзякуй усім, хто падтрымліваў праект:\n\n"
            "· Супольнасці Python і pygame\n"
            "· Аўтарам mutagen, Pillow, tkinterdnd2\n"
            "· Усім, хто дасылаў баг-рэпорты і ідэі\n"
            "· Табе — за тое, што карыстаешся SCARLI-MUSIC\n\n"
            "github.com/ScarlLV/ScarliMusic"
        ),
        "stats_title": "СТАТЫСТЫКА",
        "stats_total": "Усяго праслухана:",
        "stats_tracks": "Запісаў прайграна:",
        "stats_sessions": "Сесій:",
        "stats_top_artists": "Топ выканаўцаў:",
        "stats_empty": "  (пакуль пуста)",
    },
}


_current_lang = "en"


def set_lang(code: str) -> None:
    global _current_lang
    if code in LANG:
        _current_lang = code
    else:
        _current_lang = "en"


def t(key: str) -> str:
    cur = LANG.get(_current_lang) or LANG["en"]
    return cur.get(key) or LANG["en"].get(key, key)


def current_lang() -> str:
    return _current_lang


def lang_display_name(code: str) -> str:
    return {
        "en": "ENGLISH", "ru": "РУССКИЙ", "ua": "УКРАЇНСЬКА",
        "de": "DEUTSCH", "fr": "FRANÇAIS",
        "zh": "中文", "ja": "日本語", "be": "БЕЛАРУСКАЯ",
    }.get(code, code.upper())


def all_langs():
    return ("en", "ru", "ua", "de", "fr", "zh", "ja", "be")


def faq_translated():
    """Возвращает FAQ, переведённые под текущий язык (если есть)."""
    cur = LANG.get(_current_lang) or LANG["en"]
    return cur.get("faq_items") or LANG["en"].get("faq_items") or []