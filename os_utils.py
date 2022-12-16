import hashlib
import os
from datetime import datetime
from pathlib import Path
from stat import S_ISDIR, S_ISREG, ST_MODE
from sys import platform

pwd_grp_present = False
if platform == "linux":
    import pwd
    import grp

    pwd_grp_present = True

absolute_path = os.path.dirname(__file__)


def sha256(file):
    return compute_hash(file, hashlib.sha256())


def md5(file):
    return compute_hash(file, hashlib.md5())


def sanitize(path):
    return path


def exists(path):
    return os.path.exists(path)


def is_dir(path):
    return os.path.isdir(path)


def is_parent_of_file(path, file):
    return Path(path) in Path(file).parents


def compute_hash(file, digest, buffer=65636):
    with open(file, 'rb') as f:
        while True:
            data = f.read(buffer)
            if not data:
                break
            digest.update(data)
    return digest.hexdigest()


def resolve(subpath):
    return os.path.join(absolute_path, subpath)


def walktree(top, callback_file, callback_dir):
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        stat_result = os.stat(pathname)
        if S_ISDIR(stat_result.st_mode):
            callback_dir(pathname, stat_result)
            walktree(pathname, callback_file, callback_dir)
        elif S_ISREG(stat_result.st_mode):
            callback_file(pathname, stat_result)
        else:
            # Unknown file type, print a message
            print('Skipping %s' % pathname)


def get_user(stat_result: os.stat_result) -> str:
    uid = stat_result.st_uid
    if not pwd_grp_present: return str(uid)
    return pwd.getpwuid(uid)


def get_group(stat_result: os.stat_result) -> str:
    gid = stat_result.st_gid
    if not pwd_grp_present: return str(gid)
    return grp.getgrgid(gid)


def get_modified(stat_result: os.stat_result) -> datetime:
    return datetime.fromtimestamp(stat_result.st_mtime).replace(microsecond=0)


def get_access_mode(stat_result: os.stat_result) -> str:
    return oct(stat_result[ST_MODE])[-3:]
