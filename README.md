# Stitcher
This is a helper process to vertically stitch images together using ImageMagick

## Installation 
Python >= 3.10 and [ImageMagic](https://imagemagick.org/script/download.php) need to be installed.

Then the utility can be installed by running `pip install git+https://github.com/ShoHabby/file-stitcher`

## Usage
`stitcher [-v|-h] [-a] [-r] [-o %output_name%] [*files to stitch]`

`-v` or `-h` must always be the first parameter passed to the script, they are mutually exclusive

`-a` Means that the script will look through subfolders of the directory the script was called from, find images within them, stitch them according to settings,
and output them to the directory the script was called from. While using this parameter, files should not be specified.
The output file names will be that of the directory they were stitched from.

`-r` Will reverse the order of the stitching. By default, horizontal stitching is reversed (right to left) as the intention is to stitch manga pages.
Passing that parameter means

`-o` Allows specifying the name of the output file when manually specifying the files to stitch.
The output name does not need to contain the file extension.
If not specified, the output name will be the concatenation of all the input file names.

When not using `-a`, files must be specified last. At least two files must be specified, but there is no upper limit.
The file paths may be absolute or relative to the directory the script is called from.
The output file name will be the concatenation of all the input file names.