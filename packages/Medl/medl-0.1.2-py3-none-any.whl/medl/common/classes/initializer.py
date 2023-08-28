from .init import FfmpegInitializer, FolderInitializer

__all__ = ["Initializer"]


class Initializer:
    def __init__(self) -> None:
        pass

    def init(self) -> None:
        FfmpegInitializer.init()
        FolderInitializer.init()
