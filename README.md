# muziq

A simple music utility to construct folder/ file style playlists from Apple Music's XML library file for my Toyota 4Runner.

## Pre-Requisites
Make sure you have the following installed:
* Python 3+

Use the following command to install dependencies from 'package.json'
```bash
make install
```

## Usage
```bash
(muziq) λ  muziq git:(main) ✗ muziq -h
usage: muziq [-h] -x XML_FILE -t TARGET_DIRECTORY [-f FILTER] [-e EXCLUDE_PLAYLISTS] [--debug] [--damnit]

A simple music utility to construct folder/ file style playlists for my 4Runner

optional arguments:
  -h, --help            show this help message and exit
  -x XML_FILE, --xml-file XML_FILE
                        Apple Music's exported file to be processed
  -t TARGET_DIRECTORY, --target-directory TARGET_DIRECTORY
                        The root directory where playlist folders will be generated
  -f FILTER, --filter FILTER
                        Specify a particular playlist to export
  -e EXCLUDE_PLAYLISTS, --exclude-playlists EXCLUDE_PLAYLISTS
                        Specify playlist names to be excluded
  --debug               For verbose logging
  --damnit              Perform the operation
```
