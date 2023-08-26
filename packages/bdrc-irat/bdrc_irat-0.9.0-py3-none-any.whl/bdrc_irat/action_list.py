import sys
from collections import defaultdict
from typing import Iterable
import re
import os
from datetime import datetime
from pathlib import Path
from queue import Queue
import logging
from threading import Lock
import boto3
from s3pathlib import context, S3Path

from bdrc_irat.common import *
from bdrc_irat.ActionContext import ActionContext
from util_lib.GetFromBUDA import _buda_ig_from_disk


IMAGES = "images"
FS_COUNT = 'fs'
S3_COUNT = 's3'

# Write queue lock - marshalls all igs for a work into queue together
wq_lock: Lock = Lock()


def s3_work_image_group_counts(bucket: str, work: str) -> defaultdict[None]:
    """
    Get the s3 image groups
    :param bucket:
    :param work: fully resolved prefix to work
    :return:
    """

    def s3p_matches(path: S3Path) -> bool:
        return img_re.match(path.key)

    s3_path_context = getattr(threadLocal, 's3_ctx', None)
    if s3_path_context is None:
        session = boto3.session.Session(region_name='us-east-1')
        threadLocal.s3_ctx = context
        context.attach_boto_session(session)

    img_re = getattr(threadLocal, 'img_re', None)
    if img_re is None:
        img_re = re.compile(GRAPHICS_FILE_EXTS, re.IGNORECASE)
        threadLocal.img_re = img_re

    # Rewrite using AWS S3pathlib
    s3_images_root = S3Path(bucket, work, IMAGES+"/")

    # These are expensive - cache locally
    work_rid:str = s3_images_root.parent.basename

    # now travel the results, bucketing by image group
    image_group_counts: dict = {}
    # Only get top level dir
    # Take 1 - recursive = False only gets the objects with the prefix, does not descend
    #    for image_group in s3_images_root.iter_objects(recursive=False):
    for image_group in s3_images_root.iterdir().all():
        raw_base = image_group.basename
        if not raw_base.startswith(work_rid):
            continue
        disk_ig = _buda_ig_from_disk(raw_base)

        try:
            image_group_counts[disk_ig] = len(image_group.iter_objects(recursive=False).filter(s3p_matches).all())
        except:
            ei = sys.exc_info()
            logging.error(ei)

    return image_group_counts
    # region --------  OLD STUFF   ---------
    # noinspection PyUnreachableCode
    s3 = getattr(threadLocal, 's3', None)
    if s3 is None:
        session = boto3.session.Session(region_name='us-east-1')
    s3_client = session.client('s3')
    threadLocal.s3 = s3_client

    image_prefix: str = str(Path(work, IMAGES))
    # Need a paginator to get around the 1000 item limit
    page_iterator = s3_path_context.get_paginator('list_objects_v2').paginate(Bucket=bucket,
                                                                              Prefix=image_prefix)
    s3_images_list = []
    # Get all the works' object list from the first value
    # These are broken out by image group later
    for page in page_iterator:
        if page['KeyCount'] > 0:
            try:
                object_list = [x for x in page["Contents"]]
                s3_images_list.extend([x['Key'] for x in object_list if img_re.match(x['Key'])])
            except Exception as eek:
                logging.exception(eek)

    # now travel the results, bucketing by image group
    image_group_counts: defaultdict = defaultdict(lambda: 0)
    for image in s3_images_list:
        # S3 name W----Ixxxx

        # bug - this line doesn't handle images in "subdir correctly, because assumes image group is one "folder"
        # up. Need to work down from IMAGES.
        # Poor man's S3Path
        s3_url = urlparse(image)
        s3_path = PosixPath(s3_url.path)
        s3_tree = s3_path.parts
        s3_parent_index = s3_tree.index(IMAGES)
        # Skip this if:
        # the item is just the images folder
        #      s3_tree = ['work','images']
        # the item is just the image group folder
        #      s3_tree = ['work','images','work-Ig']
        # the item is in a subfolder
        #      s3_tree = [ 'work','images','work-Ig','some_stupid_leftover','more_stuff']
        # In sum, the only things we're interested in are items in the shape:
        #     s3_tree = [ 'work','images','work-Ig','folder','object]
        # Which means items where
        #     len(s3_tree) == s3_tree.index(IMAGES) +2
        # and the image group is at
        #     len(s3_tree) == s3_tree.index(IMAGES) + 1
        if len(s3_tree) != s3_parent_index + 2:
            continue
        # is it an image file? Use the whole tree
        #
        # Convert to buda ig name
        ig_name = _buda_ig_from_disk(s3_tree[s3_parent_index + 1])
        image_group_counts[ig_name] += 1

        return image_group_counts


