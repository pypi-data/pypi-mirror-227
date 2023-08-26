#!/usr/bin/env python3
"""
Gets list of files different between S3 and image group.
Reads the output of scan-images -a list for different counts.
Doesn't look for differences internal to a file (such as size or checksum).
"""
import argparse
import sys
import csv
from pathlib import Path
import re

import boto3

from common import *
from bdrc_irat.ActionContext import ActionContext

locators: ActionContext = None

# Regexp for image file
img_re = re.compile(GRAPHICS_FILE_EXTS, re.IGNORECASE)

# global S3 boto session
S3: boto3.session

class PsParser:
    """
    Handles arguments on command line
    """

    _parser: argparse.ArgumentParser

    def __init__(self):
        self._parser = argparse.ArgumentParser(usage="See parallelscan/README.doc for details",
                                               description="Lists divergent files from a file count database")
        self._parser.add_argument("-i", "--input_count_file",
                                  help="csv file with row format  ['work', 'image_group', 'fs_count', 's3_count']. "
                                       "See common.py. ! MUST HAVE HEADER!",
                                  type=argparse.FileType(mode='r'))
        self._parser.add_argument("-o", "--output_file", help="[Optional] output file (default stdout)",
                                  type=argparse.FileType('w'), default=sys.stdout)
        self._parser.add_argument("-f", "--fs_base", help="[Optional] Base of file system resolve path",
                                  default=FS_BASE)
        self._parser.add_argument("-s", "--s3_base", help="[Optional] Prefix (not the bucket) of S3 resolution",
                                  default=S3_BASE)
        self._parser.add_argument("-b", "--s3_bucket", help="[Optional] S3 search bucket",
                                  default=BUDA_BUCKET)

    def parse_args(self, ns: PsArgs):
        """
        :parameter: ns:  namespace for compiled args
        Parse arguments on command line
        :return: command line args in ns
        """
        self._parser.parse_args(namespace=ns)


def s3_image_keys(prefix: str, bucket: str) -> set:
    """
    Gets the image keys in a prefix
    :param prefix:
    :param bucket:
    :return:
    """
    img_keys: set = {}
    continuation_token = None
    while True:
        if continuation_token:
            response = S3.list_objects_v2(Bucket=bucket, Prefix=prefix, ContinuationToken=continuation_token)
        else:
            response = S3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if 'Contents' in response and response['Contents']:
            for obj in response['Contents']:
                obj_key = obj['Key']

                if not img_re.match(obj_key):
                    continue

                # ? obj_key.endswith()?
                key_noprefix = obj_key[len(prefix):]
                if "/" in key_noprefix:
                    # don't look at subdirectories
                    continue

                img_keys.add(obj_key)
        continuation_token = response.get("NextContinuationToken")
        if not continuation_token:
            break
    return img_keys


def fs_image_files(directory: Path) -> set:
    fs_files: set = {}
    for thing in os.scandir(directory):
        realname=os.fsdecode(thing.name)
        if thing.is_dir() or not img_re.match(realname):
            continue
        fs_files.add(thing.name)
    return fs_files


def ig_diff(work_rid: str, ig_rid: str):
    """
    Returns differences between two resources
    :param work_rid: work id
    :param ig_rid: image group id
    :return:
    """
    fs_ig_list: set = fs_image_files(Path(locators.fs_path(work_rid), IMAGES_FOLDER, f"{work_rid}-{ig_rid}"))
    s3_ig_list: set = s3_image_keys(
        f"{locators.s3_path(work_rid)}/{IMAGES_FOLDER}/{work_rid}-{ig_rid}/", locators.s3_bucket)


def get_shell():
    """
    outer shell
    :return:
    """
    args = PsArgs()
    PsParser().parse_args(args)

    diffs: {}

    global locators

    locators = ActionContext(fs_base=args.fs_base, s3_base=args.s3_base, s3_bucket=args.s3_bucket)

    global S3

    session = boto3.session.Session(region_name='us-east-1')
    S3 = session.client('s3')

    # We could use list comprehension, but we don't need to load
    # up > 90000 lines
    with open(args.input_list_file, 'r') as src:
        csv_reader: csv.DictReader = csv.DictReader(src, csv_out_headers[LIST_ACTION])
        for row in csv_reader:

            # Some simple cases
            # Not on S3
            if row['fs_count'] and (not row['s3_count'] or row['s3_count'] == 0):
                print(f"{row['work']}-{row['image_group']} has {row['fs_count']} images in archive, but not S3.")
            if row['s3_count'] and (not row['fs_count'] or row['fs_count'] == 0):
                print(f"{row['work']}-{row['image_group']} has {row['s3_count']} in S3, but not archive.")
            if row['fs_count'] == row['s3_count']:
                print(f"{row['work']}-{row['image_group']} has same image count: {row['fs_count']}")
            else:
                fs_only, s3_only = ig_diff(locators, row['work'], row['image_group'])


if __name__ == '__main__':
    get_shell()
