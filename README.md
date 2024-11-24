# Stitcher
This is a helper process to vertically stitch images together using ImageMagick

## Installation 
Python >= 3.10 and [ImageMagick](https://imagemagick.org/script/download.php) need to be installed.

Then the utility can be installed by running `pip install git+https://github.com/ShoHabby/file-stitcher`

## Usage
`stitcher [-v|-h] [-a] [-r] [-o %output_name%] [*files to stitch]`

`-v` or `-h` is required and must always be the first parameter passed to the script. Both options are mutually exclusive.
`-v` will stitch files vertically, from top to bottom, and `-h` will stitch files horizontally, from right to left (manga reading order)

`-a` Means that the script will look through subfolders of the directory the script was called from, find images within them, stitch them according to settings,
and output them to the directory the script was called from. While using this parameter, files should not be specified.
The output file names will be that of the directory they were stitched from. The `-o` parameter cannot be used with this either.

`-r` Will reverse the order of the stitching to bottom to top for vertical, and left to right for horizontal.

`-o` Allows specifying the name of the output file when manually specifying the files to stitch. The output name does not need to contain the file extension.
If not specified, the output name will be the concatenation of all the input file names.

When not using `-a`, files must be specified last. At least two files must be specified, but there is no upper limit.
The file paths may be absolute or relative to the directory the script is called from.
The output file name will be the concatenation of all the input file names.