def fs_work_image_group_counts(work: str) -> defaultdict[None]:
    """
    Count the files in the image groups under the work path
    :param work:
    :return:
    """
    # DEBUG: Skip the files
    # out_list: [()] = []
    # return out_list
    img_re = getattr(threadLocal, 'img_re', None)
    if img_re is None:
        img_re = re.compile(GRAPHICS_FILE_EXTS, re.IGNORECASE)
        threadLocal.img_re = img_re

    image_group_counts: defaultdict = defaultdict(lambda: 0)
    try:
        for thing in os.scandir(Path(work, IMAGES)):

            if thing.is_dir():
                # Transform disk name to BUDA name from {Workgroup}-{ImageGroup}
                image_group_name = _buda_ig_from_disk(thing.name.split('-')[1])
                ig_count = -1
                for _, _dir, _files in os.walk(Path(thing.path), topdown=True):
                    ig_count = len([file for file in _files if img_re.match(file)])

                    # Just count top level, don't iterate in _dir
                    break
                image_group_counts[image_group_name] = ig_count
    except FileNotFoundError as fnfe:
        logging.warning(fnfe)

    return image_group_counts


def count_files_in_image_groups(q: Queue, results_queue: Queue, ctx: ActionContext) -> None:
    """
    Map action
    q contains two paths
    :param q:
    :param results_queue:
    :param ctx: Fixed parameters and methods
    :type ctx: ActionContext
    :return: pushes items on queue
    """

    while True:
        work_rid: str = q.get()
        try:
            wbt = datetime.now()
            fs_ig_counts = fs_work_image_group_counts(ctx.fs_path(work_rid))
            s3_ig_counts = s3_work_image_group_counts(ctx.s3_bucket, ctx.s3_path(work_rid))

            # Merge the image group counts
            merged_image_group_keys: set = set(fs_ig_counts.keys()).union(s3_ig_counts.keys())

            # Foe ease, make sure all igs for this group arrive in the queue uninterrupted
            wq_lock.acquire(blocking=True)
            try:
                for ig in merged_image_group_keys:
                    # Must be the same order as in csv_headers[LIST_ACTION]
                    results_queue.put((work_rid, ig, fs_ig_counts[ig], s3_ig_counts[ig]))
            finally:
                wq_lock.release()
            wet = datetime.now()
            logging.debug(
                f" collected count {work_rid} sec: {(wet - wbt).total_seconds()}")
        finally:
            q.task_done()


# Deprecated
def write_output(output_file: object, total_ig_counts: defaultdict[lambda: None], headers: Iterable[str]):
    """
    writes csv formatted output to the list
    :param output_file: Python File object
    :param total_ig_counts: sparse dict of counts
    :param headers: output csv headers
    :return:
    """
    # with open(args.output_file,'w') as outf:
    writer = csv.writer(output_file)
    writer.writerow(headers)
    # items() returns tuple
    for ig in total_ig_counts.items():
        ig_work = ig[0]
        from collections import defaultdict
        ig_counts: defaultdict[lambda: None] = ig[1]
        # items() is tuple
        if len(ig_counts.items()) > 0:
            for ig_count in ig_counts.items():
                ig_counts = ig_count[1]
                writer.writerow((ig_work, ig_count[0], ig_counts['fs'], ig_counts['s3']))
        else:
            writer.writerow((ig_work, None, None, None))
