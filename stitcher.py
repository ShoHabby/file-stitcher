import os
import multiprocessing
import subprocess
from typing import List

def main() -> None:
    cwd: str = os.getcwd()
    subdirs: List[str] = [f.name for f in os.scandir(cwd) if f.is_dir()]
    with multiprocessing.Pool() as pool:
        pool.map(stitch_subdir, subdirs)

def stitch_subdir(subdir: str) -> None:
    args: List[str] = ["magick", "convert", "-append", f"{subdir}/*.png", f"{subdir}.png"]
    subprocess.call(args)
    print(f"Folder {os.path.join(os.getcwd(), subdir)} stitched to file {subdir}.png")

if __name__ == "__main__":
    main()