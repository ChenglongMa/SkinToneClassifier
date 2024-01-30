import argparse
import functools
import logging
import os
import re
import string
import sys
from pathlib import Path
from typing import Union
from urllib.parse import urlparse

from stone.package import __version__, __package_name__, __description__, __app_name__

LOG = logging.getLogger(__name__)


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
    paths = set([f.resolve() for fs in filenames for f in fs] + urls)
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


def is_debugging():
    gettrace = getattr(sys, "gettrace", None)
    return gettrace is not None and gettrace()


def build_arguments_deprecated():
    print("Using CLI mode.")
    LOG.info("LOG: Using CLI mode.")
    parser = argparse.ArgumentParser(
        description=f"{__app_name__} v{__version__}",
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
        help="Skin tone labels;\n"
        "Default values are the uppercase alphabet list leading by the image type ('C' for 'color'; 'B' for 'Black&White'), "
        "e.g., ['CA', 'CB', ..., 'CZ'] or ['BA', 'BB', ..., 'BZ'].\n"
        "Since v1.2.0, supports range of labels, e.g., 'A-Z' or '1-10'.\n"
        "Refer to https://github.com/ChenglongMa/SkinToneClassifier for more details.",
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
        help="CONFIG: what percentage of the skin area is required to identify the face, defaults to 0.15.",
        default=0.15,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the version number and exit.",
    )

    return parser.parse_args()


