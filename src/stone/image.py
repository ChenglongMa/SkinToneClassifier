import logging
import math

import cv2
import numpy as np
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import sRGBColor, LabColor

LOG = logging.getLogger(__name__)


def create_color_bar(height, width, color):
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:] = color
    return bar


def is_black_white(image, threshold=192) -> bool:
    """
    Check if the image is black and white
    :param image:
    :param threshold:
    :return:
    """
    # Reading Images
    if len(image.shape) == 2:
        return True
    h, w, *_ = image.shape

    # Extracting Standard Deviation
    std = np.std(image, axis=2)
    below_t = np.sum(np.where(std <= 25))
    prob_bt = below_t / (h * w)

    return prob_bt >= threshold


def resize(image, width: int = -1, height: int = -1):
    """
    Resize the image, -1 means auto, but the image won't be resized if both width and height are -1
    :param image:
    :param width: -1 means auto
    :param height: -1 means auto
    :return:
    """
    if width < 0 and height < 0:
        return image
    elif width < 0:
        ratio = height / image.shape[0]
        width = int(image.shape[1] * ratio)
    elif height < 0:
        ratio = width / image.shape[1]
        height = int(image.shape[0] * ratio)

    return cv2.resize(image, (width, height))


def detect_faces(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), biggest_only=True, is_bw=False, threshold=0.3):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    flags = cv2.CASCADE_SCALE_IMAGE | cv2.CASCADE_FIND_BIGGEST_OBJECT if biggest_only else cv2.CASCADE_SCALE_IMAGE
    faces = cascade.detectMultiScale(
        gray,
        scaleFactor=scaleFactor,
        minNeighbors=minNeighbors,
        minSize=minSize,
        flags=flags
    )
    if len(faces) == 0:
        return []
    # Change the format of faces from (x, y, w, h) to (x, y, x+w, y+h)
    faces[:, 2:] += faces[:, :2]
    return [face for face in faces if is_face(face, image, is_bw, threshold)]


def is_face(face_coord, image, is_bw, threshold=0.3):
    x1, y1, x2, y2 = face_coord
    face_image = image[y1:y2, x1:x2]
    detect_skin_fn = detect_skin_in_bw if is_bw else detect_skin_in_color
    _, skin_mask = detect_skin_fn(face_image)
    skin_pixels = cv2.countNonZero(skin_mask)
    total_pixels = face_image.shape[0] * face_image.shape[1]
    skin_ratio = skin_pixels / total_pixels
    return skin_ratio >= threshold


def mask_face(image, face):
    x1, y1, x2, y2 = face
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    mask[y1: y2, x1: x2] = 255
    image = cv2.bitwise_and(image, image, mask=mask)
    return image


def detect_skin_in_bw(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    skin_mask = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)

    skin = cv2.bitwise_and(image, image, mask=skin_mask)
    all_0 = np.isclose(skin, 0).all()
    return image if all_0 else skin, skin_mask


def detect_skin_in_color(image):
    # Converting from BGR Colours Space to HSV
    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Defining skin Thresholds
    low_hsv = np.array([0, 48, 80], dtype=np.uint8)
    high_hsv = np.array([20, 255, 255], dtype=np.uint8)

    skin_mask = cv2.inRange(img, low_hsv, high_hsv)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)
    skin_mask = cv2.GaussianBlur(skin_mask, ksize=(3, 3), sigmaX=0)

    skin = cv2.bitwise_and(image, image, mask=skin_mask)

    all_0 = np.isclose(skin, 0).all()
    return image if all_0 else skin, skin_mask


def draw_rects(image, *rects, color=(255, 0, 0), thickness=2):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(image, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1), color, thickness)
    return image


def dominant_colors(image, to_bw, n_clusters=2):
    if to_bw:
        data = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        data = image
    data = np.reshape(data, (-1, 3))
    data = data[np.all(data != 0, axis=1)]
    data = np.float32(data)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, colors = cv2.kmeans(data, n_clusters, None, criteria, 10, flags)
    labels, counts = np.unique(labels, return_counts=True)

    order = (-counts).argsort()
    colors = colors[order]
    counts = counts[order]

    props = counts / counts.sum()

    return colors, props


