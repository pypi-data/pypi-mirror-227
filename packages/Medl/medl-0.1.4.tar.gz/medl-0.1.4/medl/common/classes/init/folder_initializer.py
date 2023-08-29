from medl.common import TEMP_MUSIC_PATH, MEDL_PATH

__all__ = ["FolderInitializer"]


class FolderInitializer:
    @classmethod
    def init(cls):
        if not MEDL_PATH.exists():
            MEDL_PATH.mkdir()
        if not TEMP_MUSIC_PATH.exists():
            TEMP_MUSIC_PATH.mkdir()
