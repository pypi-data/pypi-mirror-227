import static_ffmpeg

__all__ = ["FfmpegInitializer"]


class FfmpegInitializer:
    @classmethod
    def init(cls):
        result = static_ffmpeg.add_paths()
