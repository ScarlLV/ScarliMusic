"""
SCARLI-MUSIC — update checker via GitHub API.
Сверяет текущую версию с последним релизом на GitHub.
"""
import urllib.request
import json
from packaging.version import parse as vparse  # не нужен, делаем вручную

GITHUB_REPO = "ScarlLV/ScarliMusic"


def check(current_version: str) -> dict:
    """
    Возвращает:
      {"ok": bool, "new_version": str, "url": str, "error": str}
    """
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        req = urllib.request.Request(url, headers={"User-Agent": "ScarliMusic"})
        with urllib.request.urlopen(req, timeout=6) as r:
            data = json.loads(r.read().decode("utf-8"))
        tag = (data.get("tag_name") or "").lstrip("vV")
        html_url = data.get("html_url", "")
        if not tag:
            return {"ok": False, "error": "no tag"}
        if _is_newer(tag, current_version):
            return {"ok": True, "new_version": tag, "url": html_url}
        return {"ok": True, "new_version": "", "url": html_url}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _is_newer(remote: str, current: str) -> bool:
    try:
        r = [int(x) for x in remote.split(".")[:3]]
        c = [int(x) for x in current.split(".")[:3]]
        while len(r) < 3: r.append(0)
        while len(c) < 3: c.append(0)
        return tuple(r) > tuple(c)
    except Exception:
        return False