# [crctools](https://github.com/DavidRodriguezSoaresCUI/crctools) - A simple tool to check file integrity using CRC32 hash in filename

Having the hash of files in their name makes it so much easier to:
- keep track of their integrity
- deduplicate files
- probably more

This is intended to be a simple to use command-line utility to:
- add CRC32 hash into filename in a widely recognised format (suffix with 8 hex uppercase characters in square brackets)
- verify integrity of files based on hash in file name
- update hash in name

## Requirements

This project was developed for Python 3.10 and may not work on lower versions.

## Installation

From a terminal execute:

```bash
python -m pip install crctools-DavidRodriguezSoaresCUI
```

On some systems it may be necessary to specify python version as `python3`

## Usage

```bash
$> python -m crctools --help
usage: __main__.py [-h] [--skip_verify] [--overwrite] [--recursive] [--extensions [EXTENSIONS ...]]
                   [--min_size MIN_SIZE] [--debug]
                   PATH

positional arguments:
  PATH                  Can be file path or directory (all files in directory will be processed)

options:
  -h, --help            show this help message and exit
  --skip_verify         Skip verification; only process files with no hash in filename
  --overwrite           Overwrite CRC in filename when verification fails
  --recursive           (Only with PATH a directory) Enables recursive search for files to verify
  --extensions [EXTENSIONS ...]
                        Restrict files to process with extension whitelist (default: no restriction;
                        you may list extensions with leading dot separator)
  --min_size MIN_SIZE   Restrict files to ones of at least <min_size> bytes (default: 0)
  --debug               Debug mode (undocumented on purpose)
```

Example: Check large (>10MB) video files in directory `D:\Videos` (and subdirectories) :
```
python -m crctools "D:\Vidéos" --recursive --extensions mkv mp4 --min_size 10000000
```

Note: these are all equivalent:
- `--extensions mkv mp4`
- `--extensions .mkv .mp4`
- `--extensions MKV MP4`
- `--extensions .MKV .MP4`
