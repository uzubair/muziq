from dataclasses import dataclass
import logging
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional

from muziq.utils import is_file


log = logging.getLogger("i.parser")


class Track(object):
    """Track class stores track info"""

    def __init__(
        self,
        track_id: int = -1,
        name: str = None,
        genre: str = "Other",
        size: int = -1,
        location: str = None,
    ):
        self._track_id = track_id
        self._name = name
        self._genre = genre
        self._size = size
        self._location = location

    @property
    def track_id(self) -> int:
        return self._track_id

    @track_id.setter
    def track_id(self, track_id):
        self._track_id = track_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def genre(self) -> str:
        return self._genre

    @genre.setter
    def genre(self, genre):
        self._genre = genre

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, location):
        self._location = location

    def __repr__(self):
        return f"Id={self._track_id}, Name={self._name}, Genre={self._genre}, Size={self._size}, Location={self._location}"


@dataclass
class Playlist(object):
    """Playlist class stores playlist info"""

    def __init__(self, name: str = None, tracks: List[Track] = []):
        self._name = name
        self._tracks = tracks

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def tracks(self) -> List[Track]:
        return self._tracks

    @tracks.setter
    def tracks(self, tracks: List[Track]):
        self._tracks = tracks

    def __repr__(self):
        return f"Name={self._name}, Tracks={self._tracks}"


class XMLParser(object):
    """A wrapper class to parse Apple Music's XML file"""

    def __init__(
        self,
        xml_file: str,
        exclude_playlists: List[str],
        filter: List[str],
        debug: bool,
    ):
        self._xml_file = xml_file
        self._exclude_playlists = exclude_playlists
        self._filter = filter
        self._debug = debug

    def _get_tracks(self, tracks: Any) -> Dict[int, Track]:
        """Get all the tracks in the library"""
        tracks_db = {}
        _tracks = tracks[0].findall('./dict/dict/[key="Track ID"]')

        for track in _tracks:
            _track = self._get_track(track)
            if not _track:
                continue
            tracks_db[_track.track_id] = _track

        log.info(f"Found {len(tracks_db)} tracks")
        return tracks_db

    def _get_track(self, track: Any) -> Optional[Track]:
        """Get track information"""
        _track: Track = Track()
        i = 0
        while i < len(track):
            if track[i].tag == "key" and track[i].text == "Track ID":
                _track.track_id = track[i + 1].text
            if track[i].tag == "key" and track[i].text == "Name":
                _track.name = track[i + 1].text
            if track[i].tag == "key" and track[i].text == "Genre":
                _track.genre = track[i + 1].text
            if track[i].tag == "key" and track[i].text == "Size":
                _track.size = track[i + 1].text
            if track[i].tag == "key" and track[i].text == "Location":
                _track.location = track[i + 1].text
            i = i + 1
        return _track

    def _get_playlist(
        self, playlist: Any, tracks_db: Dict[int, Track]
    ) -> Optional[Playlist]:
        """Get playlist information"""
        _playlist: Playlist = Playlist()

        # Get name of the playlist
        i = 0
        while i < len(playlist):
            if playlist[i].tag == "key" and playlist[i].text == "Name":
                _playlist.name = playlist[i + 1].text
            i += 1

        # We do not need to further process the tracks in the playlist
        # if it is in the excluded list
        if _playlist.name in self._exclude_playlists:
            log.info(f"Excluding playlist {_playlist.name}")
            return None

        if self._filter and _playlist.name not in self._filter:
            log.info(
                f"Applying filter '{self._filter}'. Omitting playlist '{_playlist.name}"
            )
            return None

        # Get the tracks for the playlist
        track_ids = playlist.findall("./array/dict/integer")
        _playlist.tracks = []
        for id in track_ids:
            track = tracks_db.get(id.text)
            if not track:
                continue
            _playlist.tracks.append(track)
        return _playlist

    def _get_playlists(
        self, playlists: Any, tracks_db: Dict[int, Track]
    ) -> Dict[int, Playlist]:
        """Get all the playlists in the library"""
        playlist_db = []
        _playlists = playlists[0].findall("./array/dict/[key='Playlist ID']")

        for playlist in _playlists:
            _playlist = self._get_playlist(playlist, tracks_db)
            if not _playlist:
                continue
            playlist_db.append(_playlist)

        log.info(f"Found {len(playlist_db)} playlists")
        return playlist_db

    def process_xml(self):
        log.info(f"Starting to process library file '{self._xml_file}'")
        if not is_file(self._xml_file):
            log.info(f"{self._xml_file} does not exist")
            return
        try:
            tree = ET.parse(self._xml_file)
            root = tree.getroot()

            tracks = root.findall(".//dict/[key='Tracks']")
            tracks_db = self._get_tracks(tracks)
            if not tracks_db:
                log.info(f"Exiting! No tracks found!")
                return

            playlists = root.findall(".//dict/[key='Playlists']")
            playlist_db = self._get_playlists(playlists, tracks_db)
            if not playlist_db:
                log.info(f"Exiting! No playlist information found!")
            return playlist_db
        except ET.ParseError as e:
            raise Exception(f"ET.ParseError {e}")
