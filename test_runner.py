import hashlib
import os
import shutil
from unittest import TestCase

import time

from diff_utils import compare_snapshots
from model import FileSnapshot, DirSnapshot, SnapshotDiff
from os_utils import resolve, exists, get_modified
from snapshot_generation import create_system_snapshot
from snapshot_serialization import write_system_snapshot, load_system_snapshot

base = resolve("./test/env")

USER = "student"

def sub(path):
    return resolve(base + "/" + path)


def mkdir(path, mode=0o777):
    absolute = sub(path)
    if not exists(absolute):
        os.mkdir(absolute, mode)


def rmdir(path):
    if exists(sub(path)):
        shutil.rmtree(sub(path))


def rm(path):
    if exists(sub(path)):
        os.remove(sub(path))


def echo(path, content):
    with open(sub(path), "ab") as f:
        f.write(content.encode('utf-8'))


def md5(content):
    return hashlib.md5(content.encode("utf-8")).hexdigest()


def chmod(path, mode):
    os.chmod(sub(path), mode)


def chown(path, owner, group):
    if exists(sub(path)):
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
    chmod("alpha/beta/b.txt", 0o766)


def change():
    rmdir("alpha/beta/gamma")
    rm("delta/d.txt")

    echo("alpha/c.txt", "C")
    mkdir("alpha/new")

    echo("alpha/a.txt", "A")


    echo("o.txt", " ")
    chmod("o.txt", 0o744)
    chown("o.txt", "bob", "alice")



def cleanup():
    chown("o.txt", USER, USER)
    rmdir(".")
    rmdir("../out")


class Test(TestCase):
    maxDiff = None

    def test_init(self):
        cleanup()
        init()
        change()

    def test_integration(self):
        print("cleaning up")
        cleanup()
        print("initializing...")
        init()
        write_system_snapshot(create_system_snapshot(base, 'md5'), sub("../out/snap.txt"))
        snap = load_system_snapshot(sub("../out/snap.txt"))
        user = USER
        group = USER
        modified_alpha = m("alpha")
        modified_a = m("alpha/a.txt")
        modified_o = m("o.txt")
        modified_delta = m("delta")
        modified_beta = m("alpha/beta")
        expected = [
            DirSnapshot(sub("alpha"), user, group, "744", modified_alpha),
            DirSnapshot(sub("delta"), user, group, "741", modified_delta),
            DirSnapshot(sub("alpha/beta"), user, group, "724", modified_beta),
            DirSnapshot(sub("alpha/beta/gamma"), user, group, "744", m("alpha/beta/gamma")),

            FileSnapshot(sub("alpha/a.txt"), user, group, "711", modified_a, md5("A\n"), 2),
            FileSnapshot(sub("delta/d.txt"), user, group, "734", m("delta/d.txt"), md5("D\n" * 100), 200),
            FileSnapshot(sub("o.txt"), user, group, "734", modified_o, md5("O\n" * 500), 1000),
            FileSnapshot(sub("alpha/beta/b.txt"), user, group, "766", m("alpha/beta/b.txt"), md5("B\n" * 5), 10)

        ]

        self.assertEqual(snap.hash_function, 'md5')
        self.assertCountEqual(snap.snapshots, expected)
        time.sleep(1)
        print("changing")
        change()
        changes = [
            SnapshotDiff("delete", sub("alpha/beta/gamma"), "d", "object", None, None),
            SnapshotDiff("delete", sub("delta/d.txt"), "f", "object", None, None),

            SnapshotDiff("modify", sub("delta"), "d", "modified", modified_delta, m("delta")),
            SnapshotDiff("modify", sub("alpha/beta"), "d", "modified", modified_beta, m("alpha/beta")),

            SnapshotDiff("add", sub("alpha/c.txt"), "f", "object", None, None),
            SnapshotDiff("add", sub("alpha/new"), "d", "object", None, None),

            SnapshotDiff("modify", sub("alpha/a.txt"), "f", "hash", md5("A\n"), md5("A\nA")),
            SnapshotDiff("modify", sub("alpha/a.txt"), "f", "modified", modified_a, m("alpha/a.txt")),
            SnapshotDiff("modify", sub("alpha/a.txt"), "f", "size", 2, 3),

            SnapshotDiff("modify", sub("alpha"), "d", "modified", modified_alpha, m("alpha")),

            SnapshotDiff("modify", sub("o.txt"), "f", "modified", modified_o, m("o.txt")),
            SnapshotDiff("modify", sub("o.txt"), "f", "size", 1000, 1001),
            SnapshotDiff("modify", sub("o.txt"), "f", "hash", md5("O\n" * 500), md5("O\n" * 500 + " ")),
            SnapshotDiff("modify", sub("o.txt"), "f", "access", "734", "744"),

            SnapshotDiff("modify", sub("o.txt"), "f", "user", user, "bob"),
            SnapshotDiff("modify", sub("o.txt"), "f", "group", group, "alice"),
        ]
        compared = compare_snapshots(snap, create_system_snapshot(base, 'md5'))
        self.assertCountEqual(changes, compared)
        print("cleaning")
        cleanup()



    def test_clean_up(self):
        cleanup()
