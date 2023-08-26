"""
Global variables for action context
"""
# Use native locators - web is too slow
from archive_ops.locators import *


class ActionContext:

    @property
    def fs_base(self):
        return self._fs_base

    @fs_base.setter
    def fs_base(self, value):
        self._fs_base = value

    @property
    def s3_base(self):
        return self._s3_base

    @s3_base.setter
    def s3_base(self, value):
        self._s3_base = value

    @property
    def s3_bucket(self):
        return self._s3_bucket

    @s3_bucket.setter
    def s3_bucket(self, value):
        self._s3_bucket = value

    def fs_path(self, resource: str) -> str:
        return r_divmod_50_b_2(self.fs_base, resource)

    def s3_path(self, resource: str) -> str:
        """
        Doesn't include the bucket
        """
        return r_s3(self.s3_base, resource)

    def __init__(self, fs_base: str, s3_base: str, s3_bucket: str):
        self.fs_base = fs_base
        self.s3_base = s3_base
        self.s3_bucket = s3_bucket
