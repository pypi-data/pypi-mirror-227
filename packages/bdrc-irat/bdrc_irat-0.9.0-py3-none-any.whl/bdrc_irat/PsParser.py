import argparse
import sys

from .common import *

actions = [LIST_ACTION, TYPES_ACTION, SIZES_ACTION]


class PsParser:
    """
    Handles arguments on command line
    """

    _parser: argparse.ArgumentParser

    def __init__(self):
        self._parser = argparse.ArgumentParser(usage="See parallelscan/README.doc for details",
                                               description="Runs image scanning tools against a set of works")
        self._parser.add_argument("-a", "--action", help="Available actions", choices=actions,
                                  required=True)
        self._parser.add_argument("-w", "--work_rids", help="one or more work_rids", nargs="+")
        self._parser.add_argument("-i", "--input_list_file", help="file containing list of work_rids",
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

