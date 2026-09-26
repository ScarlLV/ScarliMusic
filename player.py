"""
SCARLI-MUSIC — player (pygame only)
"""
import pygame


class Player:
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        self.track_path = None
        self.state = "STOPPED"
        self.duration_s = 0.0
        self.seek_base = 0.0
        self.target_volume = 0.5
        pygame.mixer.music.set_volume(self.target_volume)

    def load(self, path):
        pygame.mixer.music.load(path)
        self.track_path = path
        self.state = "STOPPED"
        self.duration_s = self._probe(path)
        self.seek_base = 0.0

    def _probe(self, path):
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
        pygame.mixer.music.set_volume(self.target_volume)
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
        try:
            if self.state == "PLAYING":
                pygame.mixer.music.play(start=target)
                pygame.mixer.music.set_volume(self.target_volume)
            else:
                self.seek_base = target
                return
        except Exception:
            return
        self.seek_base = target

    def cleanup(self):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception:
            pass