""" Utilities """

import logging
import os
import shutil
from typing import Tuple


log = logging.getLogger("i.utils")


def execution_time(duration: int) -> Tuple[int, int, int]:
    mins, secs = divmod(duration, 60)
    hours, mins = divmod(mins, 60)
    return hours, mins, secs


def is_directory(path: str) -> bool:
    log.debug(f"Does directory '{path}' exists?")
    return os.path.isdir(path)


def is_file(path: str) -> bool:
    log.debug(f"Does file '{path}' exist?")
    return os.path.isfile(path)


def mkdir(path: str):
    log.debug(f"Creating directory '{path}'")
    try:
        os.mkdir(path)
    except OSError as e:
        raise Exception(f"Failed to create destination directory {path}: {e}")


def copy(source_path: str, target_path: str):
    log.debug(f"Copying from {source_path} to {target_path}")
    try:
        shutil.copyfile(source_path, target_path)
    except OSError as e:
        log.error(f"Failed to move from {source_path} to {target_path}")


def get_extension(filepath: str) -> str:
    try:
        _, ext = os.path.splitext(filepath)
        return ext
    except OSError as e:
        log.error(f"Failed to get file extension for {filepath}")


def get_file_size(filepath: str) -> int:
    try:
        return os.path.getsize(filepath)
    except OSError as e:
        log.error(f"Failed to get file size for {filepath}")