def blur(image, degree=25):
    """
    Blur the image
    :param image:
    :param degree: the degree of blur. The bigger, the more blur
    :return:
    """
    ksize = degree, degree
    return cv2.blur(image, ksize)


def skin_tone(colors, props, skin_tone_palette, tone_labels):
    lab_tones = [convert_color(sRGBColor.new_from_rgb_hex(rgb), LabColor) for rgb in skin_tone_palette]
    lab_colors = [convert_color(sRGBColor(rgb_r=r, rgb_g=g, rgb_b=b, is_upscaled=True), LabColor) for b, g, r in colors]
    distances = [np.sum([delta_e_cie2000(c, label) * p for c, p in zip(lab_colors, props)]) for label in lab_tones]
    tone_id = np.argmin(distances)
    distance: float = distances[tone_id]
    tone_hex = skin_tone_palette[tone_id].upper()
    PERLA = tone_labels[tone_id]
    return tone_id, tone_hex, PERLA, distance


def classify(image, is_bw, to_bw, skin_tone_palette, tone_labels, n_dominant_colors=2, verbose=False, report_image=None, use_face=True):
    """
    Classify the skin tone of the image
    :param image:
    :param is_bw: whether the image is black and white
    :param to_bw: whether to convert the image to black and white
    :param skin_tone_palette:
    :param tone_labels:
    :param n_dominant_colors:
    :param verbose:
    :param report_image: the image to draw the report on
    :param use_face: whether to use face area for detection
    :return:
    """
    detect_skin_fn = detect_skin_in_bw if is_bw else detect_skin_in_color
    skin, skin_mask = detect_skin_fn(image)
    dmnt_colors, dmnt_props = dominant_colors(skin, to_bw, n_dominant_colors)
    # Generate readable strings
    hex_colors = ['#%02X%02X%02X' % tuple(np.around([r, g, b]).astype(int)) for b, g, r in dmnt_colors]
    prop_strs = ['%.2f' % p for p in dmnt_props]
    result = list(np.hstack(list(zip(hex_colors, prop_strs))))
    # Calculate skin tone
    tone_id, tone_hex, PERLA, distance = skin_tone(dmnt_colors, dmnt_props, skin_tone_palette, tone_labels)
    accuracy = round(100 - distance, 2)
    result.extend([tone_hex, PERLA, accuracy])
    if not verbose:
        return result, None

    # 0. Create initial report image
    report_image = initial_report_image(image, report_image, skin_mask, use_face, to_bw)
    bar_width = 100

    # 1. Create color bar for dominant colors
    color_bars = create_dominant_color_bar(report_image, dmnt_colors, dmnt_props, bar_width)

    # 2. Create color bar for skin tone list
    palette_bars = create_tone_palette_bar(report_image, tone_id, skin_tone_palette, bar_width)

    # 3. Combine all bars and report image
    report_image = np.hstack([report_image, color_bars, palette_bars])
    msg_bar = create_message_bar(dmnt_colors, dmnt_props, tone_hex, distance, report_image.shape[1])
    report_image = np.vstack([report_image, msg_bar])
    return result, report_image


def initial_report_image(face_image, report_image, skin_mask, use_face, to_bw):
    report_image = face_image if report_image is None else report_image
    if to_bw:
        report_image = cv2.cvtColor(report_image, cv2.COLOR_BGR2GRAY)
    if use_face:
        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        skin_mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)[1]
    blurred_image = blur(report_image)
    non_skin_mask = cv2.bitwise_not(skin_mask)
    edges = cv2.Canny(skin_mask, 50, 150)
    report_image = cv2.bitwise_and(report_image, report_image, mask=skin_mask) + cv2.bitwise_and(blurred_image, blurred_image, mask=non_skin_mask)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(report_image, contours, -1, (255, 0, 0), 2)
    return report_image


def create_dominant_color_bar(report_image, dmnt_colors, dmnt_props, bar_width):
    color_bars = []
    total_height = 0
    for color, prop in zip(dmnt_colors, dmnt_props):
        bar_height = int(math.floor(report_image.shape[0] * prop))
        total_height += bar_height
        bar = create_color_bar(bar_height, bar_width, color)
        color_bars.append(bar)
    padding_height = report_image.shape[0] - total_height
    if padding_height > 0:
        padding = create_color_bar(padding_height, bar_width, (255, 255, 255))
        color_bars.append(padding)
    return np.vstack(color_bars)


