# region Globals
import os.path
import io

from threading import local

LIST_ACTION = "list"
TYPES_ACTION = "types"
SIZES_ACTION = "sizes"

threadLocal = local()

# no hyphens, please. These strings become attributes in a data frame
csv_out_headers: {} = {
    LIST_ACTION: ['work', 'image_group', 'fs_count', 's3_count'],
    TYPES_ACTION: ['Path', 'extension', 'filetype'],

    SIZES_ACTION: ['work', 'non_image_size', 'non_image_count', 'image_size', 'image_count']
}

BUDA_BUCKET = "archive.tbrc.org"
S3_BASE: str = "Works"  # path on S3

# For network connected debian (/mnt/Archive) or remote mac
# FS_BASE is just a stem, not a real directory
FS_BASE: str = "/mnt/Archive" if os.path.exists("/mnt/Archive0") else "/Volumes/Archive"

# re string
# Anything that ends in these. Assumes IgnoreCase in re.compile()
GRAPHICS_FILE_EXTS: str = r'.+\.(jpg|jpeg|tif|tiff|png|bmp|wmf|pdf)$'

IMAGES_FOLDER = 'images'

LOG_DATEFMT = "[%Z %x %H.%M.%S]"
LOG_MESSAGE_FORMAT = "%(asctime)s:%(name)s:{%(threadName)s}-%(levelname)s-%(message)s"
# endregion


class PsArgs:
    def __init__(self):
        self.action = None

    container: str
    work_rids: []
    input_list_file: io.TextIOWrapper
    output_file: io.TextIOWrapper
    fs_base:str
    s3_base: str
    s3_bucket: str
    pass

def list_img_keys(prefix, bucket=BUDA_BUCKET):
    objs = {}
    continuation_token = None
    while True:
        if continuation_token:
            response = S3.list_objects_v2(Bucket=bucket, Prefix=prefix, ContinuationToken=continuation_token)
        else:
            response = S3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if 'Contents' in response and response['Contents']:
            for obj in response['Contents']:
                obj_key = obj['Key']
                if not is_img(obj_key):
                    continue
                key_noprefix = obj_key[len(prefix):]
                if "/" in key_noprefix:
                    # don't look at subdirectories
                    continue
                objs[key_noprefix] = {"md5sum": obj["ETag"], "size": obj["Size"]}
        continuation_token = response.get("NextContinuationToken")
        if not continuation_token:
            break
    return objs

def list_files_s3(w, i):
    prefix = get_s3_folder_prefix(w, i)
    files = list_img_keys(prefix)
    return files

def list_files(directory):
    file_dict = {}
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            if not is_img(filename):
                continue
            file_path = os.path.join(directory, filename)
            md5_hash = hashlib.md5()
            with open(file_path, "rb") as file:
                for chunk in iter(lambda: file.read(4096), b""):
                    md5_hash.update(chunk)
            file_size = os.path.getsize(file_path)
            file_dict[filename] = {
                "md5sum": '"'+md5_hash.hexdigest()+'"',
                "size": file_size
            }
    return file_dict

def list_files_archive(w, i):
    basedir = get_archive_folder(w, i)
    files = list_files(basedir)
    return files
