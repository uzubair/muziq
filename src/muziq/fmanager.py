import logging
import os
import urllib.request
import math
import re
from typing import List

from muziq.parser import Playlist, Track
from muziq.utils import mkdir, is_directory, is_file, copy, get_extension, get_file_size


log = logging.getLogger("i.fmanager")


class FileManager(object):
    """A wrapper class to help make the playlist"""

    def __init__(self, target_directory: str, debug: bool, damnit: bool):
        self._target_directory = target_directory
        self._debug = debug
        self._damnit = damnit

    def _sanitize_name(self, name: str) -> str:
        _name = name.replace("?", "")
        _name = _name.replace("<", "")
        _name = _name.replace(">", "")
        _name = _name.replace("*", "")
        _name = _name.replace(",", "")
        _name = _name.replace("|", "")
        _name = _name.replace("^", "")
        _name = _name.replace(";", "")
        _name = _name.replace("&", "")
        return _name

    def _make_playlist(self, name: str, tracks: List[Track]):
        playlist_directory = os.path.join(self._target_directory, name)
        if self._damnit:
            if not is_directory(playlist_directory):
                mkdir(playlist_directory)
        num_of_tracks = len(tracks)
        if num_of_tracks < 1:
            return
        num_digits = int(math.log10(num_of_tracks)) + 1
        for idx, track in enumerate(tracks, 1):
            sanitized_name = self._sanitize_name(track.name)
            log.info(
                f'[{idx:0{num_digits}d}/{num_of_tracks}]: Processing track "{sanitized_name}"'
            )

            source_filepath = urllib.request.url2pathname(track.location).replace(
                "file://", ""
            )
            if not is_file(source_filepath):
                log.info(f"Warning: {source_filepath} not found")
                continue
            source_file_size = get_file_size(source_filepath)
            source_file_extension = get_extension(source_filepath)

            new_filename = f"{sanitized_name}{source_file_extension}"
            if not re.search("^[0-9]", new_filename):
                new_filename = f"{idx:0{num_digits}d} - {new_filename}"
            new_filepath = os.path.join(playlist_directory, new_filename)
            if is_file(new_filepath):
                new_file_size = get_file_size(new_filepath)
                if source_file_size == new_file_size:
                    continue
            copy(source_filepath, new_filepath)

    def process_playlists(self, playlists: List[Playlist]):
        if self._damnit:
            if not is_directory(self._target_directory):
                mkdir(self._target_directory)
        num_of_playlists = len(playlists)
        num_digits = int(math.log10(num_of_playlists)) + 1
        for idx, playlist in enumerate(playlists, 1):
            sanitized_name = self._sanitize_name(playlist.name)
            log.info(
                f'[{idx:0{num_digits}d}/{num_of_playlists}]: Processing playlist "{sanitized_name}"'
            )
            self._make_playlist(sanitized_name, playlist.tracks)
