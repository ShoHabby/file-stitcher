import os
import multiprocessing
import subprocess
import sys
from os import DirEntry
from typing import List


def main() -> None:
    args: List[str] = sys.argv[1:]  # Don't want the script path
    vertical_stitch(args)

def vertical_stitch(args: List[str]) -> None:
    print("Vertical stitching of all subfolders...")
    cwd: str = os.getcwd()
    subdirs: List[str] = [entry.name for entry in os.scandir(cwd) if is_valid_dir(entry)]
    with multiprocessing.Pool() as pool:
        pool.map(stitch_subdir, subdirs)

def is_valid_dir(entry: DirEntry[str]) -> bool:
    return entry.is_dir() and any(f.is_file() and f.name.endswith(".png") for f in os.scandir(entry.path))

def stitch_subdir(subdir: str) -> None:
    command: List[str] = ["magick", "convert", "-append", f"{subdir}/*.png", f"{subdir}.png"]
    subprocess.call(command)
    print(f"Folder {os.path.join(os.getcwd(), subdir)} stitched to file {subdir}.png")

if __name__ == "__main__":
    main()
