import os
import hashlib

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
