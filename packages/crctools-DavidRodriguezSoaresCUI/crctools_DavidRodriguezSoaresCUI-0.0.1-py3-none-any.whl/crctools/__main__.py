import argparse
import json
import time
from collections import defaultdict
from pathlib import Path

from .utils import Status, get_available_file_path, verify_file

CWD = Path(".").resolve()


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "PATH",
        help="Can be file path or directory (all files in directory will be processed)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite CRC in filename when verification fails",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="(Only with PATH a directory) Enables recursive search for files to verify",
    )
    parser.add_argument(
        "--extensions",
        action="store",
        nargs="*",
        help="Restrict files to process with extension whitelist (default: no restriction; you may list extensions with leading comma)",
    )
    parser.add_argument(
        "--min_size",
        action="store",
        type=int,
        default=0,
        help="Restrict files to ones of at least <min_size> bytes (default: 0)",
    )
    return parser.parse_args()


def _process_file(
    _file: Path,
    args: argparse.Namespace,
    processed_files_by_status: dict[Status, list[Path]],
) -> None:
    """Filters files against extension list and min size if given, then computes hash and puts hash in file name.
    If hash is already in filename, verifies it"""
    has_valid_extension = (
        args.extensions is None or _file.suffix.upper() in args.extensions
    )
    if not has_valid_extension:
        print(
            f"[SKIPPED] {_file}: extension '{_file.suffix.upper()}' not in {args.extensions}"
        )
        processed_files_by_status[Status.SKIPPED].append(_file)
        return
    file_large_enough = args.min_size == 0 or _file.stat().st_size >= args.min_size
    if not file_large_enough:
        print(
            f"[SKIPPED] {_file}: file of size {_file.stat().st_size} lower than bound {args.min_size}"
        )
        processed_files_by_status[Status.SKIPPED].append(_file)
        return
    return_status = verify_file(_file, args.overwrite)
    processed_files_by_status[return_status].append(_file)


def process_file(
    _file: Path,
    args: argparse.Namespace,
    processed_files_by_status: dict[Status, list[Path]],
) -> None:
    """Catches errors from process_file execution"""
    try:
        process_file(_file, args, processed_files_by_status)
    except Exception as e:
        print(f"[ERROR] {_file.name}: something went wrong\n{e}")
        processed_files_by_status[Status.ERROR].append(_file)


def process_dir(
    _dir: Path,
    args: argparse.Namespace,
    processed_files_by_status: dict[Status, list[Path]],
) -> None:
    """Process files in directory; recursive search if --recursive given"""
    search = _dir.rglob if args.recursive else _dir.glob
    for item in search(pattern="*"):
        if item.is_file():
            process_file(item, args, processed_files_by_status)


def main() -> None:
    # Get arguments
    args = get_args()
    if args.overwrite:
        print("WARNING: Overwriting hash in name enabled")

    # Process file(s)
    _path = Path(args.PATH).resolve()
    processed_files_by_status: dict[Status, list[Path]] = defaultdict(list)
    if not _path.exists():
        raise FileNotFoundError(f"Couldn't find a file or directory at '{_path}'")
    if _path.is_dir():
        process_dir(_path, args, processed_files_by_status)
    elif _path.is_file():
        process_file(_path, args, processed_files_by_status)
    else:
        raise ValueError(
            f"Unhandled case: Path '{_path}' exists but is neither a directory or a file"
        )

    # Save report to file
    json_report_file = get_available_file_path(
        CWD, time.strftime("%Y%m%d-%H%M%S"), "json"
    )
    print(f"Saving execution report to {json_report_file.name}")
    with json_report_file.open("w", encoding="utf8") as f:
        json.dump(processed_files_by_status, f, default=str, indent=2)


if __name__ == "__main__":
    main()
