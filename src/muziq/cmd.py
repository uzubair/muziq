"""  Console entrypoint """

import logging
import os
import timeit
from argparse import ArgumentParser
from muziq.parser import XMLParser
from muziq.utils import execution_time, environ_or_required, environ_or_optional
from muziq.fmanager import FileManager

log = logging.getLogger("i.cmd")


def run(args):
    """Perform the actual operation"""
    xml_parser = XMLParser(
        args.xml_file, args.exclude_playlists, args.filter, args.debug
    )
    playlists = xml_parser.process_xml()
    if not playlists:
        log.info(f"Exiting! Playlist is empty")
        return

    file_manager = FileManager(args.target_directory, args.debug, args.damnit)
    file_manager.process_playlists(playlists)


def main():
    """Entrypoint"""
    start_time = timeit.default_timer()

    if "DEBUG" in os.environ:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    parser = ArgumentParser(
        description="A simple music utility to construct folder/ file style playlists for my 4Runner"
    )
    parser.add_argument(
        "-x",
        "--xml-file",
        help="Apple Music's exported file to be processed",
        **environ_or_required("XML_FILE"),
    )
    parser.add_argument(
        "-t",
        "--target-directory",
        help="The root directory where playlist folders will be generated",
        **environ_or_required("TARGET_DIRECTORY"),
    )
    parser.add_argument(
        "-f",
        "--filter",
        default=[],
        help="Specify a particular playlist to export",
        **environ_or_optional("FILTER"),
    )
    parser.add_argument(
        "-e",
        "--exclude-playlists",
        default=["Library", "Downloaded", "Music"],
        help="Specify playlist names to be excluded",
        **environ_or_optional("EXCLUDE_PLAYLISTS"),
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="For verbose logging",
        **environ_or_optional("DEBUG"),
    )
    parser.add_argument(
        "--damnit",
        action="store_true",
        default=False,
        help="Perform the operation",
        **environ_or_optional("DAMNIT"),
    )

    args = parser.parse_args()

    try:
        run(args)
    except Exception as e:
        log.error(f"An error occurred while exporting playlists: {e}")

    duration = timeit.default_timer() - start_time
    hours, mins, secs = execution_time(duration)
    log.info("Done in %d:%d:%.2f" % (hours, mins, secs))
