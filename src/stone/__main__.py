import argparse
import glob
import logging
import os
import re
from datetime import datetime

import cv2
import imutils
import numpy as np
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import sRGBColor, LabColor
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from pathlib import Path


def patch_asscalar(a):
    return np.asarray(a).item()


setattr(np, "asscalar", patch_asscalar)


def sort_file(filename: Path):
    nums = re.findall(r'\d+', filename.stem)
    return int(nums[0]) if nums else filename


def detect_faces(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)):
    image = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    rects = cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize, flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects


def detect_skin(image):
    img = image.copy()
    # Converting from BGR Colours Space to HSV
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Defining skin Thresholds
    low_hsv = np.array([0, 48, 80], dtype=np.uint8)
    high_hsv = np.array([20, 255, 255], dtype=np.uint8)

    skinMask = cv2.inRange(img, low_hsv, high_hsv)
    skinMask = cv2.GaussianBlur(skinMask, ksize=(3, 3), sigmaX=0)
    skin = cv2.bitwise_and(img, img, mask=skinMask)

    all_0 = np.isclose(skin, 0).all()
    return image if all_0 else cv2.cvtColor(skin, cv2.COLOR_HSV2BGR)


def draw_rects(image, *rects, color=(0, 255, 0), thickness=2):
    image = image.copy()
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(image, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1), color, thickness)
    return image


def create_bar(height, width, color):
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:] = color
    return bar


def dominant_colors(image, n_clusters=3):
    data = np.reshape(image, (-1, 3))
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


def skin_label(colors, props, categories, cate_labels):
    lab_labels = [convert_color(sRGBColor.new_from_rgb_hex(lbl), LabColor) for lbl in categories]
    lab_colors = [convert_color(sRGBColor(rgb_r=r, rgb_g=g, rgb_b=b, is_upscaled=True), LabColor) for b, g, r in colors]
    distances = [np.sum([delta_e_cie2000(c, label) * p for c, p in zip(lab_colors, props)]) for label in lab_labels]
    label_id = np.argmin(distances)
    distance: float = distances[label_id]
    category_hex = categories[label_id]
    PERLA = cate_labels[label_id]
    LOG.info(f'Classified color category: {category_hex}, distance: {distance}')
    return label_id, category_hex, PERLA, distance


def classify(image, n_dominant_colors, categories, cate_labels, report_image, debug=False):
    image = image.copy()
    image = detect_skin(image)

    colors, props = dominant_colors(image, n_clusters=n_dominant_colors)

    # Generate readable strings
    hex_colors = ['#%02X%02X%02X' % tuple(np.around([r, g, b]).astype(int)) for b, g, r in colors]
    prop_strs = ['%.2f' % p for p in props]
    res = list(np.hstack(list(zip(hex_colors, prop_strs))))
    LOG.info(f'Dominant color(s) with proportion: {res}')
    label_id, category_hex, PERLA, distance = skin_label(colors, props, categories, cate_labels)
    distance = round(distance, 2)
    res.extend([category_hex, PERLA, distance])

    debug_img = None
    if debug:
        color_bars = []
        color_w = 100
        total_height = 0
        for index, color in enumerate(colors):
            color_h = round(report_image.shape[0] * props[index])
            total_height += color_h
            bar = create_bar(color_h, color_w, color)
            color_bars.append(bar)

        padding_height = report_image.shape[0] - total_height
        if padding_height > 0:
            padding = create_bar(padding_height, color_w, (255, 255, 255))
            color_bars.append(padding)
        color_bars = np.vstack(color_bars)

        label_bars = []
        label_h = report_image.shape[0] // len(categories)
        label_w = color_w
        label_bgrs = []
        for label_hex in categories:
            hex_val = label_hex.lstrip('#')
            lr, lg, lb = [int(hex_val[i:i + 2], 16) for i in (0, 2, 4)]
            label_bgrs.append([lb, lg, lr])
            label_bar = create_bar(label_h, label_w, [lb, lg, lr])
            label_bars.append(label_bar)
        padding_height = report_image.shape[0] - label_h * len(categories)
        if padding_height > 0:
            padding = create_bar(padding_height, label_w, (255, 255, 255))
            label_bars.append(padding)
        label_bars = np.vstack(label_bars)

        debug_img = np.hstack([report_image, color_bars, label_bars])

        p = 2
        y1 = label_id * label_h + p
        y2 = y1 + label_h - p
        x1 = report_image.shape[1] + color_w
        x2 = x1 + label_w - p
        debug_img = draw_rects(debug_img, [x1, y1, x2, y2], thickness=2)

        msg_bar = create_bar(50, debug_img.shape[1], color=(243, 239, 214))

        db, dg, dr = np.around(colors[0]).astype(int)
        dominant_color_hex = '#%02X%02X%02X' % (dr, dg, db)
        prop = f'{props[0] * 100:.2f}%'

        font, font_scale, thickness, line_type = cv2.FONT_HERSHEY_SIMPLEX, .5, 1, cv2.LINE_AA
        x, y = 2, 15
        msg = f'- Dominant color: {dominant_color_hex}, proportion: {prop}'
        cv2.putText(msg_bar, msg, (x, y), font, font_scale, (int(db), int(dg), int(dr)), thickness, line_type)

        text_size, _ = cv2.getTextSize(msg, font, font_scale, thickness)
        line_height = text_size[1] + 10

        cv2.putText(msg_bar, f'- Classified category: {category_hex}, distance: {distance}', (x, y + line_height), font, font_scale,
                    label_bgrs[label_id], thickness, cv2.LINE_AA)

        debug_img = np.vstack([debug_img, msg_bar])

    return res, debug_img


