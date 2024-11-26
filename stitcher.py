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
    """
    Stitching direction enum
    """

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
    """
    Script entry point
    """

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

    # If direction is None, we have not found a valid direction argument argument
    if direction is None:
        invalid_args()
        return

    subdirs: bool = False
    reverse: bool = direction == Direction.HORIZONTAL    # Horizontal defaults to reversed
    output: str | None = None
    # Find other program args
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
                # Unknown/invalid arg
                invalid_args()
                return

    # Proceed with stitching according to args
    if subdirs:
        if len(args) != 0:
            invalid_args()
        else:
            stitch_all_subdirs(direction, reverse, "" if output is None else output)
    elif len(args) >= 2:
        stitch_files(args, direction, reverse, output)
    else:
        invalid_args()


def create_magick_command(mode: str, output: str, reverse: bool, *files: str) -> List[str]:
    """
    Creates the correct Magick stitching command based on the provided arguments
    :param mode:    Stitching direction
    :param output:  Output file name
    :param reverse: If the files should be reversed
    :param files:   Files to stitch
    :return:        A list containing the subprocess args to call the Magick command
    """

    command: List[str] = ["magick", *files, mode, output]
    if reverse:
        command.insert(-2, "-reverse")
    return command


def stitch_all_subdirs(direction: Direction, reverse: bool, prefix: str) -> None:
    """
    Stitches the files in all subdirectories of the current working directory
    :param direction: Direction to stitch in
    :param reverse:   If the stitching should be reversed or not
    :param prefix:    Output file name prefix
    """

    print(f"{direction} stitching of all subfolders...")
    # Get all valid subdirectories from workind directory
    cwd: str = os.getcwd()
    subdirs: List[str] = [entry.name for entry in os.scandir(cwd) if is_valid_dir(entry)]
    # Stitch each directory from a different thread
    with multiprocessing.Pool() as pool:
        pool.starmap(stitch_subdir, zip(subdirs, repeat(direction.value), repeat(reverse), repeat(prefix)))


def is_valid_dir(entry: DirEntry[str]) -> bool:
    """
    Validates that a directory contains stitchable files
    :param entry: Directory entry to validate
    :return: True if the directory contains stitchable files, otherwise false
    """

    # Check that entries are a directory containing at least one .png file
    return entry.is_dir() and any(f.is_file() and f.name.endswith(".png") for f in os.scandir(entry.path))


def stitch_subdir(subdir: str, mode: str, reverse: bool, prefix: str) -> None:
    """
    Stitches a given subdirectory of files
    :param subdir:  Subdirectory of files to stitch
    :param mode:    Stitching direction
    :param reverse: If files should be reversed or not
    :param prefix:  Output file prefix
    """

    # Create and call stitch command
    command: List[str] = create_magick_command(mode, f"{prefix}{subdir}.png", reverse, f"{subdir}/*.png")
    subprocess.call(command)
    print(f"Folder {path.join(os.getcwd(), subdir)} stitched to file {prefix}{subdir}.png")


def stitch_files(files: List[str], direction: Direction, reverse: bool, output: str | None) -> None:
    """
    Stitches the provided files
    :param files:     Files to stitch
    :param direction: Stitching direction
    :param reverse:   If files should be reversed or not
    :param output:    Output file name
    """

    # Validate that passed files are valid
    print(f"{direction} stitching of specified files...")
    if not all(path.isfile(f) and f.endswith(".png") for f in files):
        print("Invalid files passed, aborting")
        return

    # Cleanup output file name
    if output is None:
        output = "-".join(Path(path.basename(f)).stem for f in files)
    else:
        output = path.splitext(output)[0]

    # Create and call stitch command
    command: List[str] = create_magick_command(direction.value, f"{output}.png", reverse, *files)
    subprocess.call(command)
    print(f"Files stitched to file {output}.png")


def show_help() -> None:
    """
    Shows the program's help prompt
    """

    print("""File stitcher help
    Usage:  stitcher [-v|-h] [-a] [-r] [-o %output_name%] [*files]
    -v:     Vertical file stitching, up to down order by default
    -h:     Horizontal file stitching, right to left order by default
    -a:     Stitch files in all subfolders together, if this is used, files should not be specified
    -r:     Reverse file order while stitching
    -o:     Specifies the a prefix for all output files when -a is passed, otherwise specifies the name of the output file
    *files: Space-separated list of files to stitch, only needed when not passing -a
    help:   Show this message""")


def invalid_args() -> None:
    """
    Prints an invalid arguments message then shows the program's help prompt
    """

    print("Invalid program arguments")
    show_help()


if __name__ == "__main__":
    main()