def build_arguments():
    from gooey import GooeyParser

    parser = GooeyParser(
        description=__description__,
    )
    files = parser.add_argument_group(
        "Images to process",
        "The locations of images to process, which can be directories, files, or URLs.\n"
        "Multiple values are separated by space;\n"
        'You can mix folders, filenames and web links together, e.g., "/path/to/dir1 /path/to/pic.jpg https://example.com/pic.png".\n',
        gooey_options={"show_border": False, "columns": 1},
    )

    files.add_argument(
        "-i",
        "--images",
        nargs="+",
        default=[os.getcwd()],
        metavar="Image Filenames",
        help="Image filename(s), Directories or URLs to process.",
        gooey_options={"visible": False},
    )
    files.add_argument(
        "--image_dirs",
        nargs="+",
        metavar="Image Directories",
        widget="DirChooser",
        # widget="MultiDirChooser", # fixme: enable this widget when issues are fixed
        gooey_options={
            "message": "Select directories to process",
            "initial_value": os.getcwd(),
            "default_path": os.getcwd(),
            "placeholder": "e.g., /path/to/dir1 /path/to/dir2",
        },
    )
    files.add_argument(
        "-r",
        "--recursive",
        metavar="Recursive Search",
        action="store_true",
        help="Search images recursively in the specified directory.",
    )

    files.add_argument(
        "--image_files",
        nargs="+",
        metavar="Image Filenames",
        help="Add individual image file(s)",
        widget="MultiFileChooser",
        gooey_options={
            "wildcard": "All images|*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.tif;*.webp|"
            "JPG (*.jpg)|*.jpg|"
            "JPEG (*.jpeg)|*.jpeg|"
            "PNG (*.png)|*.png|"
            "BMP (*.bmp)|*.bmp|"
            "GIF (*.gif)|*.gif|"
            "TIFF (*.tif)|*.tif|"
            "WEBP (*.webp)|*.webp|"
            "All files (*.*)|*.*",
            "message": "Select the image file(s) to process",
            "default_dir": os.getcwd(),
            "full_width": False,
            "placeholder": "e.g., a.jpg b.png",
        },
    )

    files.add_argument(
        "--image_urls",
        nargs="+",
        metavar="Image URLs",
        help="Add image URLs",
        gooey_options={
            "full_width": False,
            "placeholder": "e.g., https://example.com/a.jpg https://example.com/b.png",
        },
    )

    images = parser.add_argument_group(
        "Image Settings",
        gooey_options={
            "show_border": False,
            "columns": 2,
        },
    )
    images.add_argument(
        "-t",
        "--image_type",
        default="auto",
        metavar="Image Type",
        help="Specify whether the input image(s) is/are colored or black/white.\n"
        'Defaults to "auto", which will be detected automatically.',
        choices=["auto", "color", "bw"],
    )
    images.add_argument(
        "-p",
        "--palette",
        nargs="+",
        metavar="Palette",
        help="Skin tone palette;\n"
        'Input RGB hex values leading by "#" or RGB values separated by comma(,),\n'
        "E.g., #373028 #422811 or 255,255,255 100,100,100\n"
        "Leave blank to use the default palette as mentioned in the document.\n",
        gooey_options={"full_width": True},
    )
    images.add_argument(
        "-l",
        "--labels",
        nargs="+",
        metavar="Labels",
        help="Skin tone labels;\n"
        "Leave blank to use the default values: the uppercase alphabet list leading by the image type ('C' for 'color'; 'B' for 'Black&White'), "
        "e.g., ['CA', 'CB', ..., 'CZ'] or ['BA', 'BB', ..., 'BZ'].\n"
        "Since v1.2.0, supports range of labels, e.g., 'A-Z' or '1-10'.\n"
        "Refer to https://github.com/ChenglongMa/SkinToneClassifier#3-specify-category-labels for more details.",
        gooey_options={"full_width": True},
    )

    images.add_argument(
        "-bw",
        "--black_white",
        metavar="Convert to Black/White",
        action="store_true",
        help="Whether to convert the input to black/white image(s)?\n"
        "If true, the app will use the black/white palette to classify the image.",
    )

    images.add_argument(
        "--n_colors",
        metavar="Number of Dominant Colors",
        type=int,
        help="Specify the number of dominant colors to be extracted.\n"
        "The colors will be used to compare with the colors in the palette.\n",
        default=2,
        widget="IntegerField",
        gooey_options={"initial_value": 2, "min": 1, "max": 99999, "full_width": False},
    )
    images.add_argument(
        "--new_width",
        type=int,
        metavar="New Width (pixels)",
        help="Resize the images with the specified width.\n"
        "Sometimes smaller images will be processed faster and more accurately.\n"
        "No resizing will be performed if the value is negative.",
        default=250,
        widget="IntegerField",
        gooey_options={"initial_value": 250, "min": 10, "max": 99999, "full_width": False},
    )

    outputs = parser.add_argument_group("Output Settings", gooey_options={"show_border": True})
    outputs.add_argument(
        "-o",
        "--output",
        metavar="Output Directory",
        default=os.getcwd(),
        help="Specify the path of output file, defaults to current directory.",
        widget="DirChooser",
        gooey_options={
            "message": "Select the output directory",
            "default_path": os.getcwd(),
        },
    )
    outputs.add_argument(
        "-d",
        "--debug",
        metavar="Generate Report Images",
        action="store_true",
        default=True,
        help="Whether to generate report images?\n"
        "If true, the report images will be saved in the '<OUTPUT_DIRECTORY>/debug' directory.",
    )

    advanced = parser.add_argument_group(
        "Advanced Settings",
        "For advanced users only, please refer to https://stackoverflow.com/a/20805153/8860079",
        gooey_options={"show_border": False, "columns": 2},
    )
    advanced.add_argument(
        "--scale",
        type=float,
        metavar="Scale",
        help="Specify how much the image size is reduced at each image scale.",
        default=1.1,
        widget="DecimalField",
        gooey_options={"initial_value": 1.1, "min": 0.1, "max": 2.0},
    )
    advanced.add_argument(
        "--min_nbrs",
        type=int,
        metavar="Minimum Neighbors",
        help="Specify how many neighbors each candidate rectangle should have to retain it.\n"
        "Higher value results in less detections but with higher quality.",
        default=5,
        widget="IntegerField",
        gooey_options={"initial_value": 5, "min": 1, "max": 99999},
    )
    default_min_width = 90
    default_min_height = 90

    advanced.add_argument(
        "--min_size",
        type=int,
        nargs="+",
        metavar="Minimum Possible Face Size, format: <Width Height>",
        help=f'[Alias --min_width, --min_height] Specify the minimum possible face size. Faces smaller than that are ignored, defaults to "{default_min_width} {default_min_height}".',
        default=(default_min_width, default_min_height),
        gooey_options={
            "visible": False,
        },
    )

    min_size = advanced.add_argument_group(
        "Minimum Possible Face Size (pixels)",
        'Specify the minimum possible face size. Faces smaller than that are ignored, defaults to "90 90".',
        gooey_options={"show_border": True, "columns": 2},
    )

    min_size.add_argument(
        "--min_width",
        type=int,
        metavar="Minimum Width",
        # help="Specify the minimum possible face width. Faces smaller than that are ignored, defaults to 90.",
        default=default_min_width,
        widget="IntegerField",
        gooey_options={"initial_value": default_min_width, "min": 10, "max": 99999},
    )

    min_size.add_argument(
        "--min_height",
        type=int,
        metavar="Minimum Height",
        # help="Specify the minimum possible face height. Faces smaller than that are ignored, defaults to 90.",
        default=default_min_height,
        widget="IntegerField",
        gooey_options={"initial_value": default_min_height, "min": 10, "max": 99999},
    )

    advanced.add_argument(
        "--threshold",
        type=float,
        metavar="Minimum Possible Face Proportion",
        help="Specify the minimum proportion of the skin area required to identify the face, defaults to 0.15.",
        default=0.15,
        widget="DecimalField",
        gooey_options={"initial_value": 0.15, "min": 0.01, "max": 1.0},
    )
    advanced.add_argument(
        "--n_workers",
        type=int,
        metavar="Number of CPU Workers",
        help="Specify the number of workers to process the images.\n"
        "0 means the total number of CPU cores in the system.",
        default=0,
        widget="IntegerField",
        gooey_options={"initial_value": 0, "min": 0, "max": 99999},
    )

    advanced.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the version number and exit.",
        gooey_options={"visible": False},
    )
    args = parser.parse_args()
    images = args.images or []
    if args.image_dirs:
        images.extend(args.image_dirs)
    if args.image_files:
        images.extend(args.image_files)
    if args.image_urls:
        images.extend(args.image_urls)
    args.images = images
    if tuple(args.min_size) == (default_min_width, default_min_height):
        args.min_size = (args.min_width, args.min_height)
    return args


