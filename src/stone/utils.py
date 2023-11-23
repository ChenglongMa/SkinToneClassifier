import argparse
import functools
import glob
import os
import re
import string
import sys
from pathlib import Path
from typing import Union
from urllib.parse import urlparse

from stone.package import __version__, __package_name__


class ArgumentError(ValueError):
    """
    Wrapper for argument error. This exception will be raised when the arguments are invalid.
    """

    pass


# @functools.cache # Python 3.9+
@functools.lru_cache(maxsize=128)  # Python 3.2+
def alphabet_id(n):
    letters = string.ascii_uppercase
    n_letters = len(letters)
    if n < n_letters:
        return letters[n]
    _id = ""

    while n > 0:
        remainder = (n - 1) % n_letters
        _id = letters[remainder] + _id
        n = (n - 1) // n_letters

    return _id


def is_url(text):
    return urlparse(text).scheme in ["http", "https"]


def extract_filename_and_extension(url):
    """
    Extract base filename and extension from the url.
    :param url: URL with filename and extension, e.g., https://example.com/images/pic.jpg?param=value
    :return: Base filename and extension, e.g., pic, jpg
    """
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = path.split("/")[-1]
    basename, *extension = filename.split(".")
    return basename, f".{extension[0]}" if extension else None


def build_image_paths(images_paths, recursive=False):
    filenames, urls = [], []
    valid_images = ["*.jpg", "*.gif", "*.png", "*.jpeg", "*.webp", "*.tif"]
    excluded_folders = ["debug", "log"]
    if isinstance(images_paths, str):
        images_paths = [images_paths]

    for filename in images_paths:
        if is_url(filename):
            urls.append(filename)
            continue
        p = Path(filename)
        if p.is_dir():
            images = [p.glob(pattern) for pattern in valid_images]
            if recursive:
                subfolders = [f for f in p.glob("*/") if f.name not in excluded_folders]
                images.extend([sp.rglob(pattern) for pattern in valid_images for sp in subfolders])

            filenames.extend(images)
        elif p.is_file():
            filenames.append([p])
    paths = set([f for fs in filenames for f in fs] + urls)
    paths = list(paths)
    if len(paths) == 0:
        raise FileNotFoundError("No valid images in the specified path.")
    # Sort paths by (first) number extracted from the filename string
    paths.sort(key=sort_file)
    return paths


def sort_file(path: Union[str, Path]):
    if isinstance(path, Path):
        basename = path.stem
    else:
        basename, *_ = extract_filename_and_extension(path)
    nums = re.findall(r"\d+", basename)
    return (int(nums[0]) if nums else float("inf")), basename


def is_windows():
    return sys.platform in ["win32", "cygwin"]


def build_arguments():
    # Setup arguments
    parser = argparse.ArgumentParser(
        description="Skin Tone Classifier",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--images",
        nargs="+",
        default=["./"],
        metavar="IMAGE FILENAME",
        help="Image filename(s) or URLs to process;\n"
        'Supports multiple values separated by space, e.g., "a.jpg b.png";\n'
        'Supports directory or file name(s), e.g., "./path/to/images/ a.jpg";\n'
        'Supports URL(s), e.g., "https://example.com/images/pic.jpg" since v1.1.0+.\n'
        "The app will search all images in current directory in default.",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Whether to search images recursively in the specified directory.",
    )

    parser.add_argument(
        "-t",
        "--image_type",
        default="auto",
        metavar="IMAGE TYPE",
        help="Specify whether the input image(s) is/are colored or black/white.\n"
        'Valid choices are: "auto", "color" or "bw",\n'
        'Defaults to "auto", which will be detected automatically.',
        choices=["auto", "color", "bw"],
    )
    parser.add_argument(
        "-p",
        "--palette",
        nargs="+",
        metavar="PALETTE",
        help="Skin tone palette;\n"
        'Supports RGB hex value leading by "#" or RGB values separated by comma(,),\n'
        'E.g., "-p #373028 #422811" or "-p 255,255,255 100,100,100"',
    )
    parser.add_argument(
        "-l",
        "--labels",
        nargs="+",
        metavar="LABELS",
        help="Skin tone labels; default values are the uppercase alphabet list leading by the image type ('C' for 'color'; 'B' for 'Black&White'), "
        "e.g., ['CA', 'CB', ..., 'CZ'] or ['BA', 'BB', ..., 'BZ'].",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Whether to generate report images, used for debugging and verification."
        "The report images will be saved in the './debug' directory.",
    )
    parser.add_argument(
        "-bw",
        "--black_white",
        action="store_true",
        help="Whether to convert the input to black/white image(s).\n"
        "If true, the app will use the black/white palette to classify the image.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="./",
        metavar="DIRECTORY",
        help="The path of output file, defaults to current directory.",
    )
    parser.add_argument(
        "--n_workers",
        type=int,
        metavar="WORKERS",
        help="The number of workers to process the images, defaults to the number of CPUs in the system.",
        default=0,
    )

    parser.add_argument(
        "--n_colors",
        type=int,
        metavar="COLORS",
        help="CONFIG: the number of dominant colors to be extracted, defaults to 2.",
        default=2,
    )
    parser.add_argument(
        "--new_width",
        type=int,
        metavar="WIDTH",
        help="CONFIG: resize the images with the specified width. Negative value will be ignored, defaults to 250.",
        default=250,
    )

    # For the next parameters, refer to https://stackoverflow.com/a/20805153/8860079
    parser.add_argument(
        "--scale",
        type=float,
        metavar="SCALE",
        help="CONFIG: how much the image size is reduced at each image scale, defaults to 1.1",
        default=1.1,
    )
    parser.add_argument(
        "--min_nbrs",
        type=int,
        metavar="NEIGHBORS",
        help="CONFIG: how many neighbors each candidate rectangle should have to retain it.\n"
        "Higher value results in less detections but with higher quality, defaults to 5.",
        default=5,
    )
    parser.add_argument(
        "--min_size",
        type=int,
        nargs="+",
        metavar=("WIDTH", "HEIGHT"),
        help='CONFIG: minimum possible face size. Faces smaller than that are ignored, defaults to "90 90".',
        default=(90, 90),
    )
    parser.add_argument(
        "--threshold",
        type=float,
        metavar="THRESHOLD",
        help="CONFIG: what percentage of the skin area is required to identify the face, defaults to 0.3.",
        default=0.3,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the version number and exit.",
    )

    return parser.parse_args()


def get_latest_version_from_pypi(package_name):
    try:
        import requests

        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        response.raise_for_status()

        data = response.json()
        latest_version = data["info"]["version"]
        return latest_version
    except Exception:
        pass


def check_version():
    if "STONE_UPGRADE_FLAG" in os.environ:
        return
    try:
        from packaging.version import parse
        import importlib.metadata

        latest_version = get_latest_version_from_pypi(__package_name__)
        if not latest_version:
            return
        distribution = importlib.metadata.distribution(__package_name__)
        installed_version = distribution.version
        if parse(installed_version) < parse(latest_version):
            from colorama import just_fix_windows_console, Fore

            just_fix_windows_console()
            print(
                Fore.YELLOW + f"You are using an outdated version of {__package_name__} ({installed_version}).\n"
                f"Please upgrade to the latest version ({latest_version}) with the following command:\n",
                Fore.GREEN + f"pip install {__package_name__} --upgrade\n" + Fore.RESET,
            )
            os.environ["STONE_UPGRADE_FLAG"] = "1"
    except Exception:
        pass
