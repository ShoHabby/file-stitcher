from setuptools import setup

setup(
    name = "stitcher",
    version = "1.2.2",
    author = "stupid_chris",
    author_email = "christophe_savard@hotmail.ca",
    license = "MIT",
    url = "https://github.com/ShoHabby/file-stitcher",
    description = "ImageMagick powered image stitcher for manga or longstrip usage.",
    classifiers = [
        "Development Status :: 4 - Beta",

        "Intended Audience :: End Users/Desktop",
        "Environment :: Console",
        "Topic :: Utilities",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10"
    ],
    entry_points = {
        "console_scripts": [
            "stitcher = stitcher:main"
        ]
    },
    python_requires = ">=3.10",
)
