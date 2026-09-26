"""
SCARLI-MUSIC — theme (single, purple)
"""

THEMES = {
    "purple": {
        "label": "PURPLE",
        # Фон — глубокий тёмный с холодным оттенком
        "bg_body":      "#0e0b14",
        "bg_panel":     "#161122",
        "bg_screen":    "#0b0810",
        "bg_trough":    "#1f1730",
        # Акцент — насыщенный фиолетовый
        "accent":       "#a855f7",
        "accent_hover": "#c084fc",
        "accent_dim":   "#7c3aed",
        # Текст — высокий контраст
        "fg_main":      "#a855f7",
        "fg_dim":       "#6b6480",
        "fg_soft":      "#ece9f5",
        # Кнопки — поверхность + акцент
        "btn_bg":       "#1e1830",
        "btn_fg":       "#ece9f5",
        "btn_active":   "#2a2140",
        "btn_outline":  "#2a2140",
        # Рамки
        "frame":        "#241b38",
        # Крутилка
        "knob_bg":      "#181226",
        "knob_edge":    "#2a2140",
        "knob_line":    "#a855f7",
        "knob_dot":     "#a855f7",
        # Список
        "list_bg":      "#0b0810",
        "list_sel":     "#2a1e48",
        "list_fav":     "#a855f7",
        # Геометрия и шрифты
        "btn_radius":   16,
        "font_btn":     ("Segoe UI", 10, "bold"),
        "font_display": ("Segoe UI", 14, "bold"),
        "font_title":   ("Segoe UI", 20, "bold"),
        "font_small":   ("Segoe UI", 9),
    },
}


def get_theme(key):
    return THEMES.get(key, THEMES["purple"])


def all_theme_keys():
    return list(THEMES.keys())