import logging
from pathlib import Path
from typing import Union, Literal

import cv2

from stone.image import (
    load_image,
    is_black_white,
    DEFAULT_TONE_PALETTE,
    DEFAULT_TONE_LABELS,
    process_image,
    normalize_palette,
)
from stone.utils import ArgumentError

LOG = logging.getLogger(__name__)


def process(
    filename_or_url: Union[str, Path],
    image_type: Literal["auto", "color", "bw"] = "auto",
    tone_palette: list = None,
    tone_labels: list = None,
    convert_to_black_white: bool = False,
    n_dominant_colors=2,
    new_width=250,
    scale=1.1,
    min_nbrs=5,
    min_size=(90, 90),
    threshold=0.15,
    return_report_image=False,
):
    """
    Process the image and return the result.
    :param filename_or_url: The filename (in local devices) or URL (in Internet) of the image.
    :param image_type: Specify whether the input image(s) is/are colored or black/white.
           Valid choices are: "auto", "color" or "bw", Defaults to "auto", which will be detected automatically.
    :param tone_palette: Skin tone palette; Supports RGB hex value leading by "#" or RGB values separated by comma(,).
           E.g., ['#373028', '#422811'] or ['255,255,255', '100,100,100']
    :param tone_labels: Skin tone labels; default values are the uppercase alphabet list leading by the image type
           ('C' for 'color'; 'B' for 'Black&White'), e.g., ['CA', 'CB', ..., 'CZ'] or ['BA', 'BB', ..., 'BZ'].
    :param convert_to_black_white: Whether to convert the image to black/white before processing. Defaults to False.
    :param n_dominant_colors: Number of dominant colors to be extracted from the image. Defaults to 2.
    :param new_width: Resize the images with the specified width. Negative value will be ignored, defaults to 250.
    :param scale: How much the image size is reduced at each image scale. Defaults to 1.1.
    :param min_nbrs: How many neighbors each candidate rectangle should have to retain it.
           Higher value results in less detections but with higher quality, defaults to 5.
    :param min_size: Minimum possible face size. Faces smaller than that are ignored, defaults to (90, 90).
    :param threshold: What percentage of the skin area is required to identify the face, defaults to 0.15.
    :param return_report_image: Whether to return the report image(s) in the result. Defaults to False.
    :return:
    """
    image, basename, extension = load_image(filename_or_url, flags=cv2.IMREAD_COLOR)
    if image is None:
        msg = f"{basename}{extension} is not found or is not a valid image."
        LOG.error(msg)
        return {
            "filename": basename,
            "message": msg,
        }

    is_bw = is_black_white(image)
    decoded_image_type = image_type
    if image_type == "auto":
        decoded_image_type = "bw" if convert_to_black_white or is_bw else "color"
    else:
        is_bw = image_type == "bw"

    if tone_palette is None or len(tone_palette) == 0:
        skin_tone_palette = DEFAULT_TONE_PALETTE[decoded_image_type]
    else:
        skin_tone_palette = normalize_palette(tone_palette)

    skin_tone_labels = tone_labels or DEFAULT_TONE_LABELS[decoded_image_type]
    if len(skin_tone_palette) != len(skin_tone_labels):
        raise ArgumentError("argument -p/--palette and -l/--labels must have the same length.")

    records, report_images = process_image(
        image,
        is_bw,
        convert_to_black_white,
        skin_tone_palette,
        skin_tone_labels,
        new_width=new_width,
        n_dominant_colors=n_dominant_colors,
        scaleFactor=scale,
        minNeighbors=min_nbrs,
        minSize=min_size,
        threshold=threshold,
        verbose=return_report_image,
    )
    return {
        "basename": basename,
        "extension": extension,
        "image_type": decoded_image_type,
        "faces": records,
        "report_images": report_images,
    }
