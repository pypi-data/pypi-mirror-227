from taipan_di import ServiceCollection

from medl.common import add_common
from medl.main.di import add_main
from medl.main.classes import MusicToolbox
from medl.common.classes.init import FfmpegInitializer, FolderInitializer


def main():
    FolderInitializer().init()
    FfmpegInitializer().init()

    services = ServiceCollection()
    add_common(services)
    add_main(services)

    provider = services.build()
    toolbox = provider.resolve(MusicToolbox)

    queries = [
        "faint - linkin park",
        "https://music.youtube.com/watch?v=ymo9oX83kJI",
        "https://open.spotify.com/track/5BVNXl23xEtFgsKmbKpYfA?si=d738d02b327142c4",
        "https://music.youtube.com/playlist?list=PLNvqJjX5l6qVcR7mriyRcQjTBw4QGdX1s&feature=share",
    ]
    toolbox.search_and_download(queries)


main()
