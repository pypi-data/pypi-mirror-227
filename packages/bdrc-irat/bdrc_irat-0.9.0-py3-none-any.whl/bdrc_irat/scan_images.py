#!/usr/bin/env python3
"""
walk a directory tree and count its files. (an extension will enumerate them)

Build a thread pools of producers which crawl a tree and list the image files in it.

A consumer thread reads the results_queue as entries come in and checks the list for file extension X type
compatibility. in that way, the results queue never gets too big - because each work can contain hundreds of images,
collecting them all before testing any of them would consume system resources.

You can parse the log output with this awk: awk -F'[: ]'  '$16 ~ /^Image_list$/{et += $14; len += $19} END{print
"et:" et "  n_img:" len " avg: " et/len } ' frelm.log This isn't an accurate count because of parallelism. Each
thread reports it's elapsed time (et), but since there are 10 in parallel, the actual e.t. is the one at the end. For
example, on a remote disk, this can sample 2997 images in 102 sec.

"""
from collections import defaultdict

from datetime import datetime

from queue import Queue
import logging

import csv

from threading import Thread, Lock
from typing import Iterable

from bdrc_irat.PsParser import *
from bdrc_irat.common import *

# import threading
from bdrc_irat.action_types import get_image_data, write_mismatch_data
from bdrc_irat.action_list import count_files_in_image_groups
from bdrc_irat.action_fs_sizes import get_image_sizes
from bdrc_irat.ActionContext import ActionContext

q: Queue = Queue(maxsize=0)
results_queue: Queue = Queue(maxsize=0)
out_file_lock: Lock = Lock()
csv_writer: csv.writer = None

#
# {work,{ { 'ig' : {'fs': n}, 's3':m}}...}
total_ig_counts: defaultdict[lambda: None] = defaultdict(lambda: None)

wrote_header: bool = False


def build_action_map(action_context: ActionContext) -> {}:
    """
    Build the action map after all its globals have been instantiated
    :return:
    """
    # noinspection PyUnboundLocalVariable
    return {
        LIST_ACTION: {
            'map':
                {
                    'call': count_files_in_image_groups,
                    'args': (q, results_queue,action_context,)
                },
            'reduce':
                {
                    'call': common_write,
                    'args': (results_queue, csv_writer, out_file_lock,csv_out_headers[LIST_ACTION],)
                }
        },
        TYPES_ACTION: {
            'map':
                {
                    'call': get_image_data,
                    'args': (q, results_queue,action_context,)
                },
            'reduce':
                {
                    'call': write_mismatch_data,
                    'args': (results_queue, csv_writer, out_file_lock,csv_out_headers[TYPES_ACTION])
                }
        },
        SIZES_ACTION: {
            'map':
                {
                    'call': get_image_sizes,
                    'args': (q, results_queue,action_context,)
                },
            'reduce':
                {
                    'call': common_write,
                    'args': (results_queue, csv_writer, out_file_lock, csv_out_headers[SIZES_ACTION],)
                }
        }
    }


def build_work_list(args: PsArgs) -> []:
    """
    Build an expanded list of the arguments
    :param args:
    :return:
    """
    src_list: [] = []
    out_list: [] = []

    # Merge --work_rids and --input_list_file values
    if args.work_rids:
        src_list.extend([aw for aw in args.work_rids])
    if args.input_list_file:
        with open(args.input_list_file.name, newline='\n') as workInFile:
            # https://stackoverflow.com/questions/12330522/how-to-read-a-file-without-newlines
            # Build the worklist to contain the prefix
            for aWork in workInFile.read().splitlines():
                src_list.append(aWork)

        # deduplicate and sort
        src_list = list(dict.fromkeys(src_list))
        src_list.sort()

    logging.info(f"Built {args.action} {len(out_list)}")
    return src_list



def common_write(rq: Queue, out_csv: csv.writer, lock: Lock, header: Iterable[str]):
    """
    Consumer of file list queues
    :param rq: input queue
    :param out_csv: output csv
    :param lock: file write sync lock
    :param header: header for csv
    :return:
    """
    global wrote_header

    while True:
        work_data = rq.get()
        try:
            #         logging.info(work_image_list)
            lock.acquire(blocking=True)
            try:
                # Data must match its header
                if not wrote_header:
                    out_csv.writerow(header)
                    wrote_header = True
                out_csv.writerow(work_data)
            finally:
                lock.release()
        finally:
            rq.task_done()
def ps_shell() -> None:
    """
    outer shell
    :return:
    """

    args = PsArgs()
    PsParser().parse_args(args)

    # Set up csv output
    global csv_writer
    csv_writer = csv.writer(args.output_file, delimiter=',', quotechar='"')

    logging.basicConfig(format=LOG_MESSAGE_FORMAT,
                        level=logging.DEBUG, datefmt=LOG_DATEFMT)

    # Just debug ourselves, mKay?
    for hush_lib in ['boto3', 'PIL', 'pillow', 'request', 'botocore', 'urllib3']:
        logging.getLogger(hush_lib).setLevel(logging.CRITICAL)

    num_threads: int = 24

    logging.info("> Begin")
    action_context:ActionContext = ActionContext(fs_base=args.fs_base, s3_base=args.s3_base, s3_bucket=args.s3_bucket)
    action_map = build_action_map(action_context)
    action_entry = action_map[args.action]
    for i in range(num_threads):
        # producer = Thread(target=do_stuff, args=(q,), name=f"t[{i}]")
        producer = Thread(target=action_entry['map']['call'], args=action_entry['map']['args'],
                          name=f"p-{i:02}")
        producer.setDaemon(True)
        producer.start()

    # Consuming is much faster than producing
    for j in range(int(num_threads / 4)):
        #
        # Create a thread to process the results as they come in
        consumer = Thread(target=action_entry['reduce']['call'], args=action_entry['reduce']['args'],
                          name=f"c-{j:02}")
        consumer.setDaemon(True)
        consumer.start()

    bt = datetime.now()
    logging.info(f"Building {args.action} list")

    # DEBUG: shorten work
    work_list = build_work_list(args)
    # the work list begins with fs works, ends with bogus s3 works. Pick some in the middle
    # This range is all live s3: work_list[89423:89433]:
    # This range tests invalid S3: work_list[-15:]
    # DEBUG:
    # sample_work_list = work_list[:10]
    # sample_work_list = [x for x in work_list
    #                     if 'W00CHZ0103345' in x
    #                     or 'W1FPL7626' in x
    #                     or 'W1KG14783' in x]
    # for x in sample_work_list:
    for x in work_list:
        logging.debug("Adding %s", x)
        q.put(x)

    logging.info("waiting")
    q.join()

    et = datetime.now()
    logging.info("Done waiting")

    results_queue.join()

    args.output_file.close()
    logging.info("< End ET: %s ", (et - bt).total_seconds())
    sys.exit(0)


if __name__ == "__main__":
    ps_shell()
