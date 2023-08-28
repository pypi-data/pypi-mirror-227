from taipan_di import ServiceCollection

from mumee.classes import (
    SpotifyOptions,
    SpotifyMetadataClient,
    YTMusicMetadataClient,
)
from mumee.classes.handlers import *
from mumee.interfaces import BaseMetadataClient, BaseMetadataExplorer

__all__ = ["add_mumee"]


def add_mumee(services: ServiceCollection) -> ServiceCollection:
    services.register(SpotifyOptions).as_singleton().with_self()

    services.register(SpotifyMetadataClient).as_singleton().with_self()
    services.register(YTMusicMetadataClient).as_singleton().with_self()

    services.register_pipeline(BaseMetadataClient).add(SpotifyTrackHandler).add(
        SpotifyPlaylistHandler
    ).add(YTMusicTrackHandler).add(YTMusicPlaylistHandler).add(SpotifySearchHandler).add(
        YTMusicSearchHandler
    ).as_factory()

    services.register_pipeline(BaseMetadataExplorer).add(SpotifyExplorerHandler).add(
        YTMusicExplorerHandler
    ).as_factory()

    return services
