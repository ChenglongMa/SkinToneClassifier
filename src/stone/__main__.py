import functools
import logging
import os
import shutil
import threading
from datetime import datetime
from multiprocessing import freeze_support, cpu_count, Pool

import cv2
import numpy as np
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

from stone.api import process
from stone.image import normalize_palette
from stone.utils import build_arguments, build_image_paths, is_windows, ArgumentError

LOG = logging.getLogger(__name__)
lock = threading.Lock()


def process_in_main(
    filename_or_url,
    image_type,
    tone_palette,
    tone_labels,
    convert_to_black_white,
    n_dominant_colors=2,
    new_width=250,
    scale=1.1,
    min_nbrs=5,
    min_size=(90, 90),
    threshold=0.3,
    return_report_image=False,
):
    try:
        return process(
            filename_or_url,
            image_type=image_type,
            tone_palette=tone_palette,
            tone_labels=tone_labels,
            convert_to_black_white=convert_to_black_white,
            n_dominant_colors=n_dominant_colors,
            new_width=new_width,
            scale=scale,
            min_nbrs=min_nbrs,
            min_size=min_size,
            threshold=threshold,
            return_report_image=return_report_image,
        )
    except ArgumentError as e:
        # Abort the app if any argument error occurs
        raise e
    except Exception as e:
        msg = f"Error processing image {filename_or_url}: {str(e)}"
        LOG.error(msg)
        return {
            "filename": filename_or_url,
            "message": msg,
        }


def main():
    args = build_arguments()
    # Setup logger
    now = datetime.now()
    os.makedirs("./log", exist_ok=True)

    logging.basicConfig(
        filename=now.strftime("./log/log-%y%m%d%H%M.log"),
        level=logging.INFO,
        format="[%(asctime)s] {%(filename)s:%(lineno)4d} %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    image_paths = build_image_paths(args.images)

    debug: bool = args.debug
    to_bw: bool = args.black_white

    specified_palette: list[str] = args.palette

    if specified_palette is not None and len(specified_palette) > 0:
        specified_palette = normalize_palette(specified_palette)

    specified_tone_labels = args.labels

    new_width = args.new_width
    n_dominant_colors = args.n_colors
    min_size = args.min_size[:2]
    scale = args.scale
    min_nbrs = args.min_nbrs
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    result_filename = os.path.join(output_dir, "./result.csv")
    image_type_setting = args.image_type
    threshold = args.threshold

    def write_to_csv(row: list):
        with lock:
            with open(result_filename, "a", newline="", encoding="UTF8") as f:
                f.write(",".join(map(str, row)) + "\n")

    num_workers = cpu_count() if args.n_workers == 0 else args.n_workers

    pool = Pool(processes=num_workers)

    # Backup result.csv if exists
    if os.path.exists(result_filename):
        renamed_file = os.path.join(output_dir, now.strftime("./result_bak_%y%m%d%H%M.csv"))
        shutil.move(result_filename, renamed_file)
    header = (
        "file,image type,face id,"
        + ",".join([f"dominant {i + 1},percent {i + 1}" for i in range(n_dominant_colors)])
        + ",skin tone,tone label,accuracy(0-100)"
    )
    write_to_csv(header.split(","))

    # Start

    process_wrapper = functools.partial(
        process_in_main,
        image_type=image_type_setting,
        tone_palette=specified_palette,
        tone_labels=specified_tone_labels,
        convert_to_black_white=to_bw,
        n_dominant_colors=n_dominant_colors,
        new_width=new_width,
        scale=scale,
        min_nbrs=min_nbrs,
        min_size=min_size,
        threshold=threshold,
        return_report_image=debug,
    )
    with logging_redirect_tqdm():
        with tqdm(image_paths, desc="Processing images", unit="images") as pbar:
            for result in pool.imap(process_wrapper, image_paths):
                if "message" in result:
                    write_to_csv([result["filename"], result["message"]])
                    pbar.update()
                    continue

                basename = result["basename"]
                extension = result["extension"]
                image_type = result["image_type"]
                faces = result["faces"]
                report_images = result["report_images"]

                pbar.set_description(f"Processing {basename}")
                n_faces = len(faces)

                for face_record in faces:
                    face_id = face_record["face_id"]
                    if face_id == "NA":
                        n_faces = 0  # Did not detect any faces
                    dominant_colors = [[item["color"], item["percent"]] for item in face_record["dominant_colors"]]
                    record = (
                        [f"{basename}{extension}", image_type, face_id]
                        + np.hstack(dominant_colors).tolist()
                        + [face_record["skin_tone"], face_record["tone_label"], face_record["accuracy"]]
                    )

                    write_to_csv(record)
                    pbar.set_postfix(
                        {
                            "Image Type": image_type,
                            "#Faces": n_faces,
                            "Face ID": face_id,
                            "Skin Tone": face_record["skin_tone"],
                            "Label": face_record["tone_label"],
                            "Accuracy": face_record["accuracy"],
                        }
                    )
                if debug:
                    debug_dir = os.path.join(output_dir, f"./debug/{image_type}/faces_{n_faces}")
                    os.makedirs(debug_dir, exist_ok=True)
                    for face_id, report_image in report_images.items():
                        image_name = f"{basename}-{face_id}"
                        report_filename = os.path.join(debug_dir, f"{image_name}{extension}")
                        with lock:
                            cv2.imwrite(report_filename, report_image)
                pbar.update()
    pool.close()
    pool.join()


if __name__ == "__main__":
    if is_windows():
        freeze_support()
    main()
