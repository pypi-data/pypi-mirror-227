from typing import Any, Dict, List, Tuple
from ytmusicapi import YTMusic
from rapidfuzz import fuzz
from slugify import slugify

from mumee.data import SongMetadata, PlaylistMetadata
from mumee.errors import MetadataClientError

__all__ = ["YTMusicMetadataClient"]


class YTMusicMetadataClient:
    def __init__(self) -> None:
        self._client = YTMusic()

    def get_track(self, url: str) -> SongMetadata:
        if "music.youtube.com" not in url or "watch?v" not in url:
            raise MetadataClientError(f"Invalid Youtube Music track URL: {url}")

        start_index = url.find("?v=") + len("?v=")
        end_index = url.find("&", start_index) if url.find("&", start_index) >= 0 else None
        track_info = self._client.get_song(url[start_index:end_index])

        if not track_info or track_info["playabilityStatus"]["status"] == "ERROR":
            raise MetadataClientError(
                f"Couldn't get metadata associated with this URL: {url}"
            )

        track_data = self.search(
            f"{track_info['videoDetails']['title']} - {track_info['videoDetails']['author']}",
            1,
            True,
        )
        return track_data[0]

    def get_playlist(self, url: str) -> PlaylistMetadata:
        if "music.youtube.com" not in url or "playlist?list" not in url:
            raise MetadataClientError(f"Invalid Youtube Music playlist URL: {url}")

        start_index = url.find("?list=") + len("?list=")
        end_index = url.find("&", start_index) if url.find("&", start_index) >= 0 else None
        playlist_info = self._client.get_playlist(url[start_index:end_index], None)  # type: ignore

        if not playlist_info:
            raise MetadataClientError(
                f"Couldn't get metadata associated with this URL: {url}"
            )

        result = PlaylistMetadata(
            name=playlist_info["title"],
            description=playlist_info["description"],
            author=playlist_info["author"]["name"],
            tracks=[
                self.search(
                    f"{track['title']} - {', '.join([artist['name'] for artist in track['artists']])}",
                    1,
                    True,
                )[0]
                for track in playlist_info["tracks"]
            ],
        )
        return result

    def search(self, query: str, limit: int, sorted: bool) -> List[SongMetadata]:
        search_results = self._client.search(query, "songs", limit=limit)

        if search_results is None or len(search_results) == 0:
            raise MetadataClientError(f"No result found for '{query}'")

        if sorted:
            best_results = self._get_best_results(query, search_results, limit)

            if not best_results or best_results[0][2] < 55:
                raise MetadataClientError(
                    "Best match found isn't close enough to your query. "
                    f"Best match : {best_results[0][1]}, query: {query}"
                )

            results = list(map(lambda r: r[0], best_results))
        else:
            results = search_results

        track_infos = [self._dict_to_song(track) for track in results]
        return track_infos

    def _get_best_results(
        self, query: str, tracks_info: List[Dict[str, Any]], limit: int
    ) -> List[Tuple[Dict[str, Any], str, float, bool]]:
        track_infos: List[Tuple[Dict[str, Any], str, float, bool]] = []

        for track in tracks_info:
            track_name = track["title"]
            track_artists = [artist["name"] for artist in track["artists"]]
            track_query = f"{track_name} - {', '.join(track_artists)}"
            track_has_album = (
                track["album"] is not None and track["album"]["id"] is not None
            )

            score = fuzz.ratio(slugify(track_query), slugify(query))

            track_infos.append((track, track_query, score, track_has_album))

        track_infos = sorted(track_infos, key=lambda t: (t[2], t[3]), reverse=True)

        return track_infos[:limit]

    def _dict_to_song(self, track_info: Dict[str, Any]) -> SongMetadata:
        if track_info.get("album", {}).get("id") is not None:
            album_info = self._client.get_album(track_info["album"]["id"])
        else:
            album_info = None

        thumbnails = [
            (tn["width"] * tn["height"], tn["url"])
            for tn in (album_info if album_info else track_info)["thumbnails"]
        ]

        result = SongMetadata(
            name=track_info["title"],
            artists=[artist["name"] for artist in track_info["artists"]],
            artist=track_info["artists"][0]["name"],
            album_name=album_info["title"] if album_info is not None else None,
            album_artist=album_info["artists"][0]["name"]
            if album_info is not None
            else None,
            disc_number=None,
            disc_count=None,
            track_number=[
                idx
                for idx, track in enumerate(album_info["tracks"])
                if fuzz.ratio(track["title"], track_info["title"]) > 80
            ][0]
            if album_info is not None
            else None,
            track_count=album_info["trackCount"] if album_info is not None else None,
            genres=[],
            duration=track_info["duration_seconds"],
            date=None,
            year=int(album_info["year"]) if album_info is not None else None,
            explicit=track_info["isExplicit"],
            cover_url=max(thumbnails)[1],
            is_song=track_info["resultType"] == "song",
            id=track_info["videoId"],
            url=f"https://{'music' if track_info['resultType'] == 'song' else 'www'}.youtube.com/watch?v={track_info['videoId']}",
        )
        return result