def resolve_labels(labels):
    if not labels or len(labels) != 1:
        return labels
    label = labels[0]

    separator = r"[-,~:;_]"
    pattern = rf"^([a-zA-Z0-9]+){separator}([a-zA-Z0-9]+)(?:{separator}([-+]?\d+))?$"
    match = re.match(pattern, label)
    if match is None:
        return labels
    start, end, step = match.groups()
    if not step:
        step = 1
    else:
        step = int(step)
    if step == 0:
        LOG.warning(f"The specified step in the '--label' setting ('{label}') cannot be 0; resetting to 1.")
        step = 1
    if step < 0:
        start, end = end, start

    if start.isdigit() and end.isalpha() or start.isalpha() and end.isdigit():
        LOG.warning(
            f"Invalid '--label' setting ('{label}'): The start value ({start}) and the end value ({end}) should be both digits or both letters."
        )
        return labels
    if start >= end:
        LOG.warning(
            f"Invalid '--label' setting ('{label}'): The start value ({start}) should be less than the end value ({end})."
        )
        return labels
    if start.isdigit() and end.isdigit():
        start, end = int(start), int(end)
        return [str(i) for i in range(start, end + 1, step)]
    if start.isalpha() and end.isalpha():
        start, end = start.upper(), end.upper()
        return [chr(i) for i in range(ord(start), ord(end) + 1, step)]
    return labels


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
