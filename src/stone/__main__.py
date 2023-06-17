import os
import logging
from datetime import datetime

import cv2
import numpy as np
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

from image import process, is_black_white
from utils import build_arguments, writerow, alphabet_id, build_filenames


def patch_asscalar(a):
    return np.asarray(a).item()


setattr(np, "asscalar", patch_asscalar)

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

    args = build_arguments()

    filenames = build_filenames(args.images)
    is_single_file = len(filenames) == 1

    debug: bool = args.debug

    default_color_palette = ["#373028", "#422811", "#513b2e", "#6f503c", "#81654f", "#9d7a54", "#bea07e", "#e5c8a6", "#e7c1b8", "#f3dad6",
                             "#fbf2f3"]

    # Refer to this paper:
    # Leigh, A., & Susilo, T. (2009). Is voting skin-deep? Estimating the effect of candidate ballot photographs on election outcomes.
    # Journal of Economic Psychology, 30(1), 61-70.
    default_bw_palette = ["#FFFFFF", "#F0F0F0", "#E0E0E0", "#D0D0D0", "#C0C0C0", "#B0B0B0", "#A0A0A0", "#909090", "#808080", "#707070", "#606060",
                          "#505050", "#404040", "#303030", "#202020", "#101010", "#000000"]

    specified_palette: list[str] = args.palette if args.palette is not None else []
    tone_labels = args.labels

    for idx, ct in enumerate(specified_palette):
        if not ct.startswith('#') and len(ct.split(',')) == 3:
            r, g, b = ct.split(',')
            specified_palette[idx] = '#%02X%02X%02X' % (int(r), int(g), int(b))

    n_dominant_colors = args.n_colors
    min_size = args.min_size[:2]
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)

    # Start - open file
    f = open(os.path.join(output_dir, './result.csv'), 'w', encoding='UTF8')
    header = 'file,image type,face id,' + ','.join(
        [f'dominant {i + 1},props {i + 1}' for i in range(n_dominant_colors)]) + ',skin tone,PERLA,distance(0-100)\n'
    f.write(header)

    # Start - processing images
    with logging_redirect_tqdm():
        for filename in tqdm(filenames):
            basename, extension = filename.stem, filename.suffix
            image_type = args.image_type

            LOG.info(f'\n----- Processing {basename} -----')
            # try:
            image: np.ndarray = cv2.imread(str(filename.resolve()), cv2.IMREAD_UNCHANGED)
            if image is None:
                LOG.warning(f'{filename}.{extension} is not found or is not a valid image.')
                continue
            is_bw = is_black_white(image)
            if image_type == 'auto':
                image_type = 'bw' if is_bw else 'color'
            if len(specified_palette) == 0:
                skin_tone_palette = default_bw_palette if image_type == 'bw' else default_color_palette
            else:
                skin_tone_palette = specified_palette
            tone_labels = tone_labels or [alphabet_id(i) for i in range(len(skin_tone_palette))]
            records, report_images = process(image, skin_tone_palette, tone_labels, new_width=args.new_width,
                                             n_dominant_colors=n_dominant_colors,
                                             scaleFactor=args.scale, minNeighbors=args.min_nbrs, minSize=min_size,
                                             verbose=debug)

            # Write to file
            n_faces = len(records)
            for face_id, record, in records.items():
                if face_id == 'NA':
                    n_faces = 0  # Did not detect any faces
                image_name = f'{basename}-{face_id}'
                writerow(f, [image_name, image_type, face_id] + record)
            if debug:
                debug_dir = os.path.join(output_dir, f'./debug/{image_type}/faces_{n_faces}')
                os.makedirs(debug_dir, exist_ok=True)
                for face_id, report_image in report_images.items():
                    image_name = f'{basename}-{face_id}'
                    report_filename = os.path.join(debug_dir, f'{image_name}{extension}')
                    cv2.imwrite(report_filename, report_image)
                    if is_single_file:
                        cv2.imshow(f'Skin Tone Classifier - {image_name}', report_image)

            # except Exception as e:
            #     LOG.error(f'Error occurred while processing {filename}: {e}')
            # writerow(f, [basename, f'Error: {e}'])
            # continue

    f.close()

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
