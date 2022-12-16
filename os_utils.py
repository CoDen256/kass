import hashlib
import os
from stat import *

absolute_path = os.path.dirname(__file__)


def sha256(file):
    return compute_hash(file, hashlib.sha256())


def md5(file):
    return compute_hash(file, hashlib.md5())


def sanitize(path):
    return path


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