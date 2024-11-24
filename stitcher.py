import os
import multiprocessing
import subprocess
import sys
from enum import Enum, auto
from itertools import repeat
from os import DirEntry, path
from pathlib import Path
from typing import List


class Direction(Enum):
    VERTICAL   = auto()
    HORIZONTAL = auto()

    def __str__(self) -> str:
        return self.name.title()


def main() -> None:
    args: List[str] = sys.argv[1:]  # Don't want the script path
    match args:
        case [] | ["help"]:
            show_help()
        case ["-v", "-a"] | ["-v", "-a", "-r"] | ["-v", "-r", "-a"]:
            stitch_all_subdirs(Direction.VERTICAL, len(args) == 3)
        case ["-v", "-r", _, _, *_]:
            stitch_files(args[2:], Direction.VERTICAL, True)
        case ["-v", _, _, *_]:
            stitch_files(args[1:], Direction.VERTICAL, False)
        case ["-h", "-a"] | ["-h", "-a", "-r"] | ["-h", "-r", "-a"]:
            stitch_all_subdirs(Direction.HORIZONTAL, len(args) == 2)    # Reverse by default
        case ["-h", "-r", _, _, *_]:
            stitch_files(args[2:], Direction.HORIZONTAL, False)         # Reverse by default
        case ["-h", _, _, *_]:
            stitch_files(args[1:], Direction.HORIZONTAL, True)          # Reverse by default
        case _:
            print("Invalid program arguments")
            show_help()

def stitch_all_subdirs(direction: Direction, reverse: bool) -> None:
    print(f"{direction} stitching of all subfolders...")
    cwd: str = os.getcwd()
    subdirs: List[str] = [entry.name for entry in os.scandir(cwd) if is_valid_dir(entry)]
    mode: str = "-append" if direction == Direction.VERTICAL else "+append"
    with multiprocessing.Pool() as pool:
        pool.starmap(stitch_subdir, zip(subdirs, repeat(mode), repeat(reverse)))

def is_valid_dir(entry: DirEntry[str]) -> bool:
    return entry.is_dir() and any(f.is_file() and f.name.endswith(".png") for f in os.scandir(entry.path))

def stitch_subdir(subdir: str, mode: str, reverse: bool) -> None:
    command: List[str] = ["magick", "convert", f"{subdir}/*.png", "-reverse", mode, f"{subdir}.png"] if reverse else ["magick", "convert", f"{subdir}/*.png", mode, f"{subdir}.png"]
    subprocess.call(command)
    print(f"Folder {path.join(os.getcwd(), subdir)} stitched to file {subdir}.png")

def stitch_files(files: List[str], direction: Direction, reverse: bool) -> None:
    print(f"{direction} stitching of specified files...")
    if not all(path.isfile(f) and f.endswith(".png") for f in files):
        print("Invalid files passed, aborting")
        return

    mode: str = "-append" if direction == Direction.VERTICAL else "+append"
    output: str = "-".join(Path(path.basename(f)).stem for f in files)
    command: List[str] = ["magick", "convert", *files, "-reverse", mode, f"{output}.png"] if reverse else ["magick", "convert", *files, mode, f"{output}.png"]
    subprocess.call(command)
    print(f"Files stitched to file {output}.png")

def show_help() -> None:
    print("File stitcher help")
    print("Usage: stitcher [-v|-h] [-a] [-r] [*files to stitch]")
    print("-v:   Vertical file stitching, up to down order by default")
    print("-h:   Horizontal file stitching, right to left order by default")
    print("-a:   Stitch files in all subfolders together, if this is used, files should not be specified")
    print("-r:   Reverse file order while stitching")
    print("help: Show this message")
    pass


if __name__ == "__main__":
    main()
