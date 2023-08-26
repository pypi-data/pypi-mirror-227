"""
routines to reconcile files against a list  image file types
"""
from os.path import getsize
import os
from datetime import datetime
from pathlib import Path
import re
from queue import Queue
import logging
from bdrc_irat.common import *
from bdrc_irat.ActionContext import ActionContext

wrote_header: bool = False


def get_image_sizes(q: Queue, results_queue: Queue, ctx: ActionContext) -> None:
    """
    Map action (see Reduce action above
    Looks for files in a filtered list whose file extension does not match their contents
    Based on util_lib.utils.get_work_image_facts
    :param q: Input queue of lists of paths to work
    :param results_queue: image lists
    :param ctx: Context (global vars)
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
        work_name: str = q.get()
        work_path: Path = Path(ctx.fs_path(work_name))

        try:

            _size: int = 0
            _count: int = 0
            _page_size: int = 0
            _page_count: int = 0

            wbt = datetime.now()
            sumsz = lambda p, f: sum(getsize(p / name) for name in f if img_re.match(name))

            for (root, dirs, files) in os.walk(work_path, topdown=True):
                rp = Path(root)
                _s = sumsz(rp, files)
                _l = len(files)
                if rp.parent.name == IMAGES_FOLDER:
                    _page_size += _s
                    _page_count += _l
                else:
                    _size += _s
                    _count += _l

            wet = datetime.now()

            # The results queue should be in the same order as the 'header' parameter to 'write_sizes()'
            results = (work_name, _size, _count, _page_size, _page_count,)
            logging.debug(
                f" v={str(work_path)} et: {(wet - wbt).total_seconds()} - Results: {results}")
            results_queue.put(results)
        finally:
            q.task_done()


