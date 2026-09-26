"""
SCARLI-MUSIC — ID3 metadata reader/writer (via mutagen).
No cover art support (removed by design).
"""

import os


def read_tags(path: str) -> dict:
    """Возвращает dict с тегами. Пустые поля = пустая строка."""
    result = {
        "artist": "", "title": "", "album": "",
        "year": "", "genre": "", "duration": 0.0,
    }
    if not os.path.exists(path):
        return result
    try:
        from mutagen import File as MFile
        f = MFile(path)
        if f is None:
            return result
        if f.info is not None:
            try:
                result["duration"] = float(f.info.length)
            except Exception:
                pass
        if hasattr(f, "tags") and f.tags:
            def g(k):
                v = f.tags.get(k)
                if v is None:
                    return ""
                if isinstance(v, list):
                    return str(v[0])
                return str(v)
            result["artist"] = g("artist") or g("TPE1") or g("\xa9ART") or ""
            result["title"]  = g("title")  or g("TIT2") or g("\xa9nam") or ""
            result["album"]  = g("album")  or g("TALB") or g("\xa9alb") or ""
            result["year"]   = g("date")   or g("TDRC") or g("year")   or ""
            result["genre"]  = g("genre")  or g("TCON") or ""
    except Exception:
        pass
    return result


def write_tags(path: str, tags: dict) -> bool:
    """Пишет теги в файл. Возвращает True/False."""
    if not os.path.exists(path):
        return False
    try:
        from mutagen import File as MFile
        f = MFile(path)
        if f is None:
            return False
        if f.tags is None:
            f.add_tags()
        def setk(k, v):
            if v == "" or v is None:
                return
            try:
                f.tags[k] = v
            except Exception:
                try:
                    f.tags[k] = [v]
                except Exception:
                    pass
        setk("artist", tags.get("artist"))
        setk("title", tags.get("title"))
        setk("album", tags.get("album"))
        setk("date", tags.get("year"))
        setk("genre", tags.get("genre"))
        f.save()
        return True
    except Exception as e:
        print("write_tags error:", e)
        return False


def fmt_duration(sec: float) -> str:
    if not sec or sec <= 0:
        return "--:--"
    s = int(sec)
    return f"{s // 60:02d}:{s % 60:02d}"


def has_cover_support() -> bool:
    """Оставлено для совместимости — всегда False."""
    return False


def cover_to_photoimage(*args, **kwargs):
    """Оставлено для совместимости — всегда None."""
    return None