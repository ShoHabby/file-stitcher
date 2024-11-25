from __future__ import annotations

import os
import multiprocessing
import subprocess
import sys
from enum import Enum
from itertools import repeat
from os import DirEntry, path
from pathlib import Path
from typing import List

class Direction(str, Enum):
    VERTICAL   = "-append"
    HORIZONTAL = "+append"

    def __str__(self) -> str:
        return self.name.title()

    @staticmethod
    def from_arg(arg: str) -> Direction | None:
        match arg:
            case "-v":
                return Direction.VERTICAL
            case "-h":
                return Direction.HORIZONTAL
            case _:
                return None


def main() -> None:
    # Don't want the script path
    args: List[str] = sys.argv[1:]
    # Get direction
    direction: Direction | None = None
    match args:
        case [] | ["help"]:
            show_help()
            return
        case [str(arg), *rest]:
            direction = Direction.from_arg(arg)
            args = rest

    if direction is None:
        invalid_args()
        return

    subdirs: bool = False
    reverse: bool = direction == Direction.HORIZONTAL    # Horizontal defaults to reversed
    output: str | None = None
    while len(args) > 0 and len(args[0]) == 2 and args[0].startswith('-'):
        match args[0]:
            case "-a":
                subdirs = True
                args.pop(0)
            case "-r":
                reverse = not reverse
                args.pop(0)
            case "-o" if len(args) >= 2:
                output = args[1]
                args = args[2:]
            case _:
                invalid_args()
                return

    if subdirs:
        # Invalid state
        if len(args) != 0:
            invalid_args()
        else:
            stitch_all_subdirs(direction, reverse, "" if output is None else output)
    elif len(args) >= 2:
        stitch_files(args, direction, reverse, output)
    else:
        invalid_args()

def stitch_all_subdirs(direction: Direction, reverse: bool, prefix: str) -> None:
    print(f"{direction} stitching of all subfolders...")
    cwd: str = os.getcwd()
    subdirs: List[str] = [entry.name for entry in os.scandir(cwd) if is_valid_dir(entry)]
    with multiprocessing.Pool() as pool:
        pool.starmap(stitch_subdir, zip(subdirs, repeat(direction.value), repeat(reverse), repeat(prefix)))

def is_valid_dir(entry: DirEntry[str]) -> bool:
    return entry.is_dir() and any(f.is_file() and f.name.endswith(".png") for f in os.scandir(entry.path))

def stitch_subdir(subdir: str, mode: str, reverse: bool, prefix: str) -> None:
    command: List[str] = ["magick", f"{subdir}/*.png", mode, f"{prefix}{subdir}.png"]
    if reverse:
        command.insert(3, "-reverse")
    subprocess.call(command)
    print(f"Folder {path.join(os.getcwd(), subdir)} stitched to file {subdir}.png")

def stitch_files(files: List[str], direction: Direction, reverse: bool, output: str | None) -> None:
    print(f"{direction} stitching of specified files...")
    if not all(path.isfile(f) and f.endswith(".png") for f in files):
        print("Invalid files passed, aborting")
        return
    if output is None:
        output = "-".join(Path(path.basename(f)).stem for f in files)
    command: List[str] = ["magick", *files, direction.value, f"{output}.png"]
    if reverse:
        command.insert(-2, "-reverse")
    subprocess.call(command)
    print(f"Files stitched to file {output}.png")

def show_help() -> None:
    print("File stitcher help")
    print("Usage: stitcher [-v|-h] [-a] [-r] [-o %output_name%] [*files to stitch]")
    print("-v:   Vertical file stitching, up to down order by default")
    print("-h:   Horizontal file stitching, right to left order by default")
    print("-a:   Stitch files in all subfolders together, if this is used, files should not be specified")
    print("-r:   Reverse file order while stitching")
    print("-o:   Specifies the a prefix for all output files when -a is passed, otherwise specifies the name of the output file")
    print("help: Show this message")

def invalid_args() -> None:
    print("Invalid program arguments")
    show_help()


if __name__ == "__main__":
    main()