def writerow(f, arr: list):
    f.write(','.join(map(str, arr)) + '\n')


LOG = logging.getLogger(__name__)


def main():
    # Setup logger
    now = datetime.now()
    os.makedirs('./log', exist_ok=True)

    logging.basicConfig(
        filename=now.strftime('./log/log-%y%m%d%H%M.log'),
        level=logging.INFO,
        format='[%(asctime)s] {%(filename)s:%(lineno)4d} %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    # Setup arguments
    parser = argparse.ArgumentParser(description='Skin Tone Classifier', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--images', nargs='+', default='./', metavar='IMAGE FILENAME',
                        help='Image filename(s) to process;\n'
                             'supports multiple values separated by space, e.g., "a.jpg b.png";\n'
                             'supports directory or file name(s), e.g., "./path/to/images/ a.jpg";\n'
                             'The app will search all images in current directory in default.')

    default_categories = ["#373028", "#422811", "#513b2e", "#6f503c", "#81654f", "#9d7a54", "#bea07e", "#e5c8a6", "#e7c1b8", "#f3dad6", "#fbf2f3"]

    default_labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:len(default_categories)]
    parser.add_argument('-c', '--categories', nargs='+', default=default_categories, metavar='COLOR',
                        help='Skin tone categories; supports RGB hex value leading by # or RGB values separated by comma(,), e.g., -c #373028 #422811 or 255,255,255 100,100,100')
    parser.add_argument('-l', '--labels', nargs='+', default=default_labels, metavar='LABEL',
                        help='Category labels; default values are uppercase alphabet list.')
    parser.add_argument('-d', '--debug', action='store_true', help='Whether to output processed images, used for debugging and verification.')
    parser.add_argument('-o', '--output', default='./', metavar='DIRECTORY',
                        help='The path of output file, defaults to current directory.')

    parser.add_argument('--n_colors', type=int, metavar='N',
                        help='CONFIG: the number of dominant colors to be extracted, defaults to 2.', default=2)
    parser.add_argument('--new_width', type=int, metavar='WIDTH',
                        help='CONFIG: resize the images with the specified width. Negative value will be ignored, defaults to -1.', default=-1)

    # Refer to https://stackoverflow.com/a/20805153/8860079
    parser.add_argument('--scale', type=float, help='CONFIG: how much the image size is reduced at each image scale, defaults to 1.1', default=1.1)
    parser.add_argument('--min_nbrs', type=int, metavar='NEIGHBORS',
                        help='CONFIG: how many neighbors each candidate rectangle should have to retain it.\n'
                             'Higher value results in less detections but with higher quality, defaults to 5', default=5)
    parser.add_argument('--min_size', type=int, nargs='+', metavar=('WIDTH', 'HEIGHT'),
                        help='CONFIG: minimum possible face size. Faces smaller than that are ignored, defaults to "30 30".', default=(30, 30))

    args = parser.parse_args()

    # Parse arguments
    filenames = []
    valid_images = ['*.jpg', '*.gif', '*.png', '*.jpeg', '*.webp', '*.tif']

    for name in args.images:
        if os.path.isdir(name):
            filenames.extend([glob.glob(os.path.join(name, i)) for i in valid_images])
        if os.path.isfile(name):
            filenames.append([name])

    filenames = [Path(f) for fs in filenames for f in fs]
    assert len(filenames) > 0, 'No valid images in the specified path.'
    # Sort filenames by (first) number extracted from the filename string
    filenames.sort(key=sort_file)
    is_single_file = len(filenames) == 1

    debug: bool = args.debug
    categories: list[str] = args.categories
    cate_labels = args.labels
    for idx, ct in enumerate(categories):
        if not ct.startswith('#') and len(ct.split(',')) == 3:
            r, g, b = ct.split(',')
            categories[idx] = '#%02X%02X%02X' % (int(r), int(g), int(b))
    n_dominant_colors = args.n_colors
    min_size = args.min_size[:2]
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)

    # Start - open file
    f = open(os.path.join(args.output, './result.csv'), 'w', encoding='UTF8')
    header = 'file,face_location,' + ','.join(
        [f'dominant_{i + 1},props_{i + 1}' for i in range(n_dominant_colors)]) + ',category,PERLA,distance(0-100)\n'
    f.write(header)

    # Start - processing images
    with logging_redirect_tqdm():
        for filename in tqdm(filenames):
            basename, extension = filename.stem, filename.suffix

            LOG.info(f'\n----- Processing {basename} -----')
            ori_image = cv2.imread(str(filename.resolve()), cv2.IMREAD_UNCHANGED)
            if ori_image is None:
                LOG.warning(f'{filename}.{extension} is not found or is not a valid image.')
                continue

            resized_image = imutils.resize(ori_image, width=args.new_width) if args.new_width > 0 else ori_image
            final_image = resized_image.copy()
            faces = detect_faces(resized_image, args.scale, args.min_nbrs, min_size)

            debug_imgs = []
            if len(faces) > 0:
                LOG.info(f'Found {len(faces)} face(s)')
                for idx, (x1, y1, x2, y2) in enumerate(faces):
                    sub_filename = f'{basename}-{idx + 1}'
                    LOG.info(f'Face {idx + 1} location: {x1}:{x2}')
                    face = resized_image[y1:y2, x1:x2]
                    if debug:
                        final_image = draw_rects(resized_image, [x1, y1, x2, y2])
                    res, _debug_img = classify(face, n_dominant_colors, categories, cate_labels, final_image, debug)
                    writerow(f, [sub_filename, f'{x1}:{x2}'] + res)
                    debug_imgs.append(_debug_img)
            else:
                LOG.info(f'Found 0 face, will detect global skin area instead')
                res, _debug_img = classify(resized_image, n_dominant_colors, categories, cate_labels, final_image, debug)
                writerow(f, [basename, 'NA'] + res)
                debug_imgs.append(_debug_img)

            if debug:
                debug_dir = os.path.join(output_dir, './debug')
                os.makedirs(debug_dir, exist_ok=True)
                for idx, img in enumerate(debug_imgs):
                    sub_filename = f'{basename}-{idx + 1}'
                    debug_filename = os.path.join(debug_dir, f'{sub_filename}{extension}')
                    cv2.imwrite(debug_filename, img)
                    if is_single_file:
                        cv2.imshow(f'Skin Tone Classifier - {sub_filename}', img)
    f.close()

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
