import enum
import re
import zlib
from pathlib import Path
from time import time

BLOCK_SIZE = 2**16
CRC_IN_FILENAME_PATTERN = re.compile(r"(\[[A-F0-9]{8}\])", re.IGNORECASE)


class Status(enum.Enum):
    """Represents the different status a file processed can have"""

    SKIPPED = enum.auto()
    VERIFIED = enum.auto()
    COMPUTED = enum.auto()
    ERROR = enum.auto()


def get_available_file_path(directory: Path, filename: str, suffix: str) -> Path:
    """Returns available file path, adds ' (<idx>)' suffix to filename as needed"""
    i = 0
    while True:
        p: Path = directory / (
            filename + suffix if i == 0 else f"{filename} ({i}){suffix}"
        )
        if not p.exists():
            return p
        i += 1


def file_crc32(_file: Path) -> int:
    """Returns _file's digest
    code based on maxschlepzig's answer
      https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
    """
    b = bytearray(BLOCK_SIZE)
    mv = memoryview(b)
    digest: int = 0
    with _file.open("rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            digest = zlib.crc32(mv[:n], digest)  # data, value
    return digest


def filename_extract_crc(filename: str) -> tuple[str | None, str]:
    """Returns (<crc_if_found:str|None>, <filename_without_crc:str>)"""
    match = re.search(CRC_IN_FILENAME_PATTERN, filename)
    if not match:
        return None, filename
    a, b = match.span()
    return match.group(1)[1:-1], filename[:a] + filename[b:]


def verify_file(_file: Path, overwrite_digest_in_name: bool = False) -> Status:
    """Compute file's digest, then either checks integrity if file has digest in name
    or adds digest to name.

    Note: CRC in filename must be 8-character hexadecimal in square brackets (case insensitive)

    Integrity verification: Displays a warning message on mismatch of computed
    digest and the one found in name.

    `overwrite_digest_in_name`: If True, overwrite digest in name in cases of failed
    integrity verification.
    """
    start_t = time()
    digest = hex(file_crc32(_file))[2:].rjust(8, "0").upper()
    file_size_MB = _file.stat().st_size / 1_000_000
    performance_MBps = f"[{file_size_MB / (time() - start_t):0.1f}MB/s]"
    rename_target = False
    return_status = None
    digest_in_name, stem_without_digest = filename_extract_crc(_file.stem)
    if digest_in_name is None:
        # Case : no digest in filename => add it
        print(f"[COMPUTED] {_file.name} {performance_MBps}: computed CRC is {digest}")
        return_status = Status.COMPUTED
        rename_target = True
    elif digest == digest_in_name.upper():
        # Case : digest in filename AND digests match => verification ok, no renaming to do
        print(f"[VERIFIED] {_file.name} {performance_MBps}")
        return_status = Status.VERIFIED
    else:
        # Case : digest in filename AND digests don't match => verification failed, renaming to do conditionally
        print(
            f"[ERROR] {_file.name} {performance_MBps}: expected {digest_in_name.upper()}, computed {digest}"
        )
        return_status = Status.ERROR
        rename_target = overwrite_digest_in_name

    if rename_target:
        new_name = get_available_file_path(
            _file.parent, stem_without_digest + f" [{digest}]", _file.suffix
        )
        print(f"[RENAMING] '{_file.name}' -> '{new_name.name}'")
        _file.rename(new_name)

    return return_status