def create_tone_palette_bar(report_image, tone_id, skin_tone_palette, bar_width):
    palette_bars = []
    tone_height = report_image.shape[0] // len(skin_tone_palette)
    tone_bgrs = []
    for tone in skin_tone_palette:
        hex_value = tone.lstrip('#')
        r, g, b = [int(hex_value[i:i + 2], 16) for i in (0, 2, 4)]
        tone_bgrs.append([b, g, r])
        bar = create_color_bar(tone_height, bar_width, [b, g, r])
        palette_bars.append(bar)
    padding_height = report_image.shape[0] - tone_height * len(skin_tone_palette)
    if padding_height > 0:
        padding = create_color_bar(padding_height, bar_width, (255, 255, 255))
        palette_bars.append(padding)
    bar = np.vstack(palette_bars)

    padding = 1
    start_point = (padding, tone_id * tone_height + padding)
    end_point = (bar_width - padding, (tone_id + 1) * tone_height)
    bar = cv2.rectangle(bar, start_point, end_point, (255, 0, 0), 2)
    return bar


def create_message_bar(dmnt_colors, dmnt_props, tone_hex, distance, bar_width):
    msg_bar = create_color_bar(height=50, width=bar_width, color=(243, 239, 214))
    b, g, r = np.around(dmnt_colors[0]).astype(int)
    dominant_color_hex = '#%02X%02X%02X' % (r, g, b)
    prop = f'{dmnt_props[0] * 100:.2f}%'

    font, font_scale, txt_colr, thickness, line_type = cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0), 1, cv2.LINE_AA
    x, y = 2, 15
    msg = f'- Dominant color: {dominant_color_hex}, proportion: {prop}'
    cv2.putText(msg_bar, msg, (x, y), font, font_scale, txt_colr, thickness, line_type)

    text_size, _ = cv2.getTextSize(msg, font, font_scale, thickness)
    line_height = text_size[1] + 10
    accuracy = round(100 - distance, 2)
    cv2.putText(msg_bar, f'- Skin tone: {tone_hex}, accuracy: {accuracy}', (x, y + line_height), font, font_scale,
                txt_colr, thickness, cv2.LINE_AA)

    return msg_bar


def process(image: np.ndarray, is_bw: bool, to_bw: bool, skin_tone_palette: list, tone_labels: list = None, new_width=-1, n_dominant_colors=2,
            scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), biggest_only=True, threshold=0.3, verbose=False):
    image = resize(image, new_width)

    records, report_images = {}, {}
    face_coords = detect_faces(image, scaleFactor, minNeighbors, minSize, biggest_only, is_bw, threshold)
    n_faces = len(face_coords)

    if n_faces == 0:
        record, report_image = classify(image, is_bw, to_bw, skin_tone_palette, tone_labels, n_dominant_colors, verbose=verbose, use_face=False)
        records['NA'] = record
        report_images['NA'] = report_image
    # Otherwise, detect skin tone for each face
    for idx, face_coord in enumerate(face_coords):
        face_image = mask_face(image, face_coord)
        record, report_image = classify(face_image, is_bw, to_bw, skin_tone_palette, tone_labels, n_dominant_colors,
                                        verbose=verbose, report_image=image, use_face=True)
        report_image = face_report_image(face_coord, idx, report_image)
        records[idx + 1] = record
        report_images[idx + 1] = report_image

    return records, report_images


def show(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def face_report_image(face, idx, image):
    if image is None:
        return None
    x1, y1, x2, y2 = face
    width = x2 - x1
    height = 20
    bar = np.ones((height, width, 3), dtype=np.uint8) * (255, 0, 0)
    report_image = image.copy()
    report_image[y2:y2 + height, x1:x2] = bar
    txt = f'Face {idx + 1}'
    text_color = (255, 255, 255)
    font_scale = 0.5
    thickness = 1
    text_size, _ = cv2.getTextSize(txt, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
    text_x = x1 + (width - text_size[0]) // 2
    text_y = y2 + 15
    cv2.putText(report_image, txt, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, thickness)
    return report_image
