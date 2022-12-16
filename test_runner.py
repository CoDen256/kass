import hashlib
import os, shutil
from unittest import TestCase

from model import FileSnapshot, DirSnapshot
from os_utils import resolve, exists, get_modified
from snapshot_generation import create_system_snapshot
from snapshot_serialization import write_system_snapshot, load_system_snapshot
from diff_utils import compare_snapshots

base = resolve("./test/env")


def sub(path):
    return resolve(base + "/" + path)


def mkdir(path, mode=0o777):
    absolute = sub(path)
    if not exists(absolute):
        os.mkdir(absolute, mode)


def rmdir(path):
    if exists(sub(path)):
        shutil.rmtree(sub(path))


def echo(path, content):
    with open(sub(path), "ab") as f:
        f.write(content.encode('utf-8'))


def md5(content):
    return hashlib.md5(content.encode("utf-8")).hexdigest()


def chmod(path, mode):
    os.chmod(sub(path), mode)


def chown(path, owner, group):
    os.system(f'sudo /bin/chown {owner}:{group} ' + sub(path))


def m(path):
    return get_modified(os.stat(sub(path)))


def init():
    mkdir("../out")
    mkdir(".")

    mkdir("alpha", 0o744)
    mkdir("delta", 0o741)
    mkdir("alpha/beta", 0o724)
    mkdir("alpha/beta/gamma", 0o744)

    echo("alpha/a.txt", "A\n")
    chmod("alpha/a.txt", 0o711)

    echo("delta/d.txt", "D\n" * 100)
    chmod("delta/d.txt", 0o734)

    echo("o.txt", "O\n" * 500)
    chmod("o.txt", 0o734)

    echo("alpha/beta/b.txt", "B\n" * 5)
    chmod("alpha/beta/b.txt", 0o777)


def change():
    pass


def cleanup():
    rmdir(".")
    rmdir("../out")


class Test(TestCase):
    maxDiff = None

    def test_init(self):
        cleanup()
        init()


    def test_integration(self):
        cleanup()
        init()
        write_system_snapshot(create_system_snapshot(base, 'md5'), sub("../out/snap.txt"))
        snap = load_system_snapshot(sub("../out/snap.txt"))
        user = "coden"
        group = "coden"
        expected = [
            DirSnapshot(sub("alpha"), user, group, "744", m("alpha")),
            DirSnapshot(sub("delta"), user, group, "741", m("delta")),
            DirSnapshot(sub("alpha/beta"), user, group, "724", m("alpha/beta")),
            DirSnapshot(sub("alpha/beta/gamma"), user, group, "744", m("alpha/beta/gamma")),

            FileSnapshot(sub("alpha/a.txt"), user, group, "711", m("alpha/a.txt"), md5("A\n"), 2),
            FileSnapshot(sub("delta/d.txt"), user, group, "734", m("delta/d.txt"), md5("D\n" * 100), 200),
            FileSnapshot(sub("o.txt"), user, group, "734", m("o.txt"), md5("O\n" * 500), 1000),
            FileSnapshot(sub("alpha/beta/b.txt"), user, group, "777", m("alpha/beta/b.txt"), md5("B\n" * 5), 10)

        ]

        self.assertEqual(snap.hash_function, 'md5')
        self.assertCountEqual(snap.snapshots, expected)

    def test_clean_up(self):
        cleanup()
