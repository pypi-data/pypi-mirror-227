"""
routines to reconcile files against a list  image file types
"""
import os
from typing import Iterable

from PIL import Image, UnidentifiedImageError
from datetime import datetime
from pathlib import Path
import re
from queue import Queue
from threading import Lock
import csv
import logging
from bdrc_irat.common import *
from bdrc_irat.ActionContext import ActionContext

wrote_header: bool = False


def build_image_data_for_work(image_list: []) -> []:
    """
    Get files whose contents dont match their suffixes
    :param image_list:
    :return:
    """
    image_data: [] = []
    for img in image_list:
        i_ext: str = Path(img).suffix.replace('.', '')
        try:
            i_format: str = Image.open(img).format
            # Could filter here, but let's build the whole thing
            image_data.append((img, i_ext, i_format))
        except UnidentifiedImageError:
            pass
    return image_data


# Subset of https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
legal_extensions_for_image_type: {} = {"JPEG": ["JPG", "JPEG"],
                                       "TIFF": ["TIF", "TIFF"],
                                       "BMP": ["BMP"],
                                       "WMF": ["WMF"]}


def get_expected_extension(file_ext: str, image_format: str) -> bool:
    """
    Returns true if file_ext is in the list of expected extensions for image_format
    :param file_ext: given extension
    :param image_format: The returned value from PIL Image.format
    :return: true if case normalized search finds file_ext in legal_extensions_for_image_type.values lists
    """
    global legal_extensions_for_image_type
    if image_format not in legal_extensions_for_image_type.keys():
        logging.warning(f"Image format {image_format} not found. Extension: {file_ext}")
    else:
        if file_ext.upper() not in legal_extensions_for_image_type[image_format]:
            return False
    return True


def find_mismatches(image_data_list) -> []:
    """
    returns the subset if images whose extension doesnt match the given file type
    :param image_data_list: list of tuples of image data (path, extension, PIL Image.Format)
    :return:
    """
    return [image_data for image_data in image_data_list if not get_expected_extension(image_data[1], image_data[2])]


def write_len_mismatches(mismatches:[], out_csv: csv.writer, lock: Lock, header: Iterable[str]):
    """
    Reduce function
    Writes list entries to csv file
    :param mismatches: data to write list of tuples.
    :param out_csv: csv output writer
    :param lock: file write synchronization
    :return: None
    Duplicate of common write, but hey
    """

    global wrote_header

    # Dont waste locking when not needed
    if not mismatches:
        return

    lock.acquire(blocking=True)
    try:
        if not wrote_header:
            out_csv.writerow(header)
            wrote_header = True
        out_csv.writerows(mismatches)
    finally:
        lock.release()


def write_mismatch_data(rq: Queue, out_csv: csv.writer, lock: Lock, header: Iterable[str]):
    """
    Consumer of file lis queues
    :param rq: results queue
    :param out_csv: output csv
    :param lock: file write sync lock
    :param header: iterable of csv headings
    :return:
    """
    #  Couldn't get this queue to not hang,
    # so I put the dump in the thread
    # Take 2: setting producer thread daemon true, and marking each queue entry task_done,
    # then join when done
    while True:
        work_image_list = rq.get()
        try:
            #         logging.info(work_image_list)
            mismatches: [] = find_mismatches(work_image_list)
            logging.info(f"{len(work_image_list)} images: {len(mismatches)} mismatches: {mismatches}")

            if len(mismatches) != 0:
                write_len_mismatches(mismatches, out_csv, lock, header)
        finally:
            rq.task_done()


def get_image_data(q: Queue, results_queue: Queue, ctx: ActionContext) -> None:
    """
    Map action (see Reduce action above
    Looks for files in a filtered list whose file extension does not match their contents
    :param q: Input queue of lists of paths to work
    :param results_queue: image lists
    :param ctx: Environment
    :return:
    """

    # Prefer re to fnmatch
    # fnmatch filter
    # Problems with fnmatch:
    #    Not case independent
    # Slow (have to loop over the code explicitly)
    img_re = getattr(threadLocal, 'img_re', None)
    if img_re is None:
        img_re = re.compile(GRAPHICS_FILE_EXTS, re.IGNORECASE)
        threadLocal.img_re = img_re

    while True:
        work_path: Path = Path(ctx.fs_path(q.get()))
        try:
            image_list: [] = []

            wbt = datetime.now()
            for (root, dirs, files) in os.walk(work_path):
                image_list.extend(os.path.join(root, file) for file in files if img_re.match(file))
            # logging.info(f"{threading.current_thread().name} v={str(work_path)},Image_list: len:{len(image_list)}")
            work_image_list: [] = build_image_data_for_work(image_list)
            #
            results_queue.put(work_image_list)

            wet = datetime.now()
            logging.info(
                f"sizes {str(work_path)} sec: {(wet - wbt).total_seconds()} - #Images:{len(image_list)}")
        finally:
            q.task_done()
