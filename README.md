# Stitcher
This is a helper process to vertically stitch images together using ImageMagick

## Installation 
Python >= 3.5 and [ImageMagic](https://imagemagick.org/script/download.php) need to be installed.

Then the utility can be installed by running `pip install git+https://github.com/ShoHabby/file-stitcher`

## Usage
The program looks for subfolder in the working directory, then merges all the PNG images found within, in alphabetical order, and outputs them to a file of the same name as the subfolder in the working directory.

This means that with this folder structure:
```
- MyFolder\
 - AAA\
  - MyImage1.png
  - MyImage2.png
 - BBB\
  - MyImage3.png
  - MyImage4.png
```
Running `stitcher` from `MyFolder\` result in the creation of the folloing files:
```
- MyFolder\
 - AAA.png
 - BBB.png
```
